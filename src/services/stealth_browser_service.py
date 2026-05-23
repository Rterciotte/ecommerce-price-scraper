import random

from playwright.async_api import (
    async_playwright
)


# ======================================
# USER AGENTS
# ======================================

USER_AGENTS = [

    (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/136.0 Safari/537.36"
    ),

    (
        "Mozilla/5.0 "
        "(Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) "
        "Version/17.0 Safari/605.1.15"
    )
]


# ======================================
# CREATE STEALTH BROWSER
# ======================================

async def create_stealth_browser():

    """
    Create stealth Playwright browser.
    """

    playwright = await async_playwright().start()

    browser = await playwright.chromium.launch(

        headless=False,

        args=[

            "--disable-blink-features=AutomationControlled",

            "--disable-dev-shm-usage",

            "--no-sandbox"
        ]
    )

    context = await browser.new_context(

        user_agent=random.choice(
            USER_AGENTS
        ),

        viewport={
            "width": 1920,
            "height": 1080
        },

        locale="en-US",

        timezone_id="America/Sao_Paulo",

        color_scheme="dark"
    )

    # ======================================
    # STEALTH JAVASCRIPT
    # ======================================

    await context.add_init_script(

        """
        Object.defineProperty(
            navigator,
            'webdriver',
            {
                get: () => undefined
            }
        );

        Object.defineProperty(
            navigator,
            'languages',
            {
                get: () => ['en-US', 'en']
            }
        );

        Object.defineProperty(
            navigator,
            'platform',
            {
                get: () => 'Win32'
            }
        );

        Object.defineProperty(
            navigator,
            'hardwareConcurrency',
            {
                get: () => 8
            }
        );

        window.chrome = {
            runtime: {}
        };
        """
    )

    return playwright, browser, context