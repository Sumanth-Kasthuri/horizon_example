"""
Author: Archie Jarvis
Student ID: 20022663
"""

from app.gui.view import View


class Controller:
    def __init__(self, view: View, app):
        self._view = view
        self._app = app
        self._view.set_controller(self)
