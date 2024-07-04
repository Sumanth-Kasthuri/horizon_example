import tkinter as tk
from tkinter import ttk

from app.gui.view import View


class DiscountsView(View):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)

        self.__add_discount_button = ttk.Button(
            self._content_frame,
            text="Add Discount",
            command=self.__add_discount,
        )
        self.__add_discount_button.pack()

        self.table_container = ttk.Frame(master=self._content_frame, padding=10)
        self.table_container.pack(expand=False, side=tk.TOP, fill=tk.X)

        self.back_button.configure(command=self.__back_button_callback)

    def __add_discount(self):
        self._app.raise_screen(
            self,
            "discount_add",
            {"app": self._app},
            {"app": self._app},
        )

    def __back_button_callback(self):
        self._app.raise_screen(
            self,
            "restaurants",
            {"app": self._app},
            {"app": self._app},
        )

