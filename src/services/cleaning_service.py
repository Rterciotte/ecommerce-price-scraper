import pandas as pd


def clean_products_dataframe(df, logger):

    """
    Clean and standardize scraped product dataframe.

    Steps:
    - Remove duplicates
    - Handle missing values
    - Standardize text fields
    - Convert prices to numeric
    - Normalize availability field

    Args:
        df (pd.DataFrame):
            Raw scraped dataframe.

        logger:
            Application logger instance.

    Returns:
        pd.DataFrame:
            Cleaned dataframe.
    """
    if logger:
        logger.info(
            "Starting dataframe cleaning pipeline"
        )

    # ======================================
    # CREATE SAFE COPY
    # ======================================

    df = df.copy()

    # ======================================
    # STANDARDIZE COLUMN NAMES
    # ======================================

    df.columns = [
        column.strip().title()
        for column in df.columns
    ]

    if logger:
        logger.info(
            f"Detected columns: {list(df.columns)}"
        )

    # ======================================
    # REMOVE DUPLICATES
    # ======================================

    initial_rows = len(df)

    df.drop_duplicates(
        inplace=True
    )

    removed_rows = initial_rows - len(df)

    if logger:
        logger.info(
            f"Removed {removed_rows} duplicate rows"
        )

    # ======================================
    # CLEAN TITLE COLUMN
    # ======================================

    if "Title" in df.columns:

        df["Title"] = (
            df["Title"]
            .astype(str)
            .str.strip()
        )

    # ======================================
    # CLEAN PRICE COLUMN
    # ======================================

    if "Price" in df.columns:

        df["Price"] = pd.to_numeric(
            df["Price"],
            errors="coerce"
        )

        df["Price"] = (
            df["Price"]
            .fillna(0)
            .round(2)
        )

    # ======================================
    # CLEAN RATING COLUMN
    # ======================================

    if "Rating" in df.columns:

        df["Rating"] = (
            df["Rating"]
            .astype(str)
            .str.strip()
            .str.title()
        )

    # ======================================
    # CLEAN AVAILABILITY COLUMN
    # ======================================

    if "Availability" in df.columns:

        df["Availability"] = (
            df["Availability"]
            .astype(str)
            .str.replace(
                "\n",
                " ",
                regex=False
            )
            .str.strip()
        )

    # ======================================
    # REMOVE EMPTY TITLES
    # ======================================

    if "Title" in df.columns:

        df = df[
            df["Title"] != ""
        ]

    if logger:
        logger.info(
            f"Cleaning pipeline completed with "
            f"{len(df)} rows"
        )

    return df