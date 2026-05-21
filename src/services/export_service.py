import pandas as pd

from dataclasses import asdict


def export_data(products, output_excel, output_csv, logger):

    """
    Export scraped products to CSV and Excel files.

    Args:
        products (list):
            List of Product objects.

        output_excel (str):
            Excel output path.

        output_csv (str):
            CSV output path.

        logger:
            Application logger instance.
    """

    logger.info(
        "Converting products to DataFrame"
    )

    # ======================================
    # CONVERT PRODUCTS TO DATAFRAME
    # ======================================

    data = [

        {
            "Title": product.title,
            "Price": product.price,
            "Rating": product.rating,
            "Availability": product.availability
        }

        for product in products
    ]

    # Create pandas DataFrame
    df = pd.DataFrame(data)

    logger.info(
        f"DataFrame created with {len(df)} rows"
    )

    # Export CSV file
    logger.info(
        f"Exporting CSV file: {output_csv}"
    )

    df.to_csv(
        output_csv,
        index=False
    )

    # Export Excel file
    logger.info(
        f"Exporting Excel file: {output_excel}"
    )

    with pd.ExcelWriter(
        output_excel,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="Products",
            index=False
        )

    logger.info(
        "Data export completed successfully"
    )

    return df