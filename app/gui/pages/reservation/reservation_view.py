from app.core.services.reservation_service import ReservationService
from app.gui.utils.widgets.container_widget import Container
from app.gui.view import View


class ReservationView(View):
    def __init__(self, app, reservation, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.__reservation = reservation
        self.__build()

        self.back_button.configure(command=self.__back_button_callback)

    def __build(self):
        self.data_entry_container = Container(
            master=self._content_frame,
            padding=10,
        )
        self.data_entry_container.place(relx=0, rely=0)

    def __back_button_callback(self):
        with ReservationService(self._app.get_session()) as reservation_service:
            reservation = reservation_service.get_by_id(self.__reservation.id)
            restaurant = reservation.restaurant
            restaurant = reservation_service.expunge(restaurant)

            self._app.raise_screen(
                self,
                "reservations",
                {"app": self._app},
                {"app": self._app, "restaurant": restaurant},
            )
