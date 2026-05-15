from app.db.models import ReportLog


class ReportRepository:
    """
    Handles report logging operations.
    """

    def __init__(self, db):
        self.db = db

    def create_report_log(
        self,
        report_name: str,
        report_type: str,
        file_path: str,
        status: str
    ):
        """
        Creates report generation log.
        """

        report_log = ReportLog(
            report_name=report_name,
            report_type=report_type,
            file_path=file_path,
            status=status
        )

        self.db.add(report_log)

        self.db.commit()

        self.db.refresh(report_log)

        return report_log