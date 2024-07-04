import datetime
from tkinter.ttk import Button

from app.core.database.models import Discount
from app.core.services.discount_service import DiscountService
from app.gui.controller import Controller
from app.gui.utils.widgets.data_entry_widget import DataEntryWidget


class DiscountAddController(Controller):
    def __init__(self, view, app):
        super().__init__(view, app)
        self.__set_up_edit_widget()

    def __set_up_edit_widget(self):
        self.__data_entry_widget = DataEntryWidget(
            master=self._view.data_entry_container,
            app=self._app,
            obj=Discount(None, None, None, None),
            fields_to_show=["name", "start_date", "end_date", "discount_multiplier"],
            fields_to_translate={},
            title=f"Add Discount",
        )
        self.__data_entry_widget.pack()

        save_button = Button(
            master=self._view.data_entry_container,
            text="Save",
            command=self.__add_discount,
        )

        save_button.pack(pady=10)

    def __add_discount(self):
        with DiscountService(self._app.get_session()) as discount_service:

            discount = self.__data_entry_widget.get_obj()
            discount.start_date = self._get_date(discount.start_date)
            discount.end_date = self._get_date(discount.end_date)
            discount_service.add(discount)

            self._app.raise_screen(
                self._view,
                "discounts",
                {"app": self._app},
                {
                    "app": self._app,
                },
            )

    def _get_date(self, date_str):
        return datetime.datetime.strptime(date_str, "%d/%m/%Y").date()




