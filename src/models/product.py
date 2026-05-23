from dataclasses import dataclass


@dataclass
class Product:

    """
    Product domain model used during scraping.
    """

    title: str

    price: float

    rating: str

    availability: bool