from src.models.product_model import Product


def test_product_object():

    """
    Validate Product object creation.
    """

    product = Product(
        title="Test Book",
        price=29.99,
        rating="Five",
        availability="In stock"
    )

    assert product.title == "Test Book"

    assert product.price == 29.99

    assert product.rating == "Five"