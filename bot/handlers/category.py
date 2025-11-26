import logging

from telegram import InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot.keyboards.category import (
    edit_category_inline_keyboard,
    my_categories_inline_keyboard,
)
from bot.keyboards.main import return_inline_keyboard
from bot.models.category import Category
from bot.utils.helpers.db import SessionLocal
from bot.utils.helpers.handlers import end_conversation

logger = logging.getLogger(__name__)

CATEGORY_NAME = 1


async def my_categories_menu(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
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

        categories_data = [(cat.id, cat.name) for cat in categories]
        reply_markup = my_categories_inline_keyboard(
            data=categories_data,
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
    text = "Please write a name for the category."
    reply_markup = InlineKeyboardMarkup(
        [return_inline_keyboard(target_menu="main:my_categories")]
    )
    await query.answer()
    await query.edit_message_text(text=text, reply_markup=reply_markup)
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


async def cancel_category_creation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    return await end_conversation(update, context)


async def edit_category_menu(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    blocks = query.data.split(":")
    category_id = int(blocks[3])

    with SessionLocal() as session:
        category = Category.get(db=session, id=category_id)

        if not category:
            await query.answer("Category not found.", True)
            return

        text = (
            "Editing Category:"
            "\n"
            f"\n- Name: {category.name}"
            f"\n- Current Visibility: {category.is_public and 'Public' or 'Private'}"
            f"\n- Subscribers: {category.subscribers_count}"
        )
        reply_markup = edit_category_inline_keyboard(
            category_id=category.id,
            is_public=category.is_public,
        )

        await query.answer()
        await query.edit_message_text(text=text, reply_markup=reply_markup)


async def edit_category_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    blocks = query.data.split(":")
    category_id = int(blocks[3])
    action = blocks[4]

    with SessionLocal() as session:
        category = Category.get(db=session, id=category_id)

        if not category:
            await query.answer("Category not found.", True)
            return

        if action == "change_visibility":
            category.is_public = not category.is_public
            session.commit()
            await query.answer("Category visibility updated.")
        elif action == "delete":
            category.is_deleted = True
            session.commit()
            await query.answer("Category deleted.")
            # TODO: Ask user for confirmation before deletion
            # TODO: Redirect to my categories menu after deletion

        text = (
            "Editing Category:"
            "\n"
            f"\n- Name: {category.name}"
            f"\n- Current Visibility: {category.is_public and 'Public' or 'Private'}"
            f"\n- Subscribers: {category.subscribers_count}"
        )
        reply_markup = edit_category_inline_keyboard(
            category_id=category.id,
            is_public=category.is_public,
        )
        await query.edit_message_text(text=text, reply_markup=reply_markup)


CATEGORY_HANDLER = [
    ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                create_category_callback, pattern="^main:my_categories:create$"
            )
        ],
        states={
            CATEGORY_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, create_category_message)
            ]
        },
        fallbacks=[
            CallbackQueryHandler(
                cancel_category_creation, pattern="^main:my_categories$"
            )
        ],
    ),
    CallbackQueryHandler(my_categories_menu, pattern="^main:my_categories$"),
    CallbackQueryHandler(
        edit_category_menu, pattern=r"^main:my_categories:settings:\d+$"
    ),
    CallbackQueryHandler(
        edit_category_callback, pattern=r"^main:my_categories:settings:\d+:\w+$"
    ),
]
