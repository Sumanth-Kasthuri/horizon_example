"""
User Service

Author: Archie Jarvis
Student ID: 20022663
"""

from app.core.service import Service
from app.core.database.models import Account


class AccountService(Service):
    def __init__(self, session):
        super().__init__(session, Account)

    def get_account_by_username(self, account_username: str, options=None) -> Account:
        query = self._session.query(Account).filter_by(username=account_username)
        if options:
            query = query.options(*options)
        return query.first()
