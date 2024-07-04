from app.core.services.reservation_service import ReservationService
from app.gui.controller import Controller
from app.gui.utils.widgets.full_table_widget import TableWidget

import tkinter as tk


class ReservationsController(Controller):
    def __init__(self, view, app, restaurant):
        super().__init__(view, app)

        self.__restaurant = restaurant
        self.__set_up_table()

    def __get_table_data(self):
        with ReservationService(self._app.get_session()) as reservation_service:
            reservations = reservation_service.get_by_restaurant_id(
                self.__restaurant.id
            )
            return reservation_service.expunge_all(reservations)

    def __set_up_table(self):
        table_data = self.__get_table_data()

        self.__table_wrapper = TableWidget(
            label_text="Reservations",
            data=table_data,
            callback=self.__view_reservation,
            master=self._view.table_container,
            excluded_columns=("id", "restaurant_id"),
        )
        self.__table_wrapper.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

    def __view_reservation(self, reservation_id):
        with ReservationService(self._app.get_session()) as reservation_service:
            reservation = reservation_service.get_by_id(reservation_id)
            restaurant = reservation.restaurant
            restaurant = reservation_service.expunge(restaurant)
            reservation = reservation_service.expunge(reservation)

            self._app.raise_screen(
                self._view,
                "reservation",
                {"app": self._app, "reservation": reservation},
                {
                    "app": self._app,
                    "reservation": reservation,
                    "restaurant": restaurant,
                },
            )

    def get_restaurant(self):
        return self.__restaurant
