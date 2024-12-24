import logging

from telegram.ext import ApplicationBuilder

from bot import models
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

    app.run_polling()


if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    main()
