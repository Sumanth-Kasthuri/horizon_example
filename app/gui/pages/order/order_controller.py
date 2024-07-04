import tkinter as tk
from tkinter.ttk import Button

from app.core.database.models import Order, Recipe, Discount
from app.core.services.order_service import OrderService
from app.gui.controller import Controller
from app.gui.pages.order.order_view import OrderView
from app.gui.utils.widgets.data_entry_widget import DataEntryWidget
from app.gui.utils.widgets.select_multiple_widget import SelectMultipleWidget


class OrderController(Controller):
    def __init__(self, view: OrderView, order_id: Order, app: tk.Tk):
        super().__init__(view, app)
        self.__order_id = order_id
        self.__set_up_edit_widget()

    def __set_up_edit_widget(self):
        with OrderService(self._app.get_session()) as service:
            self.__restaurant = service.expunge(
                service.get_by_id(self.__order_id).restaurant
            )

            self.__order = service.get_by_id(self.__order_id)
            self.__data_entry_widget = DataEntryWidget(
                master=self._view.data_entry_container,
                app=self._app,
                obj=service.expunge(self.__order),
                fields_to_show=["ready"],
                fields_to_translate={
                    "discount_id": {
                        "obj_type": Discount,
                        "field_to_display": "name",
                        "display_as": "Discount",
                    }
                },
                title=f"Edit Order",
            )
            self.__data_entry_widget.pack()

            self.__select_multiple_widget = SelectMultipleWidget(
                master=self._view.data_entry_container,
                model=Recipe,
                app=self._app,
            )

            save_button = Button(
                master=self._view.data_entry_container,
                text="Save",
                command=self.__update_order,
            )
            save_button.pack(pady=10)

    def __update_order(self):
        with OrderService(self._app.get_session()) as service:
            self._app.get_order_manager().on_update_order(self.__order_id)

            order = self.__data_entry_widget.get_obj()
            order.ready = bool(order.ready)

            service.update(order)

            self._app.raise_screen(
                self._view,
                "orders",
                {"app": self._app},
                {"app": self._app, "restaurant": self.__restaurant},
            )
