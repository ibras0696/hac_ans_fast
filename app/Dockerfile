FROM python:3.12-slim
WORKDIR /app

# Устанавливаем PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/:/app:/database"

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем только код приложения
COPY ./app .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]