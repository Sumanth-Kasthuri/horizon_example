import datetime
from tkinter.ttk import Entry, Combobox, Button, Label

from app.core.database.models import Reservation
from app.core.services.reservation_service import ReservationService
from app.gui.controller import Controller


class ReservationsAddController(Controller):
    def __init__(self, view, app, restaurant):
        super().__init__(view, app)
        self.__restaurant = restaurant
        self.__set_up_edit_widget()

    __guest_input_valid = False
    __date_input_valid = False

    def __guest_input_callback(self, event):
        # if can parse to int
        if event.widget.get().isdigit():
            self.__guest_input_valid = True

            if self.__date_input_valid:
                self.__both_inputs_valid()
        else:
            self.__guest_input_valid = False

    def __date_input_callback(self, event):
        content = event.widget.get()
        if len(content.split("/")) == 3:
            self.__date_input_valid = True

            if self.__guest_input_valid:
                self.__both_inputs_valid()
        else:
            self.__date_input_valid = False

    def __get_date_formatted(self):
        split = self.date_input.get().split("/")

        dt = datetime.date(int(split[2]), int(split[1]), int(split[0]))
        return dt

    def __both_inputs_valid(self):
        available_reservations = (
            self._app.get_reservations_manager().get_available_reservations(
                self.__restaurant.id,
                self.__get_date_formatted(),
                int(self.guest_input.get()),
            )
        )

        self.table_combo["values"] = list(available_reservations.keys())

    def __table_combo_callback(self, event):
        print(
            self._app.get_reservations_manager().get_available_reservations(
                self.__restaurant.id,
                self.__get_date_formatted(),
                int(self.guest_input.get()),
            )
        )
        self.time_combo[
            "values"
        ] = self._app.get_reservations_manager().get_available_reservations(
            self.__restaurant.id,
            self.__get_date_formatted(),
            int(self.guest_input.get()),
        )[
            int(self.table_combo.get())
        ]

    def __set_up_edit_widget(self):
        self.name_input_label = Label(
            master=self._view.data_entry_container, text="Name"
        )
        self.name_input = Entry(self._view.data_entry_container)
        self.name_input_label.grid(row=0, column=0)
        self.name_input.grid(row=0, column=1)

        self.guest_input_label = Label(
            master=self._view.data_entry_container, text="Guests"
        )
        self.guest_input = Entry(self._view.data_entry_container)
        self.guest_input.bind("<KeyRelease>", self.__guest_input_callback)
        self.guest_input_label.grid(row=1, column=0)
        self.guest_input.grid(row=1, column=1)

        self.date_input_label = Label(
            master=self._view.data_entry_container, text="Date"
        )
        self.date_input = Entry(self._view.data_entry_container)
        self.date_input.bind("<KeyRelease>", self.__date_input_callback)
        self.date_input_label.grid(row=2, column=0)
        self.date_input.grid(row=2, column=1)

        self.table_combo_label = Label(
            master=self._view.data_entry_container, text="Table"
        )
        self.table_combo = Combobox(self._view.data_entry_container)
        self.table_combo.bind("<<ComboboxSelected>>", self.__table_combo_callback)
        self.table_combo_label.grid(row=3, column=0)
        self.table_combo.grid(row=3, column=1)

        self.time_combo_label = Label(
            master=self._view.data_entry_container, text="Time"
        )
        self.time_combo = Combobox(self._view.data_entry_container)
        self.time_combo_label.grid(row=4, column=0)
        self.time_combo.grid(row=4, column=1)

        save_button = Button(
            master=self._view.data_entry_container,
            text="Book",
            command=self.__add_reservation,
        )

        save_button.grid(row=5, column=0, columnspan=2)

    def __get_time_formatted(self):
        hours = int(float(self.time_combo.get()))
        minutes = int((float(self.time_combo.get()) - hours) * 60)

        return datetime.time(hours, minutes)

    def __add_reservation(self):
        with ReservationService(self._app.get_session()) as reservation_service:
            reservation_service.add(
                Reservation(
                    self.__restaurant.id,
                    self.name_input.get(),
                    self.__get_date_formatted(),
                    self.__get_time_formatted(),
                    int(self.guest_input.get()),
                    self.table_combo.get(),
                )
            )
            reservation_service.commit()

            self._app.raise_screen(
                self._view,
                "reservations",
                {"app": self._app},
                {"app": self._app, "restaurant": self.__restaurant},
            )

    def get_restaurant(self):
        return self.__restaurant
