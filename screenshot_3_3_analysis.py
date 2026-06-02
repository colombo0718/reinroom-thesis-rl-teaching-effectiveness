"""
screenshot_3_3_analysis.py — 論文 3.3 章「分析 Tab」三排截圖
獨立腳本，不動 screenshot_thesis.py。

設計：
- Maze2D「Watch the Fire」關卡，含火焰陷阱（產生負獎勵，Min Q 才有東西）
- 跑訓練 ~120 回合讓 Q-Table 各區都有值
- 切到分析 Tab，截 3 排：
    圖 3-8（上排）：動作色環（左）+ 動作價值與選擇機率三柱圖（右）
    圖 3-9（中排）：狀態價值折線圖 Q-Value Slice（左）+ 動作選擇熱力圖 Policy Heatmap（右）
    圖 3-10（下排）：最大 Q 值熱力圖（左）+ 最小 Q 值熱力圖（右）

執行：
    python screenshot_3_3_analysis.py
輸出：
    截圖/圖3-8_分析上排.png  → 對應 images/fig3-8.png
    截圖/圖3-9_分析中排.png  → 對應 images/fig3-9.png
    截圖/圖3-10_分析下排.png → 對應 images/fig3-10.png
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

RR_URL  = "https://reinroom.leaflune.org/en/"
GAME_URL = "https://reinroom.leaflune.org/games/Maze2D_emoji_en.html"
OUT_DIR = Path(r"C:\Users\USER\論文 - RL平台教學成效\截圖")

CHROME_ARGS = [
    "--start-maximized",
    "--disable-background-timer-throttling",
    "--disable-backgrounding-occluded-windows",
    "--disable-renderer-backgrounding",
    "--disable-features=CalculateNativeWinOcclusion",
]

# 分析 Tab 三排 selector（已從凍結版 ReinforceLab/en/index.html L215-222 確認）
ROW_TOP    = ['#p1-acti-color', '#p1-bars-value']   # 動作色環 + 三柱圖
ROW_MIDDLE = ['#p1-line-value', '#p1-diff-value']   # Q-Value Slice + Policy Heatmap
ROW_BOTTOM = ['#p1-maxi-value', '#p1-mini-value']   # Max Q + Min Q 熱力圖

TARGET_EPISODES = 80    # 跑 80 回合（讓中下排熱力圖更飽和）


# ── 共用 helper ────────────────────────────────────────────────

async def wait(ms=600):
    await asyncio.sleep(ms / 1000)


async def click_tab(page, subtab):
    await page.click(f'button[data-subtab="{subtab}"]')
    await wait(600)


async def set_slider(page, slider_id, value):
    await page.evaluate(f"""
        const el = document.getElementById('{slider_id}');
        if (el) {{ el.value = {value}; el.dispatchEvent(new Event('input')); }}
    """)
    await wait(200)


async def load_game(page, url):
    await page.fill('#gameUrlInput', url)
    await page.click('#loadGame')
    await wait(2500)


async def select_level(page, level_value):
    """切換 Maze2D iframe 內的關卡（level radio button）。"""
    iframe = page.frame_locator('#game-iframe')
    try:
        await iframe.locator(f'input[name="level"][value="{level_value}"]').click()
        await wait(600)
    except Exception as e:
        print(f"  ⚠ 切關卡失敗：{e}")


async def wait_episodes(page, target, timeout_s=180):
    print(f"    ⏳ 等待訓練至第 {target} 回合…", end="", flush=True)
    for _ in range(timeout_s * 2):
        count = await page.evaluate(
            "typeof episodeCount !== 'undefined' ? episodeCount : 0"
        )
        if count >= target:
            print(f" ({count} 回合)")
            return count
        await asyncio.sleep(0.5)
    count = await page.evaluate("typeof episodeCount !== 'undefined' ? episodeCount : 0")
    print(f" ⚠ 超時，目前 {count} 回合")
    return count


def out_path(filename):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    return str(OUT_DIR / filename)


async def shot_row(page, selectors, filename, padding=12):
    """截一排（聯合包圍框 = 同 row 兩個元件）。
    截圖前先 scrollIntoView 並等 plotly 完成 lazy render，否則下方元件 bbox = 0。
    """
    # 先 scroll 把第一個元件帶到視窗中央，讓 plotly 觸發渲染
    await page.evaluate("""
        (sels) => {
            const el = document.querySelector(sels[0]);
            if (el) el.scrollIntoView({block: 'center', behavior: 'instant'});
        }
    """, selectors)
    await wait(1500)   # 給 plotly 渲染時間

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
            const x1 = Math.min(...rects.map(r => r.left));
            const y1 = Math.min(...rects.map(r => r.top));
            const x2 = Math.max(...rects.map(r => r.right));
            const y2 = Math.max(...rects.map(r => r.bottom));
            return {x: x1, y: y1, width: x2 - x1, height: y2 - y1, count: rects.length};
        }
    """, selectors)
    if not bbox:
        print(f"  ⚠ 找不到元素：{selectors}")
        return
    print(f"    ↪ 抓到 {bbox['count']}/{len(selectors)} 個元素")
    if bbox['count'] < len(selectors):
        # 嘗試列出哪些 selector 有問題
        for s in selectors:
            ok = await page.evaluate(f"!!document.querySelector('{s}')")
            print(f"      {s}: {'✓' if ok else '✗ 找不到'}")

    clip = {
        'x':      max(0, bbox['x'] - padding),
        'y':      max(0, bbox['y'] - padding),
        'width':  bbox['width']  + padding * 2,
        'height': bbox['height'] + padding * 2,
    }
    await page.screenshot(path=out_path(filename), clip=clip)
    print(f"  ✅ {filename}  ({int(clip['width'])}×{int(clip['height'])}px)")


# ── 主流程 ────────────────────────────────────────────────────

async def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📁 輸出目錄：{OUT_DIR}\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=CHROME_ARGS,
        )
        context = await browser.new_context(no_viewport=True)
        page = await context.new_page()

        print("▶ 開啟 Rein Room（凍結英文版）…")
        await page.goto(RR_URL)
        await wait(2500)

        print("▶ 載入 Maze2D 遊戲…")
        await load_game(page, GAME_URL)

        print("▶ 切換到「Watch the Fire」關卡（level=4）…")
        # Watch the Fire 是 Select Level 中第 5 個選項（0=Open Field, 1=Walled In,
        # 2=Coins Added, 3=Detour Rewards, 4=Watch the Fire, 5=False Shortcut）
        # 若編號不對，請改成正確的 value
        await select_level(page, 4)

        print("▶ 啟動訓練（高速）…")
        await click_tab(page, "p1-config")
        await set_slider(page, "delay-slider", 0)
        await set_slider(page, "exploration-rate-slider", 0.3)
        # Optimism (ψ) = 0：避免樂觀初始化讓 Min Q 永遠 ≥ 0
        # ψ = 0 → targetQ 採 Q(s', a') 即實際下一步動作，遇陷阱會傳遞負獎勵
        await set_slider(page, "optimism-slider", 0)
        await wait_episodes(page, TARGET_EPISODES, timeout_s=240)
        # 截圖前稍慢一點，讓視覺更新穩定
        await set_slider(page, "delay-slider", 30)
        await wait(1500)

        print("\n▶ 切到分析 Tab…")
        await click_tab(page, "p1-qtable")
        await wait(2000)

        # 上排
        print("\n▶ 圖 3-8（上排）：動作色環 + 三柱圖")
        await shot_row(page, ROW_TOP,    "圖3-8_分析上排.png", padding=12)

        # 中排
        print("\n▶ 圖 3-9（中排）：Q-Value Slice + Policy Heatmap")
        await shot_row(page, ROW_MIDDLE, "圖3-9_分析中排.png", padding=12)

        # 下排
        print("\n▶ 圖 3-10（下排）：Max Q + Min Q 熱力圖")
        await shot_row(page, ROW_BOTTOM, "圖3-10_分析下排.png", padding=12)

        print("\n" + "─" * 50)
        print("✅ 完成！瀏覽器保持開啟方便驗證。按 Ctrl+C 結束。")
        print("   若有 selector 對不上，請依上方錯誤訊息調整腳本頂部 ROW_* 變數。")
        await asyncio.sleep(9999)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
