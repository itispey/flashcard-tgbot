from sqlalchemy.orm import Session

from bot.handlers.categories.types import CategoryType
from bot.models.category import Category


def get_categories(
    db: Session, category_type: CategoryType, user_tg_id: int, page_number: int = 1
) -> tuple[list[Category], int]:
    filters = {"is_deleted": False}
    query = None

    if category_type == CategoryType.MY_CATEGORIES:
        filters["author_id"] = user_tg_id
    # TODO: add more types later

    return Category.paginate(
        db=db,
        current_page=page_number,
        per_page=5,
        filters=filters,
        base_query=query,
    )
