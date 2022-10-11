from dataclasses import dataclass
from typing import NamedTuple
from datetime import datetime

import requests

from config import token_weather


@dataclass
class TypeWeather:
    CLEAR = "Ясно ☀"
    CLOUDS = 'Облачно ☁'
    RAIN = 'Дождь 🌧'
    DRIZZLE = 'Дождь 🌧'
    THUNDERSTORM = 'Гроза ⛈'
    SNOW = 'Снег 🌨'
    MIST = 'Туман 🌫'


class Weather(NamedTuple):
    city: str
    temperature: float
    describe: TypeWeather
    himidity: int
    pressure: int
    wind_speed: float
    at_time: datetime
    sunrise: datetime
    sunset: datetime


class EmptyWeather(Exception):
    pass


def get_weather(city: str = 'Гродно') -> Weather | EmptyWeather:
    r = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={token_weather}")

    if not r.status_code == 200:
        return EmptyWeather(f'Неудачный запрос. Код ответа от сервера: {r.status_code}')

    try:
        data = r.json()
    except:
        return EmptyWeather(f'Что-то пошло не так с обработкой ответа')

    if not data['cod'] == 200:
        return EmptyWeather('По заданным параметрам не найдена погода')

    cur_temp = data["main"]["temp"]
    weather_desc = data['weather'][0]['main']
    
    # Берем значение атрибута из TypeWeather в зависимости от weather_desc
    weather_desc = getattr(TypeWeather, weather_desc.upper())
    cur_humidity = data["main"]["humidity"]
    cur_pressure = data["main"]["pressure"]
    cur_wind = data["wind"]["speed"]
    at_time = datetime.fromtimestamp(data['dt'])
    sunrise_timestamp = datetime.fromtimestamp(data["sys"]["sunrise"])
    sunset_timestamp = datetime.fromtimestamp(data["sys"]["sunset"])

    return Weather(city=city, temperature=cur_temp, describe=weather_desc,
                   himidity=cur_humidity, pressure=cur_pressure, wind_speed=cur_wind,
                   at_time=at_time, sunrise=sunrise_timestamp, sunset=sunset_timestamp)


def main():
    weather = get_weather(city='Гродно')

    if isinstance(weather, EmptyWeather):
        raise weather

    print(f'Погода в {weather.city} сейчас.\n'
          f'Актуально на {weather.at_time.strftime("%d.%m.%Y %H:%M")}.\n\n'
          f'Температура: {weather.temperature}С {weather.describe}\n'
          f'Влажность: {weather.himidity}%\n'
          f'Давление: {weather.pressure} мм.рт.ст\n'
          f'Ветер: {weather.wind_speed} м/с\n'
          f'Рассвет: {weather.sunrise.strftime("%d.%m.%Y %H:%M")}\n'
          f'Закат: {weather.sunset.strftime("%d.%m.%Y %H:%M")}')


if __name__ == '__main__':
    main()
