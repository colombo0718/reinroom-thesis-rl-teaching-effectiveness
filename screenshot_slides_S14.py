"""screenshot_slides_S14.py — 給口試簡報 S14 用的「分析 Tab 上+中排合成」單張截圖
複用 screenshot_3_3_analysis.py 的 helpers，但只截一張 4 圖合成（上排 + 中排）。

輸出：images/fig3-analysis-top4.png（給簡報用，論文 fig3-9 不動）
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

RR_URL  = "https://reinroom.leaflune.org/en/"
GAME_URL = "https://reinroom.leaflune.org/games/Maze2D_emoji_en.html"
OUT = Path(r"C:\Users\USER\論文 - RL平台教學成效\images\fig3-analysis-top4.png")

# 上排 + 中排，共 4 個 selector
SELECTORS = [
    '#p1-acti-color', '#p1-bars-value',     # 上排
    '#p1-line-value', '#p1-diff-value',     # 中排
]
TARGET_EPISODES = 80


async def wait(ms=600):
    await asyncio.sleep(ms / 1000)


async def click_tab(page, subtab):
    await page.click(f'button[data-subtab="{subtab}"]')
    await wait(600)


async def set_slider(page, sid, value):
    await page.evaluate(f"""
        const el = document.getElementById('{sid}');
        if (el) {{ el.value = {value}; el.dispatchEvent(new Event('input')); }}
    """)
    await wait(200)


async def load_game(page, url):
    await page.fill('#gameUrlInput', url)
    await page.click('#loadGame')
    await wait(2500)


async def select_level(page, level):
    iframe = page.frame_locator('#game-iframe')
    await iframe.locator(f'input[name="level"][value="{level}"]').click()
    await wait(600)


async def wait_episodes(page, target, timeout_s=240):
    print(f"    ⏳ 等待 {target} 回合…", end="", flush=True)
    for _ in range(timeout_s * 2):
        count = await page.evaluate("typeof episodeCount !== 'undefined' ? episodeCount : 0")
        if count >= target:
            print(f" ({count})")
            return count
        await asyncio.sleep(0.5)
    print(" 超時")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=["--start-maximized"])
        ctx = await browser.new_context(no_viewport=True)
        page = await ctx.new_page()

        print("▶ 開啟 RR（凍結英文版）")
        await page.goto(RR_URL); await wait(2500)

        print("▶ 載入 Maze2D Watch the Fire")
        await load_game(page, GAME_URL)
        await select_level(page, 4)

        print("▶ 訓練")
        await click_tab(page, "p1-config")
        await set_slider(page, "delay-slider", 0)
        await set_slider(page, "exploration-rate-slider", 0.3)
        await set_slider(page, "optimism-slider", 0)
        await wait_episodes(page, TARGET_EPISODES)
        await set_slider(page, "delay-slider", 30)
        await wait(1500)

        print("▶ 切到分析 Tab")
        await click_tab(page, "p1-qtable")
        await wait(2000)

        # 把第一個元件 scroll 到頂部，讓 4 個元件都在視窗內
        await page.evaluate("""
            const el = document.querySelector('#p1-acti-color');
            if (el) el.scrollIntoView({block: 'start', behavior: 'instant'});
        """)
        await wait(2000)  # 讓 plotly 渲染

        bbox = await page.evaluate("""
            (sels) => {
                const rects = sels.map(s => {
                    const el = document.querySelector(s);
                    if (!el) return null;
                    const r = el.getBoundingClientRect();
                    if (r.width === 0 || r.height === 0) return null;
                    return r;
                }).filter(Boolean);
                if (!rects.length) return null;
                return {
                    x: Math.min(...rects.map(r => r.left)),
                    y: Math.min(...rects.map(r => r.top)),
                    width: Math.max(...rects.map(r => r.right)) - Math.min(...rects.map(r => r.left)),
                    height: Math.max(...rects.map(r => r.bottom)) - Math.min(...rects.map(r => r.top)),
                    count: rects.length
                };
            }
        """, SELECTORS)
        print(f"    抓到 {bbox['count']}/{len(SELECTORS)} 個元素")

        pad = 16
        clip = {
            'x': max(0, bbox['x'] - pad),
            'y': max(0, bbox['y'] - pad),
            'width': bbox['width'] + pad * 2,
            'height': bbox['height'] + pad * 2,
        }
        OUT.parent.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(OUT), clip=clip)
        print(f"\n✅ {OUT.name}  ({int(clip['width'])}×{int(clip['height'])}px)")

        await browser.close()


asyncio.run(main())
