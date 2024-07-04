"""
Author: Archie Jarvis
Student ID: 20022663
"""

from app.core.database.models import Restaurant
from app.core.service import Service
from tests.services.test_services_base import BaseServiceTestCase


class ServiceTestCase(BaseServiceTestCase):
    def setUp(self):
        super().setUp()

    def test_get_all(self):
        with Service(self.session, Restaurant) as service:
            self.assertEqual(0, len(service.get_all()))

            service.add(
                Restaurant(name="Test Restaurant", city="Test Location", capacity=100)
            )

            self.session.flush()

            self.assertEqual(1, len(service.get_all()))

    def test_get_by_id(self):
        with Service(self.session, Restaurant) as service:
            restaurant = Restaurant(
                name="Test Restaurant", city="Test Location", capacity=100
            )
            service.add(restaurant)

            self.session.flush()

            self.assertEqual(restaurant, service.get_by_id(restaurant.id))

    def test_add(self):
        with Service(self.session, Restaurant) as service:
            restaurant = Restaurant(
                name="Test Restaurant", city="Test Location", capacity=100
            )
            service.add(restaurant)

            self.session.flush()

            self.assertEqual(restaurant, service.get_by_id(restaurant.id))

    def test_update(self):
        with Service(self.session, Restaurant) as service:
            restaurant = Restaurant(
                name="Test Restaurant", city="Test Location", capacity=100
            )
            service.add(restaurant)

            self.session.flush()

            restaurant.name = "New Name"
            service.update(restaurant)

            self.session.flush()

            self.assertEqual(restaurant, service.get_by_id(restaurant.id))

    def test_delete(self):
        with Service(self.session, Restaurant) as service:
            restaurant = Restaurant(
                name="Test Restaurant", city="Test Location", capacity=100
            )
            service.add(restaurant)

            self.session.flush()

            service.delete(restaurant)

            self.session.flush()

            self.assertIsNone(service.get_by_id(restaurant.id))

    def test_get_by(self):
        with Service(self.session, Restaurant) as service:
            restaurant = Restaurant(
                name="Test Restaurant", city="Test Location", capacity=100
            )
            service.add(restaurant)

            self.session.flush()

            self.assertEqual(restaurant, service.get_by("name", "Test Restaurant")[0])
            self.assertEqual(restaurant, service.get_by("city", "Test Location")[0])
            self.assertEqual(restaurant, service.get_by("capacity", 100)[0])