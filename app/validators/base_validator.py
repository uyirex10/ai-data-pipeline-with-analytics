from abc import ABC, abstractmethod

from app.core.logger import logger


class BaseValidator(ABC):
    """
    Abstract base validator.
    """

    @abstractmethod
    def validate(self, dataframe):
        """
        Validate dataframe.
        """
        pass

    def log_validation_start(self):
        logger.info("Starting data validation...")

    def log_validation_success(self):
        logger.info("Data validation completed successfully.")

    def log_validation_failure(self, error_message: str):
        logger.error(f"Data validation failed: {error_message}")