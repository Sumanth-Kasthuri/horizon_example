import tkinter as tk
from tkinter.ttk import Button

from app.core.database.models import Account, Role, Restaurant
from app.core.services.account_service import AccountService
from app.gui.controller import Controller
from app.gui.pages.account.account_view import AccountView
from app.gui.utils.widgets.data_entry_widget import DataEntryWidget


class AccountController(Controller):
    def __init__(self, view: AccountView, account: Account, app: tk.Tk):
        super().__init__(view, app)
        self.__account = account
        self.__set_up_edit_widget()

    def __set_up_edit_widget(self):
        self.__data_entry_widget = DataEntryWidget(
            master=self._view.data_entry_container,
            app=self._app,
            obj=self.__account,
            fields_to_show=["username", "password"],
            fields_to_translate={
                "role": {
                    "obj_type": Role,
                    "field_to_display": "name",
                    "display_as": "Role",
                },
                "restaurant_id": {
                    "obj_type": Restaurant,
                    "field_to_display": "name",
                    "display_as": "Restaurant",
                },
            },
            title=f"Edit {self.__account.username}",
        )
        self.__data_entry_widget.pack()

        save_button = Button(
            master=self._view.data_entry_container,
            text="Save",
            command=self.__update_account,
        )
        save_button.pack(pady=10)

    def __update_account(self):
        with AccountService(self._app.get_session()) as service:
            account = self.__data_entry_widget.get_obj()
            account.password = self._app.get_accounts_manager().hash_password_with_salt(
                account.username, account.password
            )
            service.update(account)
            self._app.raise_screen(
                self._view,
                "accounts",
                {"app": self._app},
                {"app": self._app},
            )
