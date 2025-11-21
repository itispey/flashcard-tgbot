from typing import Optional

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models.base import BaseModelMixin
from bot.utils.helpers.db import Base


class Category(Base, BaseModelMixin):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # we can't use Mapped here because it's a circular import
    author = relationship("User", back_populates="categories")
    subscribers = relationship(
        "User", secondary="user_categories", back_populates="subscribed_categories"
    )

    def __repr__(self):
        return f"<Category {self.name} by user {self.author_id}>"
