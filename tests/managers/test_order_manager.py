"""
Author: Archie Jarvis
Student ID: 20022663
"""

from app.core.database.models import (
    Order,
    OrderRecipe,
)
from app.core.managers.order_manager import OrderManager
from app.core.service import Service
from app.core.services.order_service import OrderService
from tests.managers.test_manager_base import BaseManagerTestCase


class OrderManagerTestCase(BaseManagerTestCase):
    def setUp(self):
        super().setUp()
        self.add_restaurant()
        self.add_stock_item()
        self.add_table()
        self.add_food_category()
        self.add_recipe()
        self.add_order()
        self.add_recipe_item()

        self.order_manager = OrderManager(self.app)

    def test_place_order(self):
        with OrderService(self.session) as service:
            with Service(self.session, OrderRecipe) as order_recipe_service:
                order_recipe_service.add(
                    OrderRecipe(order_id=1, recipe_id=1, quantity=1)
                )

                order_recipe_service.commit()

                order_recipe = order_recipe_service.get_by_id(1)

                order = Order(table_id=1, discount_id=None, order_recipes=[order_recipe])

                self.order_manager.place_order(order)
                self.assertEquals(2, len(service.get_all()))

    def test_set_order_ready(self):
        self.order_manager.set_order_ready(1)

        with OrderService(self.session) as service:
            order = service.get_by_id(1)
            self.assertTrue(order.ready)
            self.assertIsNotNone(order.ready_time)
