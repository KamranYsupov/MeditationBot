import os

import django
from django.conf import settings
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.core.settings')

django.setup()


session = AiohttpSession(api=TelegramAPIServer.from_base(settings.TELEGRAM_SERVER_URL))
bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode='HTML'),
    session=session,
)

dp = Dispatcher()