from sqlalchemy import Column, ForeignKey, Table

from bot.utils.db import Base

user_categories = Table(
    "user_categories",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("category_id", ForeignKey("categories.id")),
)
