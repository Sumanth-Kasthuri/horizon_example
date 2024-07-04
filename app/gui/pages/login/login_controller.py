import tkinter as tk

from app.gui.pages.login.login_view import LoginView


class LoginController:
    def __init__(self, view: LoginView, app: tk.Tk):
        self.__accounts_manager = app.get_accounts_manager()
        self.__view = view
        self.__app = app
        self.__view.login_button.configure(command=self.login)

    def login(self):
        username = self.__view.username_input.get()
        password = self.__view.password_input.get()

        if self.__accounts_manager.login_user(username, password):
            self.__app.raise_screen(
                self.__view, "restaurants", {"app": self.__app}, {"app": self.__app}
            )
            return
        else:
            # TODO: Add lockout after 3 failed attempts
            self.__view.password_input.delete(0, tk.END)
            self.__view.error_label.configure(text="Invalid username or password")
