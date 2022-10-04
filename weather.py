from config import token_weather
from pprint import pprint
import datetime
import requests


def get_weather(city='Гродно', token_weather=token_weather):
    global wd
    code_to_smile = {
        'Clear': 'Ясно ☀',
        'Clouds': 'Облачно ☁',
        'Rain': 'Дождь 🌧',
        'Drizzle': 'Дождь 🌧',
        'Thunderstorm': 'Гроза ⛈',
        'Snow': 'Снег 🌨',
        'Mist': 'Туман 🌫'
    }

    try:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={token_weather}")
        data = r.json()
        # pprint(data)
        cur_temp = data["main"]["temp"]
        weather = data['weather'][0]['main']
        if weather in code_to_smile:
            weather_desc = code_to_smile[weather]
        cur_humidity = data["main"]["humidity"]
        cur_pressure = data["main"]["pressure"]
        cur_wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")

        return [city, cur_temp, weather_desc, cur_humidity, cur_pressure, cur_wind, sunrise_timestamp, sunset_timestamp]

        # print(f'Погода в {city} сейчас.\n'
        #       f'Температура: {cur_temp}С {weather_desc}\n'
        #       f'Влажность: {cur_humidity}%\n'
        #       f'Давление: {cur_pressure} мм.рт.ст\n'
        #       f'Ветер: {cur_wind} м/с\n'
        #       f'Рассвет: {sunrise_timestamp}\n'
        #       f'Закат: {sunset_timestamp}\n')

    except Exception as ex:
        print(ex)


def main():
    city = 'Гродно'
    get_weather(city, token_weather)


if __name__ == '__main__':
    main()
