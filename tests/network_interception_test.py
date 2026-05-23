import asyncio
import sys

from pathlib import Path


# ======================================
# ADD PROJECT ROOT
# ======================================

ROOT_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(ROOT_DIR)
)

from src.core.logger import setup_logger

from src.services.network_scraper_service import (
    inspect_network_requests
)


async def main():

    logger = setup_logger()

    data = await inspect_network_requests(
        logger=logger
    )

    print(
        f"\nCaptured responses: "
        f"{len(data)}"
    )

    if data:

        print("\nFirst response:")

        print(data[0])


if __name__ == "__main__":

    asyncio.run(main())