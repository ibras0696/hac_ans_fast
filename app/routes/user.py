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
        {"request": request, "title": ''})
