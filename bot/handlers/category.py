import logging

from telegram import InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot.keyboards.category import my_categories_inline_keyboard
from bot.keyboards.main import return_inline_keyboard
from bot.models.category import Category
from bot.utils.db import SessionLocal

logger = logging.getLogger(__name__)

CATEGORY_NAME = 1


async def my_categories_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Handles the callback for displaying the user's categories.
    This function is triggered when the user interacts with the "My Categories" button
    in the bot's interface. It retrieves the user's categories from the database, paginates
    them, and updates the message with the list of categories or a prompt to create a new one.

    Args:
        update (Update): The incoming update from the Telegram bot, containing the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the current conversation.
    """
    query = update.callback_query
    blocks = query.data.split(":")
    page_number = int(blocks[3]) if len(blocks) == 4 else 1

    with SessionLocal() as session:
        categories, total_pages = Category.paginate(
            db=session, current_page=page_number, per_page=5
        )

        if not categories:
            text = "You don't have any category! Try making a new one by tapping the button below."
        else:
            text = "Here's are your categories:"

        reply_markup = my_categories_inline_keyboard(
            data=[(cat.id, cat.name) for cat in categories],
            current_menu="main:my_categories",
            current_page=page_number,
            total_pages=total_pages,
            return_to_menu="main",
        )

        await query.answer()
        await query.edit_message_text(text=text, reply_markup=reply_markup)


async def create_category_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(
        [return_inline_keyboard(target_menu="main:my_categories")]
    )
    await query.answer()
    await query.edit_message_text(
        text="Please send the category name.", reply_markup=reply_markup
    )
    return CATEGORY_NAME


async def create_category_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user = update.effective_user
    message = update.message
    text = message.text

    with SessionLocal() as session:
        category = Category.create(db=session, name=text, author_id=user.id)
        logger.info("Category created: %s", category.name)

    await update.message.reply_text("Done")
    return ConversationHandler.END


CATEGORY_HANDLER = [
    CallbackQueryHandler(my_categories_callback, pattern="^main:my_categories"),
    ConversationHandler(
        entry_points=[
            CallbackQueryHandler(create_category_callback, pattern="^category:create")
        ],
        states={
            CATEGORY_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, create_category_message)
            ]
        },
        fallbacks=[],
    ),
]
