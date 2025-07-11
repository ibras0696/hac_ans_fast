from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.templates import ALL_TEMPLATES_DIR


router = APIRouter()

templates = Jinja2Templates(directory=ALL_TEMPLATES_DIR)


TECHNOLOGIES = [
    {"name": "Python", "desc": "Основной язык разработки"},
    {"name": "FastAPI", "desc": "Быстрый и современный backend-фреймворк"},
    {"name": "Jinja2", "desc": "Шаблонизатор для генерации HTML"},
    {"name": "HTML5 & CSS3", "desc": "Верстка и стилизация интерфейса"},
    {"name": "JavaScript", "desc": "Интерактивность на фронтенде"},
    {"name": "aiogram (Telegram Bot API)", "desc": "Телеграм-бот для админки и интеграции"},
    {"name": "Docker", "desc": "Контейнеризация приложения"},
    {"name": "Docker Compose", "desc": "Оркестрация контейнеров"},
    {"name": "SQLite", "desc": "Лёгкая встроенная база данных"},
    {"name": "SQLAlchemy", "desc": "ORM для работы с БД"},
    {"name": "Alembic", "desc": "Миграции базы данных"},
]

@router.get("/", response_class=HTMLResponse)
def project_technologies(request: Request):
    return templates.TemplateResponse("project_technologies.html", {"request": request, "technologies": TECHNOLOGIES})
