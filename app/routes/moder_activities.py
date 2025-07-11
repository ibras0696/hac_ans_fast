from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.templates import ALL_TEMPLATES_DIR
from database import CrudActivity

router = APIRouter()

templates = Jinja2Templates(directory=ALL_TEMPLATES_DIR)


@router.get('/', response_class=HTMLResponse)
async def check_function_moder(request: Request):
    return templates.TemplateResponse("main_moderator.html",
                                      {"request": request})


# Переход на страницу активностей
@router.get("/add_activities", response_class=HTMLResponse)
async def add_activities(request: Request):
    return templates.TemplateResponse("add_activities.html",
                                      {"request": request})


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
    images = "default_image.jpg"  # Значение по умолчанию

    if image_file and hasattr(image_file, 'filename') and image_file.filename:
        # Если файл загружен, сохраняем его имя
        images = image_file.filename
        # Здесь можно добавить логику сохранения файла на сервер
        # Например, сохранить в папку static/uploads/

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
                "error_message": "Ошибка при добавлении"
            })
    except Exception as e:
        return templates.TemplateResponse("add_activities.html", {
            "request": request,
            "error_message": f"Ошибка при добавлении: {str(e)}"
        })


# Просмотр активностей также удаление активностей
@router.get("/check_activities", response_class=HTMLResponse)
async def add_activities(request: Request):
    get_list_activities = await CrudActivity().list_activities()

    return templates.TemplateResponse("check_activities.html",
                                      {"request": request, "list_activities_all": get_list_activities})


# Удаление активности
@router.get("/delete_activity/{activity_id}", response_class=HTMLResponse)
async def delete_activity(request: Request, activity_id: int):
    try:
        success = await CrudActivity().delete_activity(activity_id)
        if success:
            # Перенаправляем обратно на страницу со списком активностей модератора
            from fastapi.responses import RedirectResponse
            return RedirectResponse(url="/moder/check_activities", status_code=302)
        else:
            # Если активность не найдена, показываем ошибку
            return templates.TemplateResponse("check_activities.html", {
                "request": request,
                "list_activities_all": await CrudActivity().list_activities(),
                "error_message": "Активность не найдена"
            })
    except Exception as e:
        return templates.TemplateResponse("check_activities.html", {
            "request": request,
            "list_activities_all": await CrudActivity().list_activities(),
            "error_message": f"Ошибка при удалении: {str(e)}"
        })


# Детальная страница активности
@router.get("/activity_detail/{activity_id}", response_class=HTMLResponse)
async def activity_detail(request: Request, activity_id: int):
    try:
        activity = await CrudActivity().get_activity_by_id(activity_id)
        if activity:
            # Здесь можно добавить получение отзывов для активности
            reviews = []  # Пока пустой список, нужно будет добавить модель отзывов
            return templates.TemplateResponse("activity_detail.html", {
                "request": request,
                "activity": activity,
                "reviews": reviews
            })
        else:
            return templates.TemplateResponse("activity_detail.html", {
                "request": request,
                "activity": None,
                "reviews": []
            })
    except Exception:
        return templates.TemplateResponse("activity_detail.html", {
            "request": request,
            "activity": None,
            "reviews": []
        })


# Добавление отзыва
@router.post("/add_review", response_class=JSONResponse)
async def add_review(request: Request):
    try:
        # Здесь будет логика добавления отзыва
        # Пока возвращаем заглушку
        return JSONResponse(content={"success": True, "message": "Отзыв успешно добавлен"})
    except Exception as e:
        return JSONResponse(content={"success": False, "message": f"Ошибка при добавлении отзыва: {str(e)}"}, status_code=500)
