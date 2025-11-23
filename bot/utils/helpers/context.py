from telegram.ext import CallbackContext, ExtBot


class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):
    """
    Custom context to extend default CallbackContext.
    """

    _translator = None

    @property
    def translate(self):
        if self._translator is None:
            from bot.utils.tools.i18n import get_translator

            self._translator = get_translator(self)

        return self._translator

    @property
    def _(self):
        return self.translate
