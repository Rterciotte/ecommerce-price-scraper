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
from core.config import (
    OUTPUT_EXCEL,
    OUTPUT_CSV
)

from services.scraper_service import scrape_products
from services.export_service import export_data
from services.formatting_service import format_excel
from services.dashboard_service import create_dashboard
from services.chart_service import create_charts
from services.cleaning_service import clean_products_dataframe
from services.database_service import (
    initialize_database,
    save_products_to_database
)


# ======================================
# CONFIGURATION FILE
# ======================================

CONFIG_PATH = "config/config.json"


def load_config():

    """
    Load application configuration file.

    Returns:
        dict:
            Application configuration dictionary.
    """

    with open(CONFIG_PATH, "r") as file:
        return json.load(file)


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

        connection = initialize_database(
            logger
        )

        # ======================================
        # LOAD CONFIGURATION FILE
        # ======================================

        config = load_config()

        # Default output paths
        output_excel = config["output_excel"]

        output_csv = config["output_csv"]

        # ======================================
        # PARSE CLI ARGUMENTS
        # ======================================

        args = parse_arguments()

        pages = args.pages

        # Override output path if provided
        if args.output:
            output_excel = args.output

        logger.info(
            f"Configured to scrape {pages} pages"
        )

        # ======================================
        # EXECUTE SCRAPING PROCESS
        # ======================================

        products = scrape_products(
            pages=pages,
            logger=logger
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
        # SAVE CLEANED DATA TO SQLITE
        # ======================================

        save_products_to_database(
            connection=connection,
            products=products,
            logger=logger
        )

        # ======================================
        # RE-EXPORT CLEANED DATA
        # ======================================

        df.to_excel(
            output_excel,
            index=False
        )

        # ======================================
        # APPLY EXCEL FORMATTING
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
        # CREATE DASHBOARD
        # ======================================

        create_dashboard(
            workbook=workbook,
            df=df,
            logger=logger
        )

        # ======================================
        # CREATE CHARTS
        # ======================================

        create_charts(
            workbook=workbook,
            df=df
        )

        # ======================================
        # SAVE FINAL WORKBOOK
        # ======================================

        workbook.save(
            output_excel
        )

        # ======================================
        # CLOSE DATABASE CONNECTION
        # ======================================

        connection.close()

        logger.info(
            "Automation finished successfully"
        )

    except Exception as error:

        logger.exception(error)


if __name__ == "__main__":
    main()