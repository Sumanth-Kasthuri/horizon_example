import threading
import time
import tkinter as tk

from app.core.services.restaurant_service import RestaurantService
from app.core.services.stock_item_service import StockItemService
from app.gui.controller import Controller
from app.gui.utils.widgets.full_table_widget import TableWidget


class InventoryController(Controller):
    def __init__(self, app, view, restaurant):
        super().__init__(view, app)
        self.__restaurant = restaurant

        self.__set_up_table()

        self.__table_update_thread = threading.Thread(target=self.__update_table)
        self.__table_update_thread.start()

    def __get_table_data(self):
        session = self._app.get_session()
        with RestaurantService(session) as restaurant_service:
            restaurant = restaurant_service.get_by_id(self.__restaurant.id)

            stock_items = restaurant.inventory.stock_items

            return restaurant_service.expunge_all(stock_items)

    def __set_up_table(self):
        table_data = self.__get_table_data()

        self.__table_wrapper = TableWidget(
            label_text=f"Inventory of {self.__restaurant.name}",
            data=table_data,
            callback=self.__view_stock_item,
            master=self._view.table_container,
            excluded_columns=("id", "inventory_id"),
        )
        self.__table_wrapper.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

    def __update_table(self):
        while not self._app.get_stop_threads().is_set() and self._view.winfo_exists():
            self.__table_wrapper.get_table().set_data(self.__get_table_data())
            time.sleep(10)

    def __view_stock_item(self, stock_item_id):
        with StockItemService(self._app.get_session()) as stock_item_service:
            stock_item = stock_item_service.get_by_id(stock_item_id)
            stock_item_service.expunge(stock_item)

        self._app.raise_screen(
            self._view,
            "stock_item",
            {"app": self._app, "stock_item": stock_item},
            {"app": self._app, "stock_item": stock_item},
        )

    def get_restaurant(self):
        return self.__restaurant
