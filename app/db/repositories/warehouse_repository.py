from sqlalchemy.orm import Session

from app.db.models import (
    CustomerDimension,
    ProductDimension,
    SalesFact
)


class WarehouseRepository:
    """
    Handles warehouse-related database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_customer(
        self,
        customer_name: str,
        email: str,
        city: str,
        country: str
    ) -> CustomerDimension:
        """
        Creates a customer dimension record.
        """

        customer = CustomerDimension(
            customer_name=customer_name,
            email=email,
            city=city,
            country=country
        )

        self.db.add(customer)

        self.db.commit()

        self.db.refresh(customer)

        return customer

    def create_product(
        self,
        product_name: str,
        category: str,
        unit_price: float
    ) -> ProductDimension:
        """
        Creates a product dimension record.
        """

        product = ProductDimension(
            product_name=product_name,
            category=category,
            unit_price=unit_price
        )

        self.db.add(product)

        self.db.commit()

        self.db.refresh(product)

        return product

    def create_sale(
        self,
        customer_id: int,
        product_id: int,
        quantity: int,
        revenue: float,
        sale_timestamp
    ) -> SalesFact:
        """
        Creates a sales fact record.
        """

        sale = SalesFact(
            customer_id=customer_id,
            product_id=product_id,
            quantity=quantity,
            revenue=revenue,
            sale_timestamp=sale_timestamp
        )

        self.db.add(sale)

        self.db.commit()

        self.db.refresh(sale)

        return sale