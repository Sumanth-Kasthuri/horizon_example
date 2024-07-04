import tkinter as tk
from tkinter import ttk

from app.gui.view import View


class OrdersView(View):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)

        self.__add_order_button = ttk.Button(
            self._content_frame,
            text="Add Order",
            command=self.__add_order,
        )
        self.__add_order_button.pack()

        self.table_container = ttk.Frame(master=self._content_frame, padding=10)
        self.table_container.pack(expand=False, side=tk.TOP, fill=tk.X)
        self.back_button.configure(
            command=self.__back_button_callback,
        )

    def __add_order(self):
        self._app.raise_screen(
            self,
            "order_add",
            {"app": self._app},
            {"restaurant": self._CONTROLLER.get_restaurant(), "app": self._app},
        )

    def __back_button_callback(self):
        self._app.raise_screen(
            self,
            "restaurant",
            {"app": self._app, "restaurant": self._CONTROLLER.get_restaurant()},
            {"app": self._app, "restaurant": self._CONTROLLER.get_restaurant()},
        )
