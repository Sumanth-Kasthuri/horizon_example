"""
Author: Archie Jarvis
Student ID: 20022663
"""

from datetime import datetime

from app.core.database.models import Payment
from app.core.services.order_service import OrderService


def get_price(order):
    """
    Returns the price of the given order.
    :param order: The order to get the amount of.
    :return: The amount of the order.
    """
    price = 0
    for order_recipe in order.order_recipes:
        price += order_recipe.recipe.price * order_recipe.quantity
    return price


class OrderManager:
    def __init__(self, app):
        self.__app = app

    def place_order(self, order):
        """
        Places the given order.
        :param order: The order to place.
        """
        with OrderService(self.__app.get_session()) as service:
            service.add(order)
            order.payment = Payment(price=get_price(order), order_id=order.id)
            service.commit()
            self.__on_place_order(order.id)
            return order.id

    def __update_price(self, order_id: int):
        """
        Updates the price of the given order.
        :param order_id: The order id to update the price of.
        :return: None
        """
        with OrderService(self.__app.get_session()) as service:
            order = service.get_by_id(order_id)
            order.payment.price = get_price(order)
            service.commit()

    def set_order_ready(self, order_id):
        """
        Sets the given order to ready.
        :param order_id: The order id to set to ready.
        :return: None
        """
        with OrderService(self.__app.get_session()) as service:
            order = service.get_by_id(order_id)
            order.ready = True
            order.ready_time = datetime.time(datetime.now())

    def on_update_order(self, order_id: int):
        """
        Called when an order is updated, calls the inventory manager to update the stock levels.
        :param order_id: The order id that was updated.
        :return: None
        """
        self.__update_price(order_id)
        self.__on_place_order(order_id)

    def __on_place_order(self, order_id: int):
        """
        Called when an order is placed, calls the inventory manager to update the stock levels.
        :param order_id: The order id that was placed.
        :return: None
        """
        self.__app.get_inventory_manager().update_stock_levels(order_id)
        self.__app.get_discounts_manager().update_discount(order_id)
