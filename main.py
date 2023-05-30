import requests
from aiogram import Bot
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from datetime import datetime
from config import bot_token, open_weather_token


bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    await message.reply("Введите название города: ")


@dp.message_handler()
async def get_weather(message: Message):
    try:
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={message.text}'
                         f'&appid={open_weather_token}'
                         f'&units=metric'
                         f'&lang=ru')

        data = r.json()

        city = data['name']
        cur_weather = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        wind_direction = data['wind']['deg']
        sunrise_timestamp = datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.fromtimestamp(data['sys']['sunset'])
        day_length = sunset_timestamp - sunrise_timestamp

        temperature_icons = {
            'Clear': 'Ясно \U00002600',
            'Clouds': 'Облачно \U00002601',
            'Rain': 'Дождь \U00002614',
            'Drizzle': 'Морось \U00002614',
            'Thunderstorm': 'Гроза \U0001F329',
            'Snow': 'Снег \U0001F328',
            'Mist': 'Туман \U0001f32B'
        }

        weather_main = data['weather'][0]['main']
        if weather_main in temperature_icons:
            weather = temperature_icons[weather_main]
        else:
            weather = "Непонятная погода"

        if wind_direction in range(330, 360) or wind_direction in range(0, 30):
            wd = 'C \U00002B07'
        elif wind_direction in range(30, 60):
            wd = 'CВ \U00002199'
        elif wind_direction in range(60, 120):
            wd = 'В \U00002B05'
        elif wind_direction in range(120, 150):
            wd = 'ЮВ \U00002196'
        elif wind_direction in range(150, 210):
            wd = 'Ю \U00002B06'
        elif wind_direction in range(210, 240):
            wd = 'ЮЗ \U00002197'
        elif wind_direction in range(240, 300):
            wd = 'З \U000027A1'
        elif wind_direction in range(300, 330):
            wd = 'СЗ \U00002198'
        else:
            wd = 'Непонятный ветер'

        await message.reply(f"\n{datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
                            f"Погода в городе: {city}\n"
                            f"Температура: {cur_weather:.1f} C° ({weather})\n"
                            f"Ветер: {wind} м/с ({wd})\n"
                            f"Влажность: {humidity}%\n"
                            f"Давление: {int(pressure/1.333)} мм.рт.ст\n"
                            f"Рассвет: {sunrise_timestamp.strftime('%H:%M')}\n"
                            f"Закат: {sunset_timestamp.strftime('%H:%M')}\n"
                            f"Продолжительность дня: {day_length}\n")

    except Exception:
        await message.reply(f"Ошибка.\nПроверьте правильность ввода города")


if __name__ == '__main__':
    executor.start_polling(dp)
