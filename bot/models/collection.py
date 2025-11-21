from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from bot.models.base import BaseModelMixin
from bot.utils.helpers.db import Base


class Collection(Base, BaseModelMixin):
    __tablename__ = "collections"

    name: Mapped[str] = mapped_column(String(64), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    # category: Mapped["Category"] = relationship(back_populates="collections")

    def __repr__(self):
        return f"<Collection {self.name}>"
