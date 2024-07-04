import tkinter as tk
from tkinter import ttk

from app.gui.view import View


class RestaurantsView(View):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)

        self.add_restaurant_button = ttk.Button(
            master=self._content_frame,
            text="Add Restaurant",
            command=self.__add_restaurant_button_callback,
        )
        self.add_restaurant_button.pack(expand=False, side=tk.TOP, fill=tk.X)

        self.table_container = ttk.Frame(master=self._content_frame, padding=10)
        self.table_container.pack(expand=False, side=tk.TOP, fill=tk.X)
        self.back_button.configure(
            command=self.__back_button_callback,
        )

    def __add_restaurant_button_callback(self):
        self._app.raise_screen(
            self,
            "restaurant_add",
            {"app": self._app},
            {"app": self._app},
        )

    def __back_button_callback(self):
        self._app.raise_screen(self, "home", {"app": self._app}, {"app": self._app})
