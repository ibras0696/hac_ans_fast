import os
from uuid import uuid4

import dotenv

dotenv.load_dotenv()


# Токен Телеграмм Бота
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Домен сайта
DOMEN = os.getenv('DOMEN')

# Ссылка на сайт
URL_DOMEN = os.getenv('URL_DOMEN')


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", str(uuid4))
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()