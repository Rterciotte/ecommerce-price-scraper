from datetime import (
    datetime,
    timezone
)

from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database.database import Base


class ProductPriceDB(Base):

    """
    SQLAlchemy ORM model for product
    price history table.
    """

    __tablename__ = "product_prices"

    # ======================================
    # PRIMARY KEY
    # ======================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # ======================================
    # FOREIGN KEY
    # ======================================

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    # ======================================
    # PRICE SNAPSHOT
    # ======================================

    price = Column(
        Float,
        nullable=False
    )

    # ======================================
    # SCRAPED TIMESTAMP
    # ======================================

    scraped_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(
            timezone.utc
        )
    )

    # ======================================
    # RELATIONSHIP
    # ======================================

    product = relationship(
        "ProductDB",
        back_populates="price_history"
    )

    # ======================================
    # STRING REPRESENTATION
    # ======================================

    def __repr__(self):

        return (
            f"<ProductPriceDB("
            f"id={self.id}, "
            f"product_id={self.product_id}, "
            f"price={self.price}"
            f")>"
        )