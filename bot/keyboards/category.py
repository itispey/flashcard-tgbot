from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.constants import Callbacks
from bot.keyboards.main import return_inline_keyboard
from bot.keyboards.paginated_inline_keyboard import build_paginated_inline_keyboard
from bot.messages import ButtonTexts
from bot.utils.helpers.handlers import get_page_number


def create_category_inline_keyboard() -> list[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            text=ButtonTexts.CREATE_CATEGORY,
            callback_data=f"{Callbacks.MY_CATEGORIES}:create",
        )
    ]


def my_categories_inline_keyboard(
    data: list[tuple[int, str]],
    current_menu: str,
    next_menu: str,
    current_page: int,
    total_pages: int,
    return_to_menu: str,
) -> InlineKeyboardMarkup:
    paginated_keyboard = build_paginated_inline_keyboard(
        data, current_menu, next_menu, current_page, total_pages
    )
    paginated_keyboard.insert(0, create_category_inline_keyboard())
    paginated_keyboard.append(return_inline_keyboard(target_menu=return_to_menu))

    return InlineKeyboardMarkup(paginated_keyboard)


def edit_category_inline_keyboard(
    context: ContextTypes.DEFAULT_TYPE, category_id: int, is_public: bool
) -> InlineKeyboardMarkup:
    last_page_number = get_page_number(context=context)
    visibility = (
        ButtonTexts.VISIBILITY_PUBLIC if is_public else ButtonTexts.VISIBILITY_PRIVATE
    )
    keyboard = [
        [
            InlineKeyboardButton(
                text=ButtonTexts.VISIBILITY_LABEL.format(visibility=visibility),
                callback_data=f"{Callbacks.MY_CATEGORIES}:settings:{category_id}:change_visibility",
            )
        ],
        [
            InlineKeyboardButton(
                text=ButtonTexts.DELETE_CATEGORY,
                callback_data=f"{Callbacks.MY_CATEGORIES}:settings:{category_id}:delete",
            )
        ],
    ]
    keyboard.append(
        return_inline_keyboard(
            target_menu=f"{Callbacks.MY_CATEGORIES}:page:{last_page_number}",
        )
    )

    return InlineKeyboardMarkup(keyboard)
