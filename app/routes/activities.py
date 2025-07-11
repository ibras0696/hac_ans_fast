from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.templates import ALL_TEMPLATES_DIR
from database import CrudActivity

router = APIRouter()

templates = Jinja2Templates(directory=ALL_TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
async def activities(request: Request):
    try:
        # Получаем все активности из базы данных
        activities_list = await CrudActivity().list_activities()
        return templates.TemplateResponse("activities.html", {
            "request": request,
            "activities": activities_list,
            "current_user": request.state.current_user
        })
    except Exception as e:
        # В случае ошибки возвращаем пустой список
        return templates.TemplateResponse("activities.html", {
            "request": request,
            "activities": [],
            "current_user": request.state.current_user
        })
