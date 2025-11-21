from telegram.ext import CallbackContext


class CustomContext(CallbackContext):
    """
    Custom context to extend default CallbackContext.
    """
    @property
    def _(self):
        from bot.utils.tools.i18n import get_translator

        return get_translator(self)
