"""
MenuItem Service

Author: Setenay Baysal
Student ID: 22074682

"""

from app.core.database.models import MenuItem
from app.core.service import Service


class MenuItemService(Service):
    def __init__(self, session):
        super().__init__(session, MenuItem)

    def get_menu_item_by_name(self, menu_item_name: str) -> MenuItem:
        return self._session.query(MenuItem).filter_by(name=menu_item_name).first()

    def get_menu_items_by_price(self, menu_item_price: float) -> MenuItem:
        return self._session.query(MenuItem).filter_by(price=menu_item_price).all()

    def get_menu_items_by_availability(
        self, menu_item_availability: bool
    ) -> list[MenuItem]:
        return (
            self._session.query(MenuItem)
            .filter_by(availability=menu_item_availability)
            .all()
        )
