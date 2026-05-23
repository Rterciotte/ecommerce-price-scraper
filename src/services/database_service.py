from sqlalchemy.orm import Session

from src.database.database import (
    engine,
    SessionLocal,
    Base
)

from src.models.product_model import ProductDB

from src.models.product_price_model import (
    ProductPriceDB
)


# ======================================
# INITIALIZE DATABASE
# ======================================

def initialize_database(logger):

    """
    Create database tables and return session.
    """

    logger.info(
        "Initializing PostgreSQL database"
    )

    # Create all ORM tables
    Base.metadata.create_all(
        bind=engine
    )

    logger.info(
        "Database tables created successfully"
    )

    # Create session
    session = SessionLocal()

    logger.info(
        "Database session initialized"
    )

    return session


# ======================================
# SAVE PRODUCTS
# ======================================

def save_products_to_database(
    session: Session,
    products,
    logger
):

    """
    Save products and price history
    into PostgreSQL database.
    """

    logger.info(
        f"Saving {len(products)} products "
        f"to PostgreSQL database"
    )

    try:

        for scraped_product in products:

            # ======================================
            # CHECK IF PRODUCT EXISTS
            # ======================================

            existing_product = (
                session.query(ProductDB)
                .filter(
                    ProductDB.title
                    == scraped_product.title
                )
                .first()
            )

            # ======================================
            # CREATE NEW PRODUCT
            # ======================================

            if existing_product is None:

                new_product = ProductDB(

                    title=scraped_product.title,

                    rating=scraped_product.rating,

                    availability=(
                        scraped_product.availability
                    )
                )

                session.add(new_product)

                # Flush generates ID immediately
                session.flush()

                product_db = new_product

                logger.info(
                    f"Created product: "
                    f"{new_product.title}"
                )

            # ======================================
            # UPDATE EXISTING PRODUCT
            # ======================================

            else:

                existing_product.rating = (
                    scraped_product.rating
                )

                existing_product.availability = (
                    scraped_product.availability
                )

                product_db = existing_product

                logger.info(
                    f"Updated product: "
                    f"{existing_product.title}"
                )

            # ======================================
            # CREATE PRICE HISTORY SNAPSHOT
            # ======================================

            price_snapshot = ProductPriceDB(

                product_id=product_db.id,

                price=scraped_product.price
            )

            session.add(price_snapshot)

        # ======================================
        # COMMIT TRANSACTION
        # ======================================

        session.commit()

        logger.info(
            "Products and price history "
            "saved successfully"
        )

    except Exception as error:

        session.rollback()

        logger.exception(
            f"Failed to save products: "
            f"{error}"
        )

        raise

    finally:

        session.close()