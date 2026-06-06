"""截整本簡報每一頁，給 Claude 自審版面用"""
import asyncio
import sys
from pathlib import Path
from playwright.async_api import async_playwright

OUT = Path(__file__).parent / "screenshots_check"
OUT.mkdir(exist_ok=True)

# 從 CLI 帶頁碼，例：python screenshot_check.py 11 21 22 23 24
if len(sys.argv) > 1:
    PAGES = [int(x) for x in sys.argv[1:]]
else:
    PAGES = list(range(1, 40))

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await ctx.new_page()
        for n in PAGES:
            url = f"http://localhost:3030/{n}?print"
            await page.goto(url, wait_until="networkidle")
            await page.wait_for_timeout(1500)
            shot = OUT / f"S{n:02d}.png"
            await page.screenshot(path=str(shot), full_page=False)
            print(f"  {shot.name}")
        await browser.close()

asyncio.run(main())
