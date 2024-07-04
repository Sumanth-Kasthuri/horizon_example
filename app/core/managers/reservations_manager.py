"""
Authors: Setenay, modified by Archie
"""

from datetime import datetime

from app.core.services.restaurant_service import RestaurantService
from app.core.services.table_service import TableService


def get_time(time_interval):
    hours = int(time_interval)
    minutes = int(float(time_interval - hours) * 60)
    dt = datetime.now()
    dt = dt.replace(hour=hours, minute=minutes, second=0, microsecond=0)
    return datetime.time(dt)


class ReservationsManager:
    OPEN_TIME = 10  # didn't have time to move this to restaurant
    CLOSE_TIME = 22
    TIME_INTERVAL = 0.5

    def __init__(self, app):
        self.__app = app

    def get_available_reservations(self, restaurant_id, date, total_guests):
        """
        Returns a list of available reservations for the given restaurant, date, and number of guests.
        :param restaurant_id: id of the restaurant
        :param date: date of the reservation
        :param total_guests: how many guests
        :return: dictionary of tables and the times they are available
        """

        available_reservations = {}
        opening_time = self.OPEN_TIME
        closing_time = self.CLOSE_TIME
        current_time = opening_time

        with RestaurantService(self.__app.get_session()) as restaurant_service:
            restaurant = restaurant_service.get_by_id(restaurant_id)
            tables = restaurant_service.expunge_all(restaurant.tables)

        while current_time < closing_time:
            for table in tables:
                # Check if the table is available at the current time
                if self.is_table_available(table.id, date, current_time, total_guests):
                    # Add the available time for the table to the dictionary
                    if table.id not in available_reservations:
                        available_reservations[table.id] = []
                    available_reservations[table.id].append(current_time)

            # Move to the next time interval
            current_time += self.TIME_INTERVAL

        return available_reservations

    def is_table_available(self, table_id, date, time, total_guests):
        """
        Checks if a table is available for the given restaurant, date, time, and number of guests.
        :param table_id: id of the restaurant
        :param date: date of the reservation
        :param time: time of the reservation
        :param total_guests: how many guests
        :return: True if the table is available, False otherwise
        """

        with TableService(self.__app.get_session()) as table_service:
            table = table_service.get_by_id(table_id)
            for reservation in table.reservations:
                if (
                    reservation.date == date
                    and reservation.time.hour == get_time(time).hour
                    and reservation.time.minute == get_time(time).minute
                ):
                    # Table is already booked at this time
                    return False

            # Check if the table can accommodate the total number of guests
            if table.capacity >= total_guests:
                return True

        return False
