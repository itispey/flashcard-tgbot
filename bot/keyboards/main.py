from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.utils.helpers.context import CustomContext


def main_inline_keyboard(context: CustomContext) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                context._("Categories"), callback_data="main:my_categories"
            )
        ],
        [
            InlineKeyboardButton(
                context._("Public Categories"), callback_data="main:public_categories"
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


def return_inline_keyboard(
    context: CustomContext, target_menu: str
) -> list[InlineKeyboardButton]:
    return [InlineKeyboardButton(text=context._("🔙 Back"), callback_data=target_menu)]
