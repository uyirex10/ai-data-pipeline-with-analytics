from abc import ABC
from abc import abstractmethod

from app.core.logger import logger


class BaseExtractor(ABC):
    """
    Abstract base extractor.

    All extractors must inherit from this class.
    """

    @abstractmethod
    def extract(self):
        """
        Extract raw data from source.
        """
        pass

    def log_extraction_start(self, source_name: str):
        """
        Logs extraction start event.
        """

        logger.info(
            f"Starting extraction from source: {source_name}"
        )

    def log_extraction_success(
        self,
        source_name: str,
        records_count: int
    ):
        """
        Logs successful extraction.
        """

        logger.info(
            f"Successfully extracted "
            f"{records_count} records "
            f"from source: {source_name}"
        )

    def log_extraction_failure(
        self,
        source_name: str,
        error_message: str
    ):
        """
        Logs extraction failure.
        """

        logger.error(
            f"Extraction failed for source: "
            f"{source_name} | Error: {error_message}"
        )