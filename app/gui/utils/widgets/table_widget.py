"""
Author: Archie Jarvis
Student ID: 20022663
"""

from functools import partial
from tkinter.ttk import Label, Frame, Button


class Table(Frame):
    __table = []
    __headers = []

    def __init__(
            self,
            data,
            callback,
            excluded_columns=("id",),
            callback_with_index=False,
            button_text="View",
            delete_callback=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.__data = data
        self.__callback = callback
        self.__excluded_columns = excluded_columns
        self.__callback_with_index = callback_with_index
        self.__button_text = button_text
        self.__delete_callback = delete_callback
        self.__build()

        if not self.__data:
            self.__table = []
            self.__label = Label(
                self,
                text="No data to display",
                font=("Arial", 12),
            )
            self.__label.place(anchor="center", relx=0.5, rely=0.5)

    def __build(self):
        for items in self.__table:
            for item in items:
                item.destroy()

        self.__table = []
        for i, item in enumerate(self.__data):
            headers = [column.name for column in item.__table__.columns]
            headers = [
                header for header in headers if header not in self.__excluded_columns
            ]
            self.__headers = headers

            if i == 0:
                header_row = [
                    Label(
                        self,
                        text=header.title().replace("_", " "),
                        font=("Arial", 12),
                    )
                    for header in self.__headers
                ]
                self.__table.append(header_row)

            row_labels = [
                Label(
                    self,
                    text=getattr(item, header),
                    font=("Arial", 12),
                )
                for header in self.__headers
            ]

            callback_arg = item.id if not self.__callback_with_index else i

            button = Button(
                self,
                text=self.__button_text,
                command=partial(self.__callback, callback_arg),
            )

            row_labels.append(button)

            if self.__delete_callback:
                delete_button = Button(
                    self,
                    text="Delete",
                    command=partial(self.__delete_callback, callback_arg),
                )
                row_labels.append(delete_button)

            self.__table.append(row_labels)

        for i, row in enumerate(self.__table):
            for j, label in enumerate(row):
                label.grid(row=i, column=j, sticky="nsew")
                self.grid_rowconfigure(i, weight=1)
                self.grid_columnconfigure(j, weight=1)

    def __update(self):
        if not self.__table:
            self.__build()
            return

        if len(self.__table) != len(self.__data) + 1:
            self.__build()
            return

        for i, item in enumerate(self.__data, start=1):
            for j, header in enumerate(self.__headers):
                if self.__table[i][j] is Button:
                    callback_arg = item.id if not self.__callback_with_index else i
                    self.__table[i][j].configure(
                        command=partial(self.__callback, callback_arg)
                    )
                    continue
                self.__table[i][j].configure(text=getattr(item, header))

        for i, row in enumerate(self.__table):
            for j, label in enumerate(row):
                label.grid(row=i, column=j, sticky="nsew")

    def set_data(self, data):
        self.__data = data
        self.__update()
