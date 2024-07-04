"""
Author: Archie Jarvis
Student ID: 20022663
"""

from tkinter import ttk
import tkinter as tk


class ImageFrame(ttk.Frame):
    def __init__(self, image_path, master, **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)

        self.image = tk.PhotoImage(file=image_path)
        self.label = ttk.Label(self, image=self.image)
        self.label.pack(expand=True, fill=tk.BOTH)
