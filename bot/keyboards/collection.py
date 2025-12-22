from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants import Callbacks
from bot.keyboards.main import return_inline_keyboard
from bot.keyboards.paginated_inline_keyboard import build_paginated_inline_keyboard
from bot.messages import ButtonTexts


def create_collection_inline_keyboard(category_id: int) -> list[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            text=ButtonTexts.CREATE_COLLECTION,
            callback_data=f"{Callbacks.COLLECTIONS}:{category_id}:create",
        )
    ]


def collections_inline_keyboard(
    data: list[tuple[int, str]],
    category_id: int,
    current_page: int,
    total_pages: int,
    return_to_menu: str,
) -> InlineKeyboardMarkup:
    current_menu = f"{Callbacks.COLLECTIONS}:{category_id}"
    paginated_keyboard = build_paginated_inline_keyboard(
        data, current_menu, current_page, total_pages
    )
    paginated_keyboard.insert(0, create_collection_inline_keyboard(category_id))
    paginated_keyboard.append(return_inline_keyboard(target_menu=return_to_menu))

    return InlineKeyboardMarkup(paginated_keyboard)
