from src.database.database import (
    SessionLocal
)

from src.models.product_model import (
    ProductDB
)

from src.models.product_price_model import (
    ProductPriceDB
)


def main():

    session = SessionLocal()

    products = (
        session.query(ProductDB)
        .all()
    )

    for product in products:

        print("\n")
        print("=" * 50)

        print(
            f"PRODUCT: {product.title}"
        )

        print(
            f"RATING: {product.rating}"
        )

        print(
            f"AVAILABLE: "
            f"{product.availability}"
        )

        print("-" * 50)

        for price in product.price_history:

            print(
                f"${price.price} | "
                f"{price.scraped_at}"
            )

    session.close()


if __name__ == "__main__":

    main()