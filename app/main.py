import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.routes import router
from app.routes.auth import get_current_user_from_cookie
from database.crud import CrudFavorite, CrudActivity

app = FastAPI()

# Правильный путь до папки templates
TEMPLATES_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(TEMPLATES_DIR, "templates"))


# Правильный путь до папки static
STATIC_DIR = os.path.dirname(os.path.abspath(__file__))
# Подключение css
app.mount("/static", StaticFiles(directory=os.path.join(STATIC_DIR, "static")), name="static")


@app.middleware("http")
async def add_user_to_request(request: Request, call_next):
    """Добавляет текущего пользователя в request.state для всех шаблонов"""
    request.state.current_user = await get_current_user_from_cookie(request)
    # Явно подгружаем избранное, если пользователь есть
    if request.state.current_user:
        favorites = await CrudFavorite().get_favorites_by_user(request.state.current_user.id)
        fav_acts = []
        for fav in favorites:
            activity = await CrudActivity().get_activity_by_id(fav.activity_id)
            if activity:
                fav_acts.append({"activity": activity, "favorite_id": fav.id, "activity_id": fav.activity_id, "id": fav.id})
        request.state.favorites = fav_acts
    else:
        request.state.favorites = []
    response = await call_next(request)
    return response


# Роуты
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8001)  # host="0.0.0.0", port=600)
