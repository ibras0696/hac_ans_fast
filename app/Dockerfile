FROM python:3.12-slim
WORKDIR /app

# Копируем общий requirements.txt из корня проекта
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем только содержимое папки app (не весь проект)
COPY ./app .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]