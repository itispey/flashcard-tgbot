from telegram import InlineKeyboardButton

from bot.messages import ButtonTexts


def build_paginated_inline_keyboard(
    data: list[tuple[int, str]], current_menu: str, current_page: int, total_pages: int
) -> list[InlineKeyboardButton]:
    """
    Builds a paginated inline keyboard for a Telegram bot.

    Args:
        data (list[tuple[int, str]]): A list of tuples where each tuple contains an
            integer ID and a string label for the button.
        current_menu (str): The identifier for the current menu, used in callback data.
        current_page (int): The current page number being displayed.
        total_pages (int): The total number of pages available.

    Returns:
        list[InlineKeyboardButton]: A list of InlineKeyboardButton objects representing
            the inline keyboard layout, including pagination controls if applicable.

    The keyboard includes:
        - Buttons for each item in the `data` list, with a "select" and "settings" option.
        - Pagination controls (<<, <, current page indicator, >, >>) if there are
          multiple pages.
    """
    keyboard = [
        [
            InlineKeyboardButton(
                text=item[1], callback_data=f"{current_menu}:select:{item[0]}"
            ),
            InlineKeyboardButton(
                text=ButtonTexts.SETTINGS,
                callback_data=f"{current_menu}:settings:{item[0]}",
            ),
        ]
        for item in data
    ]

    if total_pages > 1:
        pagination_row = []

        if current_page > 1:
            pagination_row.extend(
                [
                    InlineKeyboardButton(
                        text=ButtonTexts.FIRST_PAGE,
                        callback_data=f"{current_menu}:page:1",
                    ),
                    InlineKeyboardButton(
                        text=ButtonTexts.PREVIOUS_PAGE,
                        callback_data=f"{current_menu}:page:{current_page - 1}",
                    ),
                ]
            )

        pagination_row.append(
            InlineKeyboardButton(
                text=f"{current_page}/{total_pages}",
                callback_data=f"{current_menu}:show_page_number",
            )
        )

        if current_page < total_pages:
            pagination_row.extend(
                [
                    InlineKeyboardButton(
                        text=ButtonTexts.NEXT_PAGE,
                        callback_data=f"{current_menu}:page:{current_page + 1}",
                    ),
                    InlineKeyboardButton(
                        text=ButtonTexts.LAST_PAGE,
                        callback_data=f"{current_menu}:page:{total_pages}",
                    ),
                ]
            )

        keyboard.append(pagination_row)

    return keyboard
