"""
DietaryNeed Service

Author: Setenay Baysal
Student ID: 22074682

"""

from app.core.database.models import DietaryRequirement
from app.core.service import Service


class DietaryNeedService(Service):
    def __init__(self, session):
        super().__init__(session, DietaryRequirement)
