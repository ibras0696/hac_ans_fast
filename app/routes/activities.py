from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from templates import ALL_TEMPLATES_DIR

router = APIRouter()

templates = Jinja2Templates(directory=ALL_TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
async def activities(request: Request):
    return templates.TemplateResponse("activities.html", {"request": request})
