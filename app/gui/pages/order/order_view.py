from app.gui.utils.widgets.container_widget import Container
from app.gui.view import View


class OrderView(View):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)

        self.data_entry_container = Container(
            master=self._content_frame,
            padding=10,
        )
        self.data_entry_container.place(relx=0, rely=0)
