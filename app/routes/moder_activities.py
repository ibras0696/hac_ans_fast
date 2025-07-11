import os
import uuid
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.templates import ALL_TEMPLATES_DIR
from database import CrudActivity
from database.crud import CrudUser

router = APIRouter()

templates = Jinja2Templates(directory=ALL_TEMPLATES_DIR)


@router.get('/', response_class=HTMLResponse)
async def check_function_moder(request: Request):
    return templates.TemplateResponse("main_moderator.html",
                                      {
                                          "request": request,
                                          "current_user": request.state.current_user
                                      })


@router.get('/check_activities', response_class=HTMLResponse)
async def check_activities(request: Request):
    try:
        # Получаем все активности из базы данных
        activities_list = await CrudActivity().list_activities()
        return templates.TemplateResponse("check_activities.html", {
            "request": request,
            "activities": activities_list,
            "current_user": request.state.current_user
        })
    except Exception:
        # В случае ошибки возвращаем пустой список
        return templates.TemplateResponse("check_activities.html", {
            "request": request,
            "activities": [],
            "current_user": request.state.current_user
        })


@router.get('/add_activities', response_class=HTMLResponse)
async def add_activities_page(request: Request):
    return templates.TemplateResponse("add_activities.html", {
        "request": request,
        "current_user": request.state.current_user
    })


# Добавление активностей
@router.post("/add_activities", response_class=HTMLResponse)
async def add_activities(request: Request):
    form_data = await request.form()

    title = form_data.get("title"),
    description = form_data.get("description"),
    category = form_data.get("category"),
    rating = float(form_data.get("rating"))
    address = form_data.get("address")
    working_hours = form_data.get("working_house")

    # Обработка загруженного файла
    image_file = form_data.get("image")
    images = "/static/default_image.svg"  # Значение по умолчанию

    if image_file and hasattr(image_file, 'filename') and image_file.filename:
        try:
            # Проверяем тип файла
            allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}
            file_extension = os.path.splitext(image_file.filename)[1].lower()
            
            if file_extension not in allowed_extensions:
                raise ValueError(f"Неподдерживаемый тип файла: {file_extension}")
            
            # Проверяем размер файла (максимум 5MB)
            file_content = await image_file.read()
            if len(file_content) > 5 * 1024 * 1024:  # 5MB
                raise ValueError("Файл слишком большой. Максимальный размер: 5MB")
            
            # Проверяем, что файл не пустой
            if len(file_content) == 0:
                raise ValueError("Файл пустой")
            
            # Создаем папку для загрузок, если её нет
            upload_dir = "app/static/uploads"
            os.makedirs(upload_dir, exist_ok=True)
            
            # Генерируем уникальное имя файла
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(upload_dir, unique_filename)
            
            # Сохраняем файл
            with open(file_path, "wb") as f:
                f.write(file_content)
            
            # Устанавливаем путь для базы данных
            images = f"/static/uploads/{unique_filename}"
            
        except Exception as e:
            # В случае ошибки используем изображение по умолчанию
            images = "/static/default_image.svg"
            print(f"Ошибка при сохранении файла: {e}")
            # Возвращаем ошибку пользователю
            return templates.TemplateResponse("add_activities.html", {
                "request": request,
                "error_message": f"Ошибка при загрузке файла: {str(e)}",
                "current_user": request.state.current_user
            })

    try:
        success = await CrudActivity().add_activity(
            title=title[0],
            description=description[0],
            category=category[0],
            address=address,
            images=images,
            working_hours=working_hours,
            rating=rating,
        )

        if success:
            # Перенаправляем обратно на страницу со списком активностей
            from fastapi.responses import RedirectResponse
            return RedirectResponse(url="/activities", status_code=302)
        else:
            # Если ошибка при добавлении, показываем ошибку
            return templates.TemplateResponse("add_activities.html", {
                "request": request,
                "error_message": "Ошибка при добавлении",
                "current_user": request.state.current_user
            })
    except Exception as e:
        return templates.TemplateResponse("add_activities.html", {
            "request": request,
            "error_message": f"Ошибка при добавлении: {str(e)}",
            "current_user": request.state.current_user
        })


@router.delete("/delete_activity/{activity_id}")
async def delete_activity(activity_id: int, request: Request):
    try:
        success = await CrudActivity().delete_activity(activity_id)
        if success:
            return JSONResponse(content={"success": True, "message": "Активность успешно удалена"})
        else:
            return JSONResponse(content={"success": False, "message": "Активность не найдена"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"success": False, "message": f"Ошибка при удалении: {str(e)}"}, status_code=500)



# Просмотр всех пользователей (только для модераторов)
@router.get('/users_list', response_class=HTMLResponse)
async def list_users(request: Request):
    user = request.state.current_user
    if not user or not getattr(user, 'is_moderator', False):
        return RedirectResponse(url="/auth/login", status_code=302)
    users = await CrudUser().list_users()
    return templates.TemplateResponse("users_list.html", {
        "request": request,
        "users": users,
        "current_user": user
    })


@router.post('/toggle_role/{user_id}')
async def toggle_role(request: Request, user_id: int):
    user = request.state.current_user
    if not user or not getattr(user, 'is_moderator', False):
        return RedirectResponse(url="/auth/login", status_code=302)
    # Получаем пользователя
    target_user = await CrudUser().get_user_by_id(user_id)
    if not target_user:
        return RedirectResponse(url="/moder/users_list", status_code=302)
    # Меняем роль
    from sqlalchemy import update
    from database.db import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        await session.execute(
            update(type(target_user)).where(type(target_user).id == user_id).values(is_moderator=not target_user.is_moderator)
        )
        await session.commit()
    return RedirectResponse(url="/moder/users_list", status_code=302)
