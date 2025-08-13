---

# 🚀 ANSAR — Современная платформа активностей

![FastAPI](https://img.shields.io/badge/FastAPI-async-green?logo=fastapi)
![Jinja2](https://img.shields.io/badge/Jinja2-templates-blue?logo=jinja)
![Docker](https://img.shields.io/badge/Docker-ready-blue?logo=docker)
![SQLite](https://img.shields.io/badge/SQLite-lightgrey?logo=sqlite)
![Status](https://img.shields.io/badge/Production-ready-brightgreen)

---

## 📝 Описание

**ANSAR** — это современное веб-приложение для поиска, добавления и отслеживания интересных активностей и мест.  
Платформа поддерживает регистрацию, авторизацию, личный кабинет, избранное, историю, рекомендации, а также удобную панель модератора.

---

## 🌟 Основные возможности

- **Регистрация и авторизация** (через куки)
- **Анкета пользователя** после регистрации
- **Личный кабинет** с историей, рекомендациями и избранным
- **Добавление/удаление активностей в избранное**
- **Современный UI** (Jinja2 + кастомные стили)
- **Панель модератора** (управление пользователями и активностями)
- **Безопасность**: защита роутов, роли, куки, валидация
- **Загрузка изображений** для активностей
- **Docker-окружение** для быстрого запуска

---

## 🛠️ Технологический стек

| Компонент        | Технология                       |
| ---------------- | -------------------------------- |
| Backend API      | FastAPI (async)                  |
| ORM              | SQLAlchemy (async) + aiosqlite   |
| БД               | SQLite                           |
| Frontend         | Jinja2 + HTML5 + CSS3            |
| Авторизация      | Cookies + JWT                    |
| UI               | Jinja2, кастомные стили          |
| Контейнеризация  | Docker, Docker Compose           |
| Бот              | aiogram (Telegram Bot)           |

---

## 📂 Структура проекта

```
hac_ans_fast/
│
├── app/
│   ├── main.py
│   ├── routes/
│   ├── templates/
│   ├── static/
│   ├── shemas/
│   ├── config.py
│   └── Dockerfile
├── database/
│   ├── models.py
│   ├── crud.py
│   ├── db.py
│   └── __init__.py
├── tg_admin_bot/
│   ├── main.py
│   └── Dockerfile
├── tests/
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## ⚡ Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/ibras0696/hac_ans_fast.git
cd hac_ans_fast
```

### 2. Запуск через Docker Compose

```bash
docker-compose build --no-cache
docker-compose up -d
```

### 3. Откройте в браузере

```
http://localhost:8000
```

---

## 🔑 Авторизация и роли

- **Регистрация**: через форму, пароли хешируются
- **Авторизация**: через куки (session_token)
- **Роли**: пользователь / модератор (панель управления)
- **Защита роутов**: через Depends и Middleware

---

## 💙 Избранное

- Добавляйте активности в избранное одним кликом
- Удаляйте из избранного прямо из профиля или списка
- Все избранные доступны в личном кабинете

---

## 🖼️ Загрузка изображений

- Поддерживаемые форматы: JPG, PNG, GIF, WebP, SVG
- Без ограничения на размер файла (кроме ограничений сервера)
- Все изображения хранятся в `/static/uploads/`

---

## 🧑‍💻 Для разработчиков

- Все зависимости — в `requirements.txt`
- Настройки — через `.env`
- Миграции — через Alembic
- Тесты — в папке `tests/`

---

## 📞 Контакты и поддержка

- **Telegram:** [@kokokp95](https://t.me/your_tg)
- **Почта:** ibras@gmail.com
- **GitHub Issues:** для багов и предложений

---

## 🏆 Скриншоты

> _Добавьте сюда красивые скриншоты интерфейса для презентации!_

---

## 📝 Лицензия

MIT License

---

**Сделано с любовью и вниманием к UX!**

---

# Запуск проекта через докер компост
```bash
docker-compose down --rmi all --volumes --remove-orphans
docker-compose build --no-cache
docker-compose up -d
```
