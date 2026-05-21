from unittest.mock import patch

from src.services.scraper_service import (
    scrape_single_page
)


# ======================================
# MOCK HTML RESPONSE
# ======================================

MOCK_HTML = """

<html>
    <body>

        <article class="product_pod">

            <h3>
                <a title="Test Book"></a>
            </h3>

            <p class="price_color">
                £29.99
            </p>

            <p class="star-rating Five"></p>

            <p class="instock availability">
                In stock
            </p>

        </article>

    </body>
</html>

"""


# ======================================
# MOCK RESPONSE CLASS
# ======================================

class MockResponse:

    status_code = 200

    text = MOCK_HTML

    def raise_for_status(self):
        pass


# ======================================
# TEST SCRAPER
# ======================================

@patch(
    "src.services.scraper_service.requests.get"
)

def test_scrape_single_page(mock_get):

    """
    Validate scraping logic.
    """

    mock_get.return_value = MockResponse()

    products = scrape_single_page(
        page=1,
        logger=None
    )

    assert len(products) == 1

    product = products[0]

    assert product.title == "Test Book"

    assert product.price == 29.99

    assert product.rating == "Five"

    assert product.availability == "In stock"