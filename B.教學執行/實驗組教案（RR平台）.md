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

### 15:30–16:10｜Maze1D 任務（40 min）｜演示用，不列入測驗

**教師指示語：**
> "Now let's try a maze. In Maze1D, the agent is on a line and needs to reach the goal. Let me show you what happens when we change the discount factor γ — this controls whether the agent cares more about immediate rewards or future rewards."

**演示步驟（教師操作，學生觀察）：**

- γ = 0.1：
  > "With a low γ, the agent is very short-sighted — it only cares about the reward right now. Watch what happens."

- γ = 0.9：
  > "With a high γ, the agent is patient — it's willing to take a longer path if it leads to a bigger reward in the end."

**學生任務：** 自己試兩種 γ，觀察路徑有何不同。這段不出測驗題，純粹建立直覺。

---

### 16:10–17:00｜Maze2D 任務 + Q-table 熱力圖（50 min）

**教師指示語：**
> "Now we move to 2D maze. The agent needs to find its way from the start to the goal in a grid. This time, we're going to look at something really interesting — the Q-table heatmap."

**步驟 1：啟動訓練，觀察行為（約 10 min）**
> "Press start and watch the agent. At first it wanders randomly. Over time, does it start finding a more direct path to the goal?"

**步驟 2：切換至分析頁，講解熱力圖（約 15 min）**
> "Click on the 🔬 Analysis tab. This heatmap shows, for each cell in the maze, what direction the agent currently thinks is best. The color tells you the preferred action."

重點說明（對應目標 4：Q-table 基本讀法）：
> "Cells with a strong, clear color mean the agent is confident about what to do there. Cells with weak or mixed colors mean the agent hasn't figured it out yet — maybe it hasn't visited there much."

> "Look at the cells near the goal. What direction do most of them point?"

**學生任務（約 25 min）：**
- 啟動 Maze2D 訓練，等待約 500–1000 steps
- 切換到分析頁，回答以下問題（口頭討論）：
  1. Which area of the map has the clearest colors? What does that tell you?
  2. Can you trace a path from start to goal just by following the arrow colors?
  3. Are there any cells where the color is unclear or surprising?

---

## 第 2 堂（4/28）

### 14:10–14:20｜複習（10 min）

**教師指示語：**
> "Let's do a quick recap. Last week we covered the core loop of reinforcement learning. Can anyone tell me — what are the three key elements in every RL step?"

預期學生回答：State, Action, Reward（目標 1 確認）

> "And what does ε control in the MAB task?"

預期回答：exploration vs exploitation（目標 2 確認）

---

### 14:20–15:10｜CartPole 任務（50 min）

**教師指示語：**
> "Today we try CartPole. The goal is to keep a pole balanced on a moving cart. The agent controls the cart — it can push left or right. The episode ends when the pole falls over."

> "Unlike the maze, the cart's position and speed are *continuous* values — not just grid squares. But don't worry, the platform handles that automatically. Your job is to watch the learning curve."

**步驟 1：啟動，觀察早期行為（約 5 min）**
> "In the beginning, the pole falls almost immediately — that's normal. Each episode is very short. Watch the 'steps per episode' chart on the right."

**步驟 2：等待一段時間，觀察曲線變化（約 20 min）**

對應目標 3：訓練曲線判讀
> "As training continues, what do you notice about the episode length? Is it getting longer? That means the agent is learning to keep the pole balanced for longer."

> "Look at the reward curve. What does an upward trend tell you? What would a flat or noisy curve mean?"

**學生任務：**
- 啟動 CartPole 訓練，觀察至少 50 episodes
- 回答（口頭或記錄）：
  1. At what point did you notice the agent starting to improve?
  2. Describe the shape of the reward curve in one sentence.
  3. Did the curve ever suddenly drop? What might cause that?

---

### 15:10–15:20｜休息（10 min）

---

### 15:20–16:00｜heli 任務（延伸體驗，40 min）｜不納入評量

**教師指示語：**
> "This one is just for fun — no test questions on this. Heli is a helicopter that needs to fly through gaps. Same idea as before: the agent learns from reward signals. You can try adjusting parameters and see if the agent gets better at flying."

**學生任務：** 自由探索，調整參數，觀察學習行為。教師巡視、回答問題。

---

### 16:00–16:30｜圖表判讀互動討論（30 min）

**教師指示語：**
> "Now let's look at some charts together and talk about what they mean. I'll show you a few examples — tell me what you think is happening."

**討論題目（教師投影，口頭討論）：**

1. 出示一條先平後上升的 reward 曲線：
   > "What's happening in the first 30 episodes? Why does it suddenly start improving?"

2. 出示兩條學習曲線 A（穩定上升）和 B（波動大但最終更高）：
   > "Which one has a higher learning rate α? How can you tell?"

3. 出示 Maze2D Q-table 熱力圖，問：
   > "Which cell does the agent feel most confident about? How do you know?"

**注意：** 此段為課堂討論，不蒐集作答資料。

---

### 16:30–17:00｜後測問卷（30 min）

**教師指示語：**
> "We're almost done. Please open the post-test Google Form on the screen. This covers the same concepts from the pre-test, plus a few questions about your experience with the platform today. Take your time — about 25–30 minutes."

**學生任務：** 完成 Google Form 後測（RR 平台分流版）。
