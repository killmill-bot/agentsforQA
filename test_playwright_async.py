import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        print("Async Playwright OK")

asyncio.run(main())