# routes/auth.py
from fastapi import APIRouter, HTTPException, Depends, Request, Response
from fastapi.responses import RedirectResponse
from fastapi import Form
from fastapi.templating import Jinja2Templates
from app.templates import ALL_TEMPLATES_DIR
from fastapi.responses import HTMLResponse

from app.utils.security import hash_password, verify_password, create_access_token, decode_access_token
from app.shemas.user import UserCreate, Token
from database.crud import CrudUser, User

router = APIRouter()

templates = Jinja2Templates(directory=ALL_TEMPLATES_DIR)


async def get_current_user_from_cookie(request: Request) -> User | None:
    """Получает текущего пользователя из cookie сессии"""
    session_token = request.cookies.get("session_token")
    if not session_token:
        return None
    
    user_id = decode_access_token(session_token)
    if not user_id:
        return None
    
    user = await CrudUser().get_user_by_id(user_id)
    return user


@router.get("/register", response_class=HTMLResponse)
async def get_form_register(request: Request):
    return templates.TemplateResponse("register.html",
                                      {
                                          "request": request,
                                          "current_user": request.state.current_user
                                      })


@router.post("/register", response_model=Token)
async def register(
        response: Response,
        fullname: str = Form(...),
        username: str = Form(...),
        password: str = Form(...),
        password2: str = Form(...)
):
    if password != password2:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    existing = await CrudUser().get_user_by_username(username)
    if existing:
        return RedirectResponse(url="/auth/login", status_code=302)

    user_obj = await CrudUser().add_user(
        username=username,
        password_hash=hash_password(password),
        full_name=fullname
    )
    
    # Создаем токен и устанавливаем cookie
    token = create_access_token(user_obj.id)
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        max_age=60 * 60 * 24,  # 1 день
        samesite="lax"
    )
    return response


@router.get("/login", response_class=HTMLResponse)
async def get_form_login(request: Request):
    return templates.TemplateResponse("login.html",
                                      {
                                          "request": request,
                                          "current_user": request.state.current_user
                                      })


@router.post("/login")
async def login(
        response: Response,
        username: str = Form(...),
        password: str = Form(...)
):
    db_user = await CrudUser().get_user_by_username(username)
    if not db_user or not verify_password(password, db_user.password_hash):
        return RedirectResponse(url="/auth/login?error=invalid_credentials", status_code=302)

    # Создаем токен и устанавливаем cookie
    token = create_access_token(db_user.id)
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        max_age=60 * 60 * 24,  # 1 день
        samesite="lax"
    )
    return response


@router.get("/logout")
async def logout(response: Response):
    """Выход из аккаунта - удаляем cookie"""
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("session_token")
    return response


@router.get("/me")
async def get_me(request: Request):
    """Получение информации о текущем пользователе"""
    user = await get_current_user_from_cookie(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "is_moderator": user.is_moderator
    }
