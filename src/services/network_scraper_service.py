import re
import time
import random
import requests

from bs4 import BeautifulSoup

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

from src.models.product import Product


# ======================================
# USER AGENTS
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
    )
]


# ======================================
# BASE URL
# ======================================

BASE_URL = (
    "https://books.toscrape.com/"
    "catalogue/page-{}.html"
)


# ======================================
# HEADERS
# ======================================

def get_headers():

    return {
        "User-Agent": random.choice(USER_AGENTS)
    }


# ======================================
# SCRAPE SINGLE PAGE
# ======================================

def scrape_single_page(
    page,
    logger
):

    url = BASE_URL.format(page)

    logger.info(
        f"Scraping page {page}: {url}"
    )

    time.sleep(
        random.uniform(1, 2)
    )

    response = requests.get(
        url,
        headers=get_headers(),
        timeout=10
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "lxml"
    )

    cards = soup.find_all(
        "article",
        class_="product_pod"
    )

    products = []

    for card in cards:

        try:

            title = (
                card.h3.a["title"]
                .strip()
            )

            raw_price = (
                card.find(
                    "p",
                    class_="price_color"
                ).text
            )

            price = float(

                re.sub(
                    r"[^0-9.]",
                    "",
                    raw_price
                )
            )

            rating = (
                card.find(
                    "p",
                    class_="star-rating"
                )["class"][1]
            )

            availability = (
                "In stock"
                in
                card.find(
                    "p",
                    class_="instock availability"
                ).text
            )

            products.append(

                Product(
                    title=title,
                    price=price,
                    rating=rating,
                    availability=availability
                )
            )

        except Exception as error:

            logger.warning(
                f"Failed to parse product: {error}"
            )

    return products


# ======================================
# REQUESTS SCRAPER
# ======================================

def scrape_with_requests(
    pages,
    logger
):

    logger.info(
        f"Starting scraping for {pages} pages"
    )

    products = []

    with ThreadPoolExecutor(
        max_workers=5
    ) as executor:

        futures = [

            executor.submit(
                scrape_single_page,
                page,
                logger
            )

            for page in range(
                1,
                pages + 1
            )
        ]

        for future in as_completed(futures):

            products.extend(
                future.result()
            )

    logger.info(
        f"Scraping completed with "
        f"{len(products)} products"
    )

    return products