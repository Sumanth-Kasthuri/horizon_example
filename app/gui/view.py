"""
Author: Archie Jarvis
Student ID: 20022663
"""

import os
import tkinter as tk
from functools import partial
from tkinter import ttk


class View(ttk.Frame):
    # Sizing properties
    _WINDOW_WIDTH = 1280
    _WINDOW_HEIGHT = 720
    _HEADER_HEIGHT = 100
    _CONTENT_HEIGHT = _WINDOW_HEIGHT - _HEADER_HEIGHT

    # Resource paths
    _CURRENT_FILE_PATH = os.path.abspath(__file__)
    _RESOURCES_PATH = os.path.join(
        os.path.sep, os.path.dirname(_CURRENT_FILE_PATH), "..", "resources"
    )

    _CONTROLLER = None

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._app = app
        self.__build()

    def __build(self):
        self.header_frame = ttk.Frame(self)
        self.header_frame.pack(side="top", fill="x")
        self.header_frame.configure(height=self._HEADER_HEIGHT)

        self.border_frame = ttk.Frame(self.header_frame, height=2)
        self.border_frame.pack(side="bottom", fill="x")

        self.header_label = ttk.Label(
            self.header_frame,
            text="Horizon Restaurants",
            font=("Arial", 18),
            anchor="w",
        )

        self.header_label.pack(side="left", fill=tk.NONE, pady=10, padx=10)

        if self._app.get_accounts_manager().is_logged_in():
            self.back_button = ttk.Button(
                self.header_frame,
                text="Back",
                command=self.__back_button_callback,
            )

            self.back_button.pack(side="left", fill=tk.NONE, pady=10, padx=10)

            if self._app.get_accounts_manager().is_user_admin():
                self.admin_button = ttk.Button(
                    self.header_frame,
                    text="Manage Accounts",
                    command=partial(
                        self._app.raise_screen,
                        self,
                        "accounts",
                        {"app": self._app},
                        {"app": self._app},
                    ),
                )

                self.admin_button.pack(side="left", fill=tk.NONE, pady=10, padx=10)

                self.discounts_button = ttk.Button(
                    self.header_frame,
                    text="Manage Discounts",
                    command=partial(
                        self._app.raise_screen,
                        self,
                        "discounts",
                        {"app": self._app},
                        {"app": self._app},
                    ),
                )

                self.discounts_button.pack(side="left", fill=tk.NONE, pady=10, padx=10)

            self.logout_button = ttk.Button(
                self.header_frame,
                text="Logout",
                command=partial(self._app.get_accounts_manager().logout_user, self),
            )

            self.logout_button.pack(side="right", fill=tk.NONE, pady=10, padx=10)

        self._content_frame = ttk.Frame(self)
        self._content_frame.pack(expand=True, fill=tk.BOTH)

    def set_controller(self, controller):
        self._CONTROLLER = controller

    def __back_button_callback(self):
        self._app.raise_screen(
            self,
            "restaurants",
            {"app": self._app},
            {"app": self._app},
        )
