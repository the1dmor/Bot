from aiogram.filters import Command
from aiogram.types import Message
from config import ADMIN_ID

@admin_router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Siz admin emassiz")
        return

    await message.answer(" Admin panelga xush kelibsiz")