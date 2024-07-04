"""
Author: Archie Jarvis
Student ID: 20022663
"""

from tkinter import ttk
import tkinter as tk

from app.core.service import Service
from app.gui.utils.widgets.key_value_combobox import KeyValueComboBox
from app.gui.utils.widgets.table_widget import Table


class SelectMultipleWidget(ttk.Frame):
    def __init__(self, master, app, model, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.__model = model
        self.__app = app
        self.__selected_items = []

        self.__create_widgets()

    def __get_possible_items(self):
        with Service(self.__app.get_session(), self.__model) as service:
            return {item.name: item.id for item in service.get_all()}

    def __create_widgets(self):
        cols = [col.name for col in self.__model.__table__.columns]
        cols.remove("name")

        self.key_value_combobox = KeyValueComboBox(
            master=self,
            data=self.__get_possible_items(),
        )

        self.key_value_combobox.pack()

        self.__add_button = ttk.Button(
            master=self,
            text="Add",
            command=lambda: self.__add_item(
                self.key_value_combobox.get_selected_value()
            ),
        )

        self.__add_button.pack()

        self.__table = Table(
            master=self,
            data=self.__selected_items,
            excluded_columns=cols,
            callback=self.__remove_selected_item,
            callback_with_index=True,
            button_text="Remove",
        )

        self.__table.pack(fill=tk.BOTH, expand=True, side=tk.BOTTOM)

    def __add_item(self, item_id):
        with Service(self.__app.get_session(), self.__model) as service:
            item = service.get_by_id(item_id)
            item = service.expunge(item)

        self.__selected_items.append(item)
        self.__table.set_data(self.__selected_items)

    def get_items(self):
        return self.__selected_items

    def __remove_selected_item(self, index):
        self.__selected_items.pop(index)
        self.__table.set_data(self.__selected_items)

    def set_selected_items(self, items):
        self.__selected_items = items
        self.__table.set_data(self.__selected_items)
