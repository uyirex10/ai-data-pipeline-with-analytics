import pandas as pd

from app.extractors.base_extractor import BaseExtractor
from app.utils.retry import retry


class CSVExtractor(BaseExtractor):
    """
    Extracts raw data from CSV files.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    @retry(Exception, retries=3)
    def extract(self):
        """
        Extracts data from CSV file.
        """

        source_name = self.file_path

        self.log_extraction_start(source_name)

        dataframe = pd.read_csv(self.file_path)

        self.log_extraction_success(
            source_name=source_name,
            records_count=len(dataframe)
        )

        return dataframe