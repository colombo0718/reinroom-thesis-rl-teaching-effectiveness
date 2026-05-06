# 實驗組教案（RR 平台）

**對象：** 大學生（國際生）｜**授課語言：** 英文
**日期：** 第1堂 4/21（二）、第2堂 4/28（二）｜**時間：** 14:10–17:00
**平台：** Rein Room — https://reinroom.leaflune.org/

---

## 第 1 堂（4/21）

### 14:10–14:30｜前測問卷（20 min）

**教師指示語：**
> "Before we start today's class, please open the Google Form link on the screen and complete the questionnaire. This is NOT a graded test — it's just to understand your background. Please answer honestly, including if you've never heard of reinforcement learning before. It should take about 15–20 minutes."

**學生任務：**
- 打開 Google Form（教師投影連結或分享連結）
- 完成背景資料、RL 概念題

**注意事項：** 確保每位學生都有填寫學號或班級代號，以利配對前後測。

---

### 14:30–14:50｜RL 概念講解 PPT（20 min）

**教師指示語：**
> "Now let's talk about what reinforcement learning actually is. You might have heard of AlphaGo, or games where AI learns to play by itself — that's reinforcement learning. Let me show you the core idea."

**講解重點（對應目標 1：SAR 循環）：**

1. **情境類比：** 訓練寵物的過程
   > "Imagine you're training a dog. The dog is the *agent*. The room is the *environment*. What the dog sees right now — that's the *state*. What the dog does (sit, run, bark) — that's the *action*. When the dog does something right and gets a treat — that's the *reward*."

2. **SAR 循環圖示：**
   > "Every single step follows this loop: the agent observes the state → chooses an action → receives a reward → moves to the next state. This loop repeats until the episode ends."

3. **Episode 概念：**
   > "An *episode* is one complete run — like one game of chess from start to finish. After the episode ends, we reset and start a new one. The agent learns a little more each episode."

**學生任務：** 聆聽，可舉手提問。PPT 留一張空白：讓學生口頭說出「State / Action / Reward 各是什麼」。

---

### 14:50–15:20｜RR 介面導覽 + MAB 任務（30 min）

**教師指示語（介面導覽）：**
> "Now open your browser and go to this URL: reinroom.leaflune.org — that's R-E-I-N-R-O-O-M dot leaflune dot org. This is the platform we'll be using today. Let me walk you through the interface."

**介面說明重點：**
- 左側遊戲區：Agent 在這裡行動
- 右側控制面板：
  - 🎮 遊戲頁：選任務
  - 📊 儀錶頁：調參數（α、γ、ε）、看訓練圖表
  - 🔬 分析頁：Q-table 熱力圖

**MAB 任務（對應目標 2：探索 vs 利用）：**

> "Let's start with the simplest task — Multi-Armed Bandit. Think of it as a row of slot machines. Each machine has a different hidden probability of giving you a reward. Your agent has to figure out which machine is best — but it can only learn by trying."

步驟 1：載入 MAB 任務，ε 設為 **0.9**，按啟動，讓學生觀察約 1 分鐘。
> "With ε = 0.9, the agent tries random machines 90% of the time. What do you notice about the reward curve?"

步驟 2：清除，ε 改為 **0.1**，重新啟動，觀察比較。
> "Now with ε = 0.1, the agent mostly sticks to what it thinks is the best machine. Is this better or worse? Why might always choosing the 'best' option be a problem?"

**學生任務：**
- 自己試兩種設定（ε = 0.9 和 ε = 0.1）
- 觀察報酬曲線差異，準備口頭回答：「哪種設定讓平均報酬更穩定？」

---

### 15:20–15:30｜休息（10 min）

---

### 15:30–15:45｜V2 影片：How Agents Learn — Q-table & Update Rule（15 min）

**教師指示語：**
> "Before we try Maze1D, watch this short video — it explains how the agent actually stores and updates what it learns."

---

### 15:45–16:30｜Maze1D 任務（45 min）｜目標 1：SAR 循環 + Q-table（T2）

**教師指示語：**
> "Now let's try a maze. In Maze1D, the agent is on a line and needs to reach the goal. This environment is simple enough that we can clearly see what state, action, reward, and episode each mean — let's verify your understanding here."

**Part A：教師演示 γ 效果（約 15 min）**

> "First, I'll show you how the discount factor γ affects behavior. γ controls whether the agent cares about immediate or future rewards."

- γ = 0.1：
  > "With a low γ, the agent is short-sighted — it only cares about the reward right now. Watch what happens."

- γ = 0.9：
  > "With a high γ, the agent is patient — willing to take a longer path for a bigger reward later."

> Note: γ will not be tested directly — this is for building intuition only.

**Part B：SAR 循環確認（約 15 min）｜T2 評量**

學生跑 Maze1D 後，助教逐一詢問每位學生：

> "In this Maze1D game — **what is the state? What are the actions? When does the agent receive a reward? Where does one episode start and end?**"

預期回答：
- **State**：agent 在 1D line 上的位置
- **Actions**：向左移 / 向右移
- **Reward**：到達 goal 得正獎勵；掉入陷阱或超時得負獎勵
- **Episode**：從起點出發，到達 goal 或超時為止，reset 後開始下一 episode

**學生任務：** 自己試兩種 γ，觀察路徑差異；然後能口頭回答上述四個問題。

> ✅ **T2 完成標準：** 能正確說出 Maze1D 中 state / action / reward / episode 各代表什麼

---

### 16:30–17:00｜Maze2D 初探（30 min）｜不評量

**教師指示語：**
> "Now let's get a first look at 2D maze. Just start the agent and watch it explore — we'll do a deeper analysis next class after watching a video about Q-table heatmaps."

**學生任務：**
- 開啟 Maze2D，按 Start，觀察 agent 在 grid 中的移動
- 可自由調整參數，觀察行為變化
- **不需要完成任何評量任務**，純粹熟悉環境

> ℹ️ T3（Q-table 熱力圖路徑指認）在第 2 堂 V3 影片後進行。

---

## 第 2 堂（4/28）

### 14:10–14:20｜複習（10 min）

**教師指示語：**
> "Let's do a quick recap. Last week we covered the core loop of reinforcement learning. Can anyone tell me — what are the three key elements in every RL step?"

預期學生回答：State, Action, Reward（目標 1 確認）

> "And what does ε control in the MAB task?"

預期回答：exploration vs exploitation（目標 2 確認）

---

### 14:20–14:35｜V3 影片：Reading the Q-table Heatmap（15 min）

**教師指示語：**
> "Before we dive into Maze2D analysis, watch this video — it explains how to read the Q-table heatmap and trace a path."

---

### 14:35–15:05｜Maze2D 深探（30 min）｜目標 4：Q-table 基本讀法（T3）

**教師指示語：**
> "Now open Maze2D again. This time we're going to the Analysis tab to read the Q-table heatmap."

**步驟 1：切換至分析頁，講解熱力圖（約 10 min）**
> "Click on the 🔬 Analysis tab. Each cell shows the direction the agent currently thinks is best. Strong color = confident; weak color = hasn't explored much."

**步驟 2：學生追蹤路徑（約 20 min）**
> "Can you trace a path from Start to Goal just by following the arrow colors?"

**學生任務：**
- 啟動 Maze2D 訓練，等待約 500–1000 steps
- 切換到分析頁，口頭指出從 Start 到 Goal 的路徑

> ✅ **T3 完成標準：** 能在 Q-table 熱力圖上指出 Start→Goal 路徑

---

### 15:05–15:20｜V4 影片：Reading Training Curves + A4 Heli Demo（15 min）

**教師指示語：**
> "Good work on Maze2D. Now watch these two short videos — one on how to read training curves, one showing what we'll do with Heli."

---

### 15:20–15:30｜休息（10 min）

---

### 15:30–16:00｜Heli 任務（30 min）｜目標 3：訓練曲線判讀（T4）

**教師指示語：**
> "Today's main task is Heli — a helicopter that needs to fly through gaps. Each episode, the helicopter starts fresh. Your job is to watch the reward curve and figure out when the agent starts improving."

**步驟 1：啟動，觀察早期行為（約 5 min）**
> "In the first few episodes, the helicopter crashes quickly — that's expected. Watch the reward chart on the right. What does a very low reward mean?"

**步驟 2：觀察至少 50 episodes，觀察曲線趨勢（約 25 min）**

對應目標 3：訓練曲線判讀
> "As training continues, does the reward go up? Stay flat? What does an upward trend tell you about the agent's learning?"

> "Look at the shape of the curve. Is it noisy? Smooth? Does it ever suddenly drop after improving — what might cause that?"

**步驟 3：對比高低 ε（選做，約 15 min）**

先 Reset，將 ε 從 0.3 改為 0.05，重新觀察 50 episodes：
> "With almost no exploration, does the agent improve faster or slower? Why might that be a problem?"

**學生任務（T4 評量）：**
- 觀察至少 50 episodes
- 回答（口頭）：
  1. Describe the shape of the reward curve in one sentence.
  2. Around which episode did you first notice improvement?
  3. What does a sudden drop in reward tell you?

> ✅ **T4 完成標準：** 觀察至少 50 episodes，能描述 reward 曲線趨勢（例如：先低後升、持續震盪等）

---

### 16:00–16:10｜V5 影片：Continuous State & Discretization（10 min）

**教師指示語：**
> "Before Fighter, watch this short video on continuous states — it explains why Heli and Fighter need a different approach."

---

### 16:10–16:40｜Fighter 挑戰（30 min）｜延伸自由體驗，不納入評量（T5 選做）

**教師指示語：**
> "This one is free exploration — no assessment. Fighter is a fighting game environment. Try any parameter combinations you want and see how the agent learns. Have fun with it."

**學生任務：** 自由調整 ε、α，觀察 agent 學習行為。教師巡視、回答問題。

> ✅ **T5 記錄：** 有嘗試 Fighter 即記錄為完成（不計入完成率分析）

---

### 16:40–17:00｜後測問卷（20 min）

**教師指示語：**
> "Last step — please open the post-test Google Form on the screen. It covers the same RL concept questions from the pre-test, plus questions about the platform, a cognitive load survey, and a usability survey."

**學生任務：** 完成 Google Form 後測（Section 1+2 概念題、Section 3A RR 平台回饋、Section 4 NASA-TLX、Section 5A SUS）。
