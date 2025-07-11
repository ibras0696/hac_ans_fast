from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.templates import ALL_TEMPLATES_DIR
from database.crud import CrudFavorite, CrudActivity

router = APIRouter()
templates = Jinja2Templates(directory=ALL_TEMPLATES_DIR)

@router.get("/", name="favorites")
async def favorites(request: Request):
    user = request.state.current_user
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)
    favorites = await CrudFavorite().get_favorites_by_user(user.id)
    # Получаем активности по id
    activities = []
    for fav in favorites:
        activity = await CrudActivity().get_activity_by_id(fav.activity_id)
        if activity:
            activities.append({"activity": activity, "favorite_id": fav.id})
    return templates.TemplateResponse("favorites.html", {"request": request, "favorites": activities, "current_user": user, "message": request.query_params.get('message')})

@router.post("/add/{activity_id}")
async def add_favorite(request: Request, activity_id: int):
    user = request.state.current_user
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)
    await CrudFavorite().add_favorite(user.id, activity_id)
    url = f"/favorites?message=Добавлено%20в%20избранное"
    return RedirectResponse(url=url, status_code=302)

@router.post("/remove/{favorite_id}")
async def remove_favorite(request: Request, favorite_id: int):
    user = request.state.current_user
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)
    await CrudFavorite().remove_favorite(favorite_id)
    url = f"/favorites?message=Удалено%20из%20избранного"
    return RedirectResponse(url=url, status_code=302)

@router.get("/detail/{activity_id}")
async def favorite_detail(request: Request, activity_id: int):
    user = request.state.current_user
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)
    activity = await CrudActivity().get_activity_by_id(activity_id)
    favorite_id = None
    favorites = await CrudFavorite().get_favorites_by_user(user.id)
    for fav in favorites:
        if fav.activity_id == activity_id:
            favorite_id = fav.id
            break
    return templates.TemplateResponse("favorite_detail.html", {"request": request, "activity": activity, "current_user": user, "favorite_id": favorite_id})