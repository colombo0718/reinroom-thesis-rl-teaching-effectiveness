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

# (HTML 檔, 輸出 PNG 名, viewport 寬, viewport 高)
# 註：移除 title/subtitle/footnote 後，body height 已縮減
FIGURES = [
    ("fig3-2-protocol-flow.html",       "fig3-2.png", 1200, 800),
    ("fig3-3-qlearning-flow.html",      "fig3-3.png",  900, 620),
    ("fig3-4-dqn-bidirectional.html",   "fig3-4.png",  800, 500),
    ("fig4-1-experiment-flow.html",     "fig4-1.png", 1400, 980),
    ("fig5-1-pretest-posttest-box.html","fig5-1.png", 1200, 640),
    ("fig5-2-gain-comparison.html",     "fig5-2.png", 1200, 640),
    ("fig5-3-task-completion.html",     "fig5-3.png", 1200, 640),
    ("fig5-4-section3-comparison.html", "fig5-4.png", 1200, 640),
    ("fig5-5-sus-comparison.html",      "fig5-5.png", 1200, 640),
]


async def shot_one(context, html_file: str, png_name: str, w: int, h: int):
    html_path = FIGURES_DIR / html_file
    if not html_path.exists():
        print(f"  ⚠ 跳過：{html_file}（不存在）")
        return False

    page = await context.new_page()
    await page.set_viewport_size({"width": w, "height": h})
    url = html_path.absolute().as_uri()
    await page.goto(url)
    await page.wait_for_load_state("networkidle")
    # 給 Chart.js / Mermaid 渲染完成的時間
    await asyncio.sleep(2.5)

    out_path = IMAGES_DIR / png_name
    out_path.parent.mkdir(parents=True, exist_ok=True)
    await page.screenshot(path=str(out_path), full_page=False)
    await page.close()
    print(f"  ✅ {png_name}  ({w}x{h})")
    return True


async def main():
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📁 輸出目錄：{IMAGES_DIR}\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        for html_file, png_name, w, h in FIGURES:
            print(f"▶ {html_file}")
            await shot_one(context, html_file, png_name, w, h)

        await browser.close()
    print("\n完成。")


if __name__ == "__main__":
    asyncio.run(main())
