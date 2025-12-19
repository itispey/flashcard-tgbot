from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.messages import ButtonTexts


def main_inline_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                ButtonTexts.MAKE_FLASHCARD, callback_data="main:categories:my"
            )
        ],
        [
            InlineKeyboardButton(
                ButtonTexts.BOOKMARKS, callback_data="main:categories:bookmarks"
            )
        ],
        [
            InlineKeyboardButton(
                ButtonTexts.POPULAR_FLASHCARDS, callback_data="main:categories:public"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def return_inline_keyboard(target_menu: str) -> list[InlineKeyboardButton]:
    return [InlineKeyboardButton(text=ButtonTexts.BACK, callback_data=target_menu)]
