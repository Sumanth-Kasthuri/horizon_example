from app.gui.pages.home.home_view import HomeView
import tkinter as tk


class HomeController:
    def __init__(self, view: HomeView, app: tk.Tk):
        self.__view = view
        self.__app = app
