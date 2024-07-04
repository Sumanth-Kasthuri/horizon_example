from tkinter import ttk

from app.gui.utils.widgets.container_widget import Container
from app.gui.view import View


class RestaurantView(View):
    def __init__(self, app, restaurant, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.__restaurant = restaurant
        self.__build()

    def __build(self):
        self.data_entry_container = Container(
            master=self._content_frame,
            padding=10,
        )
        self.data_entry_container.place(relx=0, rely=0)

        self.__view_inventory_button = ttk.Button(
            self._content_frame,
            text="View Inventory",
            command=self.__view_inventory,
        )
        self.__view_inventory_button.pack()

        self.__view_orders_button = ttk.Button(
            self._content_frame,
            text="View Orders",
            command=self.__view_orders,
        )
        self.__view_orders_button.pack()

        self.__view_reservations_button = ttk.Button(
            self._content_frame,
            text="View Reservations",
            command=self.__view_reservations,
        )
        self.__view_reservations_button.pack()

    def __view_orders(self):
        self._app.raise_screen(
            self,
            "orders",
            {"app": self._app},
            {"restaurant": self.__restaurant, "app": self._app},
        )

    def __view_inventory(self):
        self._app.raise_screen(
            self,
            "inventory",
            {"app": self._app},
            {"restaurant": self.__restaurant, "app": self._app},
        )

    def __view_reservations(self):
        self._app.raise_screen(
            self,
            "reservations",
            {"app": self._app},
            {"restaurant": self.__restaurant, "app": self._app},
        )

    def _back_button_callback(self):
        self._app.raise_screen(
            self,
            "restaurants",
            {"app": self._app},
            {"app": self._app},
        )
