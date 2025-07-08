Отлично! Ниже я покажу **простые и понятные примеры**:

---

## ✅ 1. Как подключить HTML-шаблоны в FastAPI

```python
# main.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Главная страница"})
```

---

## ✅ 2. 📄 Пример `index.html` (Jinja2 + CSS + подключение Bootstrap)

```html
<!-- templates/index.html -->
{% extends "base.html" %}

{% block content %}
  <div class="container mt-5">
    <h1>{{ title }}</h1>
    <p>Добро пожаловать!</p>
  </div>
{% endblock %}
```

---

## ✅ 3. 📄 Базовый шаблон `base.html` (CSS + Bootstrap)

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>{{ title if title else "FastAPI App" }}</title>
  <link rel="stylesheet" href="/static/styles.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
</head>
<body>
  {% block content %}{% endblock %}
</body>
</html>
```

---

## ✅ 4. 🔁 Цикл по элементам (Jinja2 `for`)

Передаём список:

```python
@app.get("/users")
def users(request: Request):
    data = ["Ибрагим", "Али", "Смитти"]
    return templates.TemplateResponse("users.html", {"request": request, "users": data})
```

Шаблон:

```html
<!-- templates/users.html -->
{% extends "base.html" %}
{% block content %}
  <h2>Список пользователей:</h2>
  <ul>
    {% for user in users %}
      <li>{{ user }}</li>
    {% endfor %}
  </ul>
{% endblock %}
```

---

## ✅ 5. 📦 Подгрузить один объект

Python:

```python
@app.get("/profile")
def profile(request: Request):
    user = {"name": "Ибрагим", "city": "Астана", "age": 22}
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})
```

HTML:

```html
<!-- templates/profile.html -->
{% extends "base.html" %}
{% block content %}
  <h2>Профиль</h2>
  <p>Имя: {{ user.name }}</p>
  <p>Город: {{ user.city }}</p>
  <p>Возраст: {{ user.age }}</p>
{% endblock %}
```

---

## 🔐 6. Пример авторизации через куки (упрощённо)

### 📌 Регистрация

```python
from passlib.hash import bcrypt

@app.post("/register")
async def register(username: str = Form(), password: str = Form()):
    hashed_password = bcrypt.hash(password)
    # сохранить в БД: username, hashed_password
```

### 📌 Логин и установка куки

```python
from fastapi.responses import RedirectResponse

@app.post("/login")
async def login(response: Response, username: str = Form(), password: str = Form()):
    user = await get_user(username)  # получи пользователя из БД
    if user and bcrypt.verify(password, user.password_hash):
        response = RedirectResponse(url="/profile", status_code=302)
        response.set_cookie("session_id", str(user.id))
        return response
    return HTMLResponse("Неверный логин или пароль", status_code=401)
```

---

### 📌 Получение текущего пользователя по `session_id`

```python
from fastapi import Depends, Request

async def get_current_user(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        return await get_user_by_id(session_id)
    return None

@app.get("/profile")
async def profile(request: Request, user=Depends(get_current_user)):
    if not user:
        return RedirectResponse("/login")
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})
```

---

## 💡 Заключение

| Что                  | Как                                              |
| -------------------- | ------------------------------------------------ |
| Подключить CSS       | через `/static/styles.css`                       |
| Использовать шаблоны | `Jinja2Templates`                                |
| Цикл                 | `{% for ... in ... %}`                           |
| Один объект          | `{{ object.field }}`                             |
| Авторизация          | через `set_cookie` и `Depends(get_current_user)` |

---

Можем продолжить прямо сейчас и реализовать регистрацию + вход с куками. Готов?
