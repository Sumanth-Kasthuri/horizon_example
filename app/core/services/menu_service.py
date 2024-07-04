"""
Menu Service

Author: Setenay Baysal
Student ID: 22074682

"""

from app.core.database.models import Menu
from app.core.service import Service


class MenuService(Service):
    def __init__(self, session):
        super().__init__(session, Menu)

    def get_menu_by_name(self, menu_name: str) -> Menu:
        return self._session.query(Menu).filter_by(name=menu_name).first()
