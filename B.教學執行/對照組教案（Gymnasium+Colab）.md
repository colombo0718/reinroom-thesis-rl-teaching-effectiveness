# 對照組教案（Gymnasium + Colab）

**對象：** 碩士生（國際生）｜**授課語言：** 英文
**日期：** 第1堂 4/22（三）、第2堂 4/29（三）｜**時間：** 14:10–17:00
**工具：** Google Colab（教師預先建立 notebook，學生開連結即可操作）

---

## 第 1 堂（4/22）

### 14:10–14:30｜前測問卷（20 min）

**教師指示語：**
> "Before we start, please open the Google Form link on the screen and complete the questionnaire. This is NOT a graded test — it helps us understand your background. Please answer honestly, even if you have no prior experience with reinforcement learning. It takes about 15–20 minutes."

**學生任務：**
- 打開 Google Form（與實驗組相同問卷）
- 完成背景資料、RL 概念題

**注意事項：** 確保每位學生填寫學號或班級代號，以利配對前後測。

---

### 14:30–14:50｜RL 概念講解 PPT（20 min）

**教師指示語：**（與實驗組完全相同投影片）

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

### 14:50–15:20｜Colab 介面介紹 + ε-greedy Bandit（30 min）

**教師指示語：**
> "Now open your browser and go to this Colab link: [link]. You don't need to install anything — just open it and run the cells one by one."

**介面說明重點（約 5 min）：**
> "In Colab, each block is called a *cell*. Press the play button on the left to run it. The output appears below. We'll go through the cells together."

**ε-greedy Bandit 程式（對應目標 2：探索 vs 利用）：**

> "Our first task is a bandit problem — a row of slot machines with different hidden reward probabilities. The agent uses an ε-greedy strategy: with probability ε it tries a random machine, with probability 1-ε it picks the best one it knows so far."

步驟 1：執行預設程式（ε = 0.1），觀察 matplotlib 輸出的報酬曲線。
> "Run this cell. The x-axis is the number of rounds, the y-axis is the average reward. What does the curve look like? Is it going up, staying flat, or bouncing around?"

步驟 2：將 ε 改為 **0.9**，重新執行，比較兩條曲線。
> "Now change ε to 0.9 and run again. What's different? With more exploration, does the agent learn faster or slower at the beginning?"

> "Here's the key question: if ε = 0, the agent never explores. What problem does that cause?"

**學生任務：**
- 執行 ε = 0.1 和 ε = 0.9 各一次
- 觀察兩條曲線，準備回答：哪種設定的曲線在前 50 回合更穩定？為什麼？

---

### 15:20–15:30｜休息（10 min）

---

### 15:30–16:10｜FrozenLake Q-learning（40 min）｜演示用，不列入測驗

**教師指示語：**
> "Now let's try a more complex task — FrozenLake. It's a 4×4 grid. The agent starts at the top-left and needs to reach the goal at the bottom-right. Some cells are holes — if the agent falls in, the episode ends with zero reward."

> "This time we use Q-learning, which updates a table of Q-values to learn the best action for each state."

**程式說明重點（教師逐段講解）：**
```python
env = gym.make("FrozenLake-v1", is_slippery=False)
```
> "We use is_slippery=False first — the agent moves exactly where it wants to go, no randomness."

```python
Q[state, action] = Q[state, action] + alpha * (reward + gamma * max(Q[next_state]) - Q[state, action])
```
> "This is the Bellman update — the core of Q-learning. We're adjusting our estimate of how good an action is, based on what reward we actually got plus what we expect to get in the future."

**演示：調整參數，觀察差異（教師操作，學生跟著改）**

- 調整 `alpha`（學習率）：0.1 vs 0.9 → 學習速度與穩定性的差異
- 調整 `epsilon`：0.1 vs 0.5 → 探索程度的差異
- 調整 `gamma`：0.5 vs 0.99 → 短期 vs 長期策略

> "These parameters affect learning, but we won't test them directly. Just get a feel for what they do."

**學生任務：** 跟著教師修改三個參數各一次，執行並觀察曲線變化。

---

### 16:10–17:00｜FrozenLake Q-table 視覺化（50 min）

**教師指示語：**
> "Q-learning builds a table — Q-table. Each row is a state (a cell in the grid), each column is an action (up/down/left/right). The value tells us how good that action is from that state. Let's visualize it."

**程式說明：**
```python
import seaborn as sns
import matplotlib.pyplot as plt

# 取每個 state 的最優動作
best_actions = np.argmax(Q, axis=1).reshape(4, 4)
sns.heatmap(best_actions, annot=True, cmap="coolwarm")
plt.title("Best Action per State (0=Left, 1=Down, 2=Right, 3=Up)")
plt.show()
```

> "This heatmap shows, for each grid cell, what action the agent currently prefers. The number corresponds to a direction."

對應目標 4：Q-table 基本讀法
> "Look at the cells near the goal. What direction do they mostly point? Does that make sense?"

> "Now look at cells far from the goal. Are they consistent, or all over the place? What does that tell you about how well the agent has learned those states?"

**學生任務：**
- 執行 Q-table 視覺化程式
- 回答（口頭討論）：
  1. Which cell has the clearest preferred action? Why?
  2. Are there cells where the Q-table seems uncertain? Which ones?
  3. Can you trace a path from start to goal using the heatmap?

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

### 14:20–15:10｜CartPole + 狀態離散化（50 min）

**教師指示語：**
> "Today we try CartPole. The goal is to keep a pole balanced on a cart. The state has 4 continuous values: cart position, cart velocity, pole angle, and pole angular velocity."

> "Q-learning needs a *discrete* table. But our state is continuous — so we need to manually convert it into discrete buckets first. This is called *discretization*."

**程式說明：狀態分桶（教師逐步講解）**
```python
# 定義每個維度的分桶邊界
bins = [
    np.linspace(-2.4, 2.4, 10),   # cart position
    np.linspace(-3.0, 3.0, 10),   # cart velocity
    np.linspace(-0.3, 0.3, 10),   # pole angle
    np.linspace(-3.0, 3.0, 10),   # pole angular velocity
]

def discretize(obs):
    return tuple(np.digitize(obs[i], bins[i]) for i in range(4))
```

> "Each continuous value is mapped to one of 10 bins. So instead of infinite possible states, we now have 10×10×10×10 = 10,000 possible discrete states. The Q-table has 10,000 rows."

> "This is something the Rein Room platform does automatically behind the scenes. Here we're doing it explicitly so you can see exactly what's happening."

**步驟 1：執行程式，觀察早期行為（約 10 min）**
> "In the first few episodes, the pole falls immediately — that's normal. Watch the episode length chart."

**步驟 2：等待訓練，觀察曲線（約 20 min）**

對應目標 3：訓練曲線判讀
> "As training continues, what happens to the episode length? A longer episode means the agent kept the pole balanced for longer."

> "Look at the reward curve. When does it start trending upward? Is the improvement gradual or sudden?"

> "Does the curve ever drop suddenly after improving? What might cause that?"

**學生任務：**
- 執行 CartPole Q-learning，觀察至少 100 episodes
- 回答（口頭或記錄）：
  1. Describe the reward curve shape in one sentence.
  2. At roughly what episode did you notice improvement?
  3. What does a sudden drop in reward tell you about the agent's learning?

---

### 15:10–15:20｜休息（10 min）

---

### 15:20–16:00｜FrozenLake 隨機版對比（40 min）｜演示用

**教師指示語：**
> "Let's go back to FrozenLake, but this time with is_slippery=True. This means the agent doesn't always move where it intends — sometimes it slides sideways."

```python
env = gym.make("FrozenLake-v1", is_slippery=True)
```

> "Watch how the reward curve compares to the deterministic version. With randomness in the environment, what happens to the agent's learning speed and the shape of the curve?"

**演示重點（教師操作）：**
- 比較兩條曲線：確定版 vs 隨機版
- 隨機版曲線通常更震盪、收斂更慢

> "This shows that learning is harder when the environment itself is unpredictable — not just the agent's behavior."

**學生任務：** 觀察並比較兩條曲線差異，口頭說明哪條更容易收斂及原因。此段不列入測驗。

---

### 16:00–16:30｜圖表判讀互動討論（30 min）

**教師指示語：**（與實驗組使用相同題目）
> "Let's look at some charts together. I'll show them on the screen — tell me what you think is happening."

**討論題目（教師投影，口頭討論）：**

1. 出示一條先平後上升的 reward 曲線：
   > "What's happening in the first 30 episodes? Why does it suddenly start improving?"

2. 出示兩條學習曲線 A（穩定上升）和 B（波動大但最終更高）：
   > "Which one has a higher learning rate α? How can you tell?"

3. 出示 FrozenLake Q-table 熱力圖，問：
   > "Which cell does the agent feel most confident about? How do you know?"

**注意：** 此段為課堂討論，不蒐集作答資料。

---

### 16:30–17:00｜後測問卷（30 min）

**教師指示語：**
> "Last step — please open the post-test Google Form. Same format as the pre-test, plus some questions about your experience with Colab and Gymnasium today. Take your time."

**學生任務：** 完成 Google Form 後測（Colab 分流版）。
