import tkinter as tk
from tkinter import ttk

from app.gui.view import View
from app.gui.utils.widgets.entry_with_placeholder_widget import EntryWithPlaceholder


class LoginView(View):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)

        self.left_frame = ttk.Frame(
            self,
            width=self._WINDOW_WIDTH,
            height=self._CONTENT_HEIGHT,
        )
        self.left_frame.pack(expand=True, fill=tk.BOTH)

        login_frame = ttk.Frame(self.left_frame)
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        login_label = ttk.Label(login_frame, text="Login", font=("Arial", 24))
        login_label.pack(padx=10, pady=10)

        username_frame = ttk.Frame(login_frame)
        username_frame.pack(padx=10, pady=10)

        self.username_input = EntryWithPlaceholder(
            username_frame, placeholder="Username", width=20
        )
        self.username_input.pack(side=tk.LEFT)

        password_frame = ttk.Frame(login_frame)
        password_frame.pack(padx=10, pady=10)

        self.password_input = EntryWithPlaceholder(
            password_frame,
            placeholder="Password",
            show="*",
            width=20,
        )
        self.password_input.pack(side=tk.LEFT)

        self.error_label = ttk.Label(login_frame, text="", font=("Arial", 12))
        self.error_label.pack(padx=10, pady=10)

        self.login_button = ttk.Button(login_frame, text="Login", width=20)
        self.login_button.pack(padx=10, pady=10)
