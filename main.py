from aiogram import Bot, Dispatcher
import logging
import asyncio

from app.handlers.admin.admin_actions import admin_router
from app.handlers.admin.add_media import add_media_router
from app.handlers.admin.add_episode import add_episode_router
from app.handlers.admin.edit_media import edit_media_router
from app.handlers.admin.edit_episode import edit_episode_router
from app.handlers.admin.send_message import send_message_router
from app.handlers.admin.sponsor import sponsor_router
from app.handlers.admin.staff import staff_router
from app.handlers.admin.post_media import post_media_router
from app.handlers.admin.post_episode import post_media_episode_router

from app.handlers.user.user_actions import router
from app.handlers.user.search_anime import user_search_router
from app.handlers.user.media import user_media_router
from app.handlers.user.search_by_image import user_search_by_image_router

# ✅ TO‘G‘RI IMPORT
from config import TOKEN, trailers_base_chat, series_base_chat, bot_username


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(router)
    dp.include_router(admin_router)
    dp.include_router(add_episode_router)
    dp.include_router(add_media_router)
    dp.include_router(edit_media_router)
    dp.include_router(edit_episode_router)
    dp.include_router(send_message_router)
    dp.include_router(post_media_router)
    dp.include_router(post_media_episode_router)
    dp.include_router(sponsor_router)
    dp.include_router(staff_router)
    dp.include_router(user_search_router)
    dp.include_router(user_media_router)
    dp.include_router(user_search_by_image_router)

    logging.info("Bot ishga tushmoqda...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Bot xatosi: {e}")
        print("Bot to'xtatildi")