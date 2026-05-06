# 對照組教案（Gymnasium + Colab）

**對象：** 碩士生（國際生）｜**授課語言：** 英文
**日期：** 第1堂 4/22（三）、第2堂 4/29（三）｜**時間：** 14:10–17:00
**工具：** Google Colab（教師預先建立 notebook，學生開連結即可操作）
**教材：** `RL_Day1_RR.ipynb`（MAB → Maze1D → Maze2D）、`RL_Day2_RR.ipynb`（Heli → Fighter）
**環境：** `rr_envs.py`（自製 Gymnasium 環境，reward 完全對齊 RR 原始碼）

---

## 第 1 堂（4/22）

### 14:10–14:30｜前測問卷（20 min）

**教師指示語：**
> "Before we start, please open the Google Form link on the screen and complete the questionnaire. This is NOT a graded test — it helps us understand your background. Please answer honestly, even if you have no prior experience with reinforcement learning. It takes about 15–20 minutes."

**學生任務：**
- 打開 Google Form（與實驗組相同問卷）
- 完成背景資料、RL 概念題

**注意事項：** 確保每位學生填寫 Student ID，以利配對前後測。

---

### 14:30–14:50｜RL 概念講解 PPT（20 min）

**教師指示語：**（**與實驗組完全相同投影片**）

> "Now let's talk about what reinforcement learning actually is. You might have heard of AlphaGo, or games where AI learns to play by itself — that's reinforcement learning."

**講解重點（對應目標 1：SAR 循環）：**

1. **情境類比：** 訓練寵物的過程
   > "Imagine you're training a dog. The dog is the *agent*. The room is the *environment*. What the dog sees right now — that's the *state*. What the dog does — that's the *action*. When the dog does something right and gets a treat — that's the *reward*."

2. **SAR 循環圖示：**
   > "Every step follows this loop: observe state → choose action → receive reward → move to next state. This repeats until the episode ends."

3. **Episode 概念：**
   > "An *episode* is one complete run — from start to finish. The agent resets and starts fresh each episode, but carries the knowledge it has learned."

**學生任務：** 聆聽，可舉手提問。PPT 留一張空白讓學生口頭說出 State / Action / Reward 各是什麼。

---

### 14:50–15:20｜Colab 介面介紹 + MAB 程式（30 min）

**教師指示語：**
> "Now open your browser and go to this Colab link: [RL_Day1_RR.ipynb link]. You don't need to install anything — just open it and run the cells one by one."

**介面說明重點（約 5 min）：**
> "In Colab, each block is called a *cell*. Press the play button on the left to run it. The output appears below. We'll go through the cells together. You only need to change the values marked with 🔧."

**MAB 程式（對應目標 2：探索 vs 利用）：**

> "Our first task is a bandit problem — a row of slot machines with different hidden reward probabilities. The agent uses an ε-greedy strategy: with probability ε it tries a random machine, with probability 1-ε it picks the best one it knows so far."

步驟 1：執行預設程式（ε = 0.1），觀察 matplotlib 輸出的報酬曲線。
> "Run this cell. The x-axis is the number of rounds, the y-axis is the average reward. What does the curve look like?"

步驟 2：將 🔧 ε 改為 **0.9**，重新執行，比較兩條曲線。
> "Now change ε to 0.9 and run again. With more exploration, does the agent learn faster or slower at the beginning?"

> "Key question: if ε = 0, the agent never explores. What problem does that cause?"

**學生任務（對應 T1 評量）：**
- 執行 ε = 0.1 和 ε = 0.9 各一次
- 準備回答：哪種設定的曲線在前 50 回合更穩定？為什麼？

> ✅ **T1 完成標準：** 跑完兩次，能口頭說出 ε=0.9 vs ε=0.1 曲線差異

---

### 15:20–15:30｜休息（10 min）

---

### 15:30–15:45｜V2 影片：How Agents Learn — Q-table & Update Rule（15 min）

**教師指示語：**
> "Before we try Maze1D, watch this short video — it explains how the agent stores and updates what it learns."

---

### 15:45–16:30｜Maze1D 程式：γ 的效果 + SAR 確認（45 min）｜對應目標 1：RQ1（T2）

**教師指示語：**
> "Now let's look at a 1D maze. The agent is on a line and needs to reach the goal. We'll first see how gamma affects behavior, then confirm your understanding of state, action, reward, and episode."

**Part A：調整 γ，觀察行為差異（約 15 min）**

- γ = 0.5：agent 只看近期報酬，可能「短視」停在中途
- γ = 0.99：agent 更願意繞路，追求最終 goal 的高報酬

> "Gamma controls how much the agent cares about future rewards. We won't test gamma directly — this is just to build your intuition."

**學生任務：** 跟著教師修改 🔧 gamma 各一次，執行並觀察行為變化。

**Part B：SAR 循環確認（約 20 min）｜T2 評量**

學生執行 Maze1D 後，助教逐一詢問：
> "In this Maze1D code — **what is the state? What are the actions? When does the agent receive a reward? Where does one episode start and end?**"

預期回答：
- **State**：agent 在 1D line 上的位置（整數 index）
- **Actions**：向左移 / 向右移
- **Reward**：到達 goal 得正獎勵；超時得負獎勵
- **Episode**：從起點出發，到達 goal 或超時 reset 為一個 episode

> ✅ **T2 完成標準：** 能正確說出 Maze1D 程式中 state / action / reward / episode 各代表什麼

---

### 16:30–17:00｜Maze2D 初探（30 min）｜不評量

**教師指示語：**
> "Now open the Maze2D section. Just run the training cell and watch the agent. We'll do a deeper analysis next class after watching a video about Q-table heatmaps."

**學生任務：**
- 執行 Maze2D 訓練 cell，觀察 agent 探索過程
- 可自由調整 🔧 參數，觀察行為變化
- **不需要完成任何評量任務**，純粹熟悉環境

> ℹ️ T3（Q-table 熱力圖路徑指認）在第 2 堂 V3 影片後進行。

---

## 第 2 堂（4/29）

### 14:10–14:20｜複習（10 min）

**教師指示語：**
> "Quick recap. Last week we covered the RL loop and Q-learning. Let me ask a few questions."

> "What does the Q-table store? What does a high Q-value for a state-action pair mean?"

預期回答：stores expected future reward, high = this action is good from this state（目標 1、4 確認）

> "What does ε control?"

預期回答：how often the agent explores randomly（目標 2 確認）

---

### 14:20–14:35｜V3 影片：Reading the Q-table Heatmap（15 min）

**教師指示語：**
> "Before we dive into Maze2D analysis, watch this video — it explains how to read the Q-table heatmap and trace a path."

---

### 14:35–15:05｜Maze2D 深探（30 min）｜對應目標 4：RQ2（T3）

**教師指示語：**
> "Now go back to the Maze2D section. This time run the heatmap visualization cell."

**程式說明重點：**
> "Q-learning builds a Q-table. Each row is a state, each column is an action. The heatmap shows, for each maze cell, what action the agent currently prefers — arrow direction and color intensity show confidence."

步驟 1：執行訓練 cell（使用預設 🔧 參數）。

步驟 2：執行 Q-table 熱力圖 cell，觀察輸出。

**學生任務（T3 評量）：**
- 執行 Q-table 熱力圖 cell
- 口頭回答：Can you trace a path from Start to Goal using the heatmap?

> ✅ **T3 完成標準：** 在熱力圖上指出 Start→Goal 路徑

---

### 15:05–15:20｜V4 影片：Reading Training Curves + B4 Heli Demo（15 min）

**教師指示語：**
> "Good work. Now watch these two short videos — one on how to read training curves, one showing what we'll do with Heli."

---

### 15:20–15:30｜休息（10 min）

---

### 15:30–16:00｜Heli 程式：觀察訓練曲線收斂（30 min）｜對應目標 3：RQ2（T4）

**教師指示語：**
> "Today we try Heli. The agent is a helicopter that must fly through gaps. Each episode the helicopter starts fresh. We'll watch the reward curve to see when the agent starts improving."

> "This is the same Heli environment as in Rein Room — we built a Python version with the exact same reward function, so the learning behavior should be very similar."

**步驟 1：執行程式，觀察早期行為（約 10 min）**
> "In the first few episodes, the helicopter crashes quickly — that's normal. Watch the reward per episode."

**步驟 2：等待訓練，觀察曲線（約 20 min）**

對應目標 3：訓練曲線判讀
> "As training continues, what happens to the reward? A higher reward means the helicopter survived longer and flew through more gaps."

> "Look at the reward curve. When does it start trending upward? Is the improvement gradual or sudden?"

> "Does the curve ever drop suddenly after improving? What might cause that?"

**步驟 3：調整 🔧 ε 對比（約 15 min，選做）**

| 🔧 Change | Value |
|---|---|
| ε (epsilon) | **0.05** (almost no exploration) |

→ 重新執行，比較曲線差異。

**學生任務（T4 評量）：**
- 執行 Heli Q-learning，觀察至少 50 episodes
- 回答（口頭）：
  1. Describe the reward curve shape in one sentence.
  2. At roughly what episode did you notice improvement?
  3. What does a sudden drop in reward tell you?

> ✅ **T4 完成標準：** 觀察至少 50 episodes，能描述 reward 曲線趨勢

---

### 16:00–16:10｜V5 影片：Continuous State & Discretization（10 min）

**教師指示語：**
> "Before Fighter, watch this short video on continuous states — it explains why Heli and Fighter need a different approach than Maze1D/2D."

---

### 16:10–16:40｜Fighter 程式：延伸自由體驗（30 min）｜選做，不列入評量（T5）

> ⚠️ 此段為延伸體驗，**不列入後測評量**，學生可自由探索。

**教師指示語：**
> "Now open the Fighter section of Day 2 notebook. Try different parameter combinations and observe how the agent learns. There's no specific task — just explore."

**學生任務：** 自由調整 🔧 參數，觀察 agent 行為。

> ✅ **T5 記錄：** 有嘗試 Fighter 即記錄為完成（不計入完成率分析）

---

### 16:40–17:00｜後測問卷（20 min）

**教師指示語：**
> "Last step — please open the post-test Google Form. Same RL concept questions as the pre-test, plus platform questions, a cognitive load survey, and a usability survey."

**學生任務：** 完成 Google Form 後測（含 Section 1–2 概念題、Section 3B 平台回饋、Section 4 NASA-TLX、Section 5B SUS）。

---

## 補充說明

**唯一變量說明：**
- 對照組使用 `rr_envs.py` 中的 Python 環境，reward function 與 RR 平台原始碼完全對齊
- 唯一差異是操作介面：對照組修改程式碼中的 🔧 數值並重新執行 cell，實驗組使用 RR 平台圖形滑桿
- 遊戲邏輯、獎勵設計、RL 演算法（Q-learning）、教學目標、圖表討論題、前後測全部相同
