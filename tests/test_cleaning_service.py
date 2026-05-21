import pandas as pd

from src.services.cleaning_service import (
    clean_products_dataframe
)


def test_remove_duplicates():

    """
    Test duplicate row removal.
    """

    data = {

        "Title": [
            "Book A",
            "Book A"
        ],

        "Price": [
            10.0,
            10.0
        ],

        "Rating": [
            "Five",
            "Five"
        ],

        "Availability": [
            "In stock",
            "In stock"
        ]
    }

    df = pd.DataFrame(data)

    cleaned_df = clean_products_dataframe(
        df=df,
        logger=None
    )

    assert len(cleaned_df) == 1