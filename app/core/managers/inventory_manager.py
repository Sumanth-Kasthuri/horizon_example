"""
Author: Archie Jarvis
Student ID: 20022663
"""

from app.core.services.order_service import OrderService
from app.core.services.stock_item_service import StockItemService


class InventoryManager:
    def __init__(self, app):
        self.__app = app

    def update_stock_item(self, stock_item):
        """
        Adds the given stock item.
        :param stock_item: The stock item to add.
        :return: None
        """
        with StockItemService(self.__app.get_session()) as service:
            service.update(stock_item)
            service.commit()

            self.on_update_stock_item(stock_item.id)

    def on_update_stock_item(self, stock_item_id):
        with StockItemService(self.__app.get_session()) as service:
            stock_item = service.get_by_id(stock_item_id)
            if stock_item.quantity > stock_item.re_order_quantity:
                stock_item.re_order_warning = False
                service.commit()
            else:
                stock_item.re_order_warning = True
                service.commit()

            for recipe_item in stock_item.recipe_items:
                if stock_item.quantity <= recipe_item.quantity:
                    recipe_item.recipe.available = False
                    service.commit()

    def update_stock_levels(self, order_id: int):
        """
        Updates the stock levels for the given order id.
        :param order_id: The order id to update the stock levels for.
        :return: None
        """
        with OrderService(self.__app.get_session()) as service:
            order = service.get_by_id(order_id)
            for order_recipe in order.order_recipes:
                for recipe_item in order_recipe.recipe.recipe_items:
                    stock_item = recipe_item.stock_item
                    stock_item.quantity -= recipe_item.quantity * order_recipe.quantity
                    service.commit()
                    self.on_update_stock_item(stock_item.id)
