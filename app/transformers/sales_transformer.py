import pandas as pd

from app.transformers.base_transformer import BaseTransformer


class SalesTransformer(BaseTransformer):
    """
    Cleans and transforms sales data.
    """

    REQUIRED_COLUMNS = [
        "customer_name",
        "email",
        "city",
        "country",
        "product_name",
        "category",
        "unit_price",
        "quantity",
        "revenue"
    ]

    def transform(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Cleans and standardizes sales dataframe.
        """

        try:
            self.log_transformation_start()

            original_shape = dataframe.shape

            dataframe = dataframe.copy()

            dataframe.columns = [
                column.strip().lower()
                for column in dataframe.columns
            ]

            missing_columns = [
                column
                for column in self.REQUIRED_COLUMNS
                if column not in dataframe.columns
            ]

            if missing_columns:
                raise ValueError(
                    f"Missing required columns: "
                    f"{missing_columns}"
                )

            dataframe = dataframe.drop_duplicates()

            dataframe["customer_name"] = (
                dataframe["customer_name"]
                .astype(str)
                .str.strip()
                .str.title()
            )

            dataframe["email"] = (
                dataframe["email"]
                .astype(str)
                .str.strip()
                .str.lower()
            )

            dataframe["city"] = (
                dataframe["city"]
                .astype(str)
                .str.strip()
                .str.title()
            )

            dataframe["country"] = (
                dataframe["country"]
                .astype(str)
                .str.strip()
                .str.title()
            )

            dataframe["product_name"] = (
                dataframe["product_name"]
                .astype(str)
                .str.strip()
                .str.title()
            )

            dataframe["category"] = (
                dataframe["category"]
                .astype(str)
                .str.strip()
                .str.title()
            )

            numeric_columns = [
                "unit_price",
                "quantity",
                "revenue"
            ]

            for column in numeric_columns:

                dataframe[column] = pd.to_numeric(
                    dataframe[column],
                    errors="coerce"
                )

            dataframe = dataframe.dropna(
                subset=numeric_columns
            )

            dataframe["average_item_price"] = (
                dataframe["revenue"] /
                dataframe["quantity"]
            )

            transformed_shape = dataframe.shape

            self.log_transformation_success(
                original_shape=original_shape,
                transformed_shape=transformed_shape
            )

            return dataframe

        except Exception as error:

            self.log_transformation_failure(
                str(error)
            )

            raise