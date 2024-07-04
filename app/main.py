"""
Author: Archie Jarvis
Student ID: 20022663
"""

import threading
import tkinter as tk

from app.core.managers.accounts_manager import AccountManager
from app.core.database import database

import app.gui.pages
from app.core.database.models import Role
from app.core.managers.discounts_manager import DiscountsManager
from app.core.managers.inventory_manager import InventoryManager
from app.core.managers.order_manager import OrderManager
from app.core.managers.reservations_manager import ReservationsManager
from app.core.services.account_service import AccountService

from ttkthemes import ThemedTk

from app.core.services.role_service import RoleService


class App(ThemedTk):
    __WINDOW_WIDTH: int = 1280
    __WINDOW_HEIGHT: int = 720
    __DEFAULT_PAGE: str = "login"

    __stop_threads: threading.Event = threading.Event()

    __pages: dict = {
        "login": {
            "view": app.gui.pages.login.login_view.LoginView,
            "controller": app.gui.pages.login.login_controller.LoginController,
        },
        "home": {
            "view": app.gui.pages.home.home_view.HomeView,
            "controller": app.gui.pages.home.home_controller.HomeController,
        },
        "restaurants": {
            "view": app.gui.pages.restaurants.restaurants_view.RestaurantsView,
            "controller": app.gui.pages.restaurants.restaurants_controller.RestaurantsController,
        },
        "restaurant": {
            "view": app.gui.pages.restaurant.restaurant_view.RestaurantView,
            "controller": app.gui.pages.restaurant.restaurant_controller.RestaurantController,
        },
        "accounts": {
            "view": app.gui.pages.accounts.accounts_view.AccountsView,
            "controller": app.gui.pages.accounts.accounts_controller.AccountsController,
        },
        "account": {
            "view": app.gui.pages.account.account_view.AccountView,
            "controller": app.gui.pages.account.account_controller.AccountController,
        },
        "inventory": {
            "view": app.gui.pages.inventory.inventory_view.InventoryView,
            "controller": app.gui.pages.inventory.inventory_controller.InventoryController,
        },
        "stock_item": {
            "view": app.gui.pages.stock_item.stock_item_view.StockItemView,
            "controller": app.gui.pages.stock_item.stock_item_controller.StockItemController,
        },
        "stock_item_add": {
            "view": app.gui.pages.stock_item_add.stock_item_add_view.StockItemAddView,
            "controller": app.gui.pages.stock_item_add.stock_item_add_controller.StockItemAddController,
        },
        "orders": {
            "view": app.gui.pages.orders.orders_view.OrdersView,
            "controller": app.gui.pages.orders.orders_controller.OrdersController,
        },
        "order": {
            "view": app.gui.pages.order.order_view.OrderView,
            "controller": app.gui.pages.order.order_controller.OrderController,
        },
        "order_add": {
            "view": app.gui.pages.order_add.order_add_view.OrderAddView,
            "controller": app.gui.pages.order_add.order_add_controller.OrderAddController,
        },
        "reservations": {
            "view": app.gui.pages.reservations.reservations_view.ReservationsView,
            "controller": app.gui.pages.reservations.reservations_controller.ReservationsController,
        },
        "reservations_add": {
            "view": app.gui.pages.reservations_add.reservations_add_view.ReservationsAddView,
            "controller": app.gui.pages.reservations_add.reservations_add_controller.ReservationsAddController,
        },
        "reservation": {
            "view": app.gui.pages.reservation.reservation_view.ReservationView,
            "controller": app.gui.pages.reservation.reservation_controller.ReservationController,
        },
        "restaurant_add": {
            "view": app.gui.pages.restaurant_add.restaurant_add_view.RestaurantAddView,
            "controller": app.gui.pages.restaurant_add.restaurant_add_controller.RestaurantAddController,
        },
        "discounts": {
            "view": app.gui.pages.discounts.discounts_view.DiscountsView,
            "controller": app.gui.pages.discounts.discounts_controller.DiscountsController,
        },
        "discount": {
            "view": app.gui.pages.discount.discount_view.DiscountView,
            "controller": app.gui.pages.discount.discount_controller.DiscountController,
        },
        "discount_add": {
            "view": app.gui.pages.discount_add.discount_add_view.DiscountAddView,
            "controller": app.gui.pages.discount_add.discount_add_controller.DiscountAddController,
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry(f"{self.__WINDOW_WIDTH}x{self.__WINDOW_HEIGHT}")
        self.__create_managers()
        self.__create_admin_user()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.configure(theme="arc")

        self.raise_screen(
            None,
            self.__DEFAULT_PAGE,
            {"app": self},
            {"app": self},
        )

    def __create_managers(self):
        self.__account_manager = AccountManager(app=self)
        self.__inventory_manager = InventoryManager(self)
        self.__discounts_manager = DiscountsManager(self)
        self.__order_manager = OrderManager(self)
        self.__reservations_manager = ReservationsManager(self)

    def __create_admin_user(self):
        with RoleService(self.get_session()) as role_service:
            if role_service.get_role_by_name("admin") is None:
                role_service.add(Role(name="admin", admin=True))

        with AccountService(self.get_session()) as account_service:
            if account_service.get_account_by_username("admin") is None:
                self.__account_manager.register_user("admin", "admin")

        self.__account_manager.add_to_role("admin", "admin")

    def raise_screen(
        self, from_screen, screen_name, view_kwargs, controller_kwargs
    ) -> None:
        """
        Raises a screen by name, passing the view and controller kwargs
        Screens are defined in the __pages dictionary

        :param from_screen: The instance of the screen raising the new screen
        :param screen_name: The name of the screen to raise
        :param view_kwargs: The kwargs to pass to the view
        :param controller_kwargs: The kwargs to pass to the controller
        :return: None
        """
        if screen_name not in self.__pages:
            raise ValueError(f"Screen {screen_name} does not exist")

        if from_screen is not None:
            from_screen.destroy()

        page = self.__pages[screen_name]

        view = page["view"](**view_kwargs)
        controller = page["controller"](view=view, **controller_kwargs)

        view.set_controller(controller)
        view.pack(expand=True, fill=tk.BOTH)
        view.tkraise()

    def get_inventory_manager(self):
        return self.__inventory_manager

    def get_discounts_manager(self):
        return self.__discounts_manager

    def get_reservations_manager(self):
        return self.__reservations_manager

    def get_order_manager(self):
        return self.__order_manager

    def on_close(self):
        self.__stop_threads.set()
        self.destroy()

    def get_stop_threads(self):
        return self.__stop_threads

    def get_accounts_manager(self) -> AccountManager:
        return self.__account_manager

    def get_session(self) -> database.Session:
        return database.Session()


if __name__ == "__main__":
    app = App()
    app.mainloop()
