"""
Roles Service

Author: Setenay Baysal
Student ID: 22074682

"""

from app.core.database.models import Role
from app.core.service import Service


class RoleService(Service):
    def __init__(self, session):
        super().__init__(session, Role)

    def get_role_by_name(self, role_name: str) -> Role:
        return self._session.query(Role).filter_by(name=role_name).first()
