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

from src.services.stealth_browser_service import (
    create_stealth_browser
)


async def main():

    playwright, browser, context = (
        await create_stealth_browser()
    )

    page = await context.new_page()

    await page.goto(
        "https://bot.sannysoft.com/",
        wait_until="domcontentloaded"
    )

    print(
        "\nStealth browser running..."
    )

    await page.wait_for_timeout(15000)

    await browser.close()

    await playwright.stop()


if __name__ == "__main__":

    asyncio.run(main())