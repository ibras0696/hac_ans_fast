# utils/security.py

from passlib.hash import bcrypt

# Преобразования пароля в хеш
def hash_password(password: str) -> str:
    return bcrypt.hash(password)

# Проверка хеш пароля   Пароль | Хеш пароля
def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.verify(password, password_hash)


print(hash_password('124'))