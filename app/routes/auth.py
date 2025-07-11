# routes/auth.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import status

from utils import hash_password, verify_password, create_access_token, decode_access_token, get_current_user
from shemas.user import UserCreate, Token
from database.crud import CrudUser, User


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    existing = await CrudUser().get_user_by_username(user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    user_obj = await CrudUser().add_user(
        username=user.username,
        password_hash=hash_password(user.password),
        full_name=user.full_name or ""
    )
    token = create_access_token(user_obj.id)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(user: UserCreate):
    db_user = await CrudUser().get_user_by_username(user.username)
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(db_user.id)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def get_me(token: str = Depends(oauth2_scheme)):
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await CrudUser().get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "is_moderator": user.is_moderator
    }



