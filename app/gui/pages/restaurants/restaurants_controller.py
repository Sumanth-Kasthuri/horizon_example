import threading
import time
import tkinter as tk

from app.core.services.restaurant_service import RestaurantService
from app.gui.controller import Controller
from app.gui.pages.restaurants.restaurants_view import RestaurantsView
from app.gui.utils.widgets.full_table_widget import TableWidget


class RestaurantsController(Controller):
    def __init__(self, view: RestaurantsView, app: tk.Tk):
        super().__init__(view, app)
        self.__set_up_table()

        self.__table_update_thread = threading.Thread(target=self.__update_table)
        self.__table_update_thread.start()

    def __get_table_data(self):
        with RestaurantService(self._app.get_session()) as restaurant_service:
            restaurants = restaurant_service.get_all()
            return restaurant_service.expunge_all(restaurants)

    def __set_up_table(self):
        table_data = self.__get_table_data()

        self.__table_wrapper = TableWidget(
            label_text="Restaurants",
            data=table_data,
            callback=self.__view_restaurant,
            master=self._view.table_container,
        )
        self.__table_wrapper.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

    def __update_table(self):
        while not self._app.get_stop_threads().is_set() and self._view.winfo_exists():
            self.__table_wrapper.get_table().set_data(self.__get_table_data())
            time.sleep(10)

    def __view_restaurant(self, restaurant_id):
        with RestaurantService(self._app.get_session()) as restaurant_service:
            restaurant = restaurant_service.get_by_id(restaurant_id)
            restaurant_service.expunge(restaurant)
        self._app.raise_screen(
            self._view,
            "restaurant",
            {"app": self._app, "restaurant": restaurant},
            {"app": self._app, "restaurant": restaurant},
        )
