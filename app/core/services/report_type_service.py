"""
ReportType Service

Author: Setenay Baysal
Student ID: 22074682

"""

from app.core.database.models import ReportType
from app.core.service import Service


class ReportTypeService(Service):
    def __init__(self, session):
        super().__init__(session, ReportType)

    def get_report_type_by_name(self, report_type_name: str) -> ReportType:
        return self._session.query(ReportType).filter_by(name=report_type_name).first()
