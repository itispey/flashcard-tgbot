from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def confirmation_inline_keyboard(
    confirm_callback: str,
    cancel_callback: str,
    confirm_text: str = "Confirm",
    cancel_text: str = "Cancel",
) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(confirm_text, callback_data=confirm_callback),
            InlineKeyboardButton(cancel_text, callback_data=cancel_callback),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)
