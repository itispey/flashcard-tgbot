from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext._handlers.callbackqueryhandler import CallbackQueryHandler

from bot.constants import Callbacks
from bot.keyboards.collection import collections_inline_keyboard
from bot.messages import Messages
from bot.models.collection import Collection
from bot.utils.helpers.db import SessionLocal


def collections_menu(category_id: int, page_number: int = 1):
    with SessionLocal() as session:
        collections, total_pages = Collection.paginate(
            db=session,
            current_page=page_number,
            per_page=5,
            filters={"category_id": category_id},
        )

        text = (
            Messages.COLLECTION_LIST_HEADER
            if collections
            else Messages.COLLECTION_EMPTY
        )
        reply_markup = collections_inline_keyboard(
            data=[(col.id, col.name) for col in collections],
            category_id=category_id,
            next_menu=Callbacks.COLLECTIONS,
            current_page=page_number,
            total_pages=total_pages,
            return_to_menu=Callbacks.MY_CATEGORIES,  # FIXME: still not sure about this, since the previous menu could be public categories or bookmarks one
        )

        return text, reply_markup


async def collections_menu_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE, category_id: int
):
    text, reply_markup = collections_menu(category_id=category_id)
    await context.bot.send_message(
        chat_id=update.effective_user.id, text=text, reply_markup=reply_markup
    )


async def collections_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    blocks = query.data.split(":")
    category_id = int(blocks[1])
    page_number = int(blocks[3]) if len(blocks) == 4 else 1

    text, reply_markup = collections_menu(
        category_id=category_id, page_number=page_number
    )
    await query.answer()
    await query.edit_message_text(text=text, reply_markup=reply_markup)


COLLECION_HANDLERS = [
    CallbackQueryHandler(
        collections_menu_callback,
        pattern=rf"^{Callbacks.COLLECTIONS}:\d+(?::page(?::\d+)?)?$",
    ),
]
