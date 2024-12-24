from typing import Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models.base import BaseModelMixin
from bot.models.collection import Collection
from bot.utils.db import Base


class Flashcard(Base, BaseModelMixin):
    __tablename__ = "flashcards"

    term: Mapped[str] = mapped_column(Text, nullable=False)
    definition: Mapped[str] = mapped_column(Text, nullable=False)
    photo_file_id: Mapped[Optional[str]] = mapped_column(String(64))
    synonym: Mapped[Optional[str]] = mapped_column(Text)
    antonym: Mapped[Optional[str]] = mapped_column(Text)
    collocation: Mapped[Optional[str]] = mapped_column(Text)
    example: Mapped[Optional[str]] = mapped_column(Text)
    collection_id: Mapped[int] = mapped_column(ForeignKey("collections.id"))

    collection: Mapped["Collection"] = relationship(back_populates="flashcards")

    def __repr__(self):
        return f"<Flashcard {self.term}>"
