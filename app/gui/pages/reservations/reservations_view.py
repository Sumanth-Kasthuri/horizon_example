from tkinter import ttk
import tkinter as tk

from app.gui.view import View


class ReservationsView(View):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)

        self.__add_reservation_button = ttk.Button(
            master=self._content_frame,
            text="Add Reservation",
            command=self.__add_reservation_button_callback,
        )
        self.__add_reservation_button.pack(expand=False, side=tk.TOP, fill=tk.X)

        self.table_container = ttk.Frame(master=self._content_frame, padding=10)
        self.table_container.pack(expand=False, side=tk.TOP, fill=tk.X)
        self.back_button.configure(
            command=self.__back_button_callback,
        )

    def __add_reservation_button_callback(self):
        self._app.raise_screen(
            self,
            "reservations_add",
            {"app": self._app},
            {"app": self._app, "restaurant": self._CONTROLLER.get_restaurant()},
        )

    def __back_button_callback(self):
        self._app.raise_screen(
            self,
            "restaurant",
            {"app": self._app, "restaurant": self._CONTROLLER.get_restaurant()},
            {"app": self._app, "restaurant": self._CONTROLLER.get_restaurant()},
        )
