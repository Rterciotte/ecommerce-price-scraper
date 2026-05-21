import argparse


def parse_arguments():

    """
    Parse command line arguments.
    """

    parser = argparse.ArgumentParser(
        description="Ecommerce Scraping Automation"
    )

    parser.add_argument(
        "--pages",
        type=int,
        default=5,
        help="Number of pages to scrape"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="output/products.xlsx",
        help="Output Excel file"
    )

    return parser.parse_args()