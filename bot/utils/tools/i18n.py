import gettext
from functools import lru_cache


@lru_cache(maxsize=32)
def _load(lang: str) -> gettext.NullTranslations.gettext:
    """Return per-user translator."""
    try:
        translator = gettext.translation(
            "messages", "locales", languages=[lang], fallback=True
        )
        return translator.gettext  # returns _()
    except FileNotFoundError:
        return gettext.NullTranslations().gettext  # returns _()


def get_translator(context):
    """Return per-user _() based on context.user_data['lang']."""
    lang = context.user_data.get("lang", "en")
    return _load(lang)
