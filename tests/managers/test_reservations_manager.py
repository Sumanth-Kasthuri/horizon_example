"""
Author: Archie Jarvis
Student ID: 20022663
"""

from datetime import datetime

from app.core.managers.reservations_manager import ReservationsManager
from tests.managers.test_manager_base import BaseManagerTestCase


class ReservationsManagerTestCase(BaseManagerTestCase):
    def setUp(self):
        super().setUp()
        self.manager = ReservationsManager(self.app)

    def test_is_table_available(self):
        self.add_restaurant()
        self.add_table()
        self.add_reservation(12)

        dt = datetime.now()
        date = datetime.date(dt)

        self.assertFalse(self.manager.is_table_available(1, date, 12, 4))
        self.assertTrue(self.manager.is_table_available(1, date, 13, 4))

        self.add_reservation(13)

        self.assertFalse(self.manager.is_table_available(1, date, 13, 4))

    def test_get_available_reservations(self):
        self.add_restaurant()
        self.add_table()
        self.add_reservation(12)
        self.add_reservation(13)

        dt = datetime.now()
        date = datetime.date(dt)

        available_reservations = self.manager.get_available_reservations(1, date, 4)

        # Check that there are 22 available slots (10-22, 0.5 hour intervals)
        self.assertEqual(len(available_reservations[1]), 22)

        self.add_reservation(14)

        available_reservations = self.manager.get_available_reservations(1, date, 4)

        # Check that there are 21 available slots (10-22, 0.5 hour intervals)
        self.assertEqual(len(available_reservations[1]), 21)
