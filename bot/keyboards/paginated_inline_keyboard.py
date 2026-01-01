from typing import Literal

from telegram import InlineKeyboardButton

from bot.messages import ButtonTexts


def build_paginated_inline_keyboard(
    data: list[tuple[int, str]],
    current_menu: str,
    next_menu: str,
    current_page: int,
    total_pages: int,
    action_type: Literal["settings", "delete"] = "settings",
) -> list[InlineKeyboardButton]:
    """
    Builds a paginated inline keyboard for a Telegram bot.

    Args:
        data (list[tuple[int, str]]): A list of tuples where each tuple contains an
            integer ID and a string label for the button.
        current_menu (str): The identifier for the current menu, used in callback data.
        current_page (int): The current page number being displayed.
        total_pages (int): The total number of pages available.
        action_type (Literal["settings", "delete"]): The type of action button to display.
            Defaults to "settings".

    Returns:
        list[InlineKeyboardButton]: A list of InlineKeyboardButton objects representing
            the inline keyboard layout, including pagination controls if applicable.

    The keyboard includes:
        - Buttons for each item in the `data` list, with a "select" and "settings"/"delete" option.
        - Pagination controls (<<, <, current page indicator, >, >>) if there are
          multiple pages.
    """
    if action_type == "delete":
        action_text = ButtonTexts.DELETE_EMOJI
        action_callback = "delete"
    else:
        action_text = ButtonTexts.SETTINGS_EMOJI
        action_callback = "settings"

    keyboard = [
        [
            InlineKeyboardButton(
                text=item[1], callback_data=f"{next_menu}:{item[0]}:page:1"
            ),
            InlineKeyboardButton(
                text=action_text,
                callback_data=f"{current_menu}:{action_callback}:{item[0]}",
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
