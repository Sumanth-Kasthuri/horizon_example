import tkinter as tk
from tkinter import ttk

from app.gui.view import View


class InventoryView(View):
    def __init__(self, app):
        super().__init__(app)

        self.__add_stock_item_button = ttk.Button(
            self._content_frame,
            text="Add Stock Item",
            command=self.__add_stock_item,
        )
        self.__add_stock_item_button.pack()

        self.table_container = ttk.Frame(master=self._content_frame, padding=10)
        self.table_container.pack(fill=tk.X)

        self.back_button.configure(
            command=self.__back_button_callback,
        )

    def __add_stock_item(self):
        self._app.raise_screen(
            self,
            "stock_item_add",
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
