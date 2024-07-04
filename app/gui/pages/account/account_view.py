"""
Author: Archie Jarvis
Student ID: 20022663
"""

from app.gui.utils.widgets.container_widget import Container
from app.gui.view import View


class AccountView(View):
    def __init__(self, app, account, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.__account = account

        self.data_entry_container = Container(
            master=self._content_frame,
            padding=10,
        )
        self.data_entry_container.place(relx=0, rely=0)

        self.back_button.configure(command=self.__back_button_callback)
