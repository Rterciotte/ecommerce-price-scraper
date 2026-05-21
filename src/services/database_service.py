import sqlite3

from pathlib import Path

from core.config import DATABASE_PATH


def initialize_database(logger):

    """
    Create SQLite database and products table.

    Args:
        logger:
            Application logger instance.
    """

    logger.info(
        "Initializing SQLite database"
    )

    # ======================================
    # ENSURE DATABASE FOLDER EXISTS
    # ======================================

    db_path = Path(DATABASE_PATH)

    db_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # ======================================
    # CONNECT TO DATABASE
    # ======================================

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    # ======================================
    # CREATE PRODUCTS TABLE
    # ======================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price REAL,
            rating TEXT,
            availability TEXT
        )
        """
    )

    connection.commit()

    logger.info(
        "Database initialized successfully"
    )

    return connection


def save_products_to_database(
    connection,
    products,
    logger
):

    """
    Save scraped products into SQLite database.

    Args:
        connection:
            SQLite connection object.

        products:
            List of Product objects.

        logger:
            Application logger instance.
    """

    logger.info(
        f"Saving {len(products)} products "
        f"to database"
    )

    cursor = connection.cursor()

    for product in products:

        cursor.execute(
            """
            INSERT INTO products (
                title,
                price,
                rating,
                availability
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                product.title,
                product.price,
                product.rating,
                product.availability
            )
        )

    connection.commit()

    logger.info(
        "Products saved successfully"
    )