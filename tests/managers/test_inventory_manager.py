"""
Author: Archie Jarvis
Student ID: 20022663
"""

from app.core.database.models import (
    StockItem,
    DietaryRequirement,
)
from app.core.managers.inventory_manager import InventoryManager
from app.core.services.order_service import OrderService
from app.core.services.stock_item_service import StockItemService
from tests.managers.test_manager_base import BaseManagerTestCase


class InventoryManagerTestCase(BaseManagerTestCase):
    def setUp(self):
        super().setUp()
        self.add_restaurant()
        self.add_table()
        self.add_table()
        self.add_food_category()
        self.add_stock_item()
        self.add_recipe()
        self.add_order()
        self.add_recipe_item()

        self.inventory_manager = InventoryManager(self.app)

    def test_update_stock_levels(self):
        with OrderService(self.app.get_session()) as order_service:
            order = order_service.get_by_id(1)
            self.inventory_manager.update_stock_levels(order.id)

            self.assertEqual(
                9,
                order_service.get_by_id(1)
                .order_recipes[0]
                .recipe.recipe_items[0]
                .stock_item.quantity,
            )

    def test_update_stock_item(self):
        stock_item = StockItem(
            inventory_id=1,
            name="Test Stock Item",
            quantity=10,
            re_order_quantity=5,
            dietary_requirements=DietaryRequirement(),
        )

        stock_item.id = 1

        self.inventory_manager.update_stock_item(stock_item)

        with StockItemService(self.app.get_session()) as stock_item_service:
            stock_item = stock_item_service.get_by_id(1)
            self.assertEqual(10, stock_item.quantity)

    def test_on_update_stock_item(self):
        with StockItemService(self.app.get_session()) as stock_item_service:
            stock_item = stock_item_service.get_by_id(1)
            stock_item.quantity = 0
            stock_item_service.commit()

        # to access private method
        self.inventory_manager.on_update_stock_item(1)

        with StockItemService(self.app.get_session()) as stock_item_service:
            stock_item = stock_item_service.get_by_id(1)
            self.assertTrue(stock_item.re_order_warning)
            stock_item.quantity = 10

            self.inventory_manager.on_update_stock_item(1)

            stock_item = stock_item_service.get_by_id(1)
            self.assertFalse(stock_item.re_order_warning)
