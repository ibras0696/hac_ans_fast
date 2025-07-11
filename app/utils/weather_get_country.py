import aiohttp
import asyncio

# 🔑 API-ключ для геокодинга
API_KEY = "68704a352e3c7425979031dtzd7db3a"

# 🧭 Словарь расшифровки погодных кодов
WEATHER_CODES = {
    0: "Ясно",
    1: "В основном ясно",
    2: "Частично облачно",
    3: "Пасмурно",
    45: "Туман",
    48: "Иней",
    51: "Слабая морось",
    53: "Морось",
    55: "Сильная морось",
    61: "Слабый дождь",
    63: "Дождь",
    65: "Сильный дождь",
    80: "Ливень",
    81: "Сильный ливень",
    82: "Очень сильный ливень"
}


async def get_coordinates(city: str, session: aiohttp.ClientSession) -> tuple[float, float] | tuple[None, None]:
    """
    Получает координаты (широту и долготу) по названию города с использованием API Maps.co.

    :param city: Название города (например, "Москва").
    :return: Кортеж из широты и долготы (lat, lon) или (None, None) при ошибке.
    """
    url = f"https://geocode.maps.co/search?q={city}&api_key={API_KEY}"
    try:
        async with session.get(url, timeout=10) as response:
            response.raise_for_status()
            data = await response.json()
            if not data:
                return None, None
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return lat, lon
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return None, None
    except (KeyError, ValueError):
        return None, None


async def get_weather(lat: float, lon: float, session: aiohttp.ClientSession) -> dict:
    """
    Получает текущую погоду по координатам с API Open-Meteo.

    :param lat: Широта местоположения.
    :param lon: Долгота местоположения.
    :return: Словарь с погодными данными (temperature, windspeed, weathercode, time) или пустой словарь при ошибке.
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )
    try:
        async with session.get(url, timeout=10) as response:
            response.raise_for_status()
            data = await response.json()
            return data.get("current_weather", {})
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return {}
    except KeyError:
        return {}


async def pars_weather_country(city: str) -> list:
    """
    Основная функция: получает координаты по городу, затем текущую погоду по этим координатам.

    :param city: Название города.
  :return: Словарь с информацией о погоде в формате:
    [
        city,           # str: Название города, например "Москва"
        temperature,    # float | None: Температура воздуха в градусах Цельсия
        windspeed,      # float | None: Скорость ветра в километрах в час
        description,    # str: Текстовое описание погодного состояния (например, "Ясно", "Пасмурно", "Дождь")
        weathercode,    # int | None: Код погоды по Open-Meteo, например 0, 1, 2, 3 и т.д.
        time            # str | None: Время обновления данных в формате ISO 8601 (например, "2025-07-11T14:00")
    ]
    """
    async with aiohttp.ClientSession() as session:
        lat, lon = await get_coordinates(city, session)
        if lat is None or lon is None:
            return []
        if lat is None or lon is None:
            return []
        weather = await get_weather(lat, lon, session)
        if not weather:
            return []

    code = weather.get("weathercode")
    description = WEATHER_CODES.get(code, "Неизвестная погода")

    return [
        city,
        weather.get("temperature"),
        weather.get("windspeed"),
        description,
        weather.get("time")
    ]


# Пример вызова (можно убрать или использовать как заготовку под бота/интерфейс)
if __name__ == "__main__":
    result = asyncio.run(pars_weather_country("Москва"))
    print(result)
