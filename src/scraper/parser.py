from bs4 import BeautifulSoup


def parse_products(html: str):

    soup = BeautifulSoup(
        html,
        "lxml"
    )

    products = []

    articles = soup.find_all(
        "article",
        class_="product_pod"
    )

    for article in articles:

        title = article.h3.a["title"]

        price_text = article.find(
            "p",
            class_="price_color"
        ).text

        price = float(
            price_text.replace("£", "")
        )

        availability = article.find(
            "p",
            class_="instock availability"
        ).text.strip()

        rating = article.p["class"][1]

        products.append({
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "source": "Books To Scrape",
            "product_url": (
                "https://books.toscrape.com/"
            )
        })

    return products