from tkinter.ttk import Button

from app.core.services.discount_service import DiscountService
from app.gui.controller import Controller
from app.gui.utils.widgets.data_entry_widget import DataEntryWidget


class DiscountController(Controller):
    def __init__(self, view, app, discount_id):
        super().__init__(view, app)
        self.__discount_id = discount_id
        self.__set_up_edit_widget()

    def __set_up_edit_widget(self):
        with DiscountService(self._app.get_session()) as service:
            self.__discount = service.get_by_id(self.__discount_id)

            self.__data_entry_widget = DataEntryWidget(
                master=self._view.data_entry_container,
                app=self._app,
                obj=self.__discount,
                fields_to_show=["name", "start_date", "end_date", "discount_multiplier"],
                fields_to_translate={},
                title=f"Edit {self.__discount.name}",
            )
            self.__data_entry_widget.pack()

            save_button = Button(
                master=self._view.data_entry_container,
                text="Save",
                command=self.__update_discount,
            )

            save_button.pack(pady=10)

    def __update_discount(self):
        with DiscountService(self._app.get_session()) as service:
            service.update(self.__data_entry_widget.get_obj())

            self._app.raise_screen(
                self._view,
                "discounts",
                {"app": self._app},
                {"app": self._app},
            )