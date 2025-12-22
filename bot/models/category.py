from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, func, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models.base import BaseModelMixin
from bot.utils.helpers.db import Base

if TYPE_CHECKING:
    from bot.models.user import User


class Category(Base, BaseModelMixin):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

    author: Mapped["User"] = relationship(back_populates="categories")
    bookmarks: Mapped[list["User"]] = relationship(
        secondary="user_categories", back_populates="bookmarked_categories"
    )

    def __repr__(self):
        return f"<Category {self.name} by user {self.author_id}>"

    @hybrid_property
    def bookmarks_count(self):
        return len(self.bookmarks)

    @bookmarks_count.expression
    def bookmarks_count(cls):
        from bot.models.user import User

        return (
            select(func.count(User.id))
            .select_from(cls)
            .join(cls.bookmarks)
            .where(cls.id == cls.id)
            .correlate(cls)
            .scalar_subquery()
        )
