from app.core.logger import logger
from app.db.models import AnomalyEvent
from app.db.models import DailyKPI


class AnomalyDetector:
    """
    Detects unusual KPI changes.
    """

    REVENUE_DROP_THRESHOLD = 0.30

    REVENUE_SPIKE_THRESHOLD = 0.50

    def __init__(self, db):
        self.db = db

    def detect_revenue_anomalies(self):
        """
        Detects abnormal revenue changes.
        """

        logger.info(
            "Starting anomaly detection..."
        )

        kpis = (
            self.db.query(DailyKPI)
            .order_by(DailyKPI.kpi_date.asc())
            .all()
        )

        if len(kpis) < 2:

            logger.warning(
                "Not enough KPI records "
                "for anomaly detection."
            )

            return []

        anomalies = []

        for index in range(1, len(kpis)):

            previous_kpi = kpis[index - 1]

            current_kpi = kpis[index]

            previous_revenue = (
                previous_kpi.total_revenue
            )

            current_revenue = (
                current_kpi.total_revenue
            )

            if previous_revenue == 0:
                continue

            revenue_change = (
                current_revenue - previous_revenue
            ) / previous_revenue

            if (
                revenue_change
                <= -self.REVENUE_DROP_THRESHOLD
            ):

                anomaly = self._create_anomaly(
                    anomaly_type="REVENUE_DROP",
                    description=(
                        f"Revenue dropped by "
                        f"{abs(revenue_change) * 100:.2f}% "
                        f"on {current_kpi.kpi_date}"
                    ),
                    severity="HIGH"
                )

                anomalies.append(anomaly)

            elif (
                revenue_change
                >= self.REVENUE_SPIKE_THRESHOLD
            ):

                anomaly = self._create_anomaly(
                    anomaly_type="REVENUE_SPIKE",
                    description=(
                        f"Revenue increased by "
                        f"{revenue_change * 100:.2f}% "
                        f"on {current_kpi.kpi_date}"
                    ),
                    severity="MEDIUM"
                )

                anomalies.append(anomaly)

        self.db.commit()

        logger.info(
            f"Anomaly detection completed. "
            f"Anomalies Found: {len(anomalies)}"
        )

        return anomalies

    def _create_anomaly(
        self,
        anomaly_type,
        description,
        severity
    ):
        """
        Persists anomaly event.
        """

        anomaly = AnomalyEvent(
            anomaly_type=anomaly_type,
            description=description,
            severity=severity
        )

        self.db.add(anomaly)

        return anomaly