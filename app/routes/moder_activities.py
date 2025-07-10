from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.templates import ALL_TEMPLATES_DIR

router = APIRouter()

templates = Jinja2Templates(directory=ALL_TEMPLATES_DIR)


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
    reit = float(form_data.get("reit"))
    # image = float(form_data.get("image"))

    # print(title, description, category, reit, image)
    print(title, description, category, reit)


    # Возвращаем ту же страницу с сообщением
    return templates.TemplateResponse("add_activities.html", {
        "request": request,
        "message": "Активность успешно добавлена!"
    })





# Просмотр активностей также удаление активностей
@router.get("/check_activities", response_class=HTMLResponse)
async def add_activities(request: Request):
    return templates.TemplateResponse("check_activities.html",
                                      {"request": request})
