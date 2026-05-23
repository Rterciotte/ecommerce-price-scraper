import json
import sys

from pathlib import Path


# ======================================
# ADD SRC DIRECTORY TO PYTHON PATH
# ======================================

SRC_DIR = Path(__file__).resolve().parent

sys.path.insert(
    0,
    str(SRC_DIR)
)


# ======================================
# IMPORTS
# ======================================

from openpyxl import load_workbook

from core.cli import parse_arguments
from core.logger import setup_logger

from services.export_service import export_data
from services.formatting_service import format_excel
from services.cleaning_service import clean_products_dataframe

from services.database_service import (
    initialize_database,
    save_products_to_database
)

from services.scraper_factory_service import (
    scrape_products
)

# ======================================
# CONFIGURATION FILE
# ======================================

CONFIG_PATH = "config/config.json"


# ======================================
# LOAD CONFIGURATION
# ======================================

def load_config():

    """
    Load application configuration file.

    Returns:
        dict:
            Application configuration dictionary.
    """

    with open(CONFIG_PATH, "r") as file:

        return json.load(file)


# ======================================
# MAIN APPLICATION
# ======================================

def main():

    """
    Main application workflow.
    """

    # ======================================
    # INITIALIZE LOGGER
    # ======================================

    logger = setup_logger()

    logger.info(
        "Starting web scraping automation"
    )

    try:

        # ======================================
        # INITIALIZE DATABASE
        # ======================================

        session = initialize_database(
            logger
        )

        # ======================================
        # LOAD CONFIGURATION FILE
        # ======================================

        config = load_config()

        # ======================================
        # OUTPUT FILES
        # ======================================

        output_excel = config["output_excel"]

        output_csv = config["output_csv"]

        # ======================================
        # PARSE CLI ARGUMENTS
        # ======================================

        args = parse_arguments()

        pages = args.pages

        # ======================================
        # OVERRIDE OUTPUT FILE
        # ======================================

        if args.output:

            output_excel = args.output

        logger.info(
            f"Configured to scrape {pages} pages"
        )

        # ======================================
        # EXECUTE SCRAPING
        # ======================================

        products = scrape_products(
            strategy="requests",
            pages=pages,
            logger=logger
        )

        logger.info(
            f"Scraped {len(products)} products"
        )

        # ======================================
        # EXPORT RAW DATA
        # ======================================

        df = export_data(
            products=products,
            output_excel=output_excel,
            output_csv=output_csv,
            logger=logger
        )

        # ======================================
        # CLEAN DATAFRAME
        # ======================================

        df = clean_products_dataframe(
            df=df,
            logger=logger
        )

        # ======================================
        # SAVE PRODUCTS TO POSTGRESQL
        # ======================================

        save_products_to_database(
            session=session,
            products=products,
            logger=logger
        )

        # ======================================
        # EXPORT CLEANED DATA
        # ======================================

        df.to_excel(
            output_excel,
            index=False
        )

        # ======================================
        # FORMAT EXCEL FILE
        # ======================================

        format_excel(
            file_path=output_excel,
            logger=logger
        )

        # ======================================
        # LOAD WORKBOOK
        # ======================================

        workbook = load_workbook(
            output_excel
        )

        # ======================================
        # SAVE FINAL WORKBOOK
        # ======================================

        workbook.save(
            output_excel
        )

        logger.info(
            "Automation finished successfully"
        )

    except Exception as error:

        logger.exception(
            f"Application failed: {error}"
        )


# ======================================
# ENTRY POINT
# ======================================

if __name__ == "__main__":

    main()