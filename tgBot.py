import asyncio
import json

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher.filters import Text

from config import token, channel_id, admin_id
from news import check_news_update
from weather import get_weather, EmptyWeather
from timetable import get_timetable, show_list_timetable
from announcement import check_ann_update, get_announcements

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
users_dict = {}


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ['Анонсы мероприятий',
                     'Последние 5 новостей',
                     'Расписание занятий',
                     'Погода в Гродно',
                     ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    global user_id
    user_id = message.from_user.id
    name = message.from_user.first_name
    last_name = message.from_user.last_name
    date = message.date.ctime()
    # def user_photo(message):
    #     photo = bot.get_user_profile_photos(message.from_user.id)
    #     bot.send_photo(message.chat.id, photo.photos[0][2].file_id)

    # users_dict[user_id] = {
    #     'name': name,
    #     'last_name': last_name,
    #     'date': date,
    # }

    with open('users.txt', 'a') as f:
        f.write(f' {date} {user_id} {name} {last_name}\n')

    await message.answer(
        f'Добрый день, {message.from_user.first_name}!\n👩🏻‍🏫 Добро пожаловать в чат-бот Гродненского областного института развития образования!‍🎓‍🏫‍ \n'
        f'👏Рады Вас приветствовать!👏\n'
        f'Больше информации Вы можете получить на нашем сайте {hlink("groiro.by", "https://groiro.by/")}.\n'
        f'Выберите один из пунктов меню ниже👇', reply_markup=keyboard, disable_web_page_preview=True)


@dp.message_handler(Text(equals='Последние 5 новостей'))
async def get_last_five_news(message: types.Message):
    with open('news_dict.json') as f:
        news_dict = json.load(f)

    for k, v in sorted(news_dict.items())[-5:]:
        image = types.input_file.InputFile.from_url(v['article_img'])
        news = f"🔥{hbold(v['article_title'])}🔥\n\n" \
               f"Подробнее 👉{hlink('ЗДЕСЬ', v['article_url'])}🎓"
        await message.answer_photo(image, news)


@dp.message_handler(Text(equals='Анонсы мероприятий'))
async def get_announcement(message: types.Message):
    ann_dict = get_announcements()

    for k, v in sorted(ann_dict.items()):
        ann = f"{hbold(v['ann_title'])}\n\n" \
              f"{hbold('Дата: ' + v['ann_date'])}\n\n" \
              f"Подробнее 👉{hlink('ЗДЕСЬ', v['ann_url'])}🎓"
        # print(ann)
        await message.answer(ann, disable_web_page_preview=True)


# @dp.message_handler(Text(equals='Сообщить об ошибке'))
# async def get_error_message(message: types.Message):
#     await message.answer('Введите Ваше сообщение и нажмите "Отправить"')
#
#     @dp.callback_query_handler(lambda call: True)
#     async def get_message_from_user(callback_query: types.CallbackQuery):
#         await bot.send_message(admin_id,
#                                f'Пользователь {message.from_user.first_name + " " + message.from_user.last_name}'
#                                f'(id: {message.from_user.id}) написал Вам сообщение.\n\n'
#                                f'{callback_query.data}')
#         await message.answer('Спасибо, Ваше сообщение отправлено администратору.')



@dp.message_handler(Text(equals="Погода в Гродно"))
async def get_weather_in_Grodno(message: types.Message):
    weather = get_weather()
    if isinstance(weather, EmptyWeather):
        await message.answer(
            f'Возникла ошибка при получении погоды.\nВероятно мы уже знаем об этом.\nПожалуйста, попробуйте позже.')
        # raise weather
        # print(weather)
    else:
        await message.answer(f'🌎 {hbold("Погода в Гродно сейчас.")} 🌈\n\n'
                             f'{hbold("Актуально на")} {weather.at_time.strftime("%d.%m %H:%M")}\n\n'
                             f'{weather.describe}\n'
                             f'{hbold("Температура:")} {round(weather.temperature)}°С\n'
                             f'{hbold("Влажность:")} {weather.himidity}%\n'
                             f'{hbold("Давление:")} {weather.pressure} мм.рт.ст\n'
                             f'{hbold("Ветер:")} {weather.wind_speed} м/с\n'
                             f'{hbold("Рассвет:")} {weather.sunrise.strftime("%d.%m %H:%M")}\n'
                             f'{hbold("Закат:")} {weather.sunset.strftime("%d.%m %H:%M")}\n\n'
                             f'{hbold("🤩 Хорошего дня 🤩")}')


@dp.message_handler(Text(equals="Расписание занятий"))
async def choose_timetable(message: types.Message):
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
            await message.answer_document(open(tt[1], "rb"),
                                          caption='Ваше расписание ☝. Нажмите на него, чтобы скачать.')


async def news_every_10_minute():
    while True:
        fresh_news = check_news_update()
        fresh_anns = check_ann_update()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                image = types.input_file.InputFile.from_url(v['article_img'])
                news = f"🔥{hbold(v['article_title'])}🔥\n\n" \
                       f"Подробнее 👉{hlink('ЗДЕСЬ', v['article_url'])}🎓"
                await bot.send_photo(user_id, image, news)

        if len(fresh_anns) >= 1:
            for k, v in sorted(fresh_anns.items()):
                ann = f"{hbold(v['ann_title'])}\n\n" \
                      f"{hbold('Дата: ' + v['ann_date'])}\n\n" \
                      f"Подробнее 👉{hlink('ЗДЕСЬ', v['ann_url'])}🎓"
                await bot.send_message(user_id, ann)

        await asyncio.sleep(600)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_10_minute())
    executor.start_polling(dp)
