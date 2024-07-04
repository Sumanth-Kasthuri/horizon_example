"""
RecipeItem Service

Author: Setenay Baysal
Student ID: 22074682

"""

from app.core.database.models import RecipeItem
from app.core.service import Service


class RecipeItemService(Service):
    def __init__(self, session):
        super().__init__(session, RecipeItem)

    def get_recipe_items_by_quantity(self, recipe_item_quantity: int) -> RecipeItem:
        return (
            self._session.query(RecipeItem)
            .filter_by(quantity=recipe_item_quantity)
            .all()
        )
