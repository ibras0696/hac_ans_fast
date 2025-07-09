from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

TEMPLATES_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(TEMPLATES_DIR, "static"))


@router.get("/")
async def user(request: Request):
    return templates.TemplateResponse(
        "user.html",
        {"request": request, "title": "Главная страница"})
