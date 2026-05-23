from datetime import (
    datetime,
    timezone
)

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime
)

from sqlalchemy.orm import relationship

from database.database import Base


class ProductDB(Base):

    """
    SQLAlchemy ORM model for products table.
    """

    __tablename__ = "products"

    # ======================================
    # PRIMARY KEY
    # ======================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # ======================================
    # PRODUCT DATA
    # ======================================

    title = Column(
        String,
        nullable=False,
        unique=True
    )

    rating = Column(
        String,
        nullable=False
    )

    availability = Column(
        Boolean,
        nullable=False
    )

    # ======================================
    # TIMESTAMPS
    # ======================================

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(
            timezone.utc
        )
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(
            timezone.utc
        ),
        onupdate=lambda: datetime.now(
            timezone.utc
        )
    )

    # ======================================
    # RELATIONSHIP
    # ======================================

    price_history = relationship(
        "ProductPriceDB",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    # ======================================
    # STRING REPRESENTATION
    # ======================================

    def __repr__(self):

        return (
            f"<ProductDB("
            f"id={self.id}, "
            f"title='{self.title}'"
            f")>"
        )