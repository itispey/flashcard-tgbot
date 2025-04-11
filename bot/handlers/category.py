from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from bot.keyboards.category import my_categories_inline_keyboard
from bot.models.category import Category
from bot.utils.db import SessionLocal


async def my_categories_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    blocks = query.data.split(":")
    page_number = blocks[2] if len(blocks) == 3 else 1

    with SessionLocal() as session:
        categories, total_pages = Category.paginate(
            db=session, current_page=page_number, per_page=5
        )

        text = "Categories"
        reply_markup = my_categories_inline_keyboard(
            data=[(cat.id, cat.name) for cat in categories],
            current_menu="main:my_categories",
            current_page=page_number,
            total_pages=total_pages,
            target_menu="main",
        )

        await query.answer()
        await query.edit_message_text(text=text, reply_markup=reply_markup)


CATEGORY_HANDLER = [
    CallbackQueryHandler(my_categories_callback, pattern="^main:my_categories")
]
