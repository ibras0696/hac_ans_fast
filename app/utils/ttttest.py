import requests

BASE_URL = "http://127.0.0.1:8001/auth"

def ttest_register():
    print("📦 Регистрируем нового пользователя...")
    data = {
        "username": "testuser",
        "password": "testpass",
        "full_name": "Тестовый Пользователь"
    }
    response = requests.post(f"{BASE_URL}/register", json=data)
    if response.status_code == 400:
        print("⚠️ Уже существует (или другая ошибка):", response.json())
        return None
    response.raise_for_status()
    token = response.json()["access_token"]
    print("✅ Успешно зарегистрирован. Токен:", token[:30], "...")
    return token

def ttest_login():
    print("\n🔐 Выполняем логин...")
    data = {
        "username": "testuser",
        "password": "testpass"
    }
    response = requests.post(f"{BASE_URL}/login", json=data)
    response.raise_for_status()
    token = response.json()["access_token"]
    print("✅ Логин успешен. Токен:", token[:30], "...")
    return token

def ttest_me(token: str):
    print("\n👤 Проверяем /me...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    response.raise_for_status()
    print("✅ Данные пользователя:", response.json())

if __name__ == "__main__":
    # 1. Регистрируем или пропускаем
    reg_token = ttest_register()
    # 2. Логинимся и получаем токен
    token = ttest_login()
    # 3. Проверяем доступ к /me
    ttest_me(token)
