"""
Author: Archie Jarvis
Student ID: 20022663
"""

from app.core.services.order_service import OrderService


class DiscountsManager:
    def __init__(self, app):
        self.__app = app

    def update_discount(self, order_id):
        """
        Applies the given discount_add to the given payment.
        :param order_id: The order id to apply the discount_add to.
        :return: None
        """
        with OrderService(self.__app.get_session()) as order_service:
            order = order_service.get_by_id(order_id)

            if order.discount_id is None:
                return

            order.payment.final_price = (
                order.payment.price * order.discount.discount_multiplier
            )
