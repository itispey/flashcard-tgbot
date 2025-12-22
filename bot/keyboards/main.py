from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.constants import Callbacks
from bot.messages import ButtonTexts


def main_inline_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                ButtonTexts.MAKE_FLASHCARD, callback_data=Callbacks.MY_CATEGORIES
            )
        ],
        [
            InlineKeyboardButton(
                ButtonTexts.BOOKMARKS, callback_data=Callbacks.BOOKMARKS
            )
        ],
        [
            InlineKeyboardButton(
                ButtonTexts.POPULAR_FLASHCARDS,
                callback_data=Callbacks.PUBLIC_CATEGORIES,
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def return_inline_keyboard(target_menu: str) -> list[InlineKeyboardButton]:
    return [InlineKeyboardButton(text=ButtonTexts.BACK, callback_data=target_menu)]
