import logging

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.models.user import User
from bot.utils.db import SessionLocal

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

    await update.message.reply_text("Hello, I'm a bot!")


MAIN_HANDLER = [CommandHandler("start", start)]
