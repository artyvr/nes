#!/usr/bin/python

import asyncio
import os
from telebot.async_telebot import AsyncTeleBot
from telebot import apihelper
from collections import defaultdict
from database.models import MX8600, MX8600S
from database.session import get_db_session
from database.utils import test_async_connection
from sqlalchemy import select
from keyboards.keyboard import get_main_keyboard, get_back_keyboard


bot = AsyncTeleBot(os.environ["NES_TELEGRAM_BOT_TOKEN"])
bot.request_timeout = 60
apihelper.READ_TIMEOUT = 60
apihelper.CONNECT_TIMEOUT = 30 

user_states = defaultdict(dict)


@bot.message_handler(commands=['start'])
async def send_welcome(message):
    user_id = message.from_user.id
    user_states[user_id] = {'model': None}
    text = ("⚠️ Выбери модель и укажи ошибку")
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=get_main_keyboard())


@bot.message_handler(func=lambda m: m.text in ["MX8600", "MX8600S"])
async def set_model(message):
    user_id = message.from_user.id
    model_text = message.text
    if model_text == "MX8600":
        user_states[user_id]['model'] = 'MX8600'
        model_name = "MX8600"
    else:
        user_states[user_id]['model'] = 'MX8600S'
        model_name = "MX8600S"
    response = (
        f"✅ *Выбрана модель: {model_name}*\n\n"
        f"Теперь введите код ошибки.\n"
    )
    await bot.reply_to(
        message, 
        response, 
        reply_markup=get_back_keyboard(),
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda m: m.text == "Выбор модели")
async def back_to_models(message):
    """Возврат к выбору модели"""
    await send_welcome(message)

@bot.message_handler(func=lambda m: m.text == "Сбросить")
async def reset_state(message):
    """Сброс состояния пользователя"""
    user_id = message.from_user.id
    user_states[user_id] = {'model': None}
    await send_welcome(message)

@bot.message_handler(func=lambda message: message.text in ["MX8600", "MX8600S"])
async def handle_model(message):
    """Обработка выбора модели"""
    model = message.text
    response = f"✅ Выбрана модель {model}\n\nТеперь введите код ошибки."
    await bot.reply_to(message, response)


@bot.message_handler(content_types=['text'])
async def search_error(message):
    user_id = message.from_user.id
    error_code = message.text.strip().upper()
    if error_code in ["MX8600", "MX8600S", "Сбросить", "Выбор модели"]:
        return
    if not user_states[user_id].get('model'):
        await bot.reply_to(
            message,
            "⚠️ *Сначала выберите модель оборудования!*\n\n"
            "Используйте кнопки ниже или команду /start",
            parse_mode='Markdown'
        )
        return
    if len(error_code) < 7 or len(error_code) > 10:
        await bot.reply_to(message, "⚠️ Кода ошибки обычно *7* символов", parse_mode='Markdown')
        return
    model = user_states[user_id]['model']
    async with get_db_session() as session:
        try:
            if model == 'MX8600':
                query = select(MX8600).where(MX8600.error_code == error_code)
            elif model == 'MX8600S':
                query = select(MX8600S).where(MX8600S.error_code == error_code)
            else:
                await bot.reply_to(message, "❌ Неизвестная модель")
                return
            result = await session.execute(query)
            error = result.scalar_one_or_none()  
            if error:
                response = (
                    f"📟 *Модель:* {model}\n\n"
                    f"✅ *Ошибка:* {error.error_code}\n\n"
                    f"📋 *Описание:* {error.description}\n\n"
                    f"🔧 *Решение:* {error.troubleshooting}"
                )
            else:
                response = "❌ Ошибка не найдена"
            await bot.reply_to(message, response, parse_mode='Markdown')
        except Exception as e:
            await bot.reply_to(message, f"Ошибка базы данных: {str(e)}")

async def main():
    try:
        if await test_async_connection():
            await bot.polling()
            return
    except Exception as e:
        print(f"Ошибка бота: {e}")
    finally:
        print("🛑 Бот остановлен")

if __name__ == '__main__':
    asyncio.run(main())

