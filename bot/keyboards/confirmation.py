from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.messages import ButtonTexts


def confirmation_inline_keyboard(
    confirm_callback: str,
    cancel_callback: str,
    confirm_text: str = ButtonTexts.CONFIRM,
    cancel_text: str = ButtonTexts.CANCEL,
) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(confirm_text, callback_data=confirm_callback),
            InlineKeyboardButton(cancel_text, callback_data=cancel_callback),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)
