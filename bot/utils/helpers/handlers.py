from collections.abc import Awaitable, Callable

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler


async def answer_and_send_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    delete_current_message: bool = False,
    **kwargs,
) -> None:
    """
    Answers the callback query and sends a new message to the user.

    Args:
        update (Update): The incoming update from the Telegram bot, containing the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object for the current conversation.
        delete_current_message (bool): Whether to delete the current message after answering the query.
        **kwargs: Additional keyword arguments to pass to the send_message method.
    """
    query = update.callback_query
    await query.answer()

    if delete_current_message:
        await query.delete_message()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        **kwargs,
    )


async def end_conversation(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    callback: Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]] = None,
    message: str = None,
    clear_user_data: bool = False,
) -> int:
    """
    Ends an ongoing conversation in a Telegram bot, optionally clearing user data and sending a message.

    Args:
        update (Update): The incoming Telegram update.
        context (ContextTypes.DEFAULT_TYPE): The context for the current conversation.
        callback (Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]): An async callback to
            execute after aborting.
        message (str, optional): An optional message to send to the user upon aborting. Defaults to None.
        clear_user_data (bool, optional): Whether to clear the user's data from context. Defaults to False.

    Returns:
        int: The ConversationHandler.END constant, indicating the conversation should be terminated.
    """
    if clear_user_data:
        context.user_data.clear()

    if message:
        if update.callback_query:
            await update.callback_query.edit_message_text(text=message)
        else:
            await update.message.reply_text(message)

    if callback:
        await callback(update, context)

    return ConversationHandler.END


def cache_page_number(context: ContextTypes.DEFAULT_TYPE, page_number: int) -> None:
    context.user_data["page_number"] = page_number


def get_page_number(context: ContextTypes.DEFAULT_TYPE) -> int:
    return context.user_data.get("page_number", 1)
