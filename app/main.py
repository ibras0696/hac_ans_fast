import os

import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from .routes import router

app = FastAPI()

# Правильный путь до папки templates
TEMPLATES_DIR = os.path.dirname(os.path.abspath(__file__))
# Подключение Шаблонизатора
templates = Jinja2Templates(directory=os.path.join(TEMPLATES_DIR, "static"))

# Правильный путь до папки static
STATIC_DIR = os.path.dirname(os.path.abspath(__file__))
# Подключение css
app.mount("/static", StaticFiles(directory=os.path.join(STATIC_DIR, "static")), name="static")

# Роуты
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8001)  # host="0.0.0.0", port=600)
