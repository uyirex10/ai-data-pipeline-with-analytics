from datetime import datetime

from app.core.logger import logger
from app.db.models import AIInsight
from app.db.models import AnomalyEvent
from app.db.models import DailyKPI
from app.db.repositories.report_repository import ReportRepository

class ReportGenerator:
    """
    Generates business reports from KPI, anomaly, and AI insight data.
    """

    def __init__(self, db):
        self.db = db

        self.report_repository = ReportRepository(db)

    def generate_daily_report(self):
        """
        Generates a daily HTML business report.
        """

        logger.info("Starting daily report generation...")

        latest_kpi = (
            self.db.query(DailyKPI)
            .order_by(DailyKPI.kpi_date.desc())
            .first()
        )

        latest_insight = (
            self.db.query(AIInsight)
            .order_by(AIInsight.generated_at.desc())
            .first()
        )

        anomalies = (
            self.db.query(AnomalyEvent)
            .order_by(AnomalyEvent.detected_at.desc())
            .limit(5)
            .all()
        )

        html_content = self._build_html_report(
            latest_kpi=latest_kpi,
            latest_insight=latest_insight,
            anomalies=anomalies
        )

        report_path = (
            f"data/reports/daily_report_"
            f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.html"
        )

        with open(report_path, "w", encoding="utf-8") as file:
            file.write(html_content)

        self.report_repository.create_report_log(
            report_name="daily_business_report",
            report_type="HTML",
            file_path=report_path,
            status="SUCCESS"
        )

        logger.info(
            f"Daily report generated: {report_path}"
        )

        return report_path

    def _build_html_report(
        self,
        latest_kpi,
        latest_insight,
        anomalies
    ):
        """
        Builds HTML report content.
        """

        if not latest_kpi:
            kpi_section = "<p>No KPI data available.</p>"
        else:
            kpi_section = f"""
            <ul>
                <li><strong>Total Revenue:</strong> {latest_kpi.total_revenue}</li>
                <li><strong>Total Orders:</strong> {latest_kpi.total_orders}</li>
                <li><strong>Average Order Value:</strong> {latest_kpi.average_order_value}</li>
            </ul>
            """

        if not latest_insight:
            insight_section = "<p>No AI insight available.</p>"
        else:
            insight_section = f"""
            <p>{latest_insight.insight_text}</p>
            """

        if not anomalies:
            anomaly_section = "<p>No anomalies detected.</p>"
        else:
            anomaly_items = "".join([
                f"<li><strong>{anomaly.severity}</strong>: {anomaly.description}</li>"
                for anomaly in anomalies
            ])

            anomaly_section = f"<ul>{anomaly_items}</ul>"

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Daily Business Report</title>
        </head>
        <body style="font-family: Arial, sans-serif; margin: 40px;">
            <h1>Daily Business Report</h1>

            <p><strong>Generated At:</strong> {datetime.utcnow()}</p>

            <hr>

            <h2>Key Performance Indicators</h2>
            {kpi_section}

            <h2>AI Business Insight</h2>
            {insight_section}

            <h2>Recent Anomalies</h2>
            {anomaly_section}
        </body>
        </html>
        """

        return html