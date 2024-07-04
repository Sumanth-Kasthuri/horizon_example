from tkinter.ttk import Button

from app.core.database.models import Restaurant
from app.core.services.restaurant_service import RestaurantService
from app.gui.controller import Controller
from app.gui.utils.widgets.data_entry_widget import DataEntryWidget


class RestaurantAddController(Controller):
    def __init__(self, view, app):
        super().__init__(view, app)
        self.__set_up_edit_widget()

    def __set_up_edit_widget(self):
        self.__data_entry_widget = DataEntryWidget(
            master=self._view.data_entry_container,
            app=self._app,
            obj=Restaurant(None, None, None),
            fields_to_show=["name", "city", "capacity"],
            fields_to_translate={},
            title=f"Add Restaurant",
        )
        self.__data_entry_widget.pack()

        save_button = Button(
            master=self._view.data_entry_container,
            text="Save",
            command=self.__add_restaurant,
        )

        save_button.pack(pady=10)

    def __add_restaurant(self):
        with RestaurantService(self._app.get_session()) as restaurant_service:
            restaurant = self.__data_entry_widget.get_obj()

            restaurant_service.add(restaurant)
            restaurant_service.commit()

            self._app.raise_screen(
                self._view,
                "restaurants",
                {"app": self._app},
                {"app": self._app},
            )