from app.analytics.anomaly_detector import AnomalyDetector
from app.analytics.kpi_calculator import KPICalculator
from app.core.logger import logger
from app.db.database import SessionLocal
from app.db.repositories.pipeline_repository import PipelineRepository
from app.extractors.csv_extractor import CSVExtractor
from app.loaders.optimized_sales_loader import OptimizedSalesLoader
from app.transformers.sales_transformer import SalesTransformer
from app.utils.batch import generate_batch_identifier
from app.validators.sales_validator import SalesValidator
from app.ai.insight_generator import InsightGenerator
from app.reports.report_generator import ReportGenerator
from app.factories.extractor_factory import ExtractorFactory


class SalesPipeline:
    """
    Orchestrates the full sales ETL workflow.
    """

    PIPELINE_NAME = "sales_pipeline"

    def __init__(
            self,
            source_type: str,
            source_config: dict
    ):
        self.source_type = source_type

        self.source_config = source_config

    def run(self):
        """
        Runs the full sales pipeline from extraction
        to analytics generation.
        """

        logger.info(
            f"Starting pipeline: "
            f"{self.PIPELINE_NAME}"
        )

        db = SessionLocal()

        pipeline_repo = PipelineRepository(db)

        pipeline_run = pipeline_repo.create_pipeline_run(
            pipeline_name=self.PIPELINE_NAME,
            status="RUNNING"
        )

        try:

            # =====================================================
            # EXTRACTION STEP
            # =====================================================

            raw_dataframe = self._run_step(
                pipeline_repo=pipeline_repo,
                pipeline_run_id=pipeline_run.id,
                step_name="extract",
                function=lambda: self._extract(
                    pipeline_repo
                )
            )

            # =====================================================
            # TRANSFORMATION STEP
            # =====================================================

            transformed_dataframe = self._run_step(
                pipeline_repo=pipeline_repo,
                pipeline_run_id=pipeline_run.id,
                step_name="transform",
                function=lambda: self._transform(
                    raw_dataframe
                )
            )

            # =====================================================
            # VALIDATION STEP
            # =====================================================

            self._run_step(
                pipeline_repo=pipeline_repo,
                pipeline_run_id=pipeline_run.id,
                step_name="validate",
                function=lambda: self._validate(
                    transformed_dataframe
                )
            )

            # =====================================================
            # LOADING STEP
            # =====================================================

            self._run_step(
                pipeline_repo=pipeline_repo,
                pipeline_run_id=pipeline_run.id,
                step_name="load",
                function=lambda: self._load(
                    db,
                    transformed_dataframe
                )
            )

            # =====================================================
            # KPI CALCULATION STEP
            # =====================================================

            self._run_step(
                pipeline_repo=pipeline_repo,
                pipeline_run_id=pipeline_run.id,
                step_name="calculate_kpis",
                function=lambda: self._calculate_kpis(
                    db
                )
            )

            # =====================================================
            # ANOMALY DETECTION STEP
            # =====================================================

            self._run_step(
                pipeline_repo=pipeline_repo,
                pipeline_run_id=pipeline_run.id,
                step_name="detect_anomalies",
                function=lambda: self._detect_anomalies(
                    db
                )
            )

            # =====================================================
            # AI INSIGHT STEP
            # =====================================================

            self._run_step(
                pipeline_repo=pipeline_repo,
                pipeline_run_id=pipeline_run.id,
                step_name="generate_ai_insights",
                function=lambda: self._generate_ai_insights(
                    db
                )
            )

            # =====================================================
            # GENERATE REPORT STEP
            # =====================================================

            self._run_step(
                pipeline_repo=pipeline_repo,
                pipeline_run_id=pipeline_run.id,
                step_name="generate_report",
                function=lambda: self._generate_report(
                    db
                )
            )

            # =====================================================
            # PIPELINE SUCCESS UPDATE
            # =====================================================

            pipeline_repo.update_pipeline_run_status(
                pipeline_run=pipeline_run,
                status="SUCCESS",
                records_processed=len(
                    transformed_dataframe
                )
            )

            logger.info(
                f"Pipeline completed successfully: "
                f"{self.PIPELINE_NAME}"
            )

        except Exception as error:

            pipeline_repo.update_pipeline_run_status(
                pipeline_run=pipeline_run,
                status="FAILED",
                records_processed=0,
                error_message=str(error)
            )

            logger.exception(
                f"Pipeline failed: "
                f"{self.PIPELINE_NAME}"
            )

            raise

        finally:
            db.close()

    def _run_step(
        self,
        pipeline_repo: PipelineRepository,
        pipeline_run_id: int,
        step_name: str,
        function
    ):
        """
        Runs and tracks one pipeline step.
        """

        step = pipeline_repo.create_pipeline_step(
            pipeline_run_id=pipeline_run_id,
            step_name=step_name,
            status="RUNNING"
        )

        try:

            result = function()

            records_processed = (
                len(result)
                if hasattr(result, "__len__")
                else 0
            )

            pipeline_repo.update_pipeline_step_status(
                step=step,
                status="SUCCESS",
                records_processed=records_processed
            )

            return result

        except Exception as error:

            pipeline_repo.update_pipeline_step_status(
                step=step,
                status="FAILED",
                records_processed=0,
                error_message=str(error)
            )

            raise

    def _extract(
        self,
        pipeline_repo=None
    ):
        """
        Extracts raw sales data.
        """

        extractor = ExtractorFactory.create(
            source_type=self.source_type,
            **self.source_config
        )

        raw_dataframe = extractor.extract()

        if pipeline_repo:

            batch_identifier = (
                generate_batch_identifier(
                    "sales_csv"
                )
            )

            pipeline_repo.create_raw_data_batch(
                source_name=self.file_path,
                batch_identifier=batch_identifier,
                records_count=len(raw_dataframe),
                status="SUCCESS"
            )

            logger.info(
                f"Raw batch tracked: "
                f"{batch_identifier}"
            )

        return raw_dataframe

    def _transform(
        self,
        raw_dataframe
    ):
        """
        Transforms raw sales data.
        """

        transformer = SalesTransformer()

        return transformer.transform(
            raw_dataframe
        )

    def _validate(
        self,
        transformed_dataframe
    ):
        """
        Validates transformed sales data.
        """

        validator = SalesValidator()

        return validator.validate(
            transformed_dataframe
        )

    def _load(
        self,
        db,
        transformed_dataframe
    ):
        """
        Loads validated data into warehouse.
        """

        loader = OptimizedSalesLoader(db)

        loader.load(
            transformed_dataframe
        )

    def _calculate_kpis(
        self,
        db
    ):
        """
        Calculates daily business KPIs.
        """

        calculator = KPICalculator(db)

        return calculator.calculate_daily_kpis()

    def _detect_anomalies(
        self,
        db
    ):
        """
        Detects KPI anomalies.
        """

        detector = AnomalyDetector(db)

        return detector.detect_revenue_anomalies()

    def _generate_ai_insights(
            self,
            db
    ):
        """
        Generates AI-powered business insights.
        """

        generator = InsightGenerator(db)

        return generator.generate_daily_insight()

    def _generate_report(
            self,
            db
    ):
        """
        Generates daily business report.
        """

        generator = ReportGenerator(db)

        return generator.generate_daily_report()