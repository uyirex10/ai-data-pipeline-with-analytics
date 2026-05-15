from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.core.logger import logger
from app.pipelines.sales_pipeline import SalesPipeline


class PipelineScheduler:
    """
    Schedules automated ETL pipeline runs.
    """

    def __init__(self):
        self.scheduler = BlockingScheduler()

    def start(self):
        """
        Starts scheduler.
        """

        logger.info(
            "Starting pipeline scheduler..."
        )

        self.scheduler.add_job(
            func=self.run_sales_pipeline,
            trigger=IntervalTrigger(
                minutes=1
            ),
            id="sales_pipeline_job",
            name="Sales Pipeline Job",
            replace_existing=True
        )

        logger.info(
            "Scheduler started successfully."
        )

        self.scheduler.start()

    @staticmethod
    def run_sales_pipeline():
        """
        Executes ETL pipeline.
        """

        logger.info(
            "Executing scheduled sales pipeline..."
        )

        try:

            pipeline = SalesPipeline(
                source_type="csv",
                source_config={
                    "file_path": (
                        "data/raw/sample_sales.csv"
                    )
                }
            )

            pipeline.run()

            logger.info(
                "Scheduled pipeline completed."
            )

        except Exception as error:

            logger.exception(
                f"Scheduled pipeline failed: "
                f"{error}"
            )