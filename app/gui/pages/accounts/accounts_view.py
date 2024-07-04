import tkinter as tk
from tkinter import ttk

from app.gui.view import View


class AccountsView(View):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)

        self.table_container = ttk.Frame(master=self._content_frame, padding=10)
        self.table_container.pack(expand=False, side=tk.TOP, fill=tk.X)
