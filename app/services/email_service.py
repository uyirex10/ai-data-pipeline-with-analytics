import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings
from app.core.logger import logger


class EmailService:
    """
    Handles report email delivery.
    """

    def send_email(
        self,
        recipient_email: str,
        subject: str,
        html_content: str
    ):
        """
        Sends HTML email report.
        """

        logger.info(
            f"Sending report email to: "
            f"{recipient_email}"
        )

        message = MIMEMultipart()

        message["From"] = settings.SMTP_USERNAME

        message["To"] = recipient_email

        message["Subject"] = subject

        message.attach(
            MIMEText(html_content, "html")
        )

        try:

            with smtplib.SMTP(
                settings.SMTP_SERVER,
                settings.SMTP_PORT
            ) as server:

                server.starttls()

                server.login(
                    settings.SMTP_USERNAME,
                    settings.SMTP_PASSWORD
                )

                server.send_message(message)

            logger.info(
                "Email sent successfully."
            )

        except Exception as error:

            logger.error(
                f"Email delivery failed: {error}"
            )

            raise