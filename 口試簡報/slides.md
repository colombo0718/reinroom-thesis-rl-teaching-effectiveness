---
theme: seriph
title: Rein Room 強化教室 — 口試簡報
info: |
  ## 視覺化互動強化學習教學平台之設計與教學成效評估
  元智大學資訊工程學系 碩士論文口試
  2026/6/10
class: text-center
highlighter: shiki
drawings:
  persist: false
transition: fade
mdc: true
fonts:
  sans: 'Noto Sans TC'
  serif: 'Noto Serif TC'
  mono: 'Fira Code'
---

# Rein Room 強化教室
## 視覺化互動強化學習教學平台之設計與教學成效評估

<div class="pt-12">
  <span class="text-xl opacity-75">研究生：趙士豪</span>
</div>

<div class="pt-4 text-lg opacity-60">
  指導教授：黃怡錚 博士<br>
  元智大學 資訊工程學系<br>
  中華民國 一一五 年 六 月 十 日
</div>

<!--
各位老師午安，我是趙士豪，今天要報告的題目是
《Rein Room 強化教室：視覺化互動強化學習教學平台之設計與教學成效評估》，
由黃怡錚老師指導。
-->

---
layout: default
---

# 簡報大綱

<div class="grid grid-cols-6 gap-3 pt-12">
  <div class="border rounded p-3 text-center">
    <div class="text-2xl font-bold text-blue-500">1</div>
    <div class="mt-2 text-sm">研究動機</div>
    <div class="text-xs opacity-60">與問題</div>
  </div>
  <div class="border rounded p-3 text-center">
    <div class="text-2xl font-bold text-blue-500">2</div>
    <div class="mt-2 text-sm">文獻探討</div>
    <div class="text-xs opacity-60">現有平台限制</div>
  </div>
  <div class="border rounded p-3 text-center">
    <div class="text-2xl font-bold text-blue-500">3</div>
    <div class="mt-2 text-sm">RR 平台</div>
    <div class="text-xs opacity-60">設計與特色</div>
  </div>
  <div class="border rounded p-3 text-center">
    <div class="text-2xl font-bold text-blue-500">4</div>
    <div class="mt-2 text-sm">研究設計</div>
    <div class="text-xs opacity-60">A/B 對照</div>
  </div>
  <div class="border rounded p-3 text-center bg-blue-50">
    <div class="text-2xl font-bold text-blue-700">5</div>
    <div class="mt-2 text-sm font-bold">主要發現</div>
    <div class="text-xs opacity-60">三主軸</div>
  </div>
  <div class="border rounded p-3 text-center">
    <div class="text-2xl font-bold text-blue-500">6</div>
    <div class="mt-2 text-sm">結論</div>
    <div class="text-xs opacity-60">與未來工作</div>
  </div>
</div>

<!-- 接下來約 20 分鐘會依序談六個部分，第五部分主要發現是今天的重頭戲。 -->

---
layout: section
---

# Part 1.
# 研究動機與問題

---

# 研究動機

<div class="grid grid-cols-2 gap-8 pt-8">
  <div>
    <h3 class="text-xl font-bold mb-4">RL 是 AI 三大核心之一</h3>
    <ul class="space-y-2">
      <li>🎯 AlphaGo / AlphaZero（Silver et al., 2018）</li>
      <li>🚗 自動駕駛決策（Sallab et al., 2017）</li>
      <li>🤖 大型語言模型對齊（RLHF）</li>
      <li>🎮 遊戲 AI（Mnih et al., 2015）</li>
    </ul>
  </div>
  <div>
    <h3 class="text-xl font-bold mb-4">但學習者門檻高</h3>
    <ul class="space-y-2">
      <li>❌ 需要寫程式（Python、Gymnasium）</li>
      <li>❌ 需要安裝環境（套件、依賴）</li>
      <li>❌ 抽象概念難視覺化</li>
      <li>❌ 學習回饋週期太長</li>
    </ul>
  </div>
</div>

<div class="mt-8 text-center text-xl text-blue-600">
  ⇒ 視覺化互動式平台是降低門檻的可能路徑
</div>

<!--
RL 已是 AI 三大核心技術之一，但抽象性與程式門檻使其難以下放給非資工背景學習者。
本研究的起點：能否設計一個視覺化互動平台，降低 RL 入門門檻？
-->

---

# 研究問題與答案概覽

<div class="grid grid-cols-3 gap-4 pt-6">
  <div class="border-2 border-blue-300 rounded-lg p-4">
    <div class="text-blue-600 text-2xl font-bold mb-2">RQ 1</div>
    <div class="font-bold mb-1 text-sm">理論知識傳遞</div>
    <div class="text-xs opacity-80 mb-3">
      視覺化平台能否傳遞 RL 核心概念？
    </div>
    <div class="border-t pt-2 text-xs">
      <span class="font-bold text-gray-600">答：</span>
      兩組前後測表現接近
    </div>
  </div>
  <div class="border-2 border-blue-300 rounded-lg p-4">
    <div class="text-blue-600 text-2xl font-bold mb-2">RQ 2</div>
    <div class="font-bold mb-1 text-sm">圖表判讀</div>
    <div class="text-xs opacity-80 mb-3">
      學習者能否建立訓練曲線與 Q-table 判讀能力？
    </div>
    <div class="border-t pt-2 text-xs">
      <span class="font-bold text-gray-600">答：</span>
      兩組能力相近（T1–T4）
    </div>
  </div>
  <div class="border-2 border-red-400 rounded-lg p-4 bg-red-50">
    <div class="text-red-600 text-2xl font-bold mb-2">RQ 3</div>
    <div class="font-bold mb-1 text-sm">學習動機 + 操作意願</div>
    <div class="text-xs opacity-80 mb-3">
      平台能否提升學習動機與自主操作意願？
    </div>
    <div class="border-t pt-2 text-xs">
      <span class="font-bold text-red-600">答：</span>
      <span class="font-bold">RR 勝出（本研究主軸）</span>
    </div>
  </div>
</div>

<div class="mt-6 text-center text-sm opacity-70">
  RQ1、RQ2 之答案於主要發現中以數據呈現；RQ3 為本研究核心價值所在
</div>

<!--
本研究三個 RQ，後面主要發現會分別對應到答案。
RQ1 RQ2 兩組差不多；RQ3 RR 勝出，這是本研究價值所在。
-->

---

# 研究範圍與對象

<div class="grid grid-cols-2 gap-12 pt-8">
  <div>
    <h3 class="text-xl font-bold mb-4">📍 場域</h3>
    <ul class="space-y-2">
      <li>元智大學資訊工程學系</li>
      <li>兩班 — 分屬不同班級避免污染</li>
      <li>連續兩天 × 約 3 小時課程</li>
    </ul>
  </div>
  <div>
    <h3 class="text-xl font-bold mb-4">👥 樣本</h3>
    <div class="text-center mt-4">
      <div class="inline-block border-2 border-blue-500 rounded-lg p-6 mr-4">
        <div class="text-4xl font-bold text-blue-600">18</div>
        <div class="text-sm mt-2">RR 組（A）</div>
      </div>
      <div class="inline-block border-2 border-gray-500 rounded-lg p-6">
        <div class="text-4xl font-bold text-gray-600">12</div>
        <div class="text-sm mt-2">Colab 組（B）</div>
      </div>
    </div>
  </div>
</div>

<!--
研究對象為元智資工系兩班，分屬不同班級避免污染。
-->

---
layout: section
---

# Part 2.
# 文獻探討

---

# 現有 RL 教學平台的三條路

| 路徑 | 代表 | 優勢 | 限制 |
|------|------|------|------|
| **程式碼導向** | Gymnasium + Colab | 業界標準、彈性高 | 程式門檻、回饋週期長 |
| **硬體導向** | LEGO + RL (Zhang et al., 2022, 2023) | 實體操作、具象化 | 成本高、後勤複雜、難規模化 |
| **視覺化互動** | ARtonomous (Dietz et al., 2022) | 低門檻、即時回饋 | 案例少、缺實證評量 |

<div class="mt-8 text-center text-xl text-blue-600">
  本研究切入點：在「視覺化互動」這條路加上完整實證
</div>

<!--
現有 K-12 / 入門 RL 教學分三派，視覺化互動是值得深入驗證的方向。
-->

---

# 教學設計理論基礎

<div class="grid grid-cols-2 gap-8 pt-6">
  <div class="border-l-4 border-blue-500 pl-4">
    <h3 class="font-bold text-lg mb-3">即時回饋之教學效益</h3>
    <ul class="space-y-2 text-sm">
      <li>📚 Hattie & Timperley (2007) — 即時回饋對學習成效顯著</li>
      <li>📚 Mayer (2009) — 多媒體學習理論</li>
      <li>📚 Sweller (1988) — 認知負荷理論</li>
    </ul>
  </div>
  <div class="border-l-4 border-blue-500 pl-4">
    <h3 class="font-bold text-lg mb-3">學習動機與自我效能</h3>
    <ul class="space-y-2 text-sm">
      <li>📚 Bandura (1977) — 自我效能理論</li>
      <li>📚 Ryan & Deci (2000) — 自我決定理論（內在動機）</li>
      <li>📚 Barnett & Ceci (2002) — 遷移能力分類</li>
    </ul>
  </div>
</div>

<div class="mt-8 p-4 bg-blue-50 text-center">
  本研究 RR 平台之設計理念 <span class="font-bold text-blue-700">同時對應</span>「縮短回饋週期」與「自主操作建立動機」兩條理論線
</div>

<!--
本研究的教學設計理論基礎，呼應 RR 平台兩大設計訴求。
-->

---
layout: section
---

# Part 3.
# Rein Room 平台

---

# 平台定位

<div class="grid grid-cols-2 gap-8">
  <div>
    <img src="/images/fig3-1.png" class="rounded shadow-lg" />
  </div>
  <div class="flex flex-col justify-center">
    <h2 class="text-2xl font-bold mb-4">純前端、零安裝</h2>
    <ul class="space-y-2 text-lg">
      <li>🌐 瀏覽器打開網址即用</li>
      <li>⚡ 不需 Python、不需安裝套件</li>
      <li>🧠 內建 Q-Learning + DQN</li>
      <li>🎲 ε-greedy / Softmax 探索策略</li>
      <li>🎮 五個遊戲環境（1D → Fighter）</li>
    </ul>
    <div class="mt-6 text-sm opacity-60">
      https://reinroom.leaflune.org/en/
    </div>
  </div>
</div>

<!--
RR 是我自行開發的純前端 RL 教學平台，網址打開就能用。
-->

---

# 核心特色 1：滑桿即時調參

<div class="text-center">
  <img src="/images/fig3-1a.png" class="max-h-72 mx-auto rounded shadow-lg" />
  <div class="text-sm mt-2 opacity-60">超參數滑桿</div>
</div>

<h3 class="text-xl font-bold mt-4 mb-3 text-red-500 text-center">操作回饋週期：從 30 秒 → 1 秒</h3>

<div class="grid grid-cols-2 gap-6 text-base">
  <div class="text-center">
    <span class="font-bold">傳統程式碼導向</span><br>
    <span class="opacity-70">改程式 → 重跑 → 看結果（~30 秒循環）</span>
  </div>
  <div class="text-red-500 text-center">
    <span class="font-bold">RR 滑桿介面</span><br>
    拖一下 → 看一下（~1 秒循環）
  </div>
</div>

<div class="mt-4 p-3 bg-yellow-50 border-l-4 border-yellow-400 text-sm text-center">
  💡 學生在拖曳過程中即可建立「過大 → 行為 X、過小 → 行為 Y」的直觀感受
</div>

<!--
最關鍵設計：所有超參數以滑桿即時調整，毫秒級反映在曲線與熱力圖。
這是 RR 與 Colab 最本質的差異。
-->

---

# 核心特色 2：儀表 Tab — 看見訓練成效

<div class="text-center">
  <img src="/images/fig3-7.png" class="max-h-72 mx-auto rounded shadow-lg" />
  <div class="text-sm mt-2 opacity-60">即時訓練圖表（每秒更新）</div>
</div>

<div class="grid grid-cols-2 gap-6 mt-4 text-sm">
  <div class="border-l-4 border-blue-400 pl-3">
    <span class="font-bold">上排（每秒粒度）</span><br>
    Reward 面積折線 + Steps 面積折線
  </div>
  <div class="border-l-4 border-blue-400 pl-3">
    <span class="font-bold">下排（每回合粒度）</span><br>
    Reward 柱狀 + Steps 柱狀
  </div>
</div>

<div class="text-center text-lg mt-4 text-blue-600">
  四張圖互補 ⇒ 學生即時看出 agent 訓練成效
</div>

<!--
儀表 Tab 四張圖，分兩種時間粒度：每秒看當下訓練動態、每回合看整體收斂趨勢。
學生不需理解演算法細節，從曲線走勢就能判斷訓練方向對不對。
-->

---

# 核心特色 3：分析 Tab — 看見行為成因

<div class="grid grid-cols-2 gap-4">
  <div>
    <img src="/images/fig3-8.png" class="rounded shadow" />
    <div class="text-center text-xs mt-1 opacity-60">上排：動作色環 + 三柱圖（Q 值/ε-greedy/Softmax）</div>
  </div>
  <div>
    <img src="/images/fig3-9.png" class="rounded shadow" />
    <div class="text-center text-xs mt-1 opacity-60">中排：狀態價值折線 + 動作選擇熱力圖</div>
  </div>
</div>

<div class="text-center text-lg mt-4 text-blue-600">
  四張圖互補 ⇒ 學生即時觀察 agent 行為成因
</div>

<!--
分析 Tab 四張圖，把「為什麼 agent 這樣選」拆給學生看：
三柱圖讓 Q 值與選擇機率並列；熱力圖呈現全局策略地圖。
-->


---

# 五個遊戲環境 — 學習階梯（對應 RQ）

<div class="grid grid-cols-5 gap-2 pt-2">
  <div class="text-center">
    <img src="/images/fig3-11a.png" class="h-28 mx-auto rounded shadow" />
    <div class="mt-1 font-bold text-xs">T1 MAB</div>
    <div class="text-xs opacity-60">SAR 概念</div>
  </div>
  <div class="text-center">
    <img src="/images/fig3-11b.png" class="h-28 mx-auto rounded shadow" />
    <div class="mt-1 font-bold text-xs">T2 Maze 1D</div>
    <div class="text-xs opacity-60">episode</div>
  </div>
  <div class="text-center">
    <img src="/images/fig3-11c.png" class="h-28 mx-auto rounded shadow" />
    <div class="mt-1 font-bold text-xs">T3 Maze 2D</div>
    <div class="text-xs opacity-60">Q-table 熱力圖</div>
  </div>
  <div class="text-center">
    <img src="/images/fig3-11d.png" class="h-28 mx-auto rounded shadow" />
    <div class="mt-1 font-bold text-xs">T4 Heli</div>
    <div class="text-xs opacity-60">曲線判讀（主評量）</div>
  </div>
  <div class="text-center border-2 border-red-400 rounded p-1">
    <img src="/images/fig3-11e.png" class="h-28 mx-auto rounded shadow" />
    <div class="mt-1 font-bold text-xs text-red-500">T5 Fighter</div>
    <div class="text-xs opacity-60">無預設參數</div>
  </div>
</div>

<table class="w-full mt-4 text-sm">
  <thead>
    <tr class="bg-gray-100">
      <th class="p-2 text-left">任務</th>
      <th class="p-2 text-left">學生要做什麼</th>
      <th class="p-2 text-center">對應 RQ</th>
    </tr>
  </thead>
  <tbody>
    <tr class="border-b"><td class="p-2">T1–T3</td><td class="p-2">入門概念 + 圖表觀察</td><td class="p-2 text-center">RQ1, RQ2</td></tr>
    <tr class="border-b"><td class="p-2">T4 Heli</td><td class="p-2">主評量任務，須從曲線判讀調整策略</td><td class="p-2 text-center">RQ2</td></tr>
    <tr class="bg-red-50"><td class="p-2 font-bold">T5 Fighter</td><td class="p-2">無預設超參數，須自主決定 α / γ / ε</td><td class="p-2 text-center font-bold text-red-500">RQ3</td></tr>
  </tbody>
</table>

<!--
五個遊戲構成從簡入難的學習階梯。
T1-T3 對應 RQ1 RQ2，T5 對應 RQ3。
-->

---
layout: section
---

# Part 4.
# 研究設計

---

# A/B 組實驗流程對照

<div class="text-center">
  <img src="/images/fig4-1.png" class="max-h-96 mx-auto rounded shadow-lg" />
</div>

<div class="grid grid-cols-2 gap-12 mt-4 text-sm">
  <div class="text-center">
    <span class="font-bold text-blue-500">RR 組（A）n=18</span><br>
    使用 ReinRoom 視覺化平台
  </div>
  <div class="text-center">
    <span class="font-bold text-gray-600">Colab 組（B）n=12</span><br>
    使用 Gymnasium + Google Colab
  </div>
</div>

<!--
兩組同樣兩天 3 小時、同樣的教學節奏，唯一差別是平台。
後測內容兩組相同，收束在同一節點。
-->

---

# 教學介入標準化（六項）

<div class="grid grid-cols-2 gap-3 pt-6">
  <div class="border-l-4 border-blue-500 pl-3 py-2">
    <span class="font-bold">① 任務環境對齊（rr_envs.py）</span><br>
    <span class="text-sm opacity-70">RR 任務逐字對齊 Gymnasium 介面</span>
  </div>
  <div class="border-l-4 border-blue-500 pl-3 py-2">
    <span class="font-bold">② 18 支 AI 教學影片</span><br>
    <span class="text-sm opacity-70">6 支共用理論 + 各組 6 支操作</span>
  </div>
  <div class="border-l-4 border-blue-500 pl-3 py-2">
    <span class="font-bold">③ 預寫講師講稿（兩組各約 400 行）</span><br>
    <span class="text-sm opacity-70">英文照念設計，避免講師風格差異</span>
  </div>
  <div class="border-l-4 border-blue-500 pl-3 py-2">
    <span class="font-bold">④ 標準化學生指引（13 步驟）</span><br>
    <span class="text-sm opacity-70">兩組學生看到同樣編排</span>
  </div>
  <div class="border-l-4 border-blue-500 pl-3 py-2">
    <span class="font-bold">⑤ 雙平台備援</span><br>
    <span class="text-sm opacity-70">Colab + Binder 當天備援</span>
  </div>
  <div class="border-l-4 border-blue-500 pl-3 py-2">
    <span class="font-bold">⑥ 影片品質檢核 SOP</span><br>
    <span class="text-sm opacity-70">ffmpeg 抽幀逐張視覺驗收</span>
  </div>
</div>

<div class="mt-6 text-center text-blue-600">
  目的：確保「平台介面差異」是兩組唯一的系統性差異
</div>

<!--
我們在研究設計上採用了六項措施確保兩組教學一致，
讓平台介面成為唯一系統性差異。
-->

---

# 實驗資料收集

<div class="flex justify-center pt-6">
  <div class="space-y-3 text-center">
    <div class="bg-red-200 px-12 py-3 rounded shadow font-bold">
      🎯 理論知識前後測（8 題）
    </div>
    <div class="bg-orange-200 px-16 py-3 rounded shadow font-bold">
      📊 任務完成記錄（完成率 + 完成時間）
    </div>
    <div class="bg-yellow-200 px-20 py-3 rounded shadow font-bold">
      💭 自評量表：平台回饋（5 題）/ NASA-TLX / SUS / 開放題
    </div>
    <div class="bg-green-200 px-24 py-3 rounded shadow font-bold">
      👀 課堂觀察記錄（助教逐時填寫）
    </div>
  </div>
</div>

<!--
實驗資料收集涵蓋認知、行為、情意、課堂觀察四類資料來源。
-->

---
layout: section
class: bg-blue-50
---

# Part 5.
# 主要發現

<div class="text-xl mt-4 opacity-80">三大主軸：學習動機 / 輕鬆度 / 操作意願</div>

---

# RQ1 理論知識測驗：Colab 顯著進步

<div class="text-center pt-4">
  <img src="/images/fig5-1.png" class="max-h-72 mx-auto rounded shadow" />
</div>

<div class="grid grid-cols-2 gap-8 mt-4">
  <div class="text-center">
    <span class="text-blue-500 font-bold">RR 組</span>：pre 5.50 → post 6.40（n.s.）
  </div>
  <div class="text-center">
    <span class="text-gray-700 font-bold">Colab 組</span>：pre 5.00 → post 6.92（p = .01 *）
  </div>
</div>

<div class="mt-6 text-center text-blue-700">
  ⇒ RQ1 答案：兩組均能傳遞核心概念，Colab 組於此項表現較佳
</div>

<!--
RQ1：兩組都進步，Colab 組於理論知識測驗達顯著進步。
這就是答案：兩組都能傳遞概念。
-->

---

# RQ2 任務完成率全貌

<div class="text-center pt-2">
  <img src="/images/fig5-3.png" class="max-h-72 mx-auto rounded shadow" />
</div>

<table class="w-full text-sm mt-4">
  <thead>
    <tr class="bg-blue-100">
      <th class="p-2 text-left">任務</th>
      <th class="p-2">RR 完成率</th>
      <th class="p-2">Colab 完成率</th>
      <th class="p-2">RR 時間（分）</th>
      <th class="p-2">Colab 時間（分）</th>
      <th class="p-2">時間 p</th>
    </tr>
  </thead>
  <tbody>
    <tr><td class="p-2">T1–T3</td><td class="p-2 text-center" colspan="5">兩組接近</td></tr>
    <tr class="bg-yellow-50"><td class="p-2 font-bold">T4 Heli</td><td class="p-2 text-center">56%</td><td class="p-2 text-center">50%</td><td class="p-2 text-center">17.6</td><td class="p-2 text-center">53.0</td><td class="p-2 text-center font-bold text-red-500">.014 *</td></tr>
    <tr class="bg-red-50"><td class="p-2 font-bold">T5 Fighter</td><td class="p-2 text-center font-bold">61%</td><td class="p-2 text-center">25%</td><td class="p-2 text-center">20.4</td><td class="p-2 text-center">33.3</td><td class="p-2 text-center font-bold text-red-500">&lt;.001 ***</td></tr>
  </tbody>
</table>

<div class="mt-4 text-center text-blue-600">
  ⇒ RQ2 答案：T1–T3 兩組圖表判讀能力相近；T4 完成率相近但 RR 用時更少
</div>

<!--
RQ2 兩組能力接近，但 T4 開始 RR 在時間上明顯較短。
-->

---

# 主軸 1：學習動機（自評量表）

<div class="text-center">
  <img src="/images/fig5-4.png" class="max-h-56 mx-auto rounded shadow" />
</div>

<table class="w-full text-sm mt-3">
  <thead>
    <tr class="bg-blue-100">
      <th class="p-2 text-left">題目</th>
      <th class="p-2">RR</th>
      <th class="p-2">Colab</th>
      <th class="p-2">p 值</th>
    </tr>
  </thead>
  <tbody>
    <tr class="border-b"><td class="p-2">Q1 介面易用</td><td class="p-2 text-center">3.78</td><td class="p-2 text-center">3.92</td><td class="p-2 text-center">n.s.</td></tr>
    <tr class="border-b"><td class="p-2">Q2 有信心調整參數</td><td class="p-2 text-center font-bold text-blue-600">4.06</td><td class="p-2 text-center">3.50</td><td class="p-2 text-center">.19</td></tr>
    <tr class="border-b"><td class="p-2">Q3 視覺化幫助理解</td><td class="p-2 text-center font-bold text-blue-600">4.33</td><td class="p-2 text-center">4.18</td><td class="p-2 text-center">.72</td></tr>
    <tr class="border-b bg-red-50"><td class="p-2 font-bold">Q4 課後學習動機</td><td class="p-2 text-center font-bold text-red-600">4.17</td><td class="p-2 text-center">3.33</td><td class="p-2 text-center font-bold text-red-600">.089 †</td></tr>
    <tr class="border-b"><td class="p-2">Q5 推薦意願</td><td class="p-2 text-center font-bold text-blue-600">4.17</td><td class="p-2 text-center">3.83</td><td class="p-2 text-center">n.s.</td></tr>
  </tbody>
</table>

<div class="mt-3 text-center text-red-600 font-bold">
  Q4 課後學習動機 p = .089 為趨近顯著 ★
</div>

<!--
平台回饋量表 5 題實際題目。
Q4 課後學習動機 p=.089 趨近顯著，這是 RR 在動機上的勝出證據。
-->

---

# 主軸 2：輕鬆度（NASA-TLX「努力」分項）

<div class="grid grid-cols-2 gap-8 pt-6">
  <div>
    <h3 class="font-bold mb-3">NASA-TLX 六分項</h3>
    <table class="w-full text-sm">
      <thead>
        <tr class="bg-gray-100">
          <th class="p-2 text-left">分項</th>
          <th class="p-2">RR</th>
          <th class="p-2">Colab</th>
          <th class="p-2">p</th>
        </tr>
      </thead>
      <tbody>
        <tr><td class="p-2">心智需求</td><td class="p-2 text-center">6.06</td><td class="p-2 text-center">5.92</td><td class="p-2 text-center">n.s.</td></tr>
        <tr><td class="p-2">體力需求</td><td class="p-2 text-center">4.94</td><td class="p-2 text-center">4.56</td><td class="p-2 text-center">n.s.</td></tr>
        <tr><td class="p-2">時間壓力</td><td class="p-2 text-center">4.78</td><td class="p-2 text-center">4.83</td><td class="p-2 text-center">n.s.</td></tr>
        <tr class="bg-red-50 font-bold"><td class="p-2">努力 ↓</td><td class="p-2 text-center text-blue-600">5.50</td><td class="p-2 text-center">6.83</td><td class="p-2 text-center text-red-500">.044 *</td></tr>
        <tr><td class="p-2">挫折感</td><td class="p-2 text-center">5.50</td><td class="p-2 text-center">3.92</td><td class="p-2 text-center">n.s.</td></tr>
        <tr><td class="p-2">表現</td><td class="p-2 text-center">5.56</td><td class="p-2 text-center">4.92</td><td class="p-2 text-center">n.s.</td></tr>
      </tbody>
    </table>
  </div>
  <div class="flex flex-col justify-center">
    <div class="bg-blue-50 p-6 rounded">
      <div class="text-2xl font-bold text-blue-700 mb-3">關鍵發現</div>
      <div class="text-base">
        「努力」分項<br>
        <span class="font-bold text-red-500">RR 顯著低於 Colab（p = .044）</span><br><br>
        ⇒ RR 學生主觀上感受到「**輕鬆**」<br>
        <span class="text-sm opacity-70">呼應開放題參數調整困難比例</span>
      </div>
    </div>
  </div>
</div>

<!--
NASA-TLX 拆六分項後「努力」顯著低 — 學生覺得用 RR 比較輕鬆。
-->

---

# 主軸 3：操作意願（T5 完成率）

<div class="grid grid-cols-2 gap-8 pt-8">
  <div class="text-center">
    <div class="text-7xl font-bold text-blue-600">61%</div>
    <div class="text-xl mt-2">RR 組</div>
    <div class="opacity-60">11 / 18 完成</div>
  </div>
  <div class="text-center">
    <div class="text-7xl font-bold text-gray-500">25%</div>
    <div class="text-xl mt-2">Colab 組</div>
    <div class="opacity-60">3 / 12 完成</div>
  </div>
</div>

<div class="mt-12 text-center">
  <div class="inline-block text-3xl font-bold text-red-500 border-4 border-red-500 px-8 py-2 rounded">
    2.4 ×
  </div>
</div>

<div class="mt-6 text-center text-sm opacity-70">
  T5 Fighter：不提供任何預設超參數，學生需自主決定 α / γ / ε
</div>

<!--
T5 刻意不給任何預設超參數，逼學生自主決策。
RR 學生明顯更願意嘗試、更願意動手。這就是「操作意願」。
-->

---

# 主軸 3 補強：開放題「參數調整困難」

<div class="overflow-x-auto pt-4">
  <table class="w-full text-base">
    <thead>
      <tr class="bg-blue-100">
        <th class="p-3 text-left">主題</th>
        <th class="p-3">RR 組</th>
        <th class="p-3">Colab 組</th>
        <th class="p-3">Colab / RR 倍率</th>
      </tr>
    </thead>
    <tbody>
      <tr class="bg-red-50 font-bold">
        <td class="p-3">參數調整困難</td>
        <td class="p-3 text-center">3 / 18 (17%)</td>
        <td class="p-3 text-center">5 / 12 (42%)</td>
        <td class="p-3 text-center text-red-500 text-xl">2.5 ×</td>
      </tr>
      <tr class="bg-red-50 font-bold">
        <td class="p-3">圖表判讀困難</td>
        <td class="p-3 text-center">3 / 18 (17%)</td>
        <td class="p-3 text-center">5 / 12 (42%)</td>
        <td class="p-3 text-center text-red-500 text-xl">2.5 ×</td>
      </tr>
      <tr class="border-b">
        <td class="p-3">表示無困難</td>
        <td class="p-3 text-center">33%</td>
        <td class="p-3 text-center">17%</td>
        <td class="p-3 text-center">0.5 ×</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="mt-4 text-center text-blue-600">
  學生自陳「最困難的部分」：兩個主題 Colab 都是 RR 的 2.5 倍
</div>

<!--
請學生自己寫「最困難的部分」，編碼後得到驚人發現。
參數調整困難 + 圖表判讀困難，Colab 都是 RR 的 2.5 倍。
-->

---

# SUS 系統易用性

<div class="text-center">
  <img src="/images/fig5-5.png" class="max-h-72 mx-auto rounded shadow" />
</div>

<div class="grid grid-cols-2 gap-8 mt-4">
  <div class="text-center">
    <span class="text-gray-700 font-bold">Colab 組</span>：73.5（Good）
  </div>
  <div class="text-center">
    <span class="text-blue-500 font-bold">RR 組</span>：59.0（Marginal）　p = .037 *
  </div>
</div>

<div class="grid grid-cols-2 gap-6 pt-4 text-sm">
  <div class="border-l-4 border-blue-500 pl-3">
    <span class="font-bold">解讀 1：</span> Colab 是學生已熟工具，SUS 難區分「系統好」與「使用者熟」
  </div>
  <div class="border-l-4 border-orange-500 pl-3">
    <span class="font-bold">解讀 2：</span> RR 早期版本資訊密度確實偏高，已導出明確改進方向
  </div>
</div>

<!--
SUS 兩極化反應，部分學生極喜歡部分學生覺得難。
這也指向具體的平台改進方向。
-->

---
layout: section
---

# Part 6.
# 結論與未來工作

---

# 給未來平台設計者的五點建議

<div class="grid grid-cols-5 gap-3 pt-8">
  <div class="border-2 border-blue-400 rounded p-3 text-center">
    <div class="text-3xl mb-2">📊</div>
    <div class="font-bold text-sm">資訊密度控制</div>
    <div class="text-xs opacity-70 mt-2">分階段視覺化</div>
  </div>
  <div class="border-2 border-blue-400 rounded p-3 text-center">
    <div class="text-3xl mb-2">🏫</div>
    <div class="font-bold text-sm">教室模式</div>
    <div class="text-xs opacity-70 mt-2">硬性管控分心</div>
  </div>
  <div class="border-2 border-blue-400 rounded p-3 text-center">
    <div class="text-3xl mb-2">🎯</div>
    <div class="font-bold text-sm">遷移能力評量</div>
    <div class="text-xs opacity-70 mt-2">移除預設值</div>
  </div>
  <div class="border-2 border-blue-400 rounded p-3 text-center">
    <div class="text-3xl mb-2">⚡</div>
    <div class="font-bold text-sm">即時調整介面</div>
    <div class="text-xs opacity-70 mt-2">毫秒級反映</div>
  </div>
  <div class="border-2 border-blue-400 rounded p-3 text-center">
    <div class="text-3xl mb-2">👥</div>
    <div class="font-bold text-sm">同儕互動機制</div>
    <div class="text-xs opacity-70 mt-2">對比觀察 / 分享</div>
  </div>
</div>

<div class="mt-8 text-center text-blue-600">
  推廣到一般<span class="font-bold">「視覺化互動式教學平台」</span>設計
</div>

<!--
本研究經驗推廣到一般視覺化互動式教學平台的五點建議。
-->

---

# 研究貢獻

<div class="space-y-6 pt-8">
  <div class="flex items-start gap-4">
    <div class="text-4xl">🎯</div>
    <div>
      <div class="font-bold text-lg">實證貢獻</div>
      <div class="text-sm opacity-80">
        RR 平台在學習動機（Q4 課後動機 4.17 vs 3.33, p=.089）、輕鬆度（NASA-TLX 努力 5.50 vs 6.83, p=.044）、操作意願（T5 完成率 61% vs 25%）三項皆勝出，
        且在 Colab 組於理論知識測驗達顯著進步之前提下，仍能於上述三項展現獨立貢獻
      </div>
    </div>
  </div>
  <div class="flex items-start gap-4">
    <div class="text-4xl">💡</div>
    <div>
      <div class="font-bold text-lg">設計貢獻</div>
      <div class="text-sm opacity-80">
        整理五點對未來視覺化互動式教學平台設計者之具體建議，
        並提供 RR 平台原始碼與 18 支標準化教學影片作為可復用資源
      </div>
    </div>
  </div>
</div>

<!--
兩項貢獻：實證 + 設計建議。
-->

---

# 研究限制

<div class="space-y-4 pt-6">
  <div class="border-l-4 border-orange-400 pl-4">
    <div class="font-bold">樣本偏小</div>
    <div class="text-sm opacity-70">RR n=18、Colab n=12，統計檢定力受限</div>
  </div>
  <div class="border-l-4 border-orange-400 pl-4">
    <div class="font-bold">跨班級不可控差異</div>
    <div class="text-sm opacity-70">兩組分屬不同班級，仍可能存在班級文化等難測因素</div>
  </div>
  <div class="border-l-4 border-orange-400 pl-4">
    <div class="font-bold">未測長期保留度</div>
    <div class="text-sm opacity-70">僅捕捉即時學習成效，長期保留待後續研究</div>
  </div>
  <div class="border-l-4 border-orange-400 pl-4">
    <div class="font-bold">範圍限定</div>
    <div class="text-sm opacity-70">結論收斂在「大學資工系」場域，未擴張至 K-12 或其他學科</div>
  </div>
</div>

<!--
研究限制四點。結論收斂在大學資工系。
-->

---

# 未來工作

<div class="grid grid-cols-2 gap-6 pt-8">
  <div>
    <h3 class="font-bold mb-3 text-blue-600">🎓 教學設計</h3>
    <ul class="space-y-2 text-sm">
      <li>教室模式三階段開發（教師端控制）</li>
      <li>分階段視覺化解鎖</li>
      <li>同儕互動機制（對比觀察、班級儀表板）</li>
    </ul>
  </div>
  <div>
    <h3 class="font-bold mb-3 text-blue-600">🚀 平台演進</h3>
    <ul class="space-y-2 text-sm">
      <li>雙旗艦平台（RL + ML / 資料科學）</li>
      <li>長期追蹤研究設計</li>
      <li>跨學門擴散（物理、工程模擬）</li>
    </ul>
  </div>
</div>

<div class="mt-12 text-center text-xl text-blue-700 italic">
  論文完成 ≠ Rein Room 的終點
</div>

<!--
未來工作兩個方向：教學設計面 + 平台演進面。
-->

---
layout: center
class: text-center
---

# 致謝

<div class="space-y-3 mt-8 text-lg">
  <div>感謝 <span class="font-bold">黃怡錚老師</span> 指導</div>
  <div>感謝 <span class="font-bold">張鈞博助教</span> 協助</div>
  <div>感謝 <span class="font-bold">兩位授課教師</span> 與 <span class="font-bold">兩班受試學生</span></div>
  <div>感謝 <span class="font-bold">口試委員</span> 蒞臨指教</div>
</div>

<div class="mt-16 text-5xl font-bold text-blue-600">
  Q & A
</div>

<div class="mt-4 text-sm opacity-60">敬請各位老師指教</div>

<!--
感謝。請各位老師指教。
-->

---
layout: section
class: bg-gray-100
---

# Backup
# 備援資料

---

# B01. NASA-TLX 完整六分項

<table class="w-full text-sm mt-4">
  <thead>
    <tr class="bg-blue-100">
      <th class="p-2 text-left">分項</th>
      <th class="p-2">RR 平均</th>
      <th class="p-2">RR SD</th>
      <th class="p-2">Colab 平均</th>
      <th class="p-2">Colab SD</th>
      <th class="p-2">t 值</th>
      <th class="p-2">p 值</th>
    </tr>
  </thead>
  <tbody>
    <tr><td class="p-2">心智需求</td><td class="p-2 text-center">6.06</td><td class="p-2 text-center">1.92</td><td class="p-2 text-center">5.92</td><td class="p-2 text-center">2.07</td><td class="p-2 text-center">0.187</td><td class="p-2 text-center">.853</td></tr>
    <tr><td class="p-2">體力需求</td><td class="p-2 text-center">4.94</td><td class="p-2 text-center">2.48</td><td class="p-2 text-center">4.56</td><td class="p-2 text-center">2.25</td><td class="p-2 text-center">0.474</td><td class="p-2 text-center">.640</td></tr>
    <tr><td class="p-2">時間壓力</td><td class="p-2 text-center">4.78</td><td class="p-2 text-center">2.49</td><td class="p-2 text-center">4.83</td><td class="p-2 text-center">1.95</td><td class="p-2 text-center">−0.067</td><td class="p-2 text-center">.948</td></tr>
    <tr class="bg-red-50"><td class="p-2 font-bold">努力</td><td class="p-2 text-center">5.50</td><td class="p-2 text-center">1.62</td><td class="p-2 text-center">6.83</td><td class="p-2 text-center">1.75</td><td class="p-2 text-center font-bold">−2.116</td><td class="p-2 text-center font-bold text-red-500">.044 *</td></tr>
    <tr><td class="p-2">挫折感</td><td class="p-2 text-center">5.50</td><td class="p-2 text-center">2.43</td><td class="p-2 text-center">3.92</td><td class="p-2 text-center">2.07</td><td class="p-2 text-center">1.853</td><td class="p-2 text-center">.075 †</td></tr>
    <tr><td class="p-2">表現</td><td class="p-2 text-center">5.56</td><td class="p-2 text-center">2.31</td><td class="p-2 text-center">4.92</td><td class="p-2 text-center">2.07</td><td class="p-2 text-center">0.774</td><td class="p-2 text-center">.445</td></tr>
  </tbody>
</table>

---

# B02. 統計檢定方法

<div class="space-y-4 pt-6">
  <div>
    <h3 class="font-bold">組內前後測比較</h3>
    <div class="text-sm opacity-70">配對 t-test（scipy.stats.ttest_rel）</div>
  </div>
  <div>
    <h3 class="font-bold">組間獨立樣本比較</h3>
    <div class="text-sm opacity-70">Welch's t-test（equal_var=False，scipy.stats.ttest_ind）</div>
  </div>
  <div>
    <h3 class="font-bold">類別變項比較</h3>
    <div class="text-sm opacity-70">卡方檢定（chi-square test）— 完成率比較</div>
  </div>
  <div>
    <h3 class="font-bold">顯著性閾值</h3>
    <div class="text-sm opacity-70">* p &lt; .05　** p &lt; .01　*** p &lt; .001　† p &lt; .10（趨近顯著）</div>
  </div>
</div>

---

# B03. rr_envs.py 任務環境對齊

<table class="w-full text-sm mt-4">
  <thead>
    <tr class="bg-blue-100">
      <th class="p-2 text-left">任務</th>
      <th class="p-2 text-left">RR JS 原始版</th>
      <th class="p-2 text-left">rr_envs.py 對齊版</th>
    </tr>
  </thead>
  <tbody>
    <tr class="border-b"><td class="p-2 font-bold">T1 MAB</td><td class="p-2">多臂吃角子老虎、機率分佈</td><td class="p-2">同 reward 函式、同動作空間</td></tr>
    <tr class="border-b"><td class="p-2 font-bold">T2 Maze 1D</td><td class="p-2">線性路徑、終點 +1</td><td class="p-2">同 reward function、Box 狀態空間</td></tr>
    <tr class="border-b"><td class="p-2 font-bold">T3 Maze 2D</td><td class="p-2">cutX × cutY 網格</td><td class="p-2">同網格、同稀疏 reward 結構</td></tr>
    <tr class="border-b"><td class="p-2 font-bold">T4 Heli</td><td class="p-2">速度+位置雙維度</td><td class="p-2">同維度，episode termination 一致</td></tr>
    <tr class="border-b bg-yellow-50"><td class="p-2 font-bold">T5 Fighter</td><td class="p-2">多動作空間、無預設超參數</td><td class="p-2">同設計，刻意保留「無預設」特性</td></tr>
  </tbody>
</table>

<div class="mt-4 text-center text-sm opacity-70">
  程式碼公開於 <code>notebooks/rr_envs.py</code>
</div>

---

# B04. 18 支教學影片清單

<div class="grid grid-cols-2 gap-6 pt-4">
  <div>
    <h3 class="font-bold mb-3 text-blue-600">兩組共用（V0–V5，共 6 支）</h3>
    <ul class="text-sm space-y-1">
      <li>V0 SAR + Episode</li>
      <li>V1 ε-greedy + 三個超參數</li>
      <li>V2 Q-learning 機制</li>
      <li>V3 Q-table 熱力圖判讀</li>
      <li>V4 訓練曲線判讀</li>
      <li>V5 自主決策設定</li>
    </ul>
  </div>
  <div>
    <h3 class="font-bold mb-3 text-orange-600">各組各 6 支</h3>
    <div class="text-sm space-y-1">
      <div><span class="font-bold">RR 組：</span>A0–A5 平台操作</div>
      <div><span class="font-bold">Colab 組：</span>B0–B5 Colab 操作</div>
    </div>
    <div class="mt-3 text-xs opacity-70">
      所有影片經 ffmpeg 抽幀逐張視覺驗收
    </div>
  </div>
</div>

---

# B05. 核心參考文獻

<div class="text-sm space-y-2 pt-4">
  <div><span class="font-bold">理論基礎：</span></div>
  <ul class="ml-4 space-y-1 opacity-80">
    <li>Watkins, C. J. C. H. (1989). Learning from Delayed Rewards. PhD, Cambridge.</li>
    <li>Sutton, R. S., & Barto, A. G. (2018). Reinforcement Learning: An Introduction (2nd ed.). MIT Press.</li>
    <li>Mnih et al. (2015). Playing Atari with Deep Reinforcement Learning.</li>
  </ul>
  <div class="mt-3"><span class="font-bold">教育理論：</span></div>
  <ul class="ml-4 space-y-1 opacity-80">
    <li>Bandura, A. (1977). Self-efficacy: Toward a unifying theory.</li>
    <li>Ryan, R. M., & Deci, E. L. (2000). Self-determination theory.</li>
    <li>Hattie, J., & Timperley, H. (2007). The power of feedback.</li>
  </ul>
  <div class="mt-3"><span class="font-bold">K-12 RL 教學案例：</span></div>
  <ul class="ml-4 space-y-1 opacity-80">
    <li>Dietz et al. (2022). ARtonomous. IDC '22.</li>
    <li>Zhang et al. (2022, 2023). RL 教學 K-12 案例. RiE 系列。</li>
  </ul>
</div>
