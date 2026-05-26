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
各位老師午安，我是 [姓名]，今天要報告的題目是
《Rein Room 強化教室：視覺化互動強化學習教學平台之設計與教學成效評估》，
由黃怡錚老師指導。
-->

---
layout: default
---

# 簡報大綱

<div class="grid grid-cols-5 gap-4 pt-12">
  <div class="border rounded p-4 text-center">
    <div class="text-3xl font-bold text-blue-500">1</div>
    <div class="mt-2">研究動機</div>
    <div class="text-sm opacity-60">與問題</div>
  </div>
  <div class="border rounded p-4 text-center">
    <div class="text-3xl font-bold text-blue-500">2</div>
    <div class="mt-2">RR 平台</div>
    <div class="text-sm opacity-60">設計與特色</div>
  </div>
  <div class="border rounded p-4 text-center">
    <div class="text-3xl font-bold text-blue-500">3</div>
    <div class="mt-2">研究設計</div>
    <div class="text-sm opacity-60">A/B 準實驗</div>
  </div>
  <div class="border rounded p-4 text-center bg-blue-50">
    <div class="text-3xl font-bold text-blue-700">4</div>
    <div class="mt-2 font-bold">主要發現</div>
    <div class="text-sm opacity-60">三大實證</div>
  </div>
  <div class="border rounded p-4 text-center">
    <div class="text-3xl font-bold text-blue-500">5</div>
    <div class="mt-2">結論</div>
    <div class="text-sm opacity-60">與貢獻</div>
  </div>
</div>

<!-- 接下來 20 分鐘會依序談五個部分，第四部分主要發現是今天的重頭戲。 -->

---
layout: section
---

# Part 1.
# 研究動機與問題

---
layout: default
---

# 一句話結論先講

<div class="flex items-center justify-center h-3/4">
  <div class="text-3xl text-center leading-relaxed">
    本研究實證<br>
    <span class="text-blue-600 font-bold">視覺化互動式 RL 教學平台</span><br>
    在學生<span class="text-red-500 font-bold">「自主操作能力」</span>上<br>
    有<span class="font-bold">獨立於程式碼導向工具</span>的貢獻
  </div>
</div>

<!--
報告開始前先告訴各位老師結論的一句話。
詳細數據與論述待會展開。
-->

---

# RL 是 AI 核心技術，但門檻高

<div class="grid grid-cols-2 gap-8 pt-8">
  <div>
    <h3 class="text-xl font-bold mb-4">RL 已是 AI 三大核心之一</h3>
    <ul class="space-y-2">
      <li>🎯 AlphaGo / AlphaZero（Silver et al., 2018）</li>
      <li>🚗 自動駕駛決策（Sallab et al., 2017）</li>
      <li>🤖 大型語言模型對齊（RLHF）</li>
      <li>🎮 遊戲 AI（Mnih et al., 2015）</li>
    </ul>
  </div>
  <div>
    <h3 class="text-xl font-bold mb-4">但學習者的門檻很高</h3>
    <ul class="space-y-2">
      <li>❌ 需要寫程式（Python、Gymnasium）</li>
      <li>❌ 需要環境安裝（套件、依賴）</li>
      <li>❌ 抽象概念難視覺化</li>
      <li>❌ 學習回饋週期太長</li>
    </ul>
  </div>
</div>

<!--
RL 已是 AI 三大核心技術之一，但其抽象性與程式門檻
使其難以下放給非資工背景學習者。
-->

---

# 現有 RL 教學平台的限制

| 路徑 | 代表 | 優勢 | 限制 |
|------|------|------|------|
| **程式碼導向** | Gymnasium + Colab | 業界標準、彈性高 | 程式門檻、回饋週期長 |
| **硬體導向** | LEGO + RL (Zhang et al., 2022) | 實體操作、具象化 | 成本高、後勤複雜、難規模化 |
| **視覺化互動** | ARtonomous (Dietz et al., 2022) | 低門檻、即時回饋 | 案例少、缺實證評量 |

<div class="mt-12 text-center text-xl text-blue-600">
  ⇒ 第三條路是值得驗證的方向
</div>

<!--
現有 K-12 / 入門 RL 教學分兩派，視覺化互動平台是值得深入驗證的第三條路。
-->

---

# 研究問題（RQ）

<div class="grid grid-cols-3 gap-6 pt-12">
  <div class="border-2 border-blue-300 rounded-lg p-6">
    <div class="text-blue-600 text-3xl font-bold mb-3">RQ 1</div>
    <div class="font-bold mb-2">概念理解</div>
    <div class="text-sm opacity-80">
      視覺化平台能否有效傳遞 RL 核心概念（state / action / reward / episode）？
    </div>
  </div>
  <div class="border-2 border-blue-300 rounded-lg p-6">
    <div class="text-blue-600 text-3xl font-bold mb-3">RQ 2</div>
    <div class="font-bold mb-2">圖表判讀</div>
    <div class="text-sm opacity-80">
      學習者能否透過平台建立訓練曲線與 Q-table 熱力圖的判讀能力？
    </div>
  </div>
  <div class="border-2 border-blue-300 rounded-lg p-6">
    <div class="text-blue-600 text-3xl font-bold mb-3">RQ 3</div>
    <div class="font-bold mb-2">自主操作</div>
    <div class="text-sm opacity-80">
      平台能否提升學習者的自主操作能力與學習動機？
    </div>
  </div>
</div>

<!--
本研究三個核心問題。
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
      https://reinroom.leaflune.org/
    </div>
  </div>
</div>

<!--
RR 是我自行開發的純前端 RL 教學平台，網址打開就能用，不用安裝任何環境。
-->

---

# 核心特色 1：滑桿即時調參

<div class="grid grid-cols-2 gap-8">
  <div>
    <img src="/images/fig3-1a.png" class="rounded shadow-lg" />
    <div class="text-center text-sm mt-2 opacity-60">超參數滑桿</div>
  </div>
  <div class="flex flex-col justify-center">
    <h3 class="text-xl font-bold mb-3 text-red-500">操作回饋週期：從 30 秒 → 1 秒</h3>
    <div class="space-y-3 text-base">
      <div>
        <span class="font-bold">傳統程式碼導向：</span><br>
        <span class="opacity-70">改程式 → 重跑 → 看結果（~30 秒循環）</span>
      </div>
      <div class="text-red-500">
        <span class="font-bold">RR 滑桿介面：</span><br>
        拖一下 → 看一下（~1 秒循環）
      </div>
    </div>
    <div class="mt-6 p-3 bg-yellow-50 border-l-4 border-yellow-400 text-sm">
      💡 學生在拖曳過程中即可建立<br>
      「過大 → 行為 X、過小 → 行為 Y」的直觀感受
    </div>
  </div>
</div>

<!--
最關鍵設計：所有超參數以滑桿即時調整，毫秒級反映在曲線與熱力圖。
這是 RR 與 Colab 最本質的差異。
-->

---

# 核心特色 2：訓練曲線即時刷新

<div class="grid grid-cols-2 gap-6">
  <div>
    <img src="/images/fig3-7.png" class="rounded shadow-lg" />
    <div class="text-center text-sm mt-2 opacity-60">訓練曲線 — 即時更新</div>
  </div>
  <div>
    <img src="/images/fig3-8.png" class="rounded shadow-lg" />
    <div class="text-center text-sm mt-2 opacity-60">動作選擇熱力圖</div>
  </div>
</div>

<div class="text-center text-lg mt-6 text-blue-600">
  讓學生看見智能體當下的策略地圖，不再是黑盒子
</div>

<!--
即時更新的訓練曲線與動作選擇熱力圖，讓學生看見學習過程，不再是 print log 的黑盒子。
-->

---

# 核心特色 3：Q 值與動作機率視覺化

<div class="text-center">
  <img src="/images/fig3-9.png" class="max-h-80 mx-auto rounded shadow-lg" />
</div>

<div class="grid grid-cols-3 gap-4 mt-4 text-sm">
  <div class="text-center"><span class="font-bold text-blue-500">原色：</span>原始 Q 值</div>
  <div class="text-center"><span class="font-bold text-green-500">深色：</span>ε-greedy 機率</div>
  <div class="text-center"><span class="font-bold text-orange-500">紋理：</span>Softmax 機率</div>
</div>

<!--
分析頁三柱圖把「策略 Q 值」和「實際動作選擇」的關係明確攤開。
-->

---

# 五個遊戲環境 — 由簡入難的學習階梯

<div class="grid grid-cols-5 gap-2 pt-4">
  <div class="text-center">
    <img src="/images/fig3-11a.png" class="h-32 mx-auto rounded shadow" />
    <div class="mt-2 font-bold text-sm">T1 Maze 1D</div>
    <div class="text-xs opacity-60">概念入門</div>
  </div>
  <div class="text-center">
    <img src="/images/fig3-11b.png" class="h-32 mx-auto rounded shadow" />
    <div class="mt-2 font-bold text-sm">T2 Maze 2D</div>
    <div class="text-xs opacity-60">熱力圖</div>
  </div>
  <div class="text-center">
    <img src="/images/fig3-11c.png" class="h-32 mx-auto rounded shadow" />
    <div class="mt-2 font-bold text-sm">T3 Dino</div>
    <div class="text-xs opacity-60">連續狀態</div>
  </div>
  <div class="text-center">
    <img src="/images/fig3-11d.png" class="h-32 mx-auto rounded shadow" />
    <div class="mt-2 font-bold text-sm">T4 Heli</div>
    <div class="text-xs opacity-60">曲線判讀</div>
  </div>
  <div class="text-center border-2 border-red-400 rounded p-1">
    <img src="/images/fig3-11e.png" class="h-32 mx-auto rounded shadow" />
    <div class="mt-2 font-bold text-sm text-red-500">T5 Fighter</div>
    <div class="text-xs opacity-60">無預設參數</div>
  </div>
</div>

<div class="mt-6 text-center text-sm opacity-60">
  本研究使用 T1–T5 作為評量任務；T5 為「自主決策」進階任務
</div>

<!--
五個遊戲構成從 1D 迷宮到 Fighter 自主決策的學習階梯。T5 是核心評量。
-->

---
layout: section
---

# Part 3.
# 研究設計

---

# 準實驗 A/B 對照流程

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
採準實驗設計，兩天各 3 小時連續課程，相同教學節奏。
-->

---

# Treatment Fidelity 七層次（上）

<div class="space-y-3 pt-4">
  <div class="flex items-center gap-3">
    <div class="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold">1</div>
    <div><span class="font-bold">任務環境對齊（rr_envs.py）</span> — 把 RR 任務逐字對齊到 Gymnasium，兩組任務本質完全相同</div>
  </div>
  <div class="flex items-center gap-3">
    <div class="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold">2</div>
    <div><span class="font-bold">AI 影片 18 支</span> — 6 支共用 RL 理論影片 + 各組 6 支，消除講師差異</div>
  </div>
  <div class="flex items-center gap-3">
    <div class="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold">3</div>
    <div><span class="font-bold">預寫講師講稿</span> — A 組 410 行、B 組 378 行，照念設計</div>
  </div>
  <div class="flex items-center gap-3">
    <div class="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold">4</div>
    <div><span class="font-bold">標準化學生指引</span> — 兩組各以 13 步驟編號排列</div>
  </div>
</div>

<div class="mt-6 text-center text-blue-600 text-sm">
  目的：讓「平台介面差異」成為兩組唯一的系統性差異
</div>

<!--
為了讓平台介面成為唯一系統性差異，我設計七層標準化。
rr_envs.py 是最重要的一層。
-->

---

# Treatment Fidelity 七層次（下）

<div class="space-y-3 pt-4">
  <div class="flex items-center gap-3">
    <div class="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold">5</div>
    <div><span class="font-bold">雙平台 redundancy</span> — Colab 同時部署於 Colab + Binder，當天備援</div>
  </div>
  <div class="flex items-center gap-3">
    <div class="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold">6</div>
    <div><span class="font-bold">Frame Review Loop</span> — 用 ffmpeg 抽幀逐張視覺驗收影片品質</div>
  </div>
  <div class="flex items-center gap-3">
    <div class="w-8 h-8 rounded-full bg-red-500 text-white flex items-center justify-center font-bold">7</div>
    <div><span class="font-bold text-red-500">實驗用平台版本凍結</span> — 實驗期間 RR 子網域不做任何修改</div>
  </div>
</div>

<div class="mt-8 p-4 bg-yellow-50 border-l-4 border-yellow-500">
  💡 <span class="font-bold">設定平台效益的「下界」(lower bound)</span><br>
  <span class="text-sm">在最低教學介入條件下仍能觀察到的差異 = 平台介面本身可歸因的效益</span>
</div>

<!--
平台版本凍結這層特別重要：所有觀察到的效益都是「最低教學介入條件下」可歸因於平台介面的部分。
更熟練的教師、更豐富的引導，預期能進一步放大 RR 在 T5 上展現的優勢。
-->

---

# 評量工具四層次

<div class="flex justify-center pt-6">
  <div class="space-y-3 text-center">
    <div class="bg-red-200 px-12 py-4 rounded shadow font-bold">
      🎯 概念層 — 前後測概念理解測驗
    </div>
    <div class="bg-orange-200 px-16 py-4 rounded shadow font-bold">
      📊 行為層 — 任務完成率 + 完成時間（雙指標）
    </div>
    <div class="bg-yellow-200 px-20 py-4 rounded shadow font-bold">
      💭 情意層 — Section 3 / NASA-TLX / SUS / 開放題
    </div>
    <div class="bg-green-200 px-24 py-4 rounded shadow font-bold">
      👀 課堂觀察層 — 助教逐時記錄
    </div>
  </div>
</div>

<!--
四層次評量：概念、行為、情意、課堂觀察。
完整捕捉學習成效的不同面向。
-->

---
layout: section
class: bg-blue-50
---

# Part 4.
# 主要發現
<div class="text-xl mt-4 opacity-80">三大實證 + 兩個誠實面對</div>

---

# 概念測驗 — 兩組均進步

<div class="text-center pt-4">
  <img src="/images/fig5-1.png" class="max-h-80 mx-auto rounded shadow" />
</div>

<div class="grid grid-cols-2 gap-8 mt-4">
  <div class="text-center">
    <span class="text-blue-500 font-bold">RR 組</span>：pre 5.50 → post 6.40（n.s.）
  </div>
  <div class="text-center">
    <span class="text-gray-700 font-bold">Colab 組</span>：pre 5.00 → post 6.92（p = .01 *）
  </div>
</div>

<!-- 先看概念測驗：兩組都進步了，但進步幅度與顯著性不同。 -->

---

# 【誠實承認】Colab 概念顯著、RR 未顯著

<div class="grid grid-cols-2 gap-12 pt-8">
  <div class="bg-gray-100 p-6 rounded">
    <h3 class="font-bold text-gray-700 mb-3">事實</h3>
    <ul class="space-y-2 text-sm">
      <li>Colab 概念測驗達顯著進步（p = .01）</li>
      <li>RR 增益方向一致但未達顯著（p = .28）</li>
      <li>組間增益比較未顯著（p = .12）</li>
    </ul>
  </div>
  <div class="bg-blue-50 p-6 rounded">
    <h3 class="font-bold text-blue-700 mb-3">意涵</h3>
    <ul class="space-y-2 text-sm">
      <li>✓ 本研究承認此事實</li>
      <li>✓ <span class="font-bold">反向證明 Colab 組教學設計完整</span></li>
      <li>✓ Colab 組不是稻草人</li>
      <li>✓ 概念測驗只反映表層認知</li>
    </ul>
  </div>
</div>

<div class="mt-8 text-center text-lg text-blue-600">
  → 需檢視行為與情意層的多維指標
</div>

<!--
誠實承認：Colab 顯著進步，RR 未顯著。
這證明 Colab 組教學設計完整、未被刻意削弱。
但「學習成效」是多維的，標準化測驗只能反映表層認知。
-->

---

# 任務完成率全貌 — 前三接近、T4/T5 分歧

<div class="text-center">
  <img src="/images/fig5-3.png" class="max-h-96 mx-auto rounded shadow" />
</div>

<div class="mt-4 text-center text-blue-600">
  T1–T3 兩組完成率接近，但 <span class="font-bold">T4 開始出現完成時間差距，T5 完成率出現結構性差異</span>
</div>

<!-- 五個任務完成率，前三個接近，T4 與 T5 開始出現結構性差異。 -->

---

# 【主菜 1】T5 Fighter 完成率 61% vs 25%

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
  T5 Fighter：不提供任何預設超參數，學生需根據前序經驗自主決定 α / γ / ε
</div>

<!--
T5 刻意不給任何預設超參數，逼學生根據前序經驗自主決策。
RR 11/18 完成，Colab 3/12，差距 2.4 倍。
這是本研究最具說服力的單一發現。
-->

---

# 【主菜 1 補強】T4/T5 完成時間雙重勝出

<div class="overflow-x-auto pt-4">
  <table class="w-full text-base">
    <thead>
      <tr class="bg-blue-100">
        <th class="p-3 text-left">任務</th>
        <th class="p-3">RR 組（分鐘）</th>
        <th class="p-3">Colab 組（分鐘）</th>
        <th class="p-3">t 值</th>
        <th class="p-3">p 值</th>
      </tr>
    </thead>
    <tbody>
      <tr class="border-b">
        <td class="p-3 font-bold">T4 Heli</td>
        <td class="p-3 text-center">17.6</td>
        <td class="p-3 text-center">53.0</td>
        <td class="p-3 text-center">−3.505</td>
        <td class="p-3 text-center text-red-500 font-bold">.014 *</td>
      </tr>
      <tr class="bg-red-50">
        <td class="p-3 font-bold">T5 Fighter</td>
        <td class="p-3 text-center">20.4</td>
        <td class="p-3 text-center">33.3</td>
        <td class="p-3 text-center">−5.000</td>
        <td class="p-3 text-center text-red-500 font-bold">&lt; .001 ***</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="mt-6 text-center text-blue-600 text-lg">
  RR 不只完成率高，<span class="font-bold">「完成所需努力」結構性更少</span>
</div>

<!--
T5 完成時間 RR 20.4 vs Colab 33.3，p < .001。
T4 完成率相近但時間差更大（17.6 vs 53.0，p=.014）。
這是「完成率 + 完成時間」雙指標的力量。
-->

---

# 【主菜 1 收尾】「完成率 + 完成時間」雙指標方法

<div class="grid grid-cols-2 gap-4 pt-8">
  <div class="border rounded p-4">
    <h3 class="font-bold mb-2">只看完成率的問題</h3>
    <div class="text-sm opacity-70">
      可能高估能力 — 完成的人可能花很久才完成
    </div>
  </div>
  <div class="border rounded p-4">
    <h3 class="font-bold mb-2">只看完成時間的問題</h3>
    <div class="text-sm opacity-70">
      會忽略未完成樣本 — 失敗者根本不在統計裡
    </div>
  </div>
</div>

<div class="mt-8 p-6 bg-blue-100 rounded">
  <div class="text-center font-bold text-lg text-blue-700">
    雙指標互補 → 完整描述「遷移能力」
  </div>
  <div class="text-center text-sm mt-2 opacity-70">
    本研究方法學貢獻之一：可推廣到其他平台類教學工具的評量
  </div>
</div>

<!--
不只看完成率會錯失「完成所需努力」；不只看完成時間會遺漏未完成樣本。
雙指標互補才能完整描述遷移能力。這是本研究的方法學貢獻。
-->

---

# 【主菜 2】開放題 6-2「最困難的部分」

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
        <td class="p-3">概念 / 術語理解困難</td>
        <td class="p-3 text-center">17%</td>
        <td class="p-3 text-center">8%</td>
        <td class="p-3 text-center">0.5 ×</td>
      </tr>
      <tr class="border-b">
        <td class="p-3">任務不明確 / 資訊量過大</td>
        <td class="p-3 text-center">11%</td>
        <td class="p-3 text-center">0%</td>
        <td class="p-3 text-center text-orange-500">RR 獨有</td>
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

<!--
請學生自己寫「最困難的部分」，編碼後得到驚人發現。
參數調整與圖表判讀困難，Colab 都是 RR 的 2.5 倍。
-->

---

# 【主菜 2 補強】質性語言對比

<div class="grid grid-cols-2 gap-6 pt-6">
  <div class="border-2 border-blue-400 rounded-lg p-6">
    <h3 class="font-bold text-blue-600 mb-3">RR 組：感受性語言</h3>
    <ul class="space-y-3 text-sm">
      <li class="italic">"learned how the parameters affects the performance"</li>
      <li class="italic">"Task 4 because the content was pretty interesting and easy to understand"</li>
      <li class="italic">"adjusting the value"</li>
    </ul>
    <div class="mt-4 text-xs opacity-70">→ 多以「感受到」「能調」為主軸</div>
  </div>
  <div class="border-2 border-gray-400 rounded-lg p-6">
    <h3 class="font-bold text-gray-700 mb-3">Colab 組：程序性語言</h3>
    <ul class="space-y-3 text-sm">
      <li class="italic">"Hyperparameter Tuning. Choosing values for Learning rate (α), Discount factor (γ), Exploration rate (ε)."</li>
      <li class="italic">"Small changes can lead to very different behaviors"</li>
    </ul>
    <div class="mt-4 text-xs opacity-70">→ 精準描述但仍將其列為最困難</div>
  </div>
</div>

<div class="mt-6 text-center text-blue-600">
  <span class="font-bold">Colab 能精準描述參數理論、RR 則建立直觀感受</span>
</div>

<!--
兩組學生對參數的描述語言截然不同：
RR 學生用感受性語言，Colab 學生用程序性語言。
Colab 能精準描述參數理論，RR 建立直觀感受。
-->

---

# 【主菜 3】Section 3 量表 — 三項一致勝出

<div class="text-center">
  <img src="/images/fig5-4.png" class="max-h-72 mx-auto rounded shadow" />
</div>

<table class="w-full text-base mt-4">
  <thead>
    <tr class="bg-blue-100">
      <th class="p-2 text-left">構面</th>
      <th class="p-2">RR 組</th>
      <th class="p-2">Colab 組</th>
      <th class="p-2">p 值</th>
    </tr>
  </thead>
  <tbody>
    <tr class="border-b"><td class="p-2">3-2 有信心調整參數</td><td class="p-2 text-center font-bold text-blue-600">4.06</td><td class="p-2 text-center">3.50</td><td class="p-2 text-center">.19</td></tr>
    <tr class="border-b"><td class="p-2">3-3 視覺化幫助理解</td><td class="p-2 text-center font-bold text-blue-600">4.33</td><td class="p-2 text-center">4.18</td><td class="p-2 text-center">.72</td></tr>
    <tr class="border-b bg-red-50"><td class="p-2 font-bold">3-4 課後學習動機</td><td class="p-2 text-center font-bold text-blue-600">4.17</td><td class="p-2 text-center">3.33</td><td class="p-2 text-center font-bold text-orange-500">.089 †</td></tr>
  </tbody>
</table>

<!--
Section 3 三項與 RR 設計訴求對應的問項全部勝出，
其中課後學習動機 p=.089 趨近顯著。
-->

---

# 【主菜 3 補強】NASA-TLX「努力」分項顯著低

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
        RR 整體心智負荷略高（資訊密度副作用）<br><br>
        <span class="font-bold text-red-500">但「努力」分項顯著低於 Colab</span><br>
        <span class="text-sm opacity-70">呼應開放題的「參數困難」2.5× 結果</span>
      </div>
    </div>
  </div>
</div>

<!--
NASA-TLX 拆六分項後「努力」顯著低，呼應開放題的參數困難 2.5× 結果。
-->

---

# 【誠實承認】SUS 系統易用性 RR 略低

<div class="text-center">
  <img src="/images/fig5-5.png" class="max-h-80 mx-auto rounded shadow" />
</div>

<div class="grid grid-cols-2 gap-8 mt-4">
  <div class="text-center">
    <span class="text-gray-700 font-bold">Colab 組</span>：73.5（Good）
  </div>
  <div class="text-center">
    <span class="text-blue-500 font-bold">RR 組</span>：59.0（Marginal）　p = .037 *
  </div>
</div>

<!--
SUS 不掩飾：RR 59.0、Colab 73.5。
但 RR 標準差大（19.8 vs 14.1），兩極化反應。
-->

---

# SUS 結果的兩個合理解讀

<div class="grid grid-cols-2 gap-6 pt-8">
  <div class="border-l-4 border-blue-500 pl-4">
    <h3 class="font-bold text-blue-600 mb-3">解讀 1：Colab 熟悉度紅利</h3>
    <p class="text-sm">
      多數學生已使用過 Colab，SUS 量表難以區分：<br>
      <span class="opacity-70">「系統設計品質好」vs「使用者已熟悉系統」</span>
    </p>
  </div>
  <div class="border-l-4 border-orange-500 pl-4">
    <h3 class="font-bold text-orange-600 mb-3">解讀 2：RR 資訊密度副作用</h3>
    <p class="text-sm">
      課堂觀察證實 RR 視覺化資訊密度較高：<br>
      <span class="opacity-70">部分學生資訊過載 → 難以聚焦核心目標</span><br>
      <span class="opacity-70">已導出明確改進方向（教室模式、分階段視覺化）</span>
    </p>
  </div>
</div>

<div class="mt-8 text-center text-blue-600">
  ⇒ 此非否定 RR 設計，而是揭示「視覺化豐富 vs 易上手」的取捨
</div>

<!--
兩種合理解讀：Colab 熟悉度紅利 + RR 資訊密度副作用。
已導出明確改進方向，不是平台失敗。
-->

---

# 課堂觀察的補強證據

<div class="grid grid-cols-2 gap-8 pt-6">
  <div class="border rounded p-4">
    <h3 class="font-bold mb-3">RR 組：Day 1 出席流失較高</h3>
    <div class="text-3xl font-bold text-red-500 text-center mb-2">31%</div>
    <div class="text-sm opacity-70">
      Day 1 → Day 2 出席流失<br>
      （Colab 13%）<br><br>
      <span class="text-xs">反映自主操作模式下的分心風險</span>
    </div>
  </div>
  <div class="border rounded p-4">
    <h3 class="font-bold mb-3">Colab 組：Day 1 同儕討論活絡</h3>
    <div class="text-3xl text-center mb-2">✓</div>
    <div class="text-sm opacity-70">
      兩組課堂中唯一「活絡」勾選<br><br>
      <span class="text-xs">原因：程式碼錯誤需要互相協助</span><br>
      <span class="text-xs">→ RR 設計可學習之處（同儕互動機制）</span>
    </div>
  </div>
</div>

<!--
課堂觀察提供量化指標看不到的補強：
RR Day 1 流失較高，反映自主操作模式下分心風險；
Colab 同儕討論活絡，是平台設計可學習之處。
-->

---
layout: section
---

# Part 5.
# 論述收束與貢獻

---

# 凸顯 RR 優勢的四層論述

<div class="flex justify-center pt-4">
  <div class="space-y-3 text-center">
    <div class="bg-gray-200 px-8 py-3 rounded shadow w-96">
      <span class="font-bold">① 誠實承認</span><br>
      <span class="text-sm">Colab 概念顯著、SUS 勝出</span>
    </div>
    <div class="bg-yellow-200 px-12 py-3 rounded shadow w-[28rem]">
      <span class="font-bold">② 反向印證 Colab 未被放水</span><br>
      <span class="text-sm">Colab 教學設計完整且公平</span>
    </div>
    <div class="bg-orange-200 px-16 py-3 rounded shadow w-[34rem]">
      <span class="font-bold">③ 在對手亦表現良好的前提下，RR 仍逆轉</span><br>
      <span class="text-sm">T5 雙重指標 + 開放題 2.5× + 量表三項一致</span>
    </div>
    <div class="bg-red-200 px-20 py-3 rounded shadow w-[40rem]">
      <span class="font-bold">④ 可復用性與未來性</span><br>
      <span class="text-sm">教師易上手、平台可持續演進</span>
    </div>
  </div>
</div>

<!--
總結邏輯（被問貢獻時的標準答案）：
1. Colab 概念顯著、SUS 勝出，承認。
2. 這反向證明Colab 組不是稻草人。
3. 在對手亦表現良好的前提下，RR 仍於 T5 明顯逆轉。
4. 平台還具可復用性與未來演進性。
-->

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
本研究經驗推廣到一般視覺化互動式教學平台，整理五點設計建議。
-->

---

# 研究貢獻三點

<div class="space-y-6 pt-8">
  <div class="flex items-start gap-4">
    <div class="text-4xl">🎯</div>
    <div>
      <div class="font-bold text-lg">實證貢獻</div>
      <div class="text-sm opacity-80">
        實證視覺化互動式 RL 平台在不犧牲概念理解的前提下，於遷移能力與操作直覺感上產生獨特優勢
      </div>
    </div>
  </div>
  <div class="flex items-start gap-4">
    <div class="text-4xl">🔬</div>
    <div>
      <div class="font-bold text-lg">方法學貢獻</div>
      <div class="text-sm opacity-80">
        提出「完成率 + 完成時間」雙指標評量法，可推廣到其他平台類教學工具<br>
        + 七層次 Treatment Fidelity 設計範例
      </div>
    </div>
  </div>
  <div class="flex items-start gap-4">
    <div class="text-4xl">💡</div>
    <div>
      <div class="font-bold text-lg">設計貢獻</div>
      <div class="text-sm opacity-80">
        整理五點對未來視覺化互動式教學平台設計者之具體建議
      </div>
    </div>
  </div>
</div>

<!--
三項貢獻：實證 + 方法學 + 設計建議。
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
    <div class="text-sm opacity-70">雖採 Treatment Fidelity 七層次標準化，仍可能存在班級文化等難測因素</div>
  </div>
  <div class="border-l-4 border-orange-400 pl-4">
    <div class="font-bold">未測長期保留度</div>
    <div class="text-sm opacity-70">僅捕捉即時學習成效，長期記憶與技能保留待後續研究</div>
  </div>
  <div class="border-l-4 border-orange-400 pl-4">
    <div class="font-bold">範圍限定</div>
    <div class="text-sm opacity-70">結論收斂在「大學資工系」場域，未擴張至 K-12 或其他學科</div>
  </div>
</div>

<!--
研究限制：樣本偏小、跨班差異、未測長期保留度。
結論收斂在「大學資工系」實證範圍。
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
未來工作：教室模式、雙旗艦平台、長期追蹤研究。
論文完成不等於 RR 平台的終點。
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
感謝黃怡錚老師指導、張鈞博助教協助、兩位授課教師、受試學生。
請各位老師指教。
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

# B02. 統計檢定方法詳述

<div class="space-y-4 pt-6">
  <div>
    <h3 class="font-bold">組內前後測比較</h3>
    <div class="text-sm opacity-70">配對 t-test（paired t-test，scipy.stats.ttest_rel）</div>
  </div>
  <div>
    <h3 class="font-bold">組間獨立樣本比較</h3>
    <div class="text-sm opacity-70">Welch's t-test（equal_var=False，scipy.stats.ttest_ind），不假設兩組變異數相等</div>
  </div>
  <div>
    <h3 class="font-bold">類別變項比較</h3>
    <div class="text-sm opacity-70">卡方檢定（chi-square test）— 完成率比較</div>
  </div>
  <div>
    <h3 class="font-bold">效應量</h3>
    <div class="text-sm opacity-70">Cohen's d（小 0.2 / 中 0.5 / 大 0.8）</div>
  </div>
  <div>
    <h3 class="font-bold">顯著性閾值</h3>
    <div class="text-sm opacity-70">* p &lt; .05　** p &lt; .01　*** p &lt; .001　† p &lt; .10（趨近顯著）</div>
  </div>
</div>

---

# B03. rr_envs.py 對齊細節

<table class="w-full text-sm mt-4">
  <thead>
    <tr class="bg-blue-100">
      <th class="p-2 text-left">任務</th>
      <th class="p-2 text-left">RR JS 原始版</th>
      <th class="p-2 text-left">rr_envs.py 對齊版</th>
    </tr>
  </thead>
  <tbody>
    <tr class="border-b"><td class="p-2 font-bold">T1 Maze 1D</td><td class="p-2">線性路徑、終點 +1</td><td class="p-2">同 reward function，Box(low=0, high=10) 狀態空間</td></tr>
    <tr class="border-b"><td class="p-2 font-bold">T2 Maze 2D</td><td class="p-2">cutX × cutY 網格</td><td class="p-2">同網格、同稀疏 reward 結構</td></tr>
    <tr class="border-b"><td class="p-2 font-bold">T3 Dino</td><td class="p-2">連續狀態 + 跳躍動作</td><td class="p-2">同連續狀態空間 + 動作空間 {跳, 不跳}</td></tr>
    <tr class="border-b"><td class="p-2 font-bold">T4 Heli</td><td class="p-2">速度+位置雙維度</td><td class="p-2">同維度，episode termination 條件一致</td></tr>
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
    <h3 class="font-bold mb-3 text-blue-600">兩組共用（6 支）</h3>
    <ul class="text-sm space-y-1">
      <li>1. RL 基本概念 — Agent / Environment</li>
      <li>2. State / Action / Reward</li>
      <li>3. Episode 與 Episodic Task</li>
      <li>4. Q-Learning 概念</li>
      <li>5. ε-greedy 探索策略</li>
      <li>6. Hyperparameters 介紹</li>
    </ul>
  </div>
  <div>
    <h3 class="font-bold mb-3 text-orange-600">各組各 6 支</h3>
    <div class="text-sm space-y-1">
      <div><span class="font-bold">RR 組：</span>平台操作 6 支</div>
      <div><span class="font-bold">Colab 組：</span>Gymnasium 環境設定 6 支</div>
    </div>
    <div class="mt-3 text-xs opacity-70">
      所有影片經 ffmpeg 抽幀逐張視覺驗收<br>
      （Frame Review Loop SOP）
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
  <div class="mt-3"><span class="font-bold">方法學：</span></div>
  <ul class="ml-4 space-y-1 opacity-80">
    <li>Mowbray et al. (2003). Fidelity criteria.</li>
    <li>Shadish, Cook, & Campbell (2002). Quasi-Experimental Designs.</li>
    <li>Cohen, J. (1988). Statistical Power Analysis.</li>
  </ul>
  <div class="mt-3"><span class="font-bold">K-12 RL 教學案例：</span></div>
  <ul class="ml-4 space-y-1 opacity-80">
    <li>Dietz et al. (2022). ARtonomous. IDC '22.</li>
    <li>Zhang et al. (2022). An Interactive Robot Platform for K-12 RL. RiE 2021.</li>
    <li>Zhang et al. (2023). Introducing RL to K-12 with Robots and AR. RiE 2023.</li>
  </ul>
</div>
