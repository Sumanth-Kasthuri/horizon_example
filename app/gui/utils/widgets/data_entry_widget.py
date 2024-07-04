"""
Author: Archie Jarvis
Student ID: 20022663
"""

from tkinter.ttk import Frame, Label, Entry

from app.core.service import Service
from app.gui.utils.widgets.key_value_combobox import KeyValueComboBox


class DataEntryWidget(Frame):
    """
    Fields to show: dict of field names, displayed as plain text
    fields_to_translate: dict of field names, displayed as comboboxes with the options instead of id values
    e.g.: fields_to_show = {
        "restaurant_id": {
            "obj_type": Restaurant,
            "field_to_display": "name",
            "display_as": "Restaurant
        }
    }
    """

    def __init__(
        self,
        app,
        title,
        obj,
        fields_to_show: list,
        fields_to_translate: dict,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.__app = app
        self.__title = title
        self.__obj = obj
        self.__fields_to_show = fields_to_show
        self.__fields_to_translate = fields_to_translate

        self.__create_widgets()

    def __create_widgets(self):
        self.__title_label = Label(
            self,
            text=self.__title,
            font=("Arial", 18),
        )
        self.__title_label.grid(row=0, column=0, columnspan=2, pady=10)

        for i, field in enumerate(self.__fields_to_show):
            row = i + 1
            value = getattr(self.__obj, field)

            label = Label(self, text=f"{field}:")
            label.grid(row=row, column=0, sticky="w")

            entry = Entry(self)

            entry.insert(0, value or "")
            entry.bind(
                "<KeyRelease>", lambda event, f=field: self.on_entry_change(f, event)
            )
            entry.grid(row=row, column=1, sticky="e")

            if not self.__app.get_accounts_manager().is_user_admin():
                entry.configure(state="disabled")

        for i, field in enumerate(self.__fields_to_translate):
            row = i + len(self.__fields_to_show) + 1
            display_as = self.__fields_to_translate[field]["display_as"]

            get_by = self.__fields_to_translate[field].get("get_by", "all")
            get_by_value = self.__fields_to_translate[field].get("get_by_value", None)

            label = Label(self, text=f"{display_as}:")
            label.grid(row=row, column=0, sticky="w")

            data = self.__get_combo_box_values(field, get_by, get_by_value)
            combo_box = KeyValueComboBox(
                self,
                data=data,
            )
            combo_box.bind(
                "<<ComboboxSelected>>",
                lambda event, f=field: self.on_combo_change(f, event),
            )
            combo_box.grid(row=row, column=1, sticky="e")

            if not self.__app.get_accounts_manager().is_user_admin():
                combo_box.configure(state="disabled")

    def __get_combo_box_values(self, field, get_by, get_by_value):
        obj_type = self.__fields_to_translate[field]["obj_type"]
        field_to_display = self.__fields_to_translate[field]["field_to_display"]

        with Service(self.__app.get_session(), obj_type) as service:
            if get_by != "all":
                objs = service.get_by(get_by, get_by_value)
                return {
                    str(getattr(obj, field_to_display)): getattr(obj, "id")
                    for obj in objs
                }

            objs = service.get_all()
            return {getattr(obj, field_to_display): getattr(obj, "id") for obj in objs}

    def on_entry_change(self, field, event):
        widget = event.widget
        value = widget.get()

        setattr(self.__obj, field, value)

    def on_combo_change(self, field, event):
        widget = event.widget
        value = widget.get_selected_value()

        setattr(self.__obj, field, value)

    def get_obj(self):
        return self.__obj
