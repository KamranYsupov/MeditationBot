from typing import Union, List

import loguru
from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import BufferedInputFile, FSInputFile
from asgiref.sync import sync_to_async
from django.conf import settings

from bot.handlers.state import ReviewState
from bot.keyboards.inline import get_inline_keyboard, get_inline_menu_keyboard
from bot.keyboards.reply import reply_cancel_keyboard, reply_menu_keyboard
from bot.utils.message import get_bot_method_by_file_extension
from bot.utils.pagination import Paginator, get_pagination_buttons
from web.apps.bot_settings.models import BotMessages, BotReview
from web.apps.meditations.models import Meditation, Review
from web.apps.telegram_users.models import TelegramUser
from web.apps.information.models import Topic, Question

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
    topics_type = callback.data.split('_')[-2]

    per_page = 3

    topics = await Topic.objects.afilter(type=topics_type.capitalize())
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
                callback_data=f'topics_{topics_type}_{paginator.page_number - 1}'
            )
        )

    if paginator.has_next():
        pagination_buttons.append(
            InlineKeyboardButton(
                text='След. ▶️',
                callback_data=f'topics_{topics_type}_{paginator.page_number + 1}'
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
async def meditation_handler(
        callback: types.CallbackQuery,
):
    meditation_id = callback.data.split('_')[-1]

    meditation: Meditation = await Meditation.objects.aget(id=meditation_id)
    if not meditation:
        return

    buttons = {}
    buttons['Оставить отзыв / вопрос 📝'] = f'review_meditation_{meditation.id}'
    buttons['Назад'] = 'menu'


    async def send_input_meditation_file():
        meditation_file = FSInputFile(
            meditation.file.path,
            chunk_size=settings.BOT_FILE_CHUNK_SIZE
        )

        await callback.message.edit_text('Отправляю медитацию . . .')
        video_message = await callback.message.answer_video(
            video=meditation_file,
            caption=meditation.text,
            reply_markup=get_inline_keyboard(
                buttons=buttons
            ),
            width=16,
            height=9,
        )
        meditation.file_id = video_message.video.file_id
        await meditation.asave()

    if not meditation.file_id:
        await send_input_meditation_file()
        return

    try:
        await callback.message.answer_video(
            video=meditation.file_id,
            caption=meditation.text,
            reply_markup=get_inline_keyboard(
                buttons=buttons
            ),
            width=16,
            height=9,
        )
    except TelegramBadRequest:
        await send_input_meditation_file()


@router.callback_query(F.data.startswith('review_meditation_'))
async def review_meditation_handler(
        callback: types.CallbackQuery,
        state: FSMContext,
):
    meditation_id = callback.data.split('_')[-1]

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        'Отправьте свой отзыв или вопрос.',
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

@router.callback_query(F.data.startswith('faq_'))
async def faq_handler(
        callback: types.CallbackQuery,
):
    page_number = int(callback.data.split('_')[-1])
    per_page = 5

    questions = await Question.objects.a_all()
    paginator = Paginator(
        array=questions,
        page_number=page_number,
        per_page=per_page
    )

    buttons = {
        question.title: f'question_{question.id}'
        for question in paginator.get_page()
    }
    pagination_buttons = get_pagination_buttons(
        paginator, prefix='faq_'
    )
    sizes = (1,) * per_page
    if not pagination_buttons:
        pass
    elif len(pagination_buttons.items()) == 1:
        sizes += (1, 1)
    else:
        sizes += (2, 1)

    buttons.update(pagination_buttons)
    buttons['Назад'] = 'menu'

    await callback.message.edit_text(
        'Выберите интересующий вопрос',
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=sizes
        )
    )


@router.callback_query(F.data.startswith('question_'))
async def question_handler(
        callback: types.CallbackQuery,
):
    question_id = callback.data.split('_')[-1]

    question: Question = await Question.objects.aget(id=question_id)
    if not question:
        return

    reply_markup = get_inline_keyboard(
        buttons={'Назад': 'menu'}
    )

    await callback.message.delete()

    is_any_file_sent = False

    for question_file in (question.photo, question.video):
        if not question_file:
            continue

        bot_send_method = get_bot_method_by_file_extension(
            file_name=question_file.name,
            bot=callback.bot
        )

        input_file = FSInputFile(
            question_file.path,
            chunk_size=settings.BOT_FILE_CHUNK_SIZE
        )
        send_method_args = (
            callback.from_user.id,
            input_file,
        )
        send_method_kwargs = dict(
            width=settings.DEFAULT_BOT_VIDEO_WIDTH,
            height=settings.DEFAULT_BOT_VIDEO_HEIGHT,
        ) if bot_send_method == callback.bot.send_video else {}

        if (is_any_file_sent or not question.video) and not question.text:
            await bot_send_method(
                *send_method_args,
                reply_markup=reply_markup,
                **send_method_kwargs
            )
        else:
            await bot_send_method(*send_method_args, **send_method_kwargs)

        is_any_file_sent = True

    if question.text:
        await callback.message.answer(
            text=question.text,
            reply_markup=reply_markup,
        )


@router.callback_query(F.data.startswith('reviews_'))
async def reviews_callback_handler(
        callback: types.CallbackQuery,
):
    page_number = int(callback.data.split('_')[-1])
    reviews: List[BotReview] = await BotReview.objects.a_all()

    paginator = Paginator(
        page_number=page_number,
        per_page=5,
        array=reviews
    )
    page = paginator.get_page()
    for review in page:

        bot_send_method = get_bot_method_by_file_extension(
            file_name=review.file.name,
            bot=callback.bot
        )
        send_method_kwargs = dict(
            width=settings.DEFAULT_BOT_VIDEO_WIDTH,
            height=settings.DEFAULT_BOT_VIDEO_HEIGHT,
        ) if bot_send_method == callback.bot.send_video else {}

        input_file = FSInputFile(
            review.file.path,
            chunk_size=settings.BOT_FILE_CHUNK_SIZE
        )

        if review != page[-1]:
            reply_markup = None
        else:
            buttons = {}
            if paginator.has_next():
                buttons['Далее'] = f'reviews_{page_number + 1}'

            buttons['Назад'] = 'menu'


            reply_markup = get_inline_keyboard(buttons=buttons)

        await bot_send_method(
            callback.from_user.id,
            input_file,
            reply_markup=reply_markup,
            **send_method_kwargs,
        )


@router.callback_query(F.data == 'about_teacher')
@router.callback_query(F.data == 'useful_posts')
@router.callback_query(F.data == 'society')
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
        society_video = FSInputFile(
            bot_messages.society_video.path,
            chunk_size=settings.BOT_FILE_CHUNK_SIZE
        )
        await callback.message.answer_video(
            video=society_video,
            reply_markup=reply_markup,
            width=settings.DEFAULT_BOT_VIDEO_WIDTH,
            height=settings.DEFAULT_BOT_VIDEO_HEIGHT,
        )

        return

    text = getattr(bot_messages, f'{option}_text')

    if option == 'about_teacher':
        about_teacher_video = FSInputFile(
            bot_messages.about_teacher_video.path,
            chunk_size=settings.BOT_FILE_CHUNK_SIZE
        )
        await callback.message.answer_video(
            video=about_teacher_video,
            reply_markup=reply_markup,
            width=settings.DEFAULT_BOT_VIDEO_WIDTH,
            height=settings.DEFAULT_BOT_VIDEO_HEIGHT,
        )
        return


    await callback.message.answer(text, reply_markup=reply_markup)



