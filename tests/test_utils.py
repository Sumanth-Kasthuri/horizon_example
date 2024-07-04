"""
Author: Archie Jarvis
Student ID: 20022663
"""

import configparser
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database.models import Base


def get_test_database_uri():
    print(os.getcwd())
    config = configparser.ConfigParser()
    config.read("config_test.ini")
    return config["database"]["uri"]


def create_test_session():
    test_database_uri = get_test_database_uri()
    engine = create_engine(test_database_uri, echo=True)

    Base.metadata.create_all(engine)

    session_maker = sessionmaker(bind=engine)

    session = session_maker()

    return session
