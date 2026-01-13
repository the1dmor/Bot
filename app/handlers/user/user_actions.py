from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "👋 Assalomu alaykum!\n\n"
        "🎬 Anime botga xush kelibsiz!\n"
        "🔍 Anime qidirish uchun nomini yozing."
    )