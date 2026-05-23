from src.database.database import (
    engine,
    Base
)

from src.database.product_model import (
    ProductDB
)

def create_tables():

    """
    Create database tables.
    """

    Base.metadata.create_all(
        bind=engine
    )


if __name__ == "__main__":

    create_tables()

    print(
        "PostgreSQL tables created successfully"
    )