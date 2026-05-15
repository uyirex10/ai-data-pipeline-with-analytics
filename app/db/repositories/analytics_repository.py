from sqlalchemy.orm import Session

from app.db.models import DailyKPI
from app.db.models import AnomalyEvent


class AnalyticsRepository:
    """
    Handles analytics and anomaly persistence.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_daily_kpi(
        self,
        kpi_date,
        total_revenue: float,
        total_orders: int,
        average_order_value: float
    ) -> DailyKPI:
        """
        Stores daily KPI metrics.
        """

        kpi = DailyKPI(
            kpi_date=kpi_date,
            total_revenue=total_revenue,
            total_orders=total_orders,
            average_order_value=average_order_value
        )

        self.db.add(kpi)

        self.db.commit()

        self.db.refresh(kpi)

        return kpi

    def create_anomaly_event(
        self,
        anomaly_type: str,
        description: str,
        severity: str
    ) -> AnomalyEvent:
        """
        Stores anomaly event.
        """

        anomaly = AnomalyEvent(
            anomaly_type=anomaly_type,
            description=description,
            severity=severity
        )

        self.db.add(anomaly)

        self.db.commit()

        self.db.refresh(anomaly)

        return anomaly