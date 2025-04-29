from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.keyboards.main import return_inline_keyboard
from bot.keyboards.paginated_inline_keyboard import build_paginated_inline_keyboard


def create_category_inline_keyboard() -> list[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            text="+ Create a category", callback_data="category:create"
        )
    ]


def my_categories_inline_keyboard(
    data: list[tuple[int, str]],
    current_menu: str,
    current_page: int,
    total_pages: int,
    return_to_menu: str,
) -> InlineKeyboardMarkup:
    paginated_keyboard = build_paginated_inline_keyboard(
        data, current_menu, current_page, total_pages
    )
    paginated_keyboard.insert(0, create_category_inline_keyboard())
    paginated_keyboard.append(return_inline_keyboard(target_menu=return_to_menu))

    return InlineKeyboardMarkup(paginated_keyboard)
