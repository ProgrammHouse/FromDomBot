from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.utils import executor

API_TOKEN = "7809731825:AAHZG_deIAVIVfbvHZ_LeS8yYb7SiorUDxI"  # ⬅️ вставь сюда свой токен бота

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# 🔹 Товары (можешь менять, добавлять свои)
items = {
    
    "bottle": {
        "title": "💧 Бутылка Gatorade",
        "photo": "https://shopgatorade.com.au/cdn/shop/files/Gatorade_ECOM6953.png",
        "desc": "Спортивная бутылка Gatorade, почти новая",
        "price": "1500₽",
        "buy_link": "https://t.me/dmrxw73"
    }
}

# 📦 Меню с товарами
async def show_menu(message_or_callback):
    kb = InlineKeyboardMarkup(row_width=1)
    for key, item in items.items():
        kb.add(InlineKeyboardButton(text=item["title"], callback_data=f"item_{key}"))
    text = "👋 Привет! Добро пожаловать в <b>FromDomBot</b>!\n\nВыбери товар, чтобы посмотреть подробности 👇"

    if isinstance(message_or_callback, types.Message):
        await message_or_callback.answer(text, reply_markup=kb, parse_mode="HTML")
    else:
        await message_or_callback.message.edit_caption(text, reply_markup=kb, parse_mode="HTML")
        await message_or_callback.answer()

# 🔘 Команда /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await show_menu(message)

# 🔍 Показываем товар
@dp.callback_query_handler(lambda c: c.data.startswith("item_"))
async def show_item(callback: types.CallbackQuery):
    key = callback.data.split("_")[1]
    item = items.get(key)

    if not item:
        await callback.message.answer("❌ Ошибка: товар не найден.")
        return

    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("💬 Написать продавцу", url=item["buy_link"]),
        InlineKeyboardButton("⬅️ Назад в каталог", callback_data="back_to_menu")
    )

    caption = f"<b>{item['title']}</b>\n\n{item['desc']}\n\n💰 Цена: <b>{item['price']}</b>"

    await callback.message.edit_media(
        InputMediaPhoto(media=item["photo"], caption=caption, parse_mode="HTML"),
        reply_markup=kb
    )
    await callback.answer()

# 🔙 Назад в меню
@dp.callback_query_handler(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    await show_menu(callback)

# 🚀 Запуск
if __name__ == '__main__':
    
    executor.start_polling(dp, skip_updates=True)
