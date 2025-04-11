from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.keyboards.main import back_inline_keyboard


def build_paginated_inline_keyboard(
    data: list[tuple[int, str]], current_menu: str, current_page: int, total_pages: int
) -> list[InlineKeyboardButton]:
    keyboard = []
    for item in data:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=item[1], callback_data=f"{current_menu}:select:{item[0]}"
                ),
                InlineKeyboardButton(
                    text="⚙️", callback_data=f"{current_menu}:settings:{item[0]}"
                ),
            ]
        )

    if total_pages > 1:
        if current_page > 1:
            keyboard.append(
                InlineKeyboardButton(text="<<", callback_data=f"{current_menu}:page:1")
            )
        if current_page > 2:
            keyboard.append(
                InlineKeyboardButton(
                    text="<", callback_data=f"{current_menu}:page:{current_page - 1}"
                )
            )

        keyboard.append(
            InlineKeyboardButton(
                text=f"{current_page}/{total_pages}",
                callback_data=f"{current_menu}:show_page_number",
            )
        )

        if current_page < total_pages:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        text=">",
                        callback_data=f"{current_menu}:page:{current_page + 1}",
                    ),
                    InlineKeyboardButton(
                        text=">>", callback_data=f"{current_menu}:page:{total_pages}"
                    ),
                ]
            )

    return keyboard


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
    target_menu: str,
) -> InlineKeyboardMarkup:
    paginated_keyboard = build_paginated_inline_keyboard(
        data, current_menu, current_page, total_pages
    )
    paginated_keyboard.insert(0, create_category_inline_keyboard())
    paginated_keyboard.append(back_inline_keyboard(target_menu=target_menu))

    return InlineKeyboardMarkup(paginated_keyboard)
