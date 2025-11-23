import logging

from telegram import Update
from telegram.ext import CallbackQueryHandler, CommandHandler

from bot.keyboards.main import main_inline_keyboard, select_language_keyboard
from bot.models.user import User
from bot.utils.helpers.context import CustomContext
from bot.utils.helpers.db import SessionLocal

logger = logging.getLogger(__name__)


async def start(update: Update, context: CustomContext) -> None:
    tg_user = update.effective_user

    with SessionLocal() as session:
        user, created = User.get_or_create(
            db=session,
            tg_id=tg_user.id,
            defaults={
                "first_name": tg_user.first_name,
                "last_name": tg_user.last_name,
                "username": tg_user.username,
            },
        )
        logger.info(f"User {user} {'created' if created else 'fetched'}")

        if created:
            await select_language(update, context)
            return

    text = context._("Hello {user_first_name}. How can I help you today?").format(
        user_first_name=tg_user.first_name
    )
    reply_markup = main_inline_keyboard(context)
    await update.message.reply_text(text, reply_markup=reply_markup)


async def select_language(update: Update, context: CustomContext) -> None:
    text = ("Hello {user_first_name}. Please select your language.").format(
        user_first_name=update.effective_user.first_name
    )
    reply_markup = select_language_keyboard()
    await update.message.reply_text(text, reply_markup=reply_markup)


async def select_language_callback(update: Update, context: CustomContext) -> None:
    query = update.callback_query
    lang = query.data.split(":")[1]

    context.user_data["lang"] = lang

    text = context._("Language has been set successfully.")
    await query.answer()
    await query.edit_message_text(text=text)

    text = context._("Hello {user_first_name}. Welcome to the bot.").format(
        user_first_name=update.effective_user.first_name
    )
    reply_markup = main_inline_keyboard(context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup
    )


MAIN_HANDLER = [
    CommandHandler("start", start),
    CallbackQueryHandler(select_language_callback, pattern=r"^set_lang:"),
]
