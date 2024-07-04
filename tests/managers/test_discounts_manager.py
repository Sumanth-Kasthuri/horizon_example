"""
Author: Archie Jarvis
Student ID: 20022663
"""

from app.core.database.models import Order, Recipe, OrderRecipe
from app.core.managers.discounts_manager import DiscountsManager
from app.core.managers.order_manager import OrderManager
from app.core.service import Service
from app.core.services.order_service import OrderService
from tests.managers.test_manager_base import BaseManagerTestCase


class DiscountsManagerTestCase(BaseManagerTestCase):
    def setUp(self):
        super().setUp()
        self.manager = DiscountsManager(self.app)
        self.order_manager = OrderManager(self.app)

    def test_update_discount(self):
        self.add_recipe()
        self.add_recipe_item()

        with Service(self.app.get_session(), OrderRecipe) as service:
            service.add(
                OrderRecipe(order_id=1, recipe_id=1, quantity=1)
            )

            service.commit()

            order_recipe = service.get_by_id(1)

            self.order_manager.place_order(
                Order(
                    table_id=1,
                    discount_id=1,
                    order_recipes=[order_recipe],
                )
            )

        discount_multiplier = 0.5

        with OrderService(self.app.get_session()) as order_service:
            order = order_service.get_by_id(1)
            price_before = order.payment.price

        self.add_discount(discount_multiplier)

        self.manager.update_discount(1)

        with OrderService(self.app.get_session()) as order_service:
            order = order_service.get_by_id(1)
            price_after = order.payment.final_price

        self.assertEqual(price_before * discount_multiplier, price_after)
