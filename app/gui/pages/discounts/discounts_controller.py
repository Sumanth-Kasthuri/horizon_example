import threading
import time
import tkinter as tk

from app.core.services.discount_service import DiscountService
from app.gui.controller import Controller
from app.gui.pages.discounts.discounts_view import DiscountsView
from app.gui.utils.widgets.full_table_widget import TableWidget


class DiscountsController(Controller):
    def __init__(self, view: DiscountsView, app):
        super().__init__(view, app)
        self.__set_up_table()

        self.__table_update_thread = threading.Thread(target=self.__update_table)
        self.__table_update_thread.start()

    def __get_table_data(self):
        with DiscountService(self._app.get_session()) as discount_service:
            discounts = discount_service.get_all()
            return discount_service.expunge_all(discounts)

    def __set_up_table(self):
        table_data = self.__get_table_data()

        self.__table_wrapper = TableWidget(
            label_text="Discounts",
            data=table_data,
            callback=self.__view_discount,
            master=self._view.table_container,
            excluded_columns=("id",),
            delete_callback=self.__delete_callback,
        )
        self.__table_wrapper.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

    def __delete_callback(self, discount_id):
        with DiscountService(self._app.get_session()) as discount_service:
            discount = discount_service.get_by_id(discount_id)
            discount_service.delete(discount)
            discount_service.commit()

            self._app.raise_screen(
                self._view,
                "discounts",
                {"app": self._app},
                {"app": self._app},
            )

    def __update_table(self):
        while not self._app.get_stop_threads().is_set() and self._view.winfo_exists():
            self.__table_wrapper.get_table().set_data(self.__get_table_data())
            time.sleep(10)

    def __view_discount(self, discount_id):
        self._app.raise_screen(
            self._view,
            "discount",
            {"app": self._app},
            {"app": self._app, "discount_id": discount_id},
        )
