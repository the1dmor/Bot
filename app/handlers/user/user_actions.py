from aiogram.types import Message

@router.message()
async def search_anime(message: Message):
    query = message.text.strip()

    if len(query) < 2:
        await message.answer("🔍 Anime nomini yozing")
        return

    await message.answer(
        f"🔎 Qidirilmoqda: <b>{query}</b>\n\n"
        "⚠️ Hozircha demo javob.\n"
        "Keyingi bosqichda real API ulanadi.",
        parse_mode="HTML"
    )