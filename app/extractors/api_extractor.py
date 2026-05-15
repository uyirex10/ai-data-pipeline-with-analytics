import pandas as pd
import requests

from app.core.logger import logger
from app.extractors.base_extractor import BaseExtractor


class APIExtractor(BaseExtractor):
    """
    Extracts data from REST APIs.
    """

    def __init__(
        self,
        api_url: str
    ):
        self.api_url = api_url

    def extract(self):
        """
        Extracts API JSON data.
        """

        try:

            self.log_extraction_start(
                self.api_url
            )

            response = requests.get(
                self.api_url,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            dataframe = pd.DataFrame(data)

            self.log_extraction_success(
                len(dataframe),
                self.api_url
            )

            return dataframe

        except Exception as error:

            self.log_extraction_failure(
                str(error)
            )

            raise