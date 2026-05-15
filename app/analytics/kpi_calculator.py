from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.models import DailyKPI
from app.db.models import SalesFact


class KPICalculator:
    """
    Calculates business KPIs from warehouse data.
    """

    def __init__(self, db: Session):
        self.db = db

    def calculate_daily_kpis(self):
        """
        Calculates and stores daily sales KPIs.
        """

        logger.info("Starting daily KPI calculation...")

        results = (
            self.db.query(
                func.date(SalesFact.sale_timestamp).label("kpi_date"),
                func.sum(SalesFact.revenue).label("total_revenue"),
                func.count(SalesFact.id).label("total_orders"),
                func.avg(SalesFact.revenue).label("average_order_value")
            )
            .group_by(func.date(SalesFact.sale_timestamp))
            .all()
        )

        records_created = 0

        for result in results:
            existing_kpi = (
                self.db.query(DailyKPI)
                .filter(DailyKPI.kpi_date == result.kpi_date)
                .first()
            )

            if existing_kpi:
                existing_kpi.total_revenue = float(result.total_revenue or 0)
                existing_kpi.total_orders = int(result.total_orders or 0)
                existing_kpi.average_order_value = float(
                    result.average_order_value or 0
                )
            else:
                kpi = DailyKPI(
                    kpi_date=result.kpi_date,
                    total_revenue=float(result.total_revenue or 0),
                    total_orders=int(result.total_orders or 0),
                    average_order_value=float(
                        result.average_order_value or 0
                    )
                )

                self.db.add(kpi)
                records_created += 1

        self.db.commit()

        logger.info(
            f"Daily KPI calculation completed. "
            f"Records Created: {records_created}"
        )

        return results