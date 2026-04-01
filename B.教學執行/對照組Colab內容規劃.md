# 對照組 Colab Notebook 內容規劃

**設計原則：** 所有程式碼預先寫好，學生只需修改標記 `🔧` 的參數數值並執行。
不要求學生理解每一行程式碼，重點是觀察參數改變後的視覺化結果。

分為兩份 Notebook：
- `RL_Day1.ipynb`：Bandit + FrozenLake（第1堂用）
- `RL_Day2.ipynb`：CartPole + FrozenLake 隨機版（第2堂用）

---

## RL_Day1.ipynb

---

### Cell 1 — 安裝與匯入（Setup）

```python
# Run this cell first — it installs the required packages
!pip install gymnasium matplotlib seaborn numpy --quiet

import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("✅ Setup complete!")
```

---

### Cell 2 — Markdown 說明：今天的目標

```markdown
## Today's Goal

We'll explore two reinforcement learning environments:
1. **Multi-Armed Bandit** — to understand *exploration vs. exploitation*
2. **FrozenLake** — to understand *Q-learning* and *Q-table visualization*

You don't need to understand every line of code.
Focus on **what changes when you adjust the 🔧 parameters**.
```

---

### Cell 3 — Markdown 說明：Part 1 Bandit

```markdown
## Part 1: Multi-Armed Bandit

Imagine a row of slot machines. Each machine has a *hidden* probability of giving you a reward.
Your agent uses **ε-greedy strategy**:
- With probability **ε** → try a random machine (explore)
- With probability **1 - ε** → pick the machine that looked best so far (exploit)

### 🔧 Your task:
Run the cell below with **ε = 0.1**, then change it to **ε = 0.9** and run again.
What's different about the two reward curves?
```

---

### Cell 4 — Bandit 程式（學生只改 epsilon）

```python
# ============================================================
# 🔧 CHANGE THIS VALUE and re-run to see the difference
epsilon = 0.1   # try: 0.1 / 0.5 / 0.9
# ============================================================

np.random.seed(42)
n_bandits = 5
n_rounds = 500
true_probs = [0.2, 0.5, 0.8, 0.4, 0.6]  # hidden from the agent

def pull(bandit_id):
    return 1 if np.random.random() < true_probs[bandit_id] else 0

Q = np.zeros(n_bandits)
N = np.zeros(n_bandits)
rewards = []

for t in range(n_rounds):
    if np.random.random() < epsilon:
        action = np.random.randint(n_bandits)  # explore
    else:
        action = np.argmax(Q)                   # exploit

    reward = pull(action)
    N[action] += 1
    Q[action] += (reward - Q[action]) / N[action]
    rewards.append(reward)

# --- Plot ---
window = 30
smoothed = np.convolve(rewards, np.ones(window)/window, mode='valid')

plt.figure(figsize=(10, 4))
plt.plot(smoothed, label=f'ε = {epsilon}', linewidth=2)
plt.axhline(y=max(true_probs), color='gray', linestyle='--', label='Best possible reward')
plt.xlabel('Round')
plt.ylabel('Average Reward (smoothed)')
plt.title(f'ε-greedy Bandit  |  ε = {epsilon}')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print(f"Agent's best guess: Machine #{np.argmax(Q)} (estimated: {max(Q):.2f})")
print(f"Actual best machine: Machine #{np.argmax(true_probs)} (true reward: {max(true_probs):.2f})")
```

---

### Cell 5 — Markdown 說明：Part 2 FrozenLake

```markdown
## Part 2: FrozenLake — Q-Learning

FrozenLake is a 4×4 grid. The agent starts at **S** (top-left) and must reach **G** (bottom-right).
**H** cells are holes — fall in and the episode ends with no reward.

```
S  F  F  F
F  H  F  H
F  F  F  H
H  F  F  G
```

The agent learns using **Q-learning**: it builds a table (Q-table) that stores
how good each action is from each cell.

### 🔧 Your task:
Run the cell with the default settings first.
Then try changing **alpha**, **gamma**, or **epsilon** one at a time.
```

---

### Cell 6 — FrozenLake Q-learning（學生只改三個參數）

```python
# ============================================================
# 🔧 CHANGE THESE VALUES and re-run
alpha   = 0.8    # learning rate   — try: 0.1 / 0.5 / 0.8
gamma   = 0.95   # discount factor — try: 0.5 / 0.95 / 0.99
epsilon = 0.1    # exploration     — try: 0.05 / 0.1 / 0.5
n_episodes = 2000
# ============================================================

env = gym.make("FrozenLake-v1", is_slippery=False)
Q = np.zeros([env.observation_space.n, env.action_space.n])
episode_rewards = []
episode_lengths = []

for ep in range(n_episodes):
    state, _ = env.reset()
    total_reward, steps, done = 0, 0, False
    while not done:
        if np.random.random() < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q[state])
        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        Q[state, action] += alpha * (reward + gamma * np.max(Q[next_state]) - Q[state, action])
        state = next_state
        total_reward += reward
        steps += 1
    episode_rewards.append(total_reward)
    episode_lengths.append(steps)

# --- Plot ---
window = 100
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4))

smoothed_r = np.convolve(episode_rewards, np.ones(window)/window, mode='valid')
ax1.plot(smoothed_r, color='steelblue', linewidth=2)
ax1.set_title(f'Episode Reward  |  α={alpha}  γ={gamma}  ε={epsilon}')
ax1.set_xlabel('Episode')
ax1.set_ylabel('Reward (1 = reached goal)')
ax1.grid(True, alpha=0.3)

smoothed_l = np.convolve(episode_lengths, np.ones(window)/window, mode='valid')
ax2.plot(smoothed_l, color='coral', linewidth=2)
ax2.set_title('Episode Length (steps to finish)')
ax2.set_xlabel('Episode')
ax2.set_ylabel('Steps')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
print(f"Success rate (last 500 episodes): {np.mean(episode_rewards[-500:]):.1%}")
```

---

### Cell 7 — Markdown 說明：Q-table 視覺化

```markdown
## Q-Table Visualization

The Q-table stores a value for every (state, action) pair.
- **High value** → the agent thinks this action is good from this state
- **Arrow** → the action the agent currently prefers in each cell

Run the cell below to see what the agent has learned.

### 🔧 Your task:
Look at the heatmap. Can you trace a path from **S** to **G** just by following the arrows?
Change `state_to_inspect` to explore different cells.
```

---

### Cell 8 — Q-table 熱力圖（學生只改 state_to_inspect）

```python
# ============================================================
# 🔧 CHANGE THIS to inspect any cell (0 = top-left, 15 = bottom-right)
state_to_inspect = 14
# ============================================================

action_symbols = ['←', '↓', '→', '↑']
best_actions    = np.argmax(Q, axis=1).reshape(4, 4)
max_Q_vals      = np.max(Q, axis=1).reshape(4, 4)
best_arrows     = np.vectorize(lambda x: action_symbols[x])(best_actions)

# Mark holes and special cells
cell_labels = {0:'S', 5:'H', 7:'H', 11:'H', 12:'H', 15:'G'}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# --- Heatmap ---
mask = (max_Q_vals == 0)
sns.heatmap(max_Q_vals, annot=best_arrows, fmt='', cmap='YlOrRd',
            linewidths=1, ax=ax1, mask=mask,
            cbar_kws={'label': 'Max Q-value (confidence)'})
for pos, label in cell_labels.items():
    r, c = divmod(pos, 4)
    color = 'navy' if label in ('S','G') else 'red'
    ax1.text(c+0.5, r+0.5, label, ha='center', va='center',
             fontsize=14, fontweight='bold', color=color)
ax1.set_title('Best Action per State\n(arrow = preferred direction, color = confidence)')
ax1.set_xlabel('Column')
ax1.set_ylabel('Row')

# --- Bar chart for selected state ---
q_vals = Q[state_to_inspect]
colors = ['#e74c3c','#2ecc71','#3498db','#f39c12']
bars = ax2.bar(action_symbols, q_vals, color=colors)
ax2.set_title(f'Q-values for State {state_to_inspect}  '
              f'(row {state_to_inspect//4}, col {state_to_inspect%4})')
ax2.set_xlabel('Action')
ax2.set_ylabel('Q-value')
ax2.grid(True, alpha=0.3, axis='y')
for bar, val in zip(bars, q_vals):
    ax2.text(bar.get_x() + bar.get_width()/2, val + 0.005,
             f'{val:.3f}', ha='center', va='bottom', fontsize=11)

plt.tight_layout()
plt.show()
print(f"State {state_to_inspect}: preferred action = {action_symbols[np.argmax(q_vals)]}")
```

---

## RL_Day2.ipynb

---

### Cell 1 — 安裝與匯入

```python
!pip install gymnasium matplotlib numpy --quiet

import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt

print("✅ Setup complete!")
```

---

### Cell 2 — Markdown 說明：CartPole

```markdown
## CartPole — Continuous State Space

CartPole is different from FrozenLake:
- The state has **4 continuous values** (cart position, velocity, pole angle, angular velocity)
- Q-learning needs discrete states → we divide each dimension into **bins**

The platform **Rein Room** does this automatically.
Here, we do it explicitly so you can see what's happening under the hood.

### 🔧 Your task:
Run the cell and watch the reward curve.
- Does it go up over time? That means the agent is learning.
- When does it start improving?
- Does it ever suddenly drop? Why might that happen?
```

---

### Cell 3 — CartPole（學生只改三個參數）

```python
# ============================================================
# 🔧 CHANGE THESE VALUES and re-run
alpha     = 0.5    # learning rate   — try: 0.2 / 0.5 / 0.8
gamma     = 0.99   # discount factor — try: 0.9 / 0.99
epsilon   = 0.3    # exploration     — try: 0.1 / 0.3 / 0.5
n_episodes = 500
# ============================================================

env  = gym.make("CartPole-v1")
n_bins = 10

bins = [
    np.linspace(-2.4,  2.4,  n_bins),
    np.linspace(-3.0,  3.0,  n_bins),
    np.linspace(-0.25, 0.25, n_bins),
    np.linspace(-3.0,  3.0,  n_bins),
]

def discretize(obs):
    return tuple(min(np.digitize(obs[i], bins[i]), n_bins - 1) for i in range(4))

Q = {}
get_q  = lambda s, a: Q.get((s, a), 0.0)
best_a = lambda s: max(range(2), key=lambda a: get_q(s, a))

episode_rewards, episode_lengths = [], []

for ep in range(n_episodes):
    obs, _ = env.reset()
    state  = discretize(obs)
    total_reward, steps, done = 0, 0, False
    while not done:
        action = env.action_space.sample() if np.random.random() < epsilon else best_a(state)
        next_obs, reward, terminated, truncated, _ = env.step(action)
        done        = terminated or truncated
        next_state  = discretize(next_obs)
        old_q       = get_q(state, action)
        next_max_q  = max(get_q(next_state, a) for a in range(2))
        Q[(state, action)] = old_q + alpha * (reward + gamma * next_max_q - old_q)
        state = next_state
        total_reward += reward
        steps += 1
    episode_rewards.append(total_reward)
    episode_lengths.append(steps)

# --- Plot ---
window = 30
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4))

smoothed_r = np.convolve(episode_rewards, np.ones(window)/window, mode='valid')
ax1.plot(smoothed_r, linewidth=2)
ax1.axhline(195, color='red', linestyle='--', label='Solved threshold (195)')
ax1.set_title(f'CartPole Reward  |  α={alpha}  γ={gamma}  ε={epsilon}')
ax1.set_xlabel('Episode')
ax1.set_ylabel('Total Reward (max=200)')
ax1.legend()
ax1.grid(True, alpha=0.3)

smoothed_l = np.convolve(episode_lengths, np.ones(window)/window, mode='valid')
ax2.plot(smoothed_l, color='orange', linewidth=2)
ax2.set_title('Episode Length (longer = better balance)')
ax2.set_xlabel('Episode')
ax2.set_ylabel('Steps')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
print(f"Q-table entries used: {len(Q)} / {10**4 * 2} possible")
print(f"Average reward (last 50 episodes): {np.mean(episode_rewards[-50:]):.1f} / 200")
```

---

### Cell 4 — Markdown 說明：FrozenLake 隨機版對比

```markdown
## FrozenLake — Slippery vs. Non-Slippery

Previously we used `is_slippery=False` — the agent moves exactly where it intends.
Now we switch to `is_slippery=True` — the agent sometimes slides sideways.

### 🔧 Your task:
Run the cell. Compare the two reward curves.
- Which one converges faster?
- Which one is more stable (less bouncing)?
- What does this tell you about learning in unpredictable environments?
```

---

### Cell 5 — FrozenLake 確定版 vs 隨機版對比

```python
# Fixed parameters — focus on comparing the two environments
alpha, gamma, epsilon, n_episodes = 0.8, 0.95, 0.1, 2000
window = 100

def run_frozenlake(slippery):
    env = gym.make("FrozenLake-v1", is_slippery=slippery)
    Q   = np.zeros([env.observation_space.n, env.action_space.n])
    rewards = []
    for _ in range(n_episodes):
        state, _ = env.reset()
        total, done = 0, False
        while not done:
            action = env.action_space.sample() if np.random.random() < epsilon else np.argmax(Q[state])
            ns, r, ter, tru, _ = env.step(action)
            done = ter or tru
            Q[state, action] += alpha * (r + gamma * np.max(Q[ns]) - Q[state, action])
            state = ns
            total += r
        rewards.append(total)
    return rewards

print("Training... (takes ~10 seconds)")
rewards_det   = run_frozenlake(slippery=False)
rewards_slip  = run_frozenlake(slippery=True)

# --- Plot ---
plt.figure(figsize=(12, 4))
for rewards, label, color in [
    (rewards_det,  'Non-slippery (deterministic)', 'steelblue'),
    (rewards_slip, 'Slippery (stochastic)',         'coral'),
]:
    smoothed = np.convolve(rewards, np.ones(window)/window, mode='valid')
    plt.plot(smoothed, label=label, color=color, linewidth=2)

plt.title('FrozenLake: Deterministic vs. Stochastic Environment')
plt.xlabel('Episode')
plt.ylabel('Success Rate (smoothed)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print(f"Non-slippery — success rate (last 500): {np.mean(rewards_det[-500:]):.1%}")
print(f"Slippery     — success rate (last 500): {np.mean(rewards_slip[-500:]):.1%}")
```
