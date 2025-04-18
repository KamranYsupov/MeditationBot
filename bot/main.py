﻿import asyncio
import os

import django
from django.conf import settings
import loguru
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from bot.loader import bot, dp


async def main():
    """Запуск бота"""

    from middlewares.throttling import rate_limit_middleware
    from handlers.routing import get_main_router

    
    try:
        dp.message.middleware(rate_limit_middleware)
        dp.include_router(get_main_router())
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    loguru.logger.info('Bot is starting')
    asyncio.run(main())
