from datetime import datetime
from app.db.models import RawDataBatch

from sqlalchemy.orm import Session

from app.db.models import PipelineRun
from app.db.models import PipelineStep


class PipelineRepository:
    """
    Handles all pipeline-related database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_pipeline_run(
        self,
        pipeline_name: str,
        status: str
    ) -> PipelineRun:
        """
        Creates a new pipeline run record.
        """

        pipeline_run = PipelineRun(
            pipeline_name=pipeline_name,
            status=status
        )

        self.db.add(pipeline_run)

        self.db.commit()

        self.db.refresh(pipeline_run)

        return pipeline_run

    def update_pipeline_run_status(
        self,
        pipeline_run: PipelineRun,
        status: str,
        records_processed: int = 0,
        error_message: str = None
    ) -> PipelineRun:
        """
        Updates pipeline run status and completion metadata.
        """

        pipeline_run.status = status

        pipeline_run.records_processed = records_processed

        pipeline_run.error_message = error_message

        pipeline_run.finished_at = datetime.utcnow()

        self.db.commit()

        self.db.refresh(pipeline_run)

        return pipeline_run

    def create_pipeline_step(
        self,
        pipeline_run_id: int,
        step_name: str,
        status: str
    ) -> PipelineStep:
        """
        Creates a pipeline step tracking record.
        """

        step = PipelineStep(
            pipeline_run_id=pipeline_run_id,
            step_name=step_name,
            status=status
        )

        self.db.add(step)

        self.db.commit()

        self.db.refresh(step)

        return step

    def update_pipeline_step_status(
        self,
        step: PipelineStep,
        status: str,
        records_processed: int = 0,
        error_message: str = None
    ) -> PipelineStep:
        """
        Updates pipeline step status.
        """

        step.status = status

        step.records_processed = records_processed

        step.error_message = error_message

        step.finished_at = datetime.utcnow()

        self.db.commit()

        self.db.refresh(step)

        return step

    def create_raw_data_batch(
            self,
            source_name: str,
            batch_identifier: str,
            records_count: int,
            status: str
    ) -> RawDataBatch:
        """
        Tracks extracted raw data batch.
        """

        batch = RawDataBatch(
            source_name=source_name,
            batch_identifier=batch_identifier,
            records_count=records_count,
            status=status
        )

        self.db.add(batch)

        self.db.commit()

        self.db.refresh(batch)

        return batch