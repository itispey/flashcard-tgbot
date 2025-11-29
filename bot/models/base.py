import logging
import math
from datetime import datetime
from typing import Self

from sqlalchemy import DateTime, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, Query, Session, mapped_column

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
    def filter(cls, db: Session, **kwargs) -> Query[Self]:
        filter_items = []
        for key, value in kwargs.items():
            filter_items.append(getattr(cls, key) == value)

        return db.query(cls).filter(*filter_items)

    @classmethod
    def paginate(
        cls, db: Session, current_page: int, per_page: int, filters: dict | None = None
    ) -> tuple[list[Self], int]:
        offset = (current_page - 1) * per_page
        query = db.query(cls)
        if filters:
            for key, value in filters.items():
                column = getattr(cls, key, None)
                if column is None:
                    continue

                # Support simple operators via tuple syntax, e.g., ("ne", value)
                # Defaults to equality when a raw value is provided
                if isinstance(value, tuple) and len(value) == 2:
                    op, op_value = value
                    if op == "ne":
                        query = query.filter(column != op_value)
                    elif op == "gt":
                        query = query.filter(column > op_value)
                    elif op == "lt":
                        query = query.filter(column < op_value)
                    elif op == "ge":
                        query = query.filter(column >= op_value)
                    elif op == "le":
                        query = query.filter(column <= op_value)
                    elif op == "in":
                        query = query.filter(column.in_(op_value))
                    elif op == "nin":
                        query = query.filter(~column.in_(op_value))
                    else:
                        query = query.filter(column == op_value)
                else:
                    query = query.filter(column == value)

        total_rows = query.with_entities(func.count(cls.id)).scalar()
        last_page = math.ceil(total_rows / per_page) if total_rows else 1

        query = (
            query.order_by(cls.created_at.desc()).limit(per_page).offset(offset).all()
        )

        return query, last_page
