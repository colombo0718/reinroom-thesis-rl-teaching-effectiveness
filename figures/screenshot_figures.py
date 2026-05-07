"""
screenshot_figures.py — 把 figures/ 下的 HTML 圖表截圖成 images/

執行：
    cd C:\\Users\\USER\\論文 - RL平台教學成效
    python figures/screenshot_figures.py
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).parent.parent
FIGURES_DIR = Path(__file__).parent
IMAGES_DIR = ROOT / "images"

# (HTML 檔, 輸出 PNG 名)
FIGURES = [
    ("fig5-3-task-completion.html", "fig5-3.png"),
    ("fig5-1-pretest-posttest-box.html", "fig5-1.png"),
    ("fig5-2-gain-comparison.html", "fig5-2.png"),
    ("fig5-4-section3-comparison.html", "fig5-4.png"),
    ("fig5-5-sus-comparison.html", "fig5-5.png"),
]


async def shot_one(page, html_file: str, png_name: str):
    html_path = FIGURES_DIR / html_file
    if not html_path.exists():
        print(f"  ⚠ 跳過：{html_file}（不存在）")
        return False

    url = html_path.absolute().as_uri()
    await page.goto(url)
    await page.wait_for_load_state("networkidle")
    # 給 Chart.js 動畫完成的時間
    await asyncio.sleep(1.5)

    out_path = IMAGES_DIR / png_name
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # 截整個 viewport（HTML 已固定 1200x800）
    await page.screenshot(path=str(out_path), full_page=False)
    print(f"  ✅ {png_name}")
    return True


async def main():
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📁 輸出目錄：{IMAGES_DIR}\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1200, "height": 800})
        page = await context.new_page()

        for html_file, png_name in FIGURES:
            print(f"▶ {html_file}")
            await shot_one(page, html_file, png_name)

        await browser.close()
    print("\n完成。")


if __name__ == "__main__":
    asyncio.run(main())
