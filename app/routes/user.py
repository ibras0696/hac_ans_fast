from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

from app.templates import ALL_TEMPLATES_DIR

router = APIRouter()

templates = Jinja2Templates(directory=ALL_TEMPLATES_DIR)

@router.get("/")
async def user(request: Request):

    return templates.TemplateResponse(
        "user.html",
        {"request": request})

@router.post("/")
async def user(request: Request):

    form_data = await request.form()

    weather = form_data.get('weather') # Получение погоды.
    timeoftoday = form_data.get("timeofday") # Получение текущего времени пользователя
    mood = form_data.get('mood') # Получение пользовательского настроения
    time = form_data.get("time") # Время которое он может потратить на данную активность
    budget = form_data.get('budget') # получение бюджета пользователя
    location = form_data.get('location') # Получение города который он отправил

    print(weather, timeoftoday, mood, time, budget, location)

    return templates.TemplateResponse(
        "user.html",
        {"request": request, "message": 'Данные успешно отправлены!'})
