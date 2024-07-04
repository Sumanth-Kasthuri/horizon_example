from tkinter.ttk import Button

from app.core.database.models import Order, Recipe, Restaurant, Table, OrderRecipe
from app.core.service import Service
from app.gui.controller import Controller
from app.gui.utils.widgets.data_entry_widget import DataEntryWidget
from app.gui.utils.widgets.select_multiple_widget import SelectMultipleWidget


class OrderAddController(Controller):
    def __init__(self, view, restaurant, app):
        super().__init__(view, app)
        self.__restaurant = restaurant
        self.__set_up_edit_widget()

    def __set_up_edit_widget(self):
        self.__data_entry_widget = DataEntryWidget(
            master=self._view.data_entry_container,
            app=self._app,
            obj=Order(None, None, []),
            fields_to_show=[],
            fields_to_translate={
                "restaurant_id": {
                    "obj_type": Restaurant,
                    "field_to_display": "name",
                    "display_as": "Restaurant",
                },
                "table_id": {
                    "obj_type": Table,
                    "field_to_display": "id",
                    "display_as": "Table",
                    "get_by": "restaurant_id",
                    "get_by_value": self.__restaurant.id,
                },
            },
            title=f"Add Order",
        )
        self.__data_entry_widget.pack()

        self.__select_multiple_widget = SelectMultipleWidget(
            master=self._view.data_entry_container,
            model=Recipe,
            app=self._app,
        )
        self.__select_multiple_widget.pack()

        save_button = Button(
            master=self._view.data_entry_container,
            text="Save",
            command=self.__add_order,
        )

        save_button.pack(pady=10)

    def __add_order(self):
        order = self.__data_entry_widget.get_obj()
        recipes = self.__select_multiple_widget.get_items()

        recipes_set = {}
        # recipes could contain multiple of the same type, turn it into recipe and quantity
        for recipe in recipes:
            if recipe.id not in recipes_set:
                recipes_set[recipe.id] = 1
            else:
                recipes_set[recipe.id] += 1

        order.ready = bool(order.ready)

        order_id = self._app.get_order_manager().place_order(order)

        with Service(self._app.get_session(), OrderRecipe) as service:
            for k, v in recipes_set.items():
                service.add(OrderRecipe(order_id, k, v))

        self._app.raise_screen(
            self._view,
            "orders",
            {"app": self._app},
            {"app": self._app, "restaurant": self.__restaurant},
        )

    def get_restaurant(self):
        return self.__restaurant
