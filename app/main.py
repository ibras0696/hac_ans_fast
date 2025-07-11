import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.routes import router
from app.routes.auth import get_current_user_from_cookie

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
    response = await call_next(request)
    return response


# Роуты
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8001)  # host="0.0.0.0", port=600)
