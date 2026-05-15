from abc import ABC
from abc import abstractmethod

from app.core.logger import logger


class BaseTransformer(ABC):
    """
    Abstract base transformer.
    """

    @abstractmethod
    def transform(self, dataframe):
        """
        Transform raw dataframe.
        """
        pass

    def log_transformation_start(self):
        """
        Logs transformation start.
        """

        logger.info(
            "Starting dataframe transformation..."
        )

    def log_transformation_success(
        self,
        original_shape,
        transformed_shape
    ):
        """
        Logs successful transformation.
        """

        logger.info(
            f"Transformation successful | "
            f"Original Shape: {original_shape} | "
            f"Transformed Shape: {transformed_shape}"
        )

    def log_transformation_failure(
        self,
        error_message: str
    ):
        """
        Logs transformation failure.
        """

        logger.error(
            f"Transformation failed: {error_message}"
        )