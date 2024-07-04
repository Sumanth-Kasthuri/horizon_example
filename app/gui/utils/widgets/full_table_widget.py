"""
Author: Archie Jarvis
Student ID: 20022663
"""
from tkinter import BOTH
from tkinter.ttk import Label, Frame

from app.gui.utils.widgets.table_widget import Table


class TableWidget(Frame):
    def __init__(
        self, label_text, data, callback, excluded_columns=("id",), delete_callback=None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.__label_text = label_text
        self.__data = data
        self.__excluded_columns = excluded_columns
        self.__callback = callback
        self.__delete_callback = delete_callback
        self.__build()

        self.configure(borderwidth=2, relief="groove", padding=10)

    def __build(self):
        self.__table_label = Label(
            self,
            text=self.__label_text,
            font=("Arial", 18),
        )

        self.__table_label.pack(fill=BOTH, expand=False)

        self.__table = Table(
            self.__data,
            master=self,
            padding=10,
            callback=self.__callback,
            excluded_columns=self.__excluded_columns,
            delete_callback=self.__delete_callback
        )

        self.__table.pack(fill=BOTH, expand=True)

    def get_table(self):
        return self.__table
