from fastapi import FastAPI

from src.core.logger import setup_logger

from src.services.scraper_service import (
    scrape_products
)

from src.models.product_model import Product


# ======================================
# INITIALIZATION
# ======================================

app = FastAPI(

    title="E-commerce Scraper API",

    version="1.0.0"
)

logger = setup_logger()


# ======================================
# ROOT ENDPOINT
# ======================================

@app.get("/")

def root():

    """
    Health check endpoint.
    """

    return {

        "status": "online",

        "service": "scraper-api"
    }


# ======================================
# SCRAPE PRODUCTS
# ======================================

@app.get("/scrape")

def scrape_endpoint(

    pages: int = 1
):

    """
    Scrape products endpoint.
    """

    logger.info(

        f"API scraping request "
        f"received for {pages} pages"
    )

    products = scrape_products(

        pages=pages,

        logger=logger
    )

    # ======================================
    # SERIALIZE PRODUCTS
    # ======================================

    serialized_products = [

        {

            "title": product.title,
            "price": product.price,
            "rating": product.rating,
            "availability": (
                product.availability
            )
        }

        for product in products
    ]

    return {

        "pages": pages,

        "total_products": (
            len(serialized_products)
        ),

        "products": serialized_products
    }