import pandas as pd

from app.transformers.sales_transformer import SalesTransformer
from app.validators.base_validator import BaseValidator


class SalesValidator(BaseValidator):
    """
    Validates cleaned sales data before loading into warehouse.
    """

    REQUIRED_COLUMNS = SalesTransformer.REQUIRED_COLUMNS + [
        "average_item_price"
    ]

    def validate(self, dataframe: pd.DataFrame) -> bool:
        """
        Runs schema, data quality, and business rule validation.
        """

        try:
            self.log_validation_start()

            self._validate_required_columns(dataframe)
            self._validate_not_empty(dataframe)
            self._validate_no_missing_required_values(dataframe)
            self._validate_numeric_rules(dataframe)
            self._validate_email_format(dataframe)

            self.log_validation_success()

            return True

        except Exception as error:
            self.log_validation_failure(str(error))
            raise

    def _validate_required_columns(self, dataframe: pd.DataFrame):
        missing_columns = [
            column
            for column in self.REQUIRED_COLUMNS
            if column not in dataframe.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns after transformation: {missing_columns}"
            )

    def _validate_not_empty(self, dataframe: pd.DataFrame):
        if dataframe.empty:
            raise ValueError("Dataframe is empty after transformation.")

    def _validate_no_missing_required_values(self, dataframe: pd.DataFrame):
        required_fields = [
            "customer_name",
            "email",
            "product_name",
            "quantity",
            "revenue"
        ]

        missing_counts = dataframe[required_fields].isnull().sum()

        failed_fields = missing_counts[missing_counts > 0]

        if not failed_fields.empty:
            raise ValueError(
                f"Missing required values found: {failed_fields.to_dict()}"
            )

    def _validate_numeric_rules(self, dataframe: pd.DataFrame):
        if (dataframe["quantity"] <= 0).any():
            raise ValueError("Quantity must be greater than zero.")

        if (dataframe["revenue"] < 0).any():
            raise ValueError("Revenue cannot be negative.")

        if (dataframe["unit_price"] < 0).any():
            raise ValueError("Unit price cannot be negative.")

        if (dataframe["average_item_price"] < 0).any():
            raise ValueError("Average item price cannot be negative.")

    def _validate_email_format(self, dataframe: pd.DataFrame):
        invalid_emails = dataframe[
            ~dataframe["email"].str.contains("@", na=False)
        ]

        if not invalid_emails.empty:
            raise ValueError(
                f"Invalid email records found: {len(invalid_emails)}"
            )