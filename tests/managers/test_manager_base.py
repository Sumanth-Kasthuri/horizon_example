"""
Author: Archie Jarvis
Student ID: 20022663
"""

import unittest
from datetime import datetime
import logging

import mock

from app.core.database.models import (
    Restaurant,
    Table,
    Reservation,
    StockItem,
    FoodCategory,
    Recipe,
    Order,
    RecipeItem,
    Discount,
    DietaryRequirement,
    OrderRecipe,
)
from app.core.service import Service
from app.core.services.dietary_need_service import DietaryNeedService
from app.core.services.discount_service import DiscountService
from app.core.services.food_category_service import FoodCategoryService
from app.core.services.recipe_item_service import RecipeItemService
from app.core.services.reservation_service import ReservationService
from app.core.services.restaurant_service import RestaurantService
from app.core.services.stock_item_service import StockItemService
from app.core.services.table_service import TableService
from tests import test_utils


class BaseManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.session = test_utils.create_test_session()
        self.app = mock.Mock()
        self.app.get_session.return_value = self.session

    def log(self, message):
        with self.assertLogs(level=logging.INFO) as cm:
            logging.getLogger().info(message)
            self.assertEqual(cm.output, [f"INFO:roo:{message}"])

    def add_restaurant(self):
        with RestaurantService(self.session) as restaurant_service:
            restaurant_service.add(
                Restaurant(
                    name="Test Restaurant",
                    capacity=100,
                    city="Test City",
                )
            )

    def add_table(self):
        with TableService(self.session) as table_service:
            table_service.add(Table(capacity=4, restaurant_id=1))

    def add_reservation(self, time):
        with ReservationService(self.session) as reservation_service:
            dt = datetime.now()
            dt = dt.replace(hour=time, minute=0, second=0, microsecond=0)
            reservation_service.add(
                Reservation(
                    date=datetime.date(dt),
                    time=datetime.time(dt),
                    number_of_people=4,
                    restaurant_id=1,
                    table_id=1,
                    name="Test Reservation",
                )
            )

    def add_stock_item(self, vegetarian=True):
        with StockItemService(self.app.get_session()) as stock_item_service:
            stock_item_service.add(
                StockItem(
                    name="Burger bun",
                    quantity=10,
                    inventory_id=1,
                    dietary_requirements=DietaryRequirement(vegetarian=vegetarian),
                    re_order_quantity=5,
                )
            )

    def add_food_category(self):
        with FoodCategoryService(self.app.get_session()) as food_category_service:
            food_category_service.add(
                FoodCategory(name="Test Food Category", menu_id=1)
            )

    def add_recipe(self):
        with Service(self.app.get_session(), Recipe) as recipe_service:
            recipe_service.add(
                Recipe(
                    name="Burger",
                    description="A burger",
                    price=10,
                    food_category_id=1,
                )
            )

    def add_recipe_item(self):
        with RecipeItemService(self.app.get_session()) as recipe_item_service:
            recipe_item_service.add(
                RecipeItem(
                    recipe_id=1,
                    stock_item_id=1,
                    quantity=1,
                )
            )

    def add_order(self):
        with Service(self.app.get_session(), OrderRecipe) as recipe_service:
            order = Order(
                table_id=1,
                discount_id=None,
                order_recipes=[OrderRecipe(recipe_id=1, quantity=1, order_id=1)],
            )
            recipe_service.add(order)

    def add_discount(self, discount_multiplier):
        with DiscountService(self.app.get_session()) as discounts_service:
            discounts_service.add(
                Discount(
                    name="Test Discount",
                    start_date=datetime.date(datetime.now()),
                    end_date=datetime.date(datetime.now()).replace(
                        year=datetime.now().year + 1
                    ),
                    discount_multiplier=discount_multiplier,
                )
            )

    def add_dietary_requirement(self):
        with DietaryNeedService(self.app.get_session()) as dietary_need_service:
            dietary_need_service.add(
                DietaryRequirement(
                    vegetarian=False,
                )
            )

    def tearDown(self):
        self.session.close()
