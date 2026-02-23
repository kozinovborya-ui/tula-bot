import logging
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.session.aiohttp import AiohttpSession

# --- ТВОЯ ОБНОВЛЕННАЯ КОНФИГУРАЦИЯ ---
API_TOKEN = '7902415919:AAEK_BuX8CGDdhm_ubF7MlX_CFuJwibNGjU'
SUPABASE_URL = 'https://idjcpkvfivjshdxsfypp.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlkamNwa3ZmaXZqc2hkeHNmeXBwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE3MTg1NTgsImV4cCI6MjA4NzI5NDU1OH0.ZCWdHVTxcepKQE0T1eQ2tshdL4ssL_IWOdbZ_TNOa-I' 
ADMIN_USERNAME = 'somessubstance_a_d_m_i_n'

# Настройка прокси для PythonAnywhere
proxy_url = "http://proxy.server:3128"
session = AiohttpSession(proxy=proxy_url)

bot = Bot(token=API_TOKEN, session=session)
dp = Dispatcher()

def get_products():
    headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
    try:
        url = f"{SUPABASE_URL}/rest/v1/products?select=*"
        response = requests.get(url, headers=headers)
        return response.json() if response.status_code == 200 else []
    except Exception as e:
        print(f"Ошибка базы данных: {e}")
        return []

@dp.message(Command("start"))
async def start(message: types.Message):
    products = get_products()
    if not products:
        await message.answer("В магазине пока нет товаров.")
        return

    for item in products:
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(text="🛍 Купить", url=f"https://t.me/{ADMIN_USERNAME}"))
        
        caption = f"<b>{item.get('name', 'Товар')}</b>\n\n{item.get('description', '')}\n\nЦена: {item.get('price', '—')}"
        img = item.get('image_url')
        
        if img:
            await message.answer_photo(photo=img, caption=caption, parse_mode="HTML", reply_markup=builder.as_markup())
        else:
            await message.answer(text=caption, parse_mode="HTML", reply_markup=builder.as_markup())

async def main():
    # Удаляем вебхук Manybot перед запуском, чтобы не было конфликта
    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот успешно запущен с НОВЫМ токеном!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
