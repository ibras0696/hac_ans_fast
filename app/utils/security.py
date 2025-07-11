from passlib.hash import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from database.models import User

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 день

# Хеширование пароля
def hash_password(password: str) -> str:
    return bcrypt.hash(password)

# Проверка пароля
def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.verify(password, hashed)

# Создание JWT токена
def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": str(user_id), "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Расшифровка токена
def decode_access_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload.get("sub"))
    except JWTError:
        return None
