from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def main_inline_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("Categories", callback_data="main:my_categories")],
        [
            InlineKeyboardButton(
                "Public Categories", callback_data="main:public_categories"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def select_language_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("English 🇬🇧", callback_data="set_lang:en")],
        [InlineKeyboardButton("فارسی 🇮🇷", callback_data="set_lang:fa")],
    ]

    return InlineKeyboardMarkup(keyboard)


def return_inline_keyboard(target_menu: str) -> list[InlineKeyboardButton]:
    return [InlineKeyboardButton(text="🔙 Back", callback_data=target_menu)]
