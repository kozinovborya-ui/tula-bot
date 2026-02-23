import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from supabase import create_client

# --- КОНФИГУРАЦИЯ ---
API_TOKEN = '7902415919:AAFTkxU33Kc0dD6nJSPopUkteUuPrdZqfkA'
SUPABASE_URL = 'https://idjcpkvfivjshdxsfypp.supabase.co'
# ВНИМАНИЕ: Вставь ниже свой anon key из Supabase (Settings -> API)
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlkamNwa3ZmaXZqc2hkeHNmeXBwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE3MTg1NTgsImV4cCI6MjA4NzI5NDU1OH0.ZCWdHVTxcepKQE0T1eQ2tshdL4ssL_IWOdbZ_TNOa-I' 
ADMIN_USERNAME = '@somessubstance_a_d_m_i_n'

# Настройка логирования, чтобы видеть ошибки в консоли
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    try:
        # Запрос данных из таблицы Products
        res = supabase.table('Products').select("*").execute()
        products = res.data

        if not products:
            await message.answer("📦 В магазине пока нет товаров.")
            return

        for item in products:
            # Создаем кнопку связи с админом
            builder = InlineKeyboardBuilder()
            builder.row(types.InlineKeyboardButton(
                text="🛍️ Купить / Уточнить", 
                url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}")
            )
            
            # Текст карточки товара
            # Используем .get() для защиты от пустых полей
            name = item.get('name', 'Без названия')
            desc = item.get('descriptio', 'Описание скоро появится...')
            price = item.get('price', 'По запросу')
            image = item.get('image_url')

            caption = f"<b>{name}</b>\n\n{desc}\n\n💰 Цена: {price} руб."
            
            if image:
                await message.answer_photo(
                    photo=image, 
                    caption=caption, 
                    parse_mode="HTML", 
                    reply_markup=builder.as_markup()
                )
            else:
                await message.answer(text=caption, parse_mode="HTML", reply_markup=builder.as_markup())
    
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.answer("⚠️ Произошла ошибка при загрузке товаров.")

async def main():
    print("🚀 Бот запущен! Напиши /start в Telegram.")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")
