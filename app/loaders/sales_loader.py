from datetime import datetime

import pandas as pd

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.models import (
    CustomerDimension,
    ProductDimension,
    SalesFact
)
from app.loaders.base_loader import BaseLoader


class SalesLoader(BaseLoader):
    """
    Loads validated sales data into warehouse.
    """

    def __init__(self, db: Session):
        self.db = db

    def load(
        self,
        dataframe: pd.DataFrame
    ):
        """
        Loads dataframe into warehouse tables.
        """

        try:
            self.log_loading_start()

            records_loaded = 0

            for _, row in dataframe.iterrows():

                customer = self._get_or_create_customer(row)

                product = self._get_or_create_product(row)

                sale = SalesFact(
                    customer_id=customer.id,
                    product_id=product.id,
                    quantity=int(row["quantity"]),
                    revenue=float(row["revenue"]),
                    sale_timestamp=datetime.utcnow()
                )

                self.db.add(sale)

                records_loaded += 1

            self.db.commit()

            self.log_loading_success(records_loaded)

        except Exception as error:

            self.db.rollback()

            self.log_loading_failure(str(error))

            logger.exception(error)

            raise

    def _get_or_create_customer(
        self,
        row
    ) -> CustomerDimension:
        """
        Finds existing customer or creates new one.
        """

        customer = (
            self.db.query(CustomerDimension)
            .filter(
                CustomerDimension.email == row["email"]
            )
            .first()
        )

        if customer:
            return customer

        customer = CustomerDimension(
            customer_name=row["customer_name"],
            email=row["email"],
            city=row["city"],
            country=row["country"]
        )

        self.db.add(customer)

        self.db.flush()

        return customer

    def _get_or_create_product(
        self,
        row
    ) -> ProductDimension:
        """
        Finds existing product or creates new one.
        """

        product = (
            self.db.query(ProductDimension)
            .filter(
                ProductDimension.product_name
                == row["product_name"]
            )
            .first()
        )

        if product:
            return product

        product = ProductDimension(
            product_name=row["product_name"],
            category=row["category"],
            unit_price=float(row["unit_price"])
        )

        self.db.add(product)

        self.db.flush()

        return product