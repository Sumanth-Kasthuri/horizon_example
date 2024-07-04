"""
Author: Archie Jarvis
Student ID: 20022663
"""

import configparser
from typing import Optional

from passlib.hash import sha256_crypt
from sqlalchemy.orm import joinedload

from app.core.database.models import Account
from app.core.services.account_service import AccountService
from app.core.services.role_service import RoleService
from app.gui.view import View


class AccountManager:
    __current_user: str = None

    def __init__(self, app):
        self.__app = app
        self.__config = configparser.ConfigParser()
        self.__config.read("user.ini")

    def get_credentials(self):
        return (
            self.__config.get("credentials", "username"),
            self.__config.get("credentials", "hashed_password"),
            self.__config.get("credentials", "salt"),
        )

    def set_credentials(self, username, password, salt):
        self.__config.set("credentials", "username", username)
        self.__config.set(
            "credentials", "hashed_password", sha256_crypt.hash(password + salt)
        )
        self.__config.set("credentials", "salt", salt)
        with open("user.ini", "w") as configfile:
            self.__config.write(configfile)

    def is_logged_in(self) -> bool:
        """
        Returns True if the user is logged in, False otherwise.
        """
        return self.__current_user is not None

    def register_user(self, username: str, password: str) -> bool:
        """
        Registers a user with the given username and password.

        :param username: The username of the user.
        :param password: The password of the user.
        :return: True if the user was registered successfully, False otherwise.
        """

        with AccountService(self.__app.get_session()) as service:
            if service.get_account_by_username(username) is not None:
                return False

            user = Account(username=username, password=password)

            service.add(user)

            self.__current_user = user.username
        return True

    def login_user(self, username: str, password: str) -> (bool, Optional[Account]):
        """
        Logs in a user with the given username and password.

        :param username: The username of the user.
        :param password: The password of the user.s
        :return: (True, User) if the user was logged in successfully, False otherwise.
        """

        with AccountService(self.__app.get_session()) as service:
            user = service.get_account_by_username(
                username, options=[joinedload(Account.role)]
            )

            if user is None:
                return False

            if sha256_crypt.verify(password + user.salt, user.password):
                self.__current_user = user.username
                return True, user

            return False

    def logout_user(self, from_screen: View):
        """
        Logs out the current user.
        """
        self.__current_user = None
        self.__app.raise_screen(
            from_screen, "login", {"app": self.__app}, {"app": self.__app}
        )

    def get_current_user(self) -> str:
        """
        Returns the current user's username.
        :return: The current user if logged in, None otherwise.
        """
        return self.__current_user

    def add_to_role(self, user, role):
        """
        Adds a user to a role.
        :param user: The user to add.
        :param role: The role to add the user to.
        """
        session = self.__app.get_session()

        with AccountService(session) as account_service:
            with RoleService(session) as role_service:
                user = account_service.get_account_by_username(user)
                role = role_service.get_role_by_name(role)
                user.role = role
                account_service.update(user)

    def is_user_admin(self):
        if not self.__current_user:
            return False
        with AccountService(self.__app.get_session()) as account_service:
            user = account_service.get_account_by_username(self.__current_user)
            return user.is_admin()

    def hash_password_with_salt(self, username, password):
        with AccountService(self.__app.get_session()) as service:
            user = service.get_account_by_username(username)
            return sha256_crypt.hash(password + user.salt)
