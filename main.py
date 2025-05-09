import logging

from telegram.ext import ApplicationBuilder

from bot import models
from bot.handlers.category import CATEGORY_HANDLER
from bot.handlers.main import MAIN_HANDLER
from bot.utils.db import engine
from config import Config

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)


def main() -> None:
    if Config.PROXY:
        app = (
            ApplicationBuilder()
            .token(Config.TOKEN)
            .proxy(Config.PROXY_URL)
            .get_updates_proxy(Config.PROXY_URL)
            .build()
        )
    else:
        app = ApplicationBuilder().token(Config.TOKEN).build()

    app.add_handlers(MAIN_HANDLER)
    app.add_handlers(CATEGORY_HANDLER)

    app.run_polling()


if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    main()
