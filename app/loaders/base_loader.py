from abc import ABC
from abc import abstractmethod

from app.core.logger import logger


class BaseLoader(ABC):
    """
    Abstract base loader.
    """

    @abstractmethod
    def load(self, dataframe):
        """
        Load validated dataframe into warehouse.
        """
        pass

    def log_loading_start(self):
        logger.info("Starting warehouse loading...")

    def log_loading_success(
        self,
        records_loaded: int
    ):
        logger.info(
            f"Warehouse loading completed successfully. "
            f"Records Loaded: {records_loaded}"
        )

    def log_loading_failure(
        self,
        error_message: str
    ):
        logger.error(
            f"Warehouse loading failed: {error_message}"
        )