from sqlalchemy.orm import Session

from app.db.models import AIInsight


class InsightRepository:
    """
    Handles AI insight persistence.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_insight(
        self,
        insight_type: str,
        insight_text: str
    ) -> AIInsight:
        """
        Stores generated AI insight.
        """

        insight = AIInsight(
            insight_type=insight_type,
            insight_text=insight_text
        )

        self.db.add(insight)

        self.db.commit()

        self.db.refresh(insight)

        return insight