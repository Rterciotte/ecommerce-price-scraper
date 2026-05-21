import re
import time
import random
import requests

from bs4 import BeautifulSoup

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

from streamlit import logger

from src.models.product import Product


# ======================================
# REQUEST HEADERS POOL
# ======================================

USER_AGENTS = [

    (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/136.0 Safari/537.36"
    ),

    (
        "Mozilla/5.0 "
        "(Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) "
        "Version/17.0 Safari/605.1.15"
    ),

    (
        "Mozilla/5.0 "
        "(X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/135.0 Safari/537.36"
    )
]

# ======================================
# BASE URL
# ======================================

BASE_URL = (
    "https://books.toscrape.com/"
    "catalogue/page-{}.html"
)


def get_headers():

    """
    Return randomized request headers.
    """

    return {
        "User-Agent": random.choice(USER_AGENTS)
    }


def scrape_single_page(page, logger):

    """
    Scrape a single catalogue page.
    """

    url = BASE_URL.format(page)
    
    if logger:
        logger.info(
            f"Scraping page {page}: {url}"
        )

    # Random delay
    time.sleep(
        random.uniform(1, 3)
    )

    response = None

    # ======================================
    # RETRY LOGIC
    # ======================================

    for attempt in range(3):

        try:

            response = requests.get(
                url,
                headers=get_headers(),
                timeout=10
            )

            response.raise_for_status()

            break

        except requests.RequestException as error:
            if logger:
                logger.warning(
                    f"Page {page} "
                    f"- Attempt {attempt + 1} failed: "
                    f"{error}"
                )

            time.sleep(2)

    if response is None:

        logger.warning(
            f"Skipping page {page}"
        )

        return []

    # ======================================
    # PARSE HTML
    # ======================================

    soup = BeautifulSoup(
        response.text,
        "lxml"
    )

    product_cards = soup.find_all(
        "article",
        class_="product_pod"
    )
    if logger:
        logger.info(
            f"Found {len(product_cards)} "
            f"products on page {page}"
        )

    page_products = []

    # ======================================
    # EXTRACT PRODUCT DATA
    # ======================================

    for card in product_cards:

        try:

            # Product title
            title = (
                card.h3.a["title"]
                .strip()
            )

            # Product price
            raw_price = (
                card
                .find(
                    "p",
                    class_="price_color"
                )
                .text
            )

            # Clean currency symbols
            price_text = re.sub(
                r"[^0-9.]",
                "",
                raw_price
            )

            price = float(price_text)

            # Product rating
            rating = (
                card.find(
                    "p",
                    class_="star-rating"
                )["class"][1]
            )

            # Product availability
            availability = (
                card.find(
                    "p",
                    class_="instock availability"
                )
                .text
                .strip()
            )

            # Create product object
            product = Product(
                title=title,
                price=price,
                rating=rating,
                availability=availability
            )

            page_products.append(product)

        except Exception as error:
            if logger:
                logger.warning(
                    f"Failed to parse product: {error}"
                )

    return page_products


def scrape_products(pages, logger):

    """
    Scrape multiple pages concurrently.
    """

    if logger:
        logger.info(
            f"Starting concurrent scraping "
            f"for {pages} pages"
        )

    products = []

    # ======================================
    # MULTITHREADING EXECUTOR
    # ======================================

    with ThreadPoolExecutor(
        max_workers=5
    ) as executor:

        futures = [

            executor.submit(
                scrape_single_page,
                page,
                logger
            )

            for page in range(1, pages + 1)
        ]

        for future in as_completed(futures):

            try:

                result = future.result()

                products.extend(result)

            except Exception as error:

                if logger:
                    logger.error(
                        f"Thread execution failed: "
                        f"{error}"
                    )

    if logger:
        logger.info(
            f"Concurrent scraping completed "
            f"with {len(products)} products"
        )

    return products