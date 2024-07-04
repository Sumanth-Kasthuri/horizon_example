"""
Author: Archie Jarvis
Student ID: 20022663
"""

from app.core.database.models import DietaryRequirement
from app.core.managers.menu_manager import MenuManager
from app.core.services.stock_item_service import StockItemService
from tests.managers.test_manager_base import BaseManagerTestCase


class MenuManagerTestCase(BaseManagerTestCase):
    def setUp(self):
        super().setUp()
        self.manager = MenuManager(self.app)

    def test_is_menu_item_suitable_for(self):
        # Dietary requirements with all fields true, so they are vegan, vegetarian, and all other allergies
        dietary_requirements = DietaryRequirement()

        self.add_recipe()
        self.add_stock_item(vegetarian=False)
        self.add_recipe_item()

        # Recipe item is not vegetarian as the stock item is not vegetarian, so the menu item is not suitable
        self.assertFalse(
            self.manager.is_menu_item_suitable_for(dietary_requirements, 1)
        )

        # Make the stock item vegetarian
        with StockItemService(self.app.get_session()) as stock_item_service:
            stock_item = stock_item_service.get_by_id(1)
            stock_item.dietary_requirements.vegetarian = True

        self.assertTrue(self.manager.is_menu_item_suitable_for(dietary_requirements, 1))

    def test_get_suitable_food_items(self):
        # Dietary requirements with all fields true, so they are vegan, vegetarian, and all other allergies
        dietary_requirements = DietaryRequirement()

        self.add_restaurant()
        self.add_recipe()
        self.add_stock_item(vegetarian=False)
        self.add_food_category()
        self.add_recipe_item()

        # Recipe item is not vegetarian as the stock item is not vegetarian, so the menu item is not suitable
        self.assertEqual(
            0,
            len(self.manager.get_suitable_food_items(dietary_requirements, 1)),
        )

        # Make the stock item vegetarian
        with StockItemService(self.app.get_session()) as stock_item_service:
            stock_item = stock_item_service.get_by_id(1)
            stock_item.dietary_requirements.vegetarian = True

        self.assertEqual(
            1,
            len(self.manager.get_suitable_food_items(dietary_requirements, 1)),
        )
