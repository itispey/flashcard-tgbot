from decouple import Csv, config


class Config:
    DEBUG_MODE = config("DEBUG_MODE", default=False, cast=bool)

    TOKEN = config("TOKEN")
    ADMINS = config("ADMINS", cast=Csv(int))

    PROXY = config("PROXY", default=False, cast=bool)
    PROXY_URL = config("PROXY_URL")

    DB_HOST = config("MYSQL_HOST", default="localhost")
    DB_PORT = config("MYSQL_PORT", default="3306")
    DB_USER = config("MYSQL_USER", default="root")
    DB_PASS = config("MYSQL_PASS")
    DB_NAME = config("MYSQL_NAME")

    POOL_PRE_PING = config("POOL_PRE_PING", default=True, cast=bool)
    POOL_RECYCLE = config("POOL_RECYCLE", default=28000, cast=int)

    DATABASE_URL = (
        f"mysql+mysqldb://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # noqa
    )
