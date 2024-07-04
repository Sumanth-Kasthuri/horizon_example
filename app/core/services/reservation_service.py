"""
Reservation Service

Author: Setenay Baysal
Student ID: 22074682

"""

from app.core.database.models import Reservation
from app.core.service import Service


class ReservationService(Service):
    def __init__(self, session):
        super().__init__(session, Reservation)

    def get_reservation_by_name(self, reservation_name: str) -> Reservation:
        return self._session.query(Reservation).filter_by(name=reservation_name).first()

    def get_reservations_by_date(self, reservation_date) -> Reservation:
        return self._session.query(Reservation).filter_by(date=reservation_date).all()

    def get_reservations_by_end_time(self, reservation_end_time) -> Reservation:
        return (
            self._session.query(Reservation)
            .filter_by(end_time=reservation_end_time)
            .all()
        )

    def get_reservations_by_start_time(self, reservation_start_time) -> Reservation:
        return (
            self._session.query(Reservation)
            .filter_by(start_time=reservation_start_time)
            .all()
        )

    def get_reservations_by_total_guests(
        self, reservation_total_guests: int
    ) -> Reservation:
        return (
            self._session.query(Reservation)
            .filter_by(total_guests=reservation_total_guests)
            .all()
        )

    def get_by_restaurant_id(self, restaurant_id) -> list[Reservation]:
        return (
            self._session.query(Reservation)
            .filter_by(restaurant_id=restaurant_id)
            .all()
        )
