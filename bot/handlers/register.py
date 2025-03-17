import loguru
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InputFile, FSInputFile
from asgiref.sync import sync_to_async

from bot.handlers.state import RegisterState
from bot.keyboards.inline import get_inline_menu_keyboard
from bot.keyboards.reply import get_reply_contact_keyboard, reply_keyboard_remove, reply_cancel_keyboard, \
    reply_menu_keyboard
from web.apps.bot_settings.models import BotMessages
from web.apps.telegram_users.models import TelegramUser

router = Router()

@router.message(
    F.text.lower() == 'отмена ❌'
)
async def cancel_handler(
        message: types.Message,
        state: FSMContext,
):
    await message.answer(
        'Действие отменено',
        reply_markup=reply_keyboard_remove,
    )
    await state.clear()



@router.message(StateFilter(RegisterState.phone_number), F.contact)
async def process_phone_number(
        message: types.Message,
        state: FSMContext
):
    await state.update_data(phone_number=message.contact.phone_number)

    await message.answer(
        'Из какого вы города?',
        reply_markup=reply_cancel_keyboard,
    )

    await state.set_state(RegisterState.city)


@router.message(StateFilter(RegisterState.city), F.text)
async def process_phone_number(
        message: types.Message,
        state: FSMContext
):
    state_data = await state.update_data(city=message.text)

    await TelegramUser.objects.acreate(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
        **state_data
    )

    await message.answer(
        'Регистрация успешно завершена!',
        reply_markup=reply_menu_keyboard,
    )
    await state.clear()