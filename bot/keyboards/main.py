from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_inline_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("My Categories", callback_data="main:my_categories")],
        [
            InlineKeyboardButton(
                "Public Categories", callback_data="main:public_categories"
            )
        ],
        [InlineKeyboardButton("About Me", callback_data="main:about_me")],
        [InlineKeyboardButton("Our Channel", url="https://google.com")],
    ]

    return InlineKeyboardMarkup(keyboard)


def back_inline_keyboard(target_menu: str) -> list[InlineKeyboardButton]:
    return [InlineKeyboardButton(text="🔙 Back", callback_data=target_menu)]
