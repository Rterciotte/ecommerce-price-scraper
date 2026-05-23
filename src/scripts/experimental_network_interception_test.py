import asyncio

from playwright.async_api import (
    async_playwright
)


async def intercept_requests():

    async with async_playwright() as playwright:

        browser = await playwright.chromium.launch(
            headless=True
        )

        page = await browser.new_page()

        async def handle_route(route):

            request = route.request

            print(
                f"{request.method} -> {request.url}"
            )

            await route.continue_()

        await page.route(
            "**/*",
            handle_route
        )

        await page.goto(
            "https://books.toscrape.com/"
        )

        await page.wait_for_timeout(3000)

        await browser.close()


if __name__ == "__main__":

    asyncio.run(
        intercept_requests()
    )