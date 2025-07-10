FROM python:3.12-slim
WORKDIR /app

# Копируем общий requirements.txt из корня проекта
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем только содержимое папки tg_admin_bot
COPY ./tg_admin_bot .

CMD ["python", "main.py"]