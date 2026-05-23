from src.services.scraper_factory_service import (
    scrape_products
)

from src.core.logger import setup_logger


def test_requests_scraper():

    logger = setup_logger()

    products = scrape_products(
        strategy="requests",
        pages=1,
        logger=logger
    )

    assert len(products) > 0

    first_product = products[0]

    assert first_product.title is not None
    assert first_product.price > 0