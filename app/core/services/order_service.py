"""
Order Service

Author: Setenay Baysal
Student ID: 22074682

"""

from app.core.database.models import Order
from app.core.service import Service


class OrderService(Service):
    def __init__(self, session):
        super().__init__(session, Order)

    def get_orders_by_price(self, order_price: float) -> Order:
        return self._session.query(Order).filter_by(price=order_price).all()

    def get_orders_by_date(self, order_date) -> list[Order]:
        return self._session.query(Order).filter_by(date=order_date).all()

    def get_by_restaurant_id(self, restaurant_id) -> list[Order]:
        return self._session.query(Order).filter_by(restaurant_id=restaurant_id).all()
