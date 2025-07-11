from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.templates import ALL_TEMPLATES_DIR
from database import CrudActivity

router = APIRouter()

templates = Jinja2Templates(directory=ALL_TEMPLATES_DIR)


@router.get("/")
async def user(request: Request):
    return templates.TemplateResponse(
        "user.html",
        {
            "request": request,
            "current_user": request.state.current_user
        })


@router.post("/")
async def user_post(request: Request):
    form_data = await request.form()

    weather = form_data.get('weather')  # Получение погоды.
    timeoftoday = form_data.get("timeofday")  # Получение текущего времени пользователя
    mood = form_data.get('mood')  # Получение пользовательского настроения
    time = form_data.get("time")  # Время которое он может потратить на данную активность
    budget = form_data.get('budget')  # получение бюджета пользователя
    location = form_data.get('location')  # Получение города который он отправил

    print(weather, timeoftoday, mood, time, budget, location)

    # Передаём критерии через query параметры
    url = f"/recommendations/my_recommendations?mood={mood}&time={time}&budget={budget}&location={location}"
    return RedirectResponse(url=url, status_code=303)


# Детальная страница активности
@router.get("/activity_detail/{activity_id}", response_class=HTMLResponse)
async def activity_detail(request: Request, activity_id: int):
    if not request.state.current_user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login", status_code=302)
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
