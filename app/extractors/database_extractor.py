import pandas as pd

from sqlalchemy import create_engine

from app.core.logger import logger
from app.extractors.base_extractor import BaseExtractor


class DatabaseExtractor(BaseExtractor):
    """
    Extracts data from SQL databases.
    """

    def __init__(
        self,
        connection_string: str,
        query: str
    ):
        self.connection_string = connection_string
        self.query = query

    def extract(self):
        """
        Extracts data from database query.
        """

        try:

            self.log_extraction_start(
                "database"
            )

            engine = create_engine(
                self.connection_string
            )

            dataframe = pd.read_sql(
                self.query,
                engine
            )

            self.log_extraction_success(
                len(dataframe),
                "database"
            )

            return dataframe

        except Exception as error:

            self.log_extraction_failure(
                str(error)
            )

            raise