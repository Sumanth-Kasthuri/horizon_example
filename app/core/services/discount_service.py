"""
Discount Service

Author: Setenay Baysal
Student ID: 22074682

"""

from app.core.database.models import Discount
from app.core.service import Service


class DiscountService(Service):
    def __init__(self, session):
        super().__init__(session, Discount)

    def get_discount_by_name(self, discount_name: str) -> Discount:
        return self._session.query(Discount).filter_by(name=discount_name).first()

    def get_discounts_by_start_date(self, discount_start_date) -> Discount:
        return (
            self._session.query(Discount)
            .filter_by(start_date=discount_start_date)
            .all()
        )

    def get_discounts_by_end_date(self, discount_end_date) -> Discount:
        return self._session.query(Discount).filter_by(end_date=discount_end_date).all()
