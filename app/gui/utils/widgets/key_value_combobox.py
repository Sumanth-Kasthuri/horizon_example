"""
Author: Archie Jarvis
Student ID: 20022663
"""


from tkinter import ttk


class KeyValueComboBox(ttk.Combobox):

    """
    data = {
        "1": "value1",
        "2": "value2",
        "3": "value3",
    }
    """

    def __init__(self, master, data, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.__data = data
        self.configure(
            values=list(self.__data.keys()),
        )

    def get_selected_value(self):
        return self.__data[self.get()]
