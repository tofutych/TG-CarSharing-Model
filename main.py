import telebot
import json
from telebot import types
from bot_token import TOKEN
from Gender import Gender
from User import User
from os import listdir

bot = telebot.TeleBot(TOKEN)

user_dict = {}


def gender_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    buttons = []
    for gender in Gender.all():
        buttons.append(types.KeyboardButton(gender.title()))
    kb.add(*buttons)
    return kb


@bot.message_handler(commands=["start"])
def start(message):
    if f'{message.chat.id}.json' not in listdir('./users'):
        msg = bot.reply_to(
            message, f"Привет, {message.chat.first_name}!\nКак тебя зовут?")
        bot.register_next_step_handler(msg, process_name_step)
    else:
        print('on tut')


def process_name_step(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)
        user_dict[chat_id].id = chat_id
        msg = bot.send_message(chat_id, 'Выберите пол\nЕсли его здесь нет, то напишите самостоятельно', reply_markup=gender_kb())
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, 'ooops!!')


def process_sex_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        Gender(message.text)
        user.sex = message.text
        msg = bot.send_message(chat_id, 'Сколько вам полных лет?', reply_markup=types.ReplyKeyboardRemove(selective=False))
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'ooops!!')


def process_age_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.age = message.text

        msg = bot.send_message(chat_id, 'Ваш номер телефона')
        bot.register_next_step_handler(msg, process_phone_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')


def process_phone_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.phone = message.text

        msg = bot.send_message(chat_id, 'Номер водительского удостоверения')
        bot.register_next_step_handler(msg, process_license_number)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')


def process_license_number(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.license_number = message.text

        msg = bot.send_message(chat_id, 'Стаж вождения')
        bot.register_next_step_handler(msg, process_experience)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')


def process_experience(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.experience = message.text

        user_dict[chat_id] = user.__dict__
        user.save()
    except Exception as e:
        bot.reply_to(message, 'ooops!!')


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)
