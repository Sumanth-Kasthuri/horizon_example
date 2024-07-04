from app.gui.utils.widgets.container_widget import Container
from app.gui.view import View


class StockItemView(View):
    def __init__(self, app, stock_item, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.__stock_item = stock_item
        self.__build()

        self.back_button.configure(command=self.__back_button_callback)

    def __build(self):
        self.data_entry_container = Container(
            master=self._content_frame,
            padding=10,
        )
        self.data_entry_container.place(relx=0, rely=0)

    def __back_button_callback(self):
        self._app.raise_screen(
            self,
            "inventory",
            {"app": self._app},
            {"app": self._app, "restaurant": self._CONTROLLER.get_restaurant()},
        )
