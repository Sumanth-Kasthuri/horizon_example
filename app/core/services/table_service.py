"""
Table Service

Author: Setenay Baysal
Student ID: 22074682

"""
from app.core.database.models import Table
from app.core.service import Service


class TableService(Service):
    def __init__(self, session):
        super().__init__(session, Table)

    def get_tables_by_capacity(self, table_capacity: int) -> Table:
        return self._session.query(Table).filter_by(capacity=table_capacity).all()
