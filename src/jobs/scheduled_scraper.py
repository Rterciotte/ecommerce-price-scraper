from src.core.logger import setup_logger

from src.services.scraper_service import (
    scrape_products
)

from src.services.export_service import (
    export_data
)

from src.services.cleaning_service import (
    clean_products_dataframe
)

from src.services.database_service import (
    initialize_database,
    save_products_to_database
)


# ======================================
# LOGGER
# ======================================

logger = setup_logger()


# ======================================
# SCHEDULED JOB
# ======================================

def run_scheduled_scraping():

    """
    Execute scheduled scraping pipeline.
    """

    logger.info(
        "Starting scheduled scraping job"
    )

    try:

        # ======================================
        # INITIALIZE DATABASE
        # ======================================

        connection = initialize_database(
            logger
        )

        # ======================================
        # SCRAPE PRODUCTS
        # ======================================

        products = scrape_products(

            pages=2,

            logger=logger
        )

        # ======================================
        # EXPORT DATA
        # ======================================

        df = export_data(

            products=products,

            output_excel=(
                "output/products.xlsx"
            ),

            output_csv=(
                "output/products.csv"
            ),

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
        # SAVE DATABASE
        # ======================================

        save_products_to_database(

            connection=connection,

            products=products,

            logger=logger
        )

        logger.info(
            "Scheduled scraping job "
            "completed successfully"
        )

    except Exception as error:

        logger.exception(error)