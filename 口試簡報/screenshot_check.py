"""快速截 S12/S13/S14 三頁檢查版面"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

OUT = Path(__file__).parent / "screenshots_check"
OUT.mkdir(exist_ok=True)

PAGES = [12, 13, 14]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await ctx.new_page()
        for n in PAGES:
            url = f"http://localhost:3030/{n}?print"
            await page.goto(url, wait_until="networkidle")
            await page.wait_for_timeout(2000)
            shot = OUT / f"S{n:02d}.png"
            await page.screenshot(path=str(shot), full_page=False)
            print(f"  {shot.name}")
        await browser.close()

asyncio.run(main())
