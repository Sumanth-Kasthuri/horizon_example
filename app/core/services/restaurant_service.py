"""
Restaurant Service

Author: Archie Jarvis
Student ID: 20022663
"""

from app.core.database.models import Restaurant
from app.core.service import Service


class RestaurantService(Service):
    def __init__(self, session):
        super().__init__(session, Restaurant)

    def get_by_name(self, restaurant_name: str) -> Restaurant:
        return self._session.query(Restaurant).filter_by(name=restaurant_name).first()

    def get_by_city(self, restaurant_city: str) -> list[Restaurant]:
        return self._session.query(Restaurant).filter_by(city=restaurant_city).all()
