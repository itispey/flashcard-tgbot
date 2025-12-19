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
)
from bot.keyboards.confirmation import confirmation_inline_keyboard
from bot.keyboards.main import return_inline_keyboard
from bot.messages import ButtonTexts, Messages
from bot.models.category import Category
from bot.utils.helpers.db import SessionLocal
from bot.utils.helpers.handlers import end_conversation

logger = logging.getLogger(__name__)

MENU_CATEGORIES = "main:categories"
CATEGORY_NAME = 1


async def create_category_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    text = Messages.CATEGORY_NAME_PROMPT
    reply_markup = InlineKeyboardMarkup(
        [return_inline_keyboard(target_menu=MENU_CATEGORIES)]
    )
    await query.answer()
    await query.edit_message_text(text=text, reply_markup=reply_markup)
    return CATEGORY_NAME


async def create_category_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    from bot.handlers.collection import collections_menu_message

    user = update.effective_user
    message = update.message
    text = message.text

    with SessionLocal() as session:
        category = Category.create(db=session, name=text, author_id=user.id)
        logger.info("Category created: %s", category.name)

        await update.message.reply_text(Messages.CATEGORY_CREATED)
        await collections_menu_message(
            update=update, context=context, category_id=category.id
        )
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
        category = Category.filter(db=session, id=category_id, is_deleted=False).first()

        if not category:
            await query.answer(Messages.CATEGORY_NOT_FOUND, True)
            return

        text = Messages.CATEGORY_DETAIL.format(
            name=category.name,
            visibility=Messages.VISIBILITY_PUBLIC
            if category.is_public
            else Messages.VISIBILITY_PRIVATE,
            count=category.bookmarks_count,
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
        category = Category.filter(db=session, id=category_id, is_deleted=False).first()

        if not category:
            await query.answer(Messages.CATEGORY_NOT_FOUND, True)
            return

        if action == "change_visibility":
            category.is_public = not category.is_public
            session.commit()
            await query.answer(Messages.CATEGORY_VISIBILITY_UPDATED)

        if action == "delete":
            reply_markup = confirmation_inline_keyboard(
                confirm_callback=f"{MENU_CATEGORIES}:settings:{category.id}:confirm_delete",
                cancel_callback=f"{MENU_CATEGORIES}:settings:{category.id}",
                confirm_text=ButtonTexts.DELETE,
                cancel_text=ButtonTexts.CANCEL,
            )
            await query.edit_message_text(
                text=Messages.CATEGORY_DELETION_CONFIRM,
                reply_markup=reply_markup,
            )
            return
        elif action == "confirm_delete":
            category.is_deleted = True
            session.commit()
            await query.answer(Messages.CATEGORY_DELETED)
            # await my_categories_menu(update, context)
            return

        text = Messages.CATEGORY_DETAIL.format(
            name=category.name,
            visibility=Messages.VISIBILITY_PUBLIC
            if category.is_public
            else Messages.VISIBILITY_PRIVATE,
            count=category.bookmarks_count,
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
                create_category_callback, pattern=f"^{MENU_CATEGORIES}:create$"
            )
        ],
        states={
            CATEGORY_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, create_category_message)
            ]
        },
        fallbacks=[
            CallbackQueryHandler(
                cancel_category_creation, pattern=f"^{MENU_CATEGORIES}$"
            )
        ],
    ),
    # CallbackQueryHandler(my_categories_menu, pattern=f"^{MENU_CATEGORIES}$"),
    CallbackQueryHandler(
        edit_category_menu, pattern=rf"^{MENU_CATEGORIES}:settings:\d+$"
    ),
    CallbackQueryHandler(
        edit_category_callback, pattern=rf"^{MENU_CATEGORIES}:settings:\d+:\w+"
    ),
]
