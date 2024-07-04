"""
Service Base Class

Author: Archie Jarvis
Student ID: 20022663
"""


class Service:
    def __init__(self, session, model):
        self._session = session
        self.__model = model

    def get_all(self, options=None):
        query = self._session.query(self.__model)
        if options:
            query = query.options(*options)
        return query.all()

    def get_by_id(self, id, options=None):
        query = self._session.query(self.__model).filter_by(id=id)
        if options:
            query = query.options(*options)
        return query.first()

    def add(self, obj):
        return self._session.add(obj)

    def update(self, obj):
        return self._session.merge(obj)

    def delete(self, obj):
        self._session.delete(obj)

    def expunge_all(self, objects: list) -> list:
        """
        Expunges objects from the session, removing them from the session cache
        :param objects: The objects to expunge
        :return: The expunged objects
        """
        for obj in objects:
            self._session.expunge(obj)
        return objects

    def expunge(self, obj):
        """
        Expunges an object from the session, removing it from the session cache
        :param obj: The object to expunge
        :return: The expunged object
        """
        self._session.expunge(obj)
        return obj

    def commit(self):
        self._session.commit()

    def get_by(self, get_by, value):
        """
        Gets all objects by the given field and value
        :param get_by: The field to filter by
        :param value: The value to filter by
        :return:
        """
        print(get_by, value)
        print(self.__model)
        return self._session.query(self.__model).filter_by(**{get_by: value}).all()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Commits the session if no exception is raised, otherwise rolls back, then closes the session
        :param exc_type: The exception type
        :param exc_val: The exception value
        :param exc_tb: The exception traceback
        :return: None
        """
        if exc_type is None:
            self._session.commit()
        else:
            self._session.rollback()
        self._session.close()
