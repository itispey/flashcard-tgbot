from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from bot.models.base import BaseModelMixin
from bot.utils.helpers.db import Base


class FlashcardStudy(Base, BaseModelMixin):
    __tablename__ = "flashcard_studies"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))
    flashcard_id: Mapped[int] = mapped_column(ForeignKey("flashcards.id"))
    is_studied: Mapped[bool] = mapped_column(default=False)
