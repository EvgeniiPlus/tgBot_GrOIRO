import asyncio
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher.filters import Text
from config import token, channel_id
from news import check_news_update
from weather import get_weather
from timetable import get_timetable, show_list_timetable

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ['Анонсы мероприятий(в разработке)', 'Последние 5 новостей', 'Расписание занятий', 'Погода в Гродно',
                     'Сообщить об ошибке(в разработке)']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer(f'Добро пожаловать в наш чат-бот, {message.from_user.first_name}!\n'
                         f'Если Вы нашли ошибку в работе чат-бота, напишите об этом, выбрав соответствующий пункт меню.\n'
                         f'А сейчас выберите необходимое действие в меню.', reply_markup=keyboard)


@dp.message_handler(Text(equals='Последние 5 новостей'))
async def get_last_five_news(message: types.Message):
    with open('news_dict.json') as f:
        news_dict = json.load(f)

    for k, v in sorted(news_dict.items())[-5:]:
        image = types.input_file.InputFile.from_url(v['article_img'])
        news = f"🔥{hbold(v['article_title'])}🔥\n\n" \
               f"Подробнее 👉{hlink('ЗДЕСЬ', v['article_url'])}🎓"
        await message.answer_photo(image, news)


@dp.message_handler(Text(equals="Погода в Гродно"))
async def get_weather_in_Grodno(message: types.Message):
    weather = get_weather()
    await message.answer(f'🌎 {hbold("Погода в Гродно сейчас.")} 🌈\n\n'
                         f'{weather[2]}\n'
                         f'Температура: {round(weather[1])}°С\n'
                         f'Влажность: {weather[3]}%\n'
                         f'Давление: {weather[4]} мм.рт.ст\n'
                         f'Ветер: {weather[5]} м/с\n'
                         f'Рассвет: {weather[6]}\n'
                         f'Закат: {weather[7]}\n\n'
                         f'{hbold("🤩 Хорошего дня 🤩")}')


@dp.message_handler(Text(equals="Расписание занятий"))
async def get_weather_in_Grodno(message: types.Message):
    dict_ttables = show_list_timetable()
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    for k, v in dict_ttables.items():
        markup.add(types.InlineKeyboardButton(f'{k} {v}', callback_data=k))
    await bot.send_message(message.from_user.id, 'Выберите Ваше ПК:', reply_markup=markup)

    @dp.callback_query_handler(lambda call: True)
    async def send_timetable(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        if callback_query.data in dict_ttables:
            tt = get_timetable(callback_query.data)
            await message.answer(f"{hbold('Ваше ПК:')} {tt[0]}.\n\n")
            await message.answer_document(open(tt[1], "rb"), caption='Ваше расписание ☝')


async def news_every_10_minute():
    while True:
        fresh_news = check_news_update()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                image = types.input_file.InputFile.from_url(v['article_img'])
                news = f"🔥{hbold(v['article_title'])}🔥\n\n" \
                       f"Подробнее 👉{hlink('ЗДЕСЬ', v['article_url'])}🎓"
                await bot.send_photo(channel_id, image, news)

        await asyncio.sleep(600)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_10_minute())
    executor.start_polling(dp)
