from src.services.network_scraper_service import (
    scrape_with_requests
)

from src.services.playwright_scraper_service import (
    scrape_with_playwright
)


def scrape_products(
    strategy,
    pages,
    logger
):

    if strategy == "requests":
        return scrape_with_requests(
            pages,
            logger
        )

    if strategy == "playwright":
        return scrape_with_playwright(
            pages,
            logger
        )

    raise ValueError(
        f"Unknown strategy: {strategy}"
    )