from tkinter.ttk import Button

from app.core.database.models import StockItem
from app.core.services.restaurant_service import RestaurantService
from app.gui.controller import Controller
from app.gui.utils.widgets.data_entry_widget import DataEntryWidget


class StockItemAddController(Controller):
    def __init__(self, view, app, restaurant):
        super().__init__(view, app)
        self.__restaurant = restaurant
        self.__set_up_edit_widget()

    def __set_up_edit_widget(self):
        self.__data_entry_widget = DataEntryWidget(
            master=self._view.data_entry_container,
            app=self._app,
            obj=StockItem(None, None, None, None, None),
            fields_to_show=["name", "quantity", "re_order_quantity"],
            fields_to_translate={},
            title=f"Add Stock Item",
        )
        self.__data_entry_widget.pack()

        save_button = Button(
            master=self._view.data_entry_container,
            text="Save",
            command=self.__add_stock_item,
        )

        save_button.pack(pady=10)

    def __add_stock_item(self):
        with RestaurantService(self._app.get_session()) as restaurant_service:
            restaurant = restaurant_service.get_by_id(id=self.__restaurant.id)

            stock_item = self.__data_entry_widget.get_obj()

            stock_item.inventory_id = restaurant.inventory.id

            restaurant_service.add(stock_item)
            restaurant_service.commit()
            self._app.get_inventory_manager().on_update_stock_item(stock_item.id)

            self._app.raise_screen(
                self._view,
                "inventory",
                {"app": self._app},
                {
                    "app": self._app,
                    "restaurant": self.__restaurant,
                },
            )

    def get_restaurant(self):
        return self.__restaurant
