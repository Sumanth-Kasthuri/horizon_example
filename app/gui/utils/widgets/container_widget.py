"""
Author: Archie Jarvis
Student ID: 20022663
"""

from tkinter.ttk import Frame


class Container(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configure(borderwidth=2, relief="groove", padding=10)
