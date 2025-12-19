from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext._handlers.callbackqueryhandler import CallbackQueryHandler

from bot.handlers.categories.types import CategoryType
from bot.keyboards.category import my_categories_inline_keyboard
from bot.messages import Messages
from bot.queries.category import get_categories
from bot.utils.helpers.db import SessionLocal

MY_CATEGORIES = "main:categories:my"


async def my_categories_menu_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    blocks = query.data.split(":")
    page_number = int(blocks[4]) if len(blocks) == 5 else 1

    with SessionLocal() as session:
        categories, total_pages = get_categories(
            db=session,
            category_type=CategoryType.MY_CATEGORIES,
            user_tg_id=update.effective_user.id,
            page_number=page_number,
        )

        text = Messages.CATEGORY_LIST_HEADER if categories else Messages.CATEGORY_EMPTY

        categories_data = [(cat.id, cat.name) for cat in categories]
        reply_markup = my_categories_inline_keyboard(
            data=categories_data,
            current_menu=MY_CATEGORIES,
            current_page=page_number,
            total_pages=total_pages,
            return_to_menu="main",
        )

        await query.answer()
        await query.edit_message_text(text, reply_markup=reply_markup)


MY_CATEGORIES_HANDLERS = [
    CallbackQueryHandler(my_categories_menu_callback, pattern=MY_CATEGORIES)
]
