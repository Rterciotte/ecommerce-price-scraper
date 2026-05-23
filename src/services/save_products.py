from sqlalchemy.orm import Session

from src.models.product_model import ProductDB


def save_products(
    db: Session,
    products: list
):

    for product in products:

        db_product = ProductDB(
            title=product["title"],
            price=product["price"],
            rating=product["rating"],
            availability=product["availability"],
            source=product["source"],
            product_url=product["product_url"]
        )

        db.add(db_product)

    db.commit()