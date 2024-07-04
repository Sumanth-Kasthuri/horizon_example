"""
Inventory Service

Author: Setenay Baysal
Student ID: 22074682

"""

from app.core.database.models import Inventory
from app.core.service import Service


class InventoryService(Service):
    def __init__(self, session):
        super().__init__(session, Inventory)
