import re
import asyncio
import random

from playwright.async_api import (
    async_playwright
)

from src.models.product import Product


# ======================================
# BASE URL
# ======================================

BASE_URL = (
    "https://books.toscrape.com/"
    "catalogue/page-{}.html"
)


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
# SCRAPE SINGLE PAGE
# ======================================

async def scrape_dynamic_page(
    context,
    page_number,
    logger,
    semaphore
):

    """
    Scrape a single page using
    shared browser context.
    """

    async with semaphore:

        url = BASE_URL.format(
            page_number
        )

        logger.info(
            f"Playwright scraping "
            f"page {page_number}: {url}"
        )

        products = []

        page = await context.new_page()

        try:

            # ======================================
            # RANDOM HUMAN DELAY
            # ======================================

            await asyncio.sleep(
                random.uniform(1, 3)
            )

            # ======================================
            # LOAD PAGE
            # ======================================

            await page.goto(
                url,
                wait_until="networkidle",
                timeout=30000
            )

            # ======================================
            # WAIT FOR PRODUCTS
            # ======================================

            await page.wait_for_selector(
                "article.product_pod"
            )

            cards = await page.query_selector_all(
                "article.product_pod"
            )

            logger.info(
                f"Found {len(cards)} products "
                f"on page {page_number}"
            )

            # ======================================
            # EXTRACT PRODUCTS
            # ======================================

            for card in cards:

                try:

                    title = await card.eval_on_selector(
                        "h3 a",
                        """
                        el => el.getAttribute('title')
                        """
                    )

                    raw_price = await card.eval_on_selector(
                        ".price_color",
                        """
                        el => el.textContent
                        """
                    )

                    price_text = re.sub(
                        r"[^0-9.]",
                        "",
                        raw_price
                    )

                    price = float(
                        price_text
                    )

                    rating = await card.eval_on_selector(
                        "p.star-rating",
                        """
                        el => el.classList[1]
                        """
                    )

                    availability = (
                        await card.eval_on_selector(
                            ".instock.availability",
                            """
                            el => el.textContent.trim()
                            """
                        )
                    )

                    product = Product(
                        title=title,
                        price=price,
                        rating=rating,
                        availability=availability
                    )

                    products.append(product)

                except Exception as error:

                    logger.warning(
                        f"Failed to parse product "
                        f"on page {page_number}: "
                        f"{error}"
                    )

        except Exception as error:

            logger.error(
                f"Page scraping failed "
                f"for page {page_number}: "
                f"{error}"
            )

        finally:

            await page.close()

        return products


# ======================================
# SCRAPE MULTIPLE PAGES
# ======================================

async def scrape_dynamic_products(
    pages,
    logger
):

    """
    Execute concurrent Playwright scraping.
    """

    logger.info(
        f"Starting async Playwright "
        f"scraping for {pages} pages"
    )

    all_products = []

    # ======================================
    # CONCURRENCY LIMIT
    # ======================================

    semaphore = asyncio.Semaphore(5)

    async with async_playwright() as playwright:

        # ======================================
        # LAUNCH BROWSER
        # ======================================

        browser = await playwright.chromium.launch(
            headless=True
        )

        # ======================================
        # CREATE SHARED CONTEXT
        # ======================================

        context = await browser.new_context(

            user_agent=random.choice(
                USER_AGENTS
            ),

            viewport={
                "width": 1920,
                "height": 1080
            },

            locale="en-US",

            timezone_id="America/Sao_Paulo"
        )

        # ======================================
        # CREATE TASKS
        # ======================================

        tasks = [

            scrape_dynamic_page(
                context=context,
                page_number=page,
                logger=logger,
                semaphore=semaphore
            )

            for page in range(
                1,
                pages + 1
            )
        ]

        # ======================================
        # EXECUTE TASKS
        # ======================================

        results = await asyncio.gather(
            *tasks
        )

        # ======================================
        # FLATTEN RESULTS
        # ======================================

        for result in results:

            all_products.extend(
                result
            )

        await context.close()

        await browser.close()

    logger.info(
        f"Playwright scraping completed "
        f"with {len(all_products)} products"
    )

    return all_products

# ======================================
# PUBLIC PLAYWRIGHT SCRAPER
# ======================================

def scrape_with_playwright(
    pages,
    logger
):

    """
    Synchronous wrapper for
    async Playwright scraper.
    """

    return asyncio.run(
        scrape_dynamic_products(
            pages=pages,
            logger=logger
        )
    )