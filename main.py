import json
from os import listdir
from time import sleep

import telebot
from telebot import types

from bot_token import TOKEN
from Gender import Gender
from User import User

bot = telebot.TeleBot(TOKEN)

user_dict = {}


def main_menu_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton(text="Информация о профиле", callback_data="profile")
    )
    kb.add(types.InlineKeyboardButton(text="Машины на карте", callback_data="cars"))
    return kb


def back_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="↩️", callback_data="main_menu"))
    return kb


def gender_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    buttons = []
    for gender in Gender.all():
        buttons.append(types.KeyboardButton(gender.title()))
    kb.add(*buttons)
    return kb


@bot.message_handler(commands=["start"])
def start(message):
    # if f"{message.chat.id}.json" not in listdir("./users"):
    #     msg = bot.reply_to(
    #         message, f"Привет, {message.chat.first_name}!\nВведите ваше имя"
    #     )
    #     bot.register_next_step_handler(msg, process_name_step)
    # else:
    #     print("on tut")

        msg = bot.reply_to(
            message, f"Привет, {message.chat.first_name}!\nВведите ваше имя"
        )
        bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)
        user_dict[chat_id].id = chat_id

        msg = bot.send_message(chat_id, "Введите вашу фамилию")
        bot.register_next_step_handler(msg, process_surname_step)
    except Exception as e:
        bot.reply_to(message, "ooops!!")


def process_surname_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.surname = message.text
        msg = bot.send_message(
            chat_id,
            "Выберите гендер\nЕсли его здесь нет, то напишите самостоятельно",
            reply_markup=gender_kb(),
        )
        bot.register_next_step_handler(msg, process_gender_step)
    except Exception as e:
        bot.reply_to(message, "ooops!!")


def process_gender_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        Gender(message.text)
        user.gender = message.text

        msg = bot.send_message(
            chat_id,
            "Введите дату рождения в формате ДД.ММ.ГГГГ",
            reply_markup=types.ReplyKeyboardRemove(selective=False),
        )
        bot.register_next_step_handler(msg, process_bdate_step)
    except Exception as e:
        bot.reply_to(message, "ooops!!")


def process_bdate_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.bdate = message.text

        msg = bot.send_message(chat_id, "Ваш номер телефона")
        bot.register_next_step_handler(msg, process_phone_step)
    except Exception as e:
        bot.reply_to(message, "ooops!!")


def process_phone_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.phone = message.text

        msg = bot.send_message(chat_id, "Номер водительского удостоверения")
        bot.register_next_step_handler(msg, process_license_number)
    except Exception as e:
        bot.reply_to(message, "ooops!!")


def process_license_number(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.license_number = message.text

        msg = bot.send_message(chat_id, "Стаж вождения")
        bot.register_next_step_handler(msg, process_experience)

    except Exception as e:
        bot.reply_to(message, "ooops!!")


def process_experience(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.experience = message.text
        user.save()

        bot.reply_to(message, "Регистрация звершена!")
        bot.send_message(chat_id, "Меню", reply_markup=main_menu_kb())
    except Exception as e:
        bot.reply_to(message, "ooops!!")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "main_menu":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"Меню",
            reply_markup=main_menu_kb(),
        )
    elif call.data == "profile":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=str(user_dict[call.message.chat.id]),
            reply_markup=back_kb(),
        )
    elif call.data == "cars":
        photo = open("kchau.jpg", "rb")
        bot.send_photo(call.message.chat.id, photo)
        sleep(1)
        bot.delete_message(call.message.chat.id, call.message.message_id + 1)


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

if __name__ == "__main__":
    bot.polling(none_stop=True)
