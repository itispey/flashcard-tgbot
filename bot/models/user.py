from typing import List, Optional

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models.base import BaseModelMixin
from bot.models.category import Category
from bot.utils.db import Base


class User(Base, BaseModelMixin):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True, index=True
    )
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[Optional[str]] = mapped_column(String(255))
    username: Mapped[Optional[str]] = mapped_column(String(32))

    categories: Mapped[Optional[List["Category"]]] = relationship(
        back_populates="author"
    )
    subscribed_categories: Mapped[Optional[List["Category"]]] = relationship(
        secondary="user_categories", back_populates="subscribers"
    )

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"
