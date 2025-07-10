import os

import dotenv

dotenv.load_dotenv()


# Токен Телеграмм Бота
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Домен сайта
DOMEN = os.getenv('DOMEN')

# Ссылка на сайт
URL_DOMEN = os.getenv('URL_DOMEN')