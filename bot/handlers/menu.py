from typing import Union

import loguru
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import InputFile, FSInputFile
from asgiref.sync import sync_to_async
from django.conf import settings

from bot.handlers.state import ReviewState
from bot.keyboards.inline import get_inline_keyboard, get_inline_menu_keyboard
from bot.keyboards.reply import reply_cancel_keyboard, reply_menu_keyboard
from bot.utils.message import get_bot_method_by_file_extension
from bot.utils.pagination import Paginator, get_pagination_buttons
from web.apps.bot_settings.models import BotMessages
from web.apps.meditations.models import Meditation
from web.apps.reviews.models import Review
from web.apps.telegram_users.models import TelegramUser
from web.apps.topics.models import Topic

router = Router()


@router.message(F.text == 'Меню 📁')
@router.callback_query(F.data == 'menu')
async def menu_handler(
        aiogram_type: Union[types.Message, types.CallbackQuery],
):
    if isinstance(aiogram_type, types.CallbackQuery):
        await aiogram_type.message.delete()
        aiogram_type: types.Message = aiogram_type.message

    await aiogram_type.answer(
        'Выберите пункт меню.',
        reply_markup=await get_inline_menu_keyboard()
    )


@router.callback_query(F.data.startswith('meditations_'))
async def meditations_handler(
        callback: types.CallbackQuery,
):
    page_number = int(callback.data.split('_')[-1])
    per_page = 5

    meditations = await Meditation.objects.a_all()
    paginator = Paginator(
        array=meditations,
        page_number=page_number,
        per_page=per_page
    )

    buttons = {
        meditation.name: f'meditation_{meditation.id}'
        for meditation in paginator.get_page()
    }
    pagination_buttons = get_pagination_buttons(
        paginator, prefix='meditations_'
    )
    sizes = (1,) * per_page
    if not pagination_buttons:
        pass
    elif len(pagination_buttons.items()) == 1:
        sizes += (1, 1)
    else:
        sizes += (2, 1)

    buttons['Вводная информация'] = f'enter_info_{page_number}'
    buttons.update(pagination_buttons)
    buttons['Назад'] = 'menu'

    await callback.message.edit_text(
        'Выберите медитацию',
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=sizes
        )
    )


@router.callback_query(F.data.startswith('enter_info_'))
async def enter_info_handler(
        callback: types.CallbackQuery,
):
    previous_page_number = int(callback.data.split('_')[-1])
    bot_messages: BotMessages = await sync_to_async(BotMessages.load)()

    await callback.message.edit_text(
        text=bot_messages.enter_info_text,
        reply_markup=get_inline_keyboard(
            buttons={'Назад': f'meditations_{previous_page_number}'}
        )
    )


@router.callback_query(F.data.startswith('topics_'))
async def topics_handler(
        callback: types.CallbackQuery,
):
    page_number = int(callback.data.split('_')[-1])
    per_page = 3

    topics = await Topic.objects.a_all()
    paginator = Paginator(
        array=topics,
        page_number=page_number,
        per_page=per_page
    )

    keyboard = InlineKeyboardBuilder()

    for topic in paginator.get_page():
        keyboard.add(
            InlineKeyboardButton(
                text=topic.name,
                url=topic.link
            )
        )
    pagination_buttons = []
    if paginator.has_previous():
        pagination_buttons.append(
            InlineKeyboardButton(
                text='◀️ Пред.',
                callback_data=f'topics_{paginator.page_number - 1}'
            )
        )

    if paginator.has_next():
        pagination_buttons.append(
            InlineKeyboardButton(
                text='След. ▶️',
                callback_data=f'topics_{paginator.page_number + 1}'
            )
        )

    sizes = (1,) * per_page
    if not pagination_buttons:
        pass
    elif len(pagination_buttons) == 1:
        sizes += (1, 1)
    else:
        sizes += (2, 1)

    keyboard.add(*pagination_buttons)
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='menu'))
    await callback.message.edit_text(
        'Выберите тему',
        reply_markup=keyboard.adjust(*sizes).as_markup()
    )


@router.callback_query(F.data.startswith('meditation_'))
@router.callback_query(F.data.startswith('topic_'))
async def topic_or_meditation_handler(
        callback: types.CallbackQuery,
):
    model = Topic if callback.data.split('_')[0] == 'topic' else Meditation
    obj_id = callback.data.split('_')[-1]

    obj: Union[Topic, Meditation] = await model.objects.aget(id=obj_id)
    if not obj:
        return

    buttons = {}

    if isinstance(obj, Meditation):
        buttons['Оставить отзыв 📝'] = f'review_meditation_{obj.id}'

    bot_send_method = get_bot_method_by_file_extension(
        file_name=obj.file.name,
        bot=callback.bot
    )
    buttons['Назад'] = 'menu'

    obj_file = FSInputFile(obj.file.path)
    await callback.message.delete()
    await bot_send_method(
        callback.from_user.id, # chat_id
        obj_file,
        caption=obj.text,
        reply_markup=get_inline_keyboard(
            buttons=buttons
        )
    )


@router.callback_query(F.data.startswith('review_meditation_'))
async def review_meditation_handler(
        callback: types.CallbackQuery,
        state: FSMContext,
):
    meditation_id = callback.data.split('_')[-1]

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        'Отправьте свой отзыв.',
        reply_markup=reply_cancel_keyboard,
    )
    await state.update_data(meditation_id=meditation_id)
    await state.set_state(ReviewState.text)


@router.message(F.text, StateFilter(ReviewState.text))
async def review_meditation_handler(
        message: types.Message,
        state: FSMContext,
):
    state_data = await state.update_data(text=message.text)

    meditation = await Meditation.objects.aget(id=state_data.get('meditation_id'))
    telegram_user = await TelegramUser.objects.aget(telegram_id=message.from_user.id)

    review = await Review.objects.acreate(
        telegram_user_id=telegram_user.id,
        **state_data
    )

    await message.answer(
        'Спасибо за ваш отзыв!',
        reply_markup=reply_menu_keyboard,
    )
    await message.bot.send_message(
        chat_id=settings.REVIEWS_CHAT_ID,
        text=(
            'Новый отзыв\n\n'
            f'Пользователь: {telegram_user.full_name}\n'
            f'{meditation.name}\n'
            f'Отзыв: {review.text}'
        )
    )


@router.callback_query(F.data == 'about_teacher')
@router.callback_query(F.data == 'useful_posts')
@router.callback_query(F.data == 'society')
@router.callback_query(F.data == 'faq')
@router.callback_query(F.data == 'reviews')
async def menu_options_handler(
        callback: types.CallbackQuery,
):
    bot_messages: BotMessages = await sync_to_async(BotMessages.load)()
    option = callback.data
    reply_markup = get_inline_keyboard(
        buttons={'Назад': 'menu'}
    )

    await callback.message.delete()
    if option == 'society':
        society_video = FSInputFile(bot_messages.society_video.path)
        await callback.message.answer_video(
            video=society_video,
            reply_markup=reply_markup,
        )

        return

    text = getattr(bot_messages, f'{option}_text')

    if option == 'reviews':
        bot_send_method = get_bot_method_by_file_extension(
            file_name=bot_messages.reviews_file.name,
            bot=callback.bot
        )
        reviews_file = FSInputFile(bot_messages.reviews_file.path)
        await bot_send_method(
            callback.from_user.id,  # chat_id
            reviews_file,
            caption=text,
            reply_markup=reply_markup,
        )
        return

    if option == 'about_teacher':
        bot_send_method = get_bot_method_by_file_extension(
            file_name=bot_messages.about_teacher_video.name,
            bot=callback.bot
        )
        about_teacher_video = FSInputFile(bot_messages.about_teacher_video.path)
        await bot_send_method(
            callback.from_user.id,  # chat_id
            about_teacher_video,
            caption=text,
            reply_markup=reply_markup,
        )
        return


    await callback.message.answer(text, reply_markup=reply_markup)



