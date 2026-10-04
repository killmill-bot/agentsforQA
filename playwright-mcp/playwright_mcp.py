import asyncio

from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright

mcp = FastMCP("playwright-mcp")

_playwright = None
_browser = None
_page = None


async def get_page():
    global _playwright, _browser, _page

    if _page is None:
        _playwright = await async_playwright().start()
        _browser = await _playwright.chromium.launch(headless=False)
        _page = await _browser.new_page()

    return _page


@mcp.tool()
async def navigate(url: str) -> str:
    """Navigate the browser to a URL."""
    try:
        page = await get_page()
        await page.goto(url, wait_until="domcontentloaded")
        title = await page.title()
        return f"Navigated to: {url}\nPage title: {title}"
    except Exception as e:
        return f"Error navigating to {url}: {e}"


@mcp.tool()
async def click(selector: str) -> str:
    """Click an element using a CSS selector."""
    try:
        page = await get_page()
        await page.locator(selector).click()
        return f"Clicked element: {selector}"
    except Exception as e:
        return f"Error clicking element {selector}: {e}"


@mcp.tool()
async def fill(selector: str, value: str) -> str:
    """Fill an input field on the current page."""
    try:
        page = await get_page()
        await page.locator(selector).fill(value)
        return f"Filled {selector}"
    except Exception as e:
        return f"Error filling {selector}: {e}"


@mcp.tool()
async def evaluate_js(script: str) -> str:
    """Execute JavaScript in the current browser page."""
    try:
        page = await get_page()
        result = await page.evaluate(script)
        return str(result)
    except Exception as e:
        return f"Error executing JavaScript: {e}"


@mcp.tool()
async def get_text() -> str:
    """Get visible text content from the current page."""
    try:
        page = await get_page()
        text = await page.locator("body").inner_text()

        if len(text) > 2000:
            text = text[:2000] + "\n... (truncated)"

        return f"Page text content:\n\n{text}"
    except Exception as e:
        return f"Error getting text: {e}"


@mcp.tool()
async def get_current_url() -> str:
    """Return the current page URL."""
    try:
        page = await get_page()
        return f"Current URL: {page.url}"
    except Exception as e:
        return f"Error getting current URL: {e}"


@mcp.tool()
async def get_page_title() -> str:
    """Return the title of the current page."""
    try:
        page = await get_page()
        return await page.title()
    except Exception as e:
        return f"Error getting page title: {e}"


if __name__ == "__main__":
    mcp.run()