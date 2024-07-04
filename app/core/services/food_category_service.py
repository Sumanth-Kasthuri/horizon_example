"""
FoodCategory Service

Author: Setenay Baysal
Student ID: 22074682

"""

from app.core.database.models import FoodCategory
from app.core.service import Service


class FoodCategoryService(Service):
    def __init__(self, session):
        super().__init__(session, FoodCategory)

    def get_food_category_by_name(self, food_category_name: str) -> FoodCategory:
        return (
            self._session.query(FoodCategory).filter_by(name=food_category_name).first()
        )
