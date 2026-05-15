import requests

from requests.exceptions import ReadTimeout
from requests.exceptions import RequestException

from app.core.config import settings
from app.core.logger import logger
from app.db.models import AIInsight
from app.db.models import AnomalyEvent
from app.db.models import DailyKPI


class InsightGenerator:
    """
    Generates AI-powered business insights.
    """

    def __init__(self, db):
        self.db = db

    def generate_daily_insight(self):
        """
        Generates business insight from latest KPI data.
        """

        logger.info(
            "Starting AI insight generation..."
        )

        latest_kpi = (
            self.db.query(DailyKPI)
            .order_by(DailyKPI.kpi_date.desc())
            .first()
        )

        if not latest_kpi:

            logger.warning(
                "No KPI data available for insight generation."
            )

            return None

        recent_anomalies = (
            self.db.query(AnomalyEvent)
            .order_by(
                AnomalyEvent.detected_at.desc()
            )
            .limit(3)
            .all()
        )

        prompt = self._build_prompt(
            latest_kpi,
            recent_anomalies
        )

        try:

            ai_response = self._generate_with_ollama(
                prompt
            )

        except ReadTimeout:

            logger.warning(
                "Ollama inference timed out. "
                "Using fallback insight."
            )

            ai_response = (
                "AI insight generation timed out. "
                "Revenue and KPI data should be reviewed manually."
            )

        except RequestException as error:

            logger.error(
                f"Ollama request failed: {error}"
            )

            ai_response = (
                "AI insight generation failed due "
                "to model communication issue."
            )

        insight = AIInsight(
            insight_type="DAILY_BUSINESS_SUMMARY",
            insight_text=ai_response
        )

        self.db.add(insight)

        self.db.commit()

        logger.info(
            "AI insight generated successfully."
        )

        return insight

    def _build_prompt(
        self,
        latest_kpi,
        anomalies
    ):
        """
        Builds optimized prompt for Ollama.
        """

        anomaly_text = "\n".join([
            f"- {anomaly.description}"
            for anomaly in anomalies
        ])

        prompt = f"""
Business KPI Summary:

Revenue: {latest_kpi.total_revenue}
Orders: {latest_kpi.total_orders}
Average Order Value: {latest_kpi.average_order_value}

Anomalies:
{anomaly_text if anomaly_text else "No anomalies."}

Provide:
1. One short business summary
2. One business concern
3. One suggested action

Keep response under 120 words.
"""

        return prompt

    def _generate_with_ollama(
        self,
        prompt: str
    ) -> str:
        """
        Sends prompt to Ollama model.
        """

        payload = {
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            "No AI response generated."
        )