import pandas as pd

from sqlalchemy import text

from database.database import engine
from models.product_model import ProductDB
from models.product_price_model import ProductPriceDB


def load_products():

    query = text(
        """
        SELECT
            p.id,
            p.title,
            pp.price,
            p.rating,
            p.availability,
            pp.scraped_at
        FROM products p
        JOIN product_prices pp
            ON p.id = pp.product_id
        WHERE pp.scraped_at = (
            SELECT MAX(pp2.scraped_at)
            FROM product_prices pp2
            WHERE pp2.product_id = p.id
        )
        ORDER BY pp.price ASC
        """
    )

    with engine.connect() as connection:

        df = pd.read_sql(
            query,
            connection
        )

    return df


def load_price_history():

    query = text(
        """
        SELECT
            p.title,
            pp.price,
            pp.scraped_at
        FROM product_prices pp
        JOIN products p
            ON p.id = pp.product_id
        ORDER BY pp.scraped_at ASC
        """
    )

    with engine.connect() as connection:

        df = pd.read_sql(
            query,
            connection
        )

    return df