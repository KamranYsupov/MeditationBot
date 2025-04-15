import loguru
from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InputFile, FSInputFile
from asgiref.sync import sync_to_async
from django.conf import settings

from bot.handlers.state import RegisterState
from bot.keyboards.inline import get_inline_menu_keyboard
from bot.keyboards.reply import get_reply_contact_keyboard, reply_menu_keyboard
from web.apps.bot_settings.models import BotMessages
from web.apps.telegram_users.models import TelegramUser

router = Router()


@router.message(CommandStart())
async def start_command_handler(
    message: types.Message,
    state: FSMContext
):
    text = f'Привет, {message.from_user.first_name}. '
    telegram_user = await TelegramUser.objects.aget(telegram_id=message.from_user.id)
    if telegram_user:
        await message.answer(text, reply_markup=reply_menu_keyboard)
        return

    button_text = 'Отправить номер телефона 📲'

    bot_messages: BotMessages = await sync_to_async(BotMessages.load)()
    welcome_video = FSInputFile(
        bot_messages.welcome_video.path,
        chunk_size=settings.BOT_FILE_CHUNK_SIZE
    )
    await message.answer_video(
        video=welcome_video,
        caption=bot_messages.welcome_text,
        reply_markup=get_reply_contact_keyboard(button_text),
        width=settings.DEFAULT_BOT_VIDEO_WIDTH,
        height=settings.DEFAULT_BOT_VIDEO_HEIGHT,
        supports_streaming=True,
    )


    await state.set_state(RegisterState.phone_number)
    
    
    

    
    

