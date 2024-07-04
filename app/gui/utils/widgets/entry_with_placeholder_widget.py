from tkinter.ttk import Entry
from tkinter import END

"""
Custom entry widget with placeholder text.

Author: Archie Jarvis
Student ID: 20022663
"""


class EntryWithPlaceholder(Entry):
    old_show = ""

    def __init__(self, master=None, placeholder="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.placeholder = placeholder
        self.placeholder_colour = "grey"
        self.default_fg_colour = "black"

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.old_show = self["show"]
        self["show"] = ""

        self.insert(0, self.placeholder)
        self["foreground"] = self.placeholder_colour

    def foc_in(self, *args):
        if self.get() == self.placeholder and self["show"] != "*":
            self.delete(0, END)
            self["show"] = self.old_show
            self["foreground"] = self.default_fg_colour

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()
