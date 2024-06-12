import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils import executor
import requests

API_TOKEN = '6901249175:AAGUdehXeDCE-PjD0euTqn4d5efLau2uqdA'
API_URL = 'http://127.0.0.1:8000/users/users/'
CODE_VERIFICATION_URL = 'http://127.0.0.1:8000/users/code/'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

user_data = {}
url = "http://127.0.0.1:8000/users/code/"


def get_user_id_by_username(username):
    url = f"{API_URL}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        users = response.json()
        for user in users:
            if user.get('username') == username:
                return user.get('id')
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching users: {e}")
        return None


async def check_registration(user_info, url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        for user in data:
            if all(user.get(key) == value for key, value in user_info.items()):
                return True
        return False
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False


@dp.message_handler(commands=['start', 'register'])
async def send_welcome(message: types.Message):
    await message.reply("Введите ФИО")
    user_data[message.from_user.id] = {}


@dp.message_handler(lambda message: message.from_user.id in user_data and 'first_name' not in user_data[message.from_user.id])
async def process_full_name(message: types.Message):
    full_name = message.text.strip().split()
    if len(full_name) >= 2:
        user_data[message.from_user.id]['first_name'] = full_name[0]
        user_data[message.from_user.id]['last_name'] = ' '.join(full_name[1:])
        await message.reply("Отправьте свой контактный прозвище.")
    else:
        await message.reply("Пожалуйста, напишите свое полное имя и фамилию.")


@dp.message_handler(
    lambda message: message.from_user.id in user_data and 'username' not in user_data[message.from_user.id])
async def process_username(message: types.Message):
    user_data[message.from_user.id]['username'] = message.text
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton("Отправьте свой контактный номер", request_contact=True)
    keyboard.add(button)
    await message.reply("Отправьте свой контактный номер:", reply_markup=keyboard)


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def process_contact(message: types.Message):
    if message.contact is not None:
        user_data[message.from_user.id]['phone_number'] = message.contact.phone_number
        await message.reply("Отправьте свой почтовый адрес!", reply_markup=ReplyKeyboardRemove())
    else:
        await message.reply("Отправьте свой контактный номер.")

@dp.message_handler(
    lambda message: message.from_user.id in user_data and 'email' not in user_data[message.from_user.id])
async def process_email(message: types.Message):
    user_data[message.from_user.id]['email'] = message.text
    user_id = message.from_user.id
    data = user_data[user_id]
    response = requests.post(API_URL, data=data)
    if response.status_code == 201:
        await message.reply("Код успешно отправлен на вашу электронную почту!")
    else:
        await message.reply("Вы ввели неверный адрес электронной почты, начните с /start.")
    # user_data.pop(user_id, None)


@dp.message_handler(
    lambda message: message.from_user.id in user_data and 'email' in user_data[message.from_user.id])
async def process_verification_code(message: types.Message):
    username = user_data[message.from_user.id]['username']
    user_id = get_user_id_by_username(username)
    if user_id is None:
        await message.reply("Пользователь не найден.")
        return
    user_info = {
        'user': user_id,
        'otp': message.text
    }
    user_registered = await check_registration(user_info, url)
    if user_registered:
        await message.reply("Вы зарегистрированы.С Вами свяжется наш менеджер!.")
    else:
        await message.reply("Вы отправили неверный код, пожалуйста, проверьте и отправьте его повторно.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
