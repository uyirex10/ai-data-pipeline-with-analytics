from app.extractors.csv_extractor import CSVExtractor
from app.extractors.api_extractor import APIExtractor
from app.extractors.database_extractor import DatabaseExtractor


class ExtractorFactory:
    """
    Factory for creating extractors.
    """

    @staticmethod
    def create(
        source_type: str,
        **kwargs
    ):
        """
        Creates extractor instance.
        """

        if source_type == "csv":

            return CSVExtractor(
                file_path=kwargs["file_path"]
            )

        elif source_type == "api":

            return APIExtractor(
                api_url=kwargs["api_url"]
            )

        elif source_type == "database":

            return DatabaseExtractor(
                connection_string=kwargs[
                    "connection_string"
                ],
                query=kwargs["query"]
            )

        else:

            raise ValueError(
                f"Unsupported source type: "
                f"{source_type}"
            )