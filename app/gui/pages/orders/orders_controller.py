import threading
import time
import tkinter as tk

from app.core.services.order_service import OrderService
from app.gui.controller import Controller
from app.gui.pages.orders.orders_view import OrdersView
from app.gui.utils.widgets.full_table_widget import TableWidget


class OrdersController(Controller):
    def __init__(self, view: OrdersView, restaurant, app):
        super().__init__(view, app)
        self.__restaurant = restaurant
        self.__set_up_table()

        self.__table_update_thread = threading.Thread(target=self.__update_table)
        self.__table_update_thread.start()

    def __get_table_data(self):
        with OrderService(self._app.get_session()) as order_service:
            orders = order_service.get_by_restaurant_id(self.__restaurant.id)
            return order_service.expunge_all(orders)

    def __set_up_table(self):
        table_data = self.__get_table_data()

        self.__table_wrapper = TableWidget(
            label_text="Orders",
            data=table_data,
            callback=self.__view_order,
            master=self._view.table_container,
            excluded_columns=("id", "restaurant_id"),
        )
        self.__table_wrapper.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

    def __update_table(self):
        while not self._app.get_stop_threads().is_set() and self._view.winfo_exists():
            self.__table_wrapper.get_table().set_data(self.__get_table_data())
            time.sleep(10)

    def __view_order(self, order_id):
        self._app.raise_screen(
            self._view,
            "order",
            {"app": self._app},
            {"app": self._app, "order_id": order_id},
        )

    def get_restaurant(self):
        return self.__restaurant
