"""
Event Service

Author: Setenay Baysal
Student ID: 22074682

"""

from app.core.database.models import Event
from app.core.service import Service


class EventService(Service):
    def __init__(self, session):
        super().__init__(session, Event)

    def get_event_by_name(self, event_name: str) -> Event:
        return self._session.query(Event).filter_by(name=event_name).first()

    def get_events_by_date(self, event_date: str) -> Event:
        return self._session.query(Event).filter_by(date=event_date).all()

    def get_events_by_description(self, event_description: str) -> Event:
        return self._session.query(Event).filter_by(description=event_description).all()

    def get_events_by_end_time(self, event_end_time) -> Event:
        return self._session.query(Event).filter_by(end_time=event_end_time).all()

    def get_events_by_start_time(self, event_start_time) -> Event:
        return self._session.query(Event).filter_by(start_time=event_start_time).all()
