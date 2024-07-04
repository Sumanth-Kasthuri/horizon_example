"""
File containing the database connection and session scope for the application.

Author: Archie Jarvis
Student ID: 20022663
(unless otherwise stated in the docstring of the class/function)
"""

import configparser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database.models import Base

config = configparser.ConfigParser()
config.read("../config.ini")

DATABASE_URI = config.get("database", "uri")
engine = create_engine(DATABASE_URI, echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
