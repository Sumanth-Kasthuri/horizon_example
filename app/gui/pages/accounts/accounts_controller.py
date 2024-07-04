import threading
import time
import tkinter as tk

from app.core.services.account_service import AccountService
from app.gui.controller import Controller
from app.gui.pages.accounts.accounts_view import AccountsView
from app.gui.utils.widgets.full_table_widget import TableWidget


class AccountsController(Controller):
    def __init__(self, view: AccountsView, app):
        super().__init__(view, app)
        self.__set_up_table()

        self.__table_update_thread = threading.Thread(target=self.__update_table)
        self.__table_update_thread.start()

    def __get_table_data(self):
        with AccountService(self._app.get_session()) as account_service:
            accounts = account_service.get_all()
            return account_service.expunge_all(accounts)

    def __set_up_table(self):
        table_data = self.__get_table_data()

        self.__table_wrapper = TableWidget(
            label_text="Accounts",
            data=table_data,
            callback=self.__view_account,
            master=self._view.table_container,
            excluded_columns=("id", "password", "salt"),
        )
        self.__table_wrapper.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

    def __update_table(self):
        while not self._app.get_stop_threads().is_set() and self._view.winfo_exists():
            self.__table_wrapper.get_table().set_data(self.__get_table_data())
            time.sleep(10)

    def __view_account(self, account_id):
        with AccountService(self._app.get_session()) as account_service:
            account = account_service.get_by_id(account_id)
            account = account_service.expunge(account)
            self._app.raise_screen(
                self._view,
                "account",
                {"app": self._app, "account": account},
                {"app": self._app, "account": account},
            )
