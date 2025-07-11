from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.templates import ALL_TEMPLATES_DIR
from database.crud import CrudPreferences, CrudActivity, CrudRecommendation, CrudActivityHistory
import asyncio
from datetime import datetime, timezone

router = APIRouter()
templates = Jinja2Templates(directory=ALL_TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
async def get_recommendations(request: Request):
    if not request.state.current_user:
        return RedirectResponse(url="/auth/login", status_code=302)
    user_id = request.state.current_user.id
    # Показываем все рекомендации пользователя за сегодня
    today = datetime.now(timezone.utc).date()
    user_recs = await CrudRecommendation().get_recommendations_by_user(user_id)
    activities = []
    for rec in user_recs:
        if rec.recommended_at.date() == today:
            act = await CrudActivity().get_activity_by_id(rec.activity_id)
            if act:
                activities.append(act)
    return templates.TemplateResponse("recommendations.html", {"request": request, "recommendations": activities, "message": "Ваши рекомендации за сегодня:"})


@router.post("/", response_class=HTMLResponse)
async def post_recommendations(request: Request):
    if not request.state.current_user:
        return RedirectResponse(url="/auth/login", status_code=302)
    user_id = request.state.current_user.id
    prefs = await CrudPreferences().get_preferences_by_user_id(user_id)
    if not prefs:
        return templates.TemplateResponse("recommendations.html", {"request": request, "recommendations": [], "message": "Сначала заполните анкету предпочтений!"})

    # Очищаем старые рекомендации пользователя
    user_recs = await CrudRecommendation().get_recommendations_by_user(user_id)
    for rec in user_recs:
        await CrudRecommendation().delete_recommendation(rec.id)

    filtered = await CrudActivity().get_best_activities_for_user(prefs.mood, prefs.time_available, prefs.budget)
    if not filtered:
        return templates.TemplateResponse("recommendations.html", {"request": request, "recommendations": [], "message": "Нет подходящих рекомендаций по вашим параметрам."})

    for act in filtered:
        await CrudRecommendation().add_recommendation(user_id, act.id)
        await CrudActivityHistory().add_activity_history(user_id, act.id)

    # После добавления рекомендаций редиректим на новую страницу
    return RedirectResponse(url="/recommendations/my_recommendations", status_code=303)


@router.get("/my_recommendations", response_class=HTMLResponse)
async def my_recommendations(request: Request, mood: str = Query(None), time: int = Query(None), budget: int = Query(None), location: str = Query(None)):
    if not request.state.current_user:
        return RedirectResponse(url="/auth/login", status_code=302)
    user_id = request.state.current_user.id
    # Если критерии переданы — фильтруем по ним
    if any([mood, time, budget, location]):
        all_activities = await CrudActivity().list_activities()
        filtered = []
        for act in all_activities:
            match = False
            if mood and (mood.lower() in act.title.lower() or mood.lower() in act.description.lower()):
                match = True
            if location and location.lower() in act.address.lower():
                match = True
            if time is not None:
                try:
                    hours = act.working_hours.split('-')
                    duration = int(hours[1]) - int(hours[0])
                    if duration <= int(time):
                        match = True
                except Exception:
                    pass
            if budget is not None and int(budget) >= 0:
                match = True  # Можно доработать под реальные цены, если они есть
            if match:
                filtered.append(act)
        filtered = sorted(filtered, key=lambda x: x.rating, reverse=True)[:4]
        activities = filtered
        # Сохраняем рекомендации пользователя на день (только уникальные)
        today = datetime.now(timezone.utc).date()
        user_recs = await CrudRecommendation().get_recommendations_by_user(user_id)
        # Удаляем старые рекомендации за сегодня
        for rec in user_recs:
            if rec.recommended_at.date() == today:
                await CrudRecommendation().delete_recommendation(rec.id)
        # Сохраняем новые рекомендации
        for act in activities:
            await CrudRecommendation().add_recommendation(user_id, act.id)
    else:
        # fallback: рекомендации из базы
        user_recs = await CrudRecommendation().get_recommendations_by_user(user_id)
        activity_ids = [rec.activity_id for rec in user_recs]
        activities = []
        for act_id in activity_ids:
            act = await CrudActivity().get_activity_by_id(act_id)
            if act:
                activities.append(act)
    return templates.TemplateResponse("recommendations.html", {"request": request, "recommendations": activities, "message": "Ваши персональные рекомендации на сегодня:"})
