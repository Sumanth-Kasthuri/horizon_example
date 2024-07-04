"""
StockItem Service

Author: Setenay Baysal
Student ID: 22074682

"""

from app.core.database.models import StockItem
from app.core.service import Service


class StockItemService(Service):
    def __init__(self, session):
        super().__init__(session, StockItem)

    def get_stock_item_by_name(self, stock_item_name: str) -> StockItem:
        return self._session.query(StockItem).filter_by(name=stock_item_name).first()

    def get_stock_items_by_quantity(self, stock_item_quantity: int) -> StockItem:
        return (
            self._session.query(StockItem).filter_by(quantity=stock_item_quantity).all()
        )

    def get_by_inventory_id(self, inventory_id: int) -> StockItem:
        return self._session.query(StockItem).filter_by(inventory_id=inventory_id).all()
