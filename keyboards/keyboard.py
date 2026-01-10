from telebot.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton
)

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button_8600 = KeyboardButton(text="MX8600")
    button_8600S = KeyboardButton(text="MX8600S")
    button_reset = KeyboardButton(text="Сбросить")
    keyboard.add(button_8600, button_8600S, button_reset)
    return keyboard

def get_back_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Выбор модели"))
    return keyboard