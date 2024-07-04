"""
Payment Service

Author: Setenay Baysal
Student ID: 22074682

"""

from app.core.database.models import Payment
from app.core.service import Service


class PaymentService(Service):
    def __init__(self, session):
        super().__init__(session, Payment)

    def get_payments_by_amount(self, payment_amount: float) -> Payment:
        return self._session.query(Payment).filter_by(amount=payment_amount).all()

    def get_payments_by_date(self, payment_date) -> list[Payment]:
        return self._session.query(Payment).filter_by(date=payment_date).all()
