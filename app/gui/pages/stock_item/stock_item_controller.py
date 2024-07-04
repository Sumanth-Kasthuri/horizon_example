from tkinter.ttk import Button

from app.core.services.stock_item_service import StockItemService
from app.gui.controller import Controller
from app.gui.utils.widgets.data_entry_widget import DataEntryWidget


class StockItemController(Controller):
    def __init__(self, view, app, stock_item):
        super().__init__(view, app)
        self.__stock_item = stock_item
        self.__set_up_edit_widget()

    def __set_up_edit_widget(self):
        self.__data_entry_widget = DataEntryWidget(
            master=self._view.data_entry_container,
            app=self._app,
            obj=self.__stock_item,
            fields_to_show=["name", "quantity", "re_order_quantity"],
            fields_to_translate={},
            title=f"Edit {self.__stock_item.name}",
        )
        self.__data_entry_widget.pack()

        save_button = Button(
            master=self._view.data_entry_container,
            text="Save",
            command=self.__update_stock_item,
        )

        save_button.pack(pady=10)

    def get_restaurant(self):
        with StockItemService(self._app.get_session()) as service:
            stock_item = service.get_by_id(id=self.__stock_item.id)
            return service.expunge(stock_item.inventory.restaurant)

    def __update_stock_item(self):
        with StockItemService(self._app.get_session()) as service:
            stock_item = service.update(self.__data_entry_widget.get_obj())
            service.commit()
            self._app.get_inventory_manager().on_update_stock_item(stock_item.id)

            self._app.raise_screen(
                self._view,
                "inventory",
                {"app": self._app},
                {
                    "app": self._app,
                    "restaurant": service.expunge(stock_item.inventory.restaurant),
                },
            )
