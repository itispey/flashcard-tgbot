import logging

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.keyboards.main import main_inline_keyboard
from bot.messages import Messages
from bot.models.user import User
from bot.utils.helpers.db import SessionLocal

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tg_user = update.effective_user

    with SessionLocal() as session:
        # TODO: update user's info whenever they start the bot
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

    text = Messages.START_GREETING.format(first_name=tg_user.first_name)
    reply_markup = main_inline_keyboard()
    await update.message.reply_text(text, reply_markup=reply_markup)


MAIN_HANDLER = [
    CommandHandler("start", start),
]
