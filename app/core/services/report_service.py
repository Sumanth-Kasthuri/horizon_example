"""
Report Service

Author: Setenay Baysal
Student ID: 22074682

"""

from app.core.database.models import Report
from app.core.service import Service


class ReportService(Service):
    def __init__(self, session):
        super().__init__(session, Report)

    def get_report_by_name(self, report_name: str) -> Report:
        return self._session.query(Report).filter_by(name=report_name).first()
