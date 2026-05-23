import asyncio
import sys

from pathlib import Path


# ======================================
# ADD SRC TO PYTHON PATH
# ======================================

ROOT_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(ROOT_DIR)
)


from src.core.logger import setup_logger

from src.services.playwright_scraper_service import (
    scrape_dynamic_products
)


async def main():

    logger = setup_logger()

    products = await scrape_dynamic_products(
        pages=5,
        logger=logger
    )

    print(
        f"\nTotal products scraped: "
        f"{len(products)}"
    )

    if products:

        print("\nFirst product:")

        print(products[0])


if __name__ == "__main__":

    asyncio.run(main())