import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ChatMemberStatus

TOKEN = os.getenv("TOKEN") or "8928794960:AAHSxYSUiqRoGqw0OklMXcVumCMBTyuM55Y"
CHANNEL = "@DevYud0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    text = (
        "👋 Привет!\n\n"
        "Чтобы получить файлы — подпишись на канал и нажми «Подтвердить✅»"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подписаться", url="https://t.me/DevYud0")],
        [InlineKeyboardButton(text="Подтвердить✅", callback_data="check_sub")]
    ])
    
    await message.answer(text, reply_markup=keyboard)

@dp.callback_query(F.data == "check_sub")
async def check_subscription(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL, user_id=user_id)
        
        if member.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR
        ]:
            await callback.message.answer(
                "✅ Готово!\n\n"
                "Зайдите в тгк https://t.me/LiminarGhost\n"
                "и скачайте последний файл!"
            )
            await callback.answer()
        else:
            await callback.answer(
                "❌ Ты ещё не подписан на канал!\nСначала нажми «Подписаться»",
                show_alert=True
            )
            
    except Exception as e:
        await callback.answer(
            "⚠️ Ошибка проверки.\nУбедись, что бот является администратором канала @DevYud0",
            show_alert=True
        )
        print(f"Ошибка: {e}")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
