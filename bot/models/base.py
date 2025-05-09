import logging
import math
from datetime import datetime
from typing import Self

from sqlalchemy import DateTime, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, Session, mapped_column

logger = logging.getLogger(__name__)


class BaseModelMixin:
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    @classmethod
    def create(cls, db: Session, **kwargs) -> Self:
        obj = cls(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @classmethod
    def get(cls, db: Session, id: int) -> Self | None:
        return db.query(cls).get(id)

    @classmethod
    def get_or_create(
        cls, db: Session, defaults: dict | None, **kwargs
    ) -> tuple[Self, bool]:
        instance = db.query(cls).filter_by(**kwargs).first()
        if instance:
            return instance, False

        params = {**kwargs, **(defaults or {})}
        instance = cls(**params)
        db.add(instance)
        try:
            db.commit()
            return instance, True
        except IntegrityError as ie:
            logger.error(ie)
            db.rollback()
            instance = db.query(cls).filter_by(**kwargs).first()
            return instance, False

    @classmethod
    def paginate(
        cls, db: Session, current_page: int, per_page: int
    ) -> tuple[list[Self], int]:
        offset = (current_page - 1) * per_page
        total_rows = db.execute(select(func.count(cls.id))).scalar()
        last_page = math.ceil(total_rows / per_page)

        query = (
            db.query(cls)
            .order_by(cls.created_at.desc())
            .limit(per_page)
            .offset(offset)
            .all()
        )

        return query, last_page
