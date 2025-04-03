from typing import Dict, Tuple

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from asgiref.sync import sync_to_async

from web.apps.bot_settings.models import Links


def get_inline_keyboard(
        *,
        buttons: Dict[str, str],
        sizes: Tuple = (1, 2),
        as_markup: bool = True,
):
    keyboard = InlineKeyboardBuilder()

    for text, data in buttons.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    if not as_markup:
        return keyboard

    return keyboard.adjust(*sizes).as_markup()


async def get_inline_menu_keyboard():
    keyboard = get_inline_keyboard(
        buttons={
            'Пробная медитация': 'meditations_1',
            'Об учителе': 'about_teacher',
            'О технологии': 'topics_tech_1',
            'Полезная информация': 'topics_post_1',
            'Сообщество': 'society',
            'Ответы на вопросы': 'faq_1',
            'Отзывы': 'reviews',
        },
        as_markup=False,
    )
    links: Links = await sync_to_async(Links.load)()
    keyboard.add(
        InlineKeyboardButton(
            text='Задать вопрос',
            url=links.manager_link,
        )
    )

    return keyboard.adjust(*(1,) * 8).as_markup()


inline_cancel_keyboard = get_inline_keyboard(
    buttons={'Отмена ❌': 'cancel'}
)

