import logging

from telegram import InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot.constants import Callbacks
from bot.handlers.categories.my_categories import my_categories_menu_callback
from bot.keyboards.collection import collections_inline_keyboard
from bot.keyboards.main import return_inline_keyboard
from bot.messages import Messages
from bot.models.collection import Collection
from bot.utils.helpers.db import SessionLocal
from bot.utils.helpers.handlers import end_conversation

logger = logging.getLogger(__name__)

COLLECTION_NAME_STEP = 0


def collections_menu(
    category_id: int, page_number: int = 1
) -> tuple[str, InlineKeyboardMarkup]:
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
            return_to_menu=Callbacks.MY_CATEGORIES,
        )
        # FIXME: still not sure about this, since the previous menu could be public categories or bookmarks one
        # also we need to use the cached page number here

        return text, reply_markup


async def collections_menu_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE, category_id: int
) -> None:
    text, reply_markup = collections_menu(category_id=category_id)
    await context.bot.send_message(
        chat_id=update.effective_user.id, text=text, reply_markup=reply_markup
    )


async def collections_menu_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    blocks = query.data.split(":")
    category_id = int(blocks[1])
    page_number = int(blocks[3]) if len(blocks) == 4 else 1

    text, reply_markup = collections_menu(
        category_id=category_id, page_number=page_number
    )
    await query.answer()
    await query.edit_message_text(text=text, reply_markup=reply_markup)


async def create_collection_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    query = update.callback_query
    blocks = query.data.split(":")
    category_id = int(blocks[1])

    context.user_data["category_id"] = category_id  # cache the category id

    reply_markup = InlineKeyboardMarkup(
        [return_inline_keyboard(target_menu=f"{Callbacks.COLLECTIONS}:{category_id}")]
    )
    await query.answer()
    await query.edit_message_text(
        text=Messages.COLLECTION_NAME_PROMPT, reply_markup=reply_markup
    )
    return COLLECTION_NAME_STEP


async def create_collection_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    message = update.message
    text = message.text
    category_id = context.user_data.get("category_id")
    if not category_id:
        # ends the conversation and return to the my categories menu (previous menu)
        return await end_conversation(
            update=update,
            context=context,
            callback=my_categories_menu_callback,
            message=Messages.CATEGORY_ID_NOT_FOUND,
        )

    with SessionLocal() as session:
        collection = Collection.create(db=session, name=text, category_id=category_id)
        logger.info("Collection created: %s", collection.name)

        await update.message.reply_text(Messages.COLLECTION_CREATED)
        # await collections_menu_message(
        #     update=update, context=context, category_id=category_id
        # )
        return ConversationHandler.END


async def cancel_collection_creation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    return await end_conversation(
        update=update,
        context=context,
        callback=collections_menu_callback,
    )


COLLECION_HANDLERS = [
    ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                create_collection_callback,
                pattern=rf"^{Callbacks.COLLECTIONS}:\d+:create$",
            ),
        ],
        states={
            COLLECTION_NAME_STEP: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, create_collection_message
                ),
            ],
        },
        fallbacks=[
            CallbackQueryHandler(
                cancel_collection_creation,
                pattern=rf"^{Callbacks.COLLECTIONS}:\d+",  # FIXME: Add the page number later
            ),
        ],
    ),
    CallbackQueryHandler(
        collections_menu_callback,
        pattern=rf"^{Callbacks.COLLECTIONS}:\d+(?::page(?::\d+)?)?$",
    ),
]
