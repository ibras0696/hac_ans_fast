from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.templates import ALL_TEMPLATES_DIR
from database.crud import CrudUser, CrudActivityHistory, CrudPreferences, CrudRecommendation, CrudActivity

router = APIRouter()

templates = Jinja2Templates(directory=ALL_TEMPLATES_DIR)


@router.get("/{user_id}", response_class=HTMLResponse)
async def personal_detail(request: Request, user_id: int):
    # Проверяем авторизацию
    if not request.state.current_user:
        return RedirectResponse(url="/auth/login", status_code=302)
    try:
        # Получаем данные пользователя
        user = await CrudUser().get_user_by_id(user_id)
        if not user:
            return RedirectResponse(url="/", status_code=302)
        # Получаем историю активностей пользователя
        history = await CrudActivityHistory().get_history_by_user_id(user_id)
        # Получаем рекомендации пользователя
        recommendations = await CrudRecommendation().get_recommendations_by_user(user_id)
        # Получаем детали активностей для истории
        activities_details = []
        for hist in history:
            activity = await CrudActivity().get_activity_by_id(hist.activity_id)
            if activity:
                activities_details.append({
                    'history': hist,
                    'activity': activity
                })
        # Получаем детали активностей для рекомендаций
        recommendations_details = []
        for rec in recommendations:
            activity = await CrudActivity().get_activity_by_id(rec.activity_id)
            if activity:
                recommendations_details.append({
                    'recommendation': rec,
                    'activity': activity
                })
        # Получаем избранные из request.state.favorites (если есть)
        favorites = getattr(request.state, 'favorites', [])
        return templates.TemplateResponse("personal_detail.html", {
            "request": request,
            "user": user,
            "history": activities_details,
            "favorites": favorites,
            "recommendations": recommendations_details,
            "current_user": request.state.current_user
        })
    except Exception as e:
        return RedirectResponse(url="/", status_code=302)
