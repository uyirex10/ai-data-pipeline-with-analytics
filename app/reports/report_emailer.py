from app.core.logger import logger
from app.services.email_service import EmailService


class ReportEmailer:
    """
    Sends generated reports to stakeholders.
    """

    def __init__(self):
        self.email_service = EmailService()

    def send_report(
        self,
        recipient_email: str,
        report_path: str
    ):
        """
        Sends HTML report via email.
        """

        logger.info(
            f"Preparing report email: "
            f"{report_path}"
        )

        with open(
            report_path,
            "r",
            encoding="utf-8"
        ) as file:

            html_content = file.read()

        self.email_service.send_email(
            recipient_email=recipient_email,
            subject="Daily Business Report",
            html_content=html_content
        )

        logger.info(
            "Report email delivery completed."
        )