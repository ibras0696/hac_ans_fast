from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from templates import ALL_TEMPLATES_DIR

router = APIRouter()

templates = Jinja2Templates(directory=ALL_TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
async def this_command(request: Request):
    return templates.TemplateResponse("this_command.html", {"request": request})
