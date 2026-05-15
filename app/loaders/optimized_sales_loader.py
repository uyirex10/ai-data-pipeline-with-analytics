from datetime import datetime

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.models import (
    CustomerDimension,
    ProductDimension,
    SalesFact
)
from app.loaders.base_loader import BaseLoader


class OptimizedSalesLoader(BaseLoader):
    """
    Optimized bulk warehouse loader.
    """

    def __init__(self, db: Session):
        self.db = db

    def load(self, dataframe):
        """
        Bulk loads validated dataframe.
        """

        try:

            self.log_loading_start()

            # =====================================================
            # PRELOAD EXISTING CUSTOMERS
            # =====================================================

            existing_customers = {
                customer.email: customer
                for customer in (
                    self.db.query(CustomerDimension)
                    .all()
                )
            }

            # =====================================================
            # PRELOAD EXISTING PRODUCTS
            # =====================================================

            existing_products = {
                product.product_name: product
                for product in (
                    self.db.query(ProductDimension)
                    .all()
                )
            }

            new_customers = []

            new_products = []

            sales_records = []

            # =====================================================
            # PROCESS DATAFRAME
            # =====================================================

            for _, row in dataframe.iterrows():

                email = row["email"]

                product_name = row["product_name"]

                # =================================================
                # CUSTOMER HANDLING
                # =================================================

                if email not in existing_customers:

                    customer = CustomerDimension(
                        customer_name=row["customer_name"],
                        email=email,
                        city=row["city"],
                        country=row["country"]
                    )

                    new_customers.append(customer)

                    existing_customers[email] = customer

                # =================================================
                # PRODUCT HANDLING
                # =================================================

                if product_name not in existing_products:

                    product = ProductDimension(
                        product_name=product_name,
                        category=row["category"],
                        unit_price=float(
                            row["unit_price"]
                        )
                    )

                    new_products.append(product)

                    existing_products[
                        product_name
                    ] = product

            # =====================================================
            # BULK INSERT DIMENSIONS
            # =====================================================

            if new_customers:

                self.db.bulk_save_objects(
                    new_customers
                )

            if new_products:

                self.db.bulk_save_objects(
                    new_products
                )

            self.db.flush()

            # =====================================================
            # BUILD SALES FACTS
            # =====================================================

            for _, row in dataframe.iterrows():

                customer = existing_customers[
                    row["email"]
                ]

                product = existing_products[
                    row["product_name"]
                ]

                sale = SalesFact(
                    customer_id=customer.id,
                    product_id=product.id,
                    quantity=int(row["quantity"]),
                    revenue=float(row["revenue"]),
                    sale_timestamp=datetime.utcnow()
                )

                sales_records.append(sale)

            # =====================================================
            # BULK INSERT SALES FACTS
            # =====================================================

            self.db.bulk_save_objects(
                sales_records
            )

            self.db.commit()

            self.log_loading_success(
                len(sales_records)
            )

        except Exception as error:

            self.db.rollback()

            self.log_loading_failure(
                str(error)
            )

            logger.exception(error)

            raise