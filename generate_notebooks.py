import json, os

os.makedirs("notebooks", exist_ok=True)

def code(lines):
    src = [l + "\n" for l in lines[:-1]] + [lines[-1]]
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": src}

def md(lines):
    src = [l + "\n" for l in lines[:-1]] + [lines[-1]]
    return {"cell_type": "markdown", "metadata": {}, "source": src}

def nb(cells):
    return {
        "nbformat": 4, "nbformat_minor": 0,
        "metadata": {
            "colab": {"provenance": []},
            "kernelspec": {"display_name": "Python 3", "name": "python3"},
            "language_info": {"name": "python"}
        },
        "cells": cells
    }

# ──────────────────────────────────────────────────────────
# DAY 1
# ──────────────────────────────────────────────────────────
day1_cells = [

md([
    "# RL Teaching — Day 1",
    "**Bandit · FrozenLake Q-Learning · Q-Table Visualization**",
    "",
    "> 📌 **Before you start:** Go to **File → Save a copy in Drive** to make your own editable copy.",
    "",
    "You don't need to understand every line of code.",
    "Focus on **what changes when you adjust the 🔧 parameters** and re-run the cell."
]),

code([
    "# ── Setup (run this first) ──────────────────────────────────",
    "!pip install gymnasium matplotlib seaborn numpy --quiet",
    "import gymnasium as gym",
    "import numpy as np",
    "import matplotlib.pyplot as plt",
    "import seaborn as sns",
    "print('✅ Setup complete!')"
]),

md([
    "---",
    "## Part 1 · Multi-Armed Bandit",
    "",
    "Imagine a row of slot machines. Each machine has a *hidden* probability of giving a reward.",
    "The agent uses **ε-greedy strategy**:",
    "- With probability **ε** → try a random machine *(explore)*",
    "- With probability **1 - ε** → pick the best-known machine *(exploit)*",
    "",
    "### 🔧 Your task",
    "Run the cell with **ε = 0.1**, then change it to **ε = 0.9** and run again.",
    "What is different about the two reward curves?"
]),

code([
    "# ════════════════════════════════════════════",
    "epsilon = 0.1   # 🔧 Try: 0.1 / 0.5 / 0.9",
    "# ════════════════════════════════════════════",
    "",
    "np.random.seed(42)",
    "n_bandits, n_rounds = 5, 500",
    "true_probs = [0.2, 0.5, 0.8, 0.4, 0.6]   # hidden from the agent",
    "",
    "Q = np.zeros(n_bandits)",
    "N = np.zeros(n_bandits)",
    "rewards = []",
    "",
    "for t in range(n_rounds):",
    "    action = np.random.randint(n_bandits) if np.random.random() < epsilon else np.argmax(Q)",
    "    reward = 1 if np.random.random() < true_probs[action] else 0",
    "    N[action] += 1",
    "    Q[action] += (reward - Q[action]) / N[action]",
    "    rewards.append(reward)",
    "",
    "smoothed = np.convolve(rewards, np.ones(30)/30, mode='valid')",
    "plt.figure(figsize=(10, 4))",
    "plt.plot(smoothed, linewidth=2, label=f'epsilon = {epsilon}')",
    "plt.axhline(max(true_probs), color='gray', linestyle='--', label='Best possible reward')",
    "plt.xlabel('Round'); plt.ylabel('Avg Reward (smoothed)')",
    "plt.title(f'epsilon-greedy Bandit  |  epsilon = {epsilon}')",
    "plt.legend(); plt.grid(alpha=0.3); plt.show()",
    "",
    "print(f\"Agent best guess : Machine #{np.argmax(Q)} (Q = {max(Q):.2f})\")",
    "print(f\"Actual best      : Machine #{np.argmax(true_probs)} (p = {max(true_probs):.2f})\")"
]),

md([
    "---",
    "## Part 2 · FrozenLake — Q-Learning",
    "",
    "FrozenLake is a 4x4 grid. The agent starts at **S** and must reach **G** without falling into holes **H**.",
    "```",
    "S  F  F  F",
    "F  H  F  H",
    "F  F  F  H",
    "H  F  F  G",
    "```",
    "The agent learns using **Q-learning**: it builds a Q-table storing",
    "how good each action is from each state.",
    "",
    "### 🔧 Your task",
    "Run with default settings first, then change **one parameter at a time** and observe the effect."
]),

code([
    "# ════════════════════════════════════════════",
    "alpha      = 0.8    # 🔧 learning rate    — try: 0.1 / 0.5 / 0.8",
    "gamma      = 0.95   # 🔧 discount factor  — try: 0.5 / 0.95 / 0.99",
    "epsilon    = 0.1    # 🔧 exploration rate — try: 0.05 / 0.1 / 0.5",
    "n_episodes = 2000",
    "# ════════════════════════════════════════════",
    "",
    "env = gym.make('FrozenLake-v1', is_slippery=False)",
    "Q   = np.zeros([env.observation_space.n, env.action_space.n])",
    "episode_rewards, episode_lengths = [], []",
    "",
    "for _ in range(n_episodes):",
    "    state, _ = env.reset()",
    "    total, steps, done = 0, 0, False",
    "    while not done:",
    "        action = env.action_space.sample() if np.random.random() < epsilon else np.argmax(Q[state])",
    "        ns, r, ter, tru, _ = env.step(action)",
    "        done = ter or tru",
    "        Q[state, action] += alpha * (r + gamma * np.max(Q[ns]) - Q[state, action])",
    "        state, total, steps = ns, total + r, steps + 1",
    "    episode_rewards.append(total)",
    "    episode_lengths.append(steps)",
    "",
    "window = 100",
    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4))",
    "ax1.plot(np.convolve(episode_rewards, np.ones(window)/window, mode='valid'), color='steelblue', lw=2)",
    "ax1.set(title=f'Reward | alpha={alpha} gamma={gamma} epsilon={epsilon}',",
    "        xlabel='Episode', ylabel='Reward (1 = reached goal)')",
    "ax1.grid(alpha=0.3)",
    "ax2.plot(np.convolve(episode_lengths, np.ones(window)/window, mode='valid'), color='coral', lw=2)",
    "ax2.set(title='Episode Length', xlabel='Episode', ylabel='Steps')",
    "ax2.grid(alpha=0.3)",
    "plt.tight_layout(); plt.show()",
    "print(f'Success rate (last 500): {np.mean(episode_rewards[-500:]):.1%}')"
]),

md([
    "---",
    "## Part 3 · Q-Table Visualization",
    "",
    "The Q-table assigns a value to every (state, action) pair.",
    "- **High value** → agent thinks this action is good from this state",
    "- **Arrow** → preferred action in each cell",
    "",
    "### 🔧 Your task",
    "1. Can you trace a path from **S** to **G** following the arrows?",
    "2. Change `state_to_inspect` to explore Q-values in different cells."
]),

code([
    "# ════════════════════════════════════════════",
    "state_to_inspect = 14   # 🔧 any cell 0-15 (0=top-left, 15=bottom-right)",
    "# ════════════════════════════════════════════",
    "",
    "symbols     = ['L', 'D', 'R', 'U']   # Left Down Right Up",
    "best_arrows = np.vectorize(lambda x: symbols[x])(np.argmax(Q, axis=1).reshape(4,4))",
    "max_Q_grid  = np.max(Q, axis=1).reshape(4,4)",
    "special     = {0:'S', 5:'H', 7:'H', 11:'H', 12:'H', 15:'G'}",
    "",
    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))",
    "",
    "sns.heatmap(max_Q_grid, annot=best_arrows, fmt='', cmap='YlOrRd',",
    "            linewidths=1, ax=ax1, mask=(max_Q_grid == 0),",
    "            cbar_kws={'label': 'Max Q-value (confidence)'})",
    "for pos, label in special.items():",
    "    r, c = divmod(pos, 4)",
    "    ax1.text(c+0.5, r+0.5, label, ha='center', va='center',",
    "             fontsize=14, fontweight='bold',",
    "             color='navy' if label in ('S','G') else 'red')",
    "ax1.set(title='Best Action per State (L/D/R/U = direction, color = confidence)',",
    "        xlabel='Column', ylabel='Row')",
    "",
    "q_vals = Q[state_to_inspect]",
    "bars = ax2.bar(symbols, q_vals, color=['#e74c3c','#2ecc71','#3498db','#f39c12'])",
    "ax2.set(title=f'Q-values for State {state_to_inspect} (row {state_to_inspect//4}, col {state_to_inspect%4})',",
    "        xlabel='Action', ylabel='Q-value')",
    "ax2.grid(alpha=0.3, axis='y')",
    "for bar, val in zip(bars, q_vals):",
    "    ax2.text(bar.get_x()+bar.get_width()/2, val+0.005, f'{val:.3f}',",
    "             ha='center', va='bottom', fontsize=11)",
    "plt.tight_layout(); plt.show()",
    "print(f'State {state_to_inspect}: preferred action = {symbols[np.argmax(q_vals)]}')"
]),

]

with open("notebooks/RL_Day1.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb(day1_cells), f, ensure_ascii=False, indent=1)
print("✅ RL_Day1.ipynb written")

# ──────────────────────────────────────────────────────────
# DAY 2
# ──────────────────────────────────────────────────────────
day2_cells = [

md([
    "# RL Teaching — Day 2",
    "**CartPole · FrozenLake Slippery Comparison**",
    "",
    "> 📌 **Before you start:** Go to **File → Save a copy in Drive** to make your own editable copy.",
    "",
    "Focus on **what changes when you adjust the 🔧 parameters** and re-run the cell."
]),

code([
    "# ── Setup ────────────────────────────────────────────────────",
    "!pip install gymnasium matplotlib numpy --quiet",
    "import gymnasium as gym",
    "import numpy as np",
    "import matplotlib.pyplot as plt",
    "print('✅ Setup complete!')"
]),

md([
    "---",
    "## Part 1 · CartPole — Continuous State Space",
    "",
    "CartPole: keep a pole balanced on a moving cart.",
    "The state has **4 continuous values** — not grid squares like FrozenLake.",
    "",
    "Q-learning needs *discrete* states, so we divide each dimension into **bins**.",
    "Rein Room does this automatically; here you can see exactly what happens.",
    "",
    "```",
    "State dimension    | Range          | Bins",
    "Cart position      | -2.4  to  2.4  | 10",
    "Cart velocity      | -3.0  to  3.0  | 10",
    "Pole angle         | -0.25 to  0.25 | 10",
    "Pole ang. velocity | -3.0  to  3.0  | 10",
    "Total possible states: 10 x 10 x 10 x 10 = 10,000",
    "```",
    "",
    "### 🔧 Your task",
    "Watch the reward curve. When does improvement start?",
    "Does it ever drop suddenly after improving? Why might that happen?"
]),

code([
    "# ════════════════════════════════════════════",
    "alpha      = 0.5   # 🔧 learning rate    — try: 0.2 / 0.5 / 0.8",
    "gamma      = 0.99  # 🔧 discount factor  — try: 0.9 / 0.99",
    "epsilon    = 0.3   # 🔧 exploration rate — try: 0.1 / 0.3 / 0.5",
    "n_episodes = 500",
    "# ════════════════════════════════════════════",
    "",
    "env    = gym.make('CartPole-v1')",
    "n_bins = 10",
    "bins   = [",
    "    np.linspace(-2.4,  2.4,  n_bins),",
    "    np.linspace(-3.0,  3.0,  n_bins),",
    "    np.linspace(-0.25, 0.25, n_bins),",
    "    np.linspace(-3.0,  3.0,  n_bins),",
    "]",
    "",
    "def discretize(obs):",
    "    return tuple(min(np.digitize(obs[i], bins[i]), n_bins-1) for i in range(4))",
    "",
    "Q      = {}",
    "get_q  = lambda s, a: Q.get((s, a), 0.0)",
    "best_a = lambda s: max(range(2), key=lambda a: get_q(s, a))",
    "episode_rewards, episode_lengths = [], []",
    "",
    "for ep in range(n_episodes):",
    "    obs, _  = env.reset()",
    "    state   = discretize(obs)",
    "    total, steps, done = 0, 0, False",
    "    while not done:",
    "        action = env.action_space.sample() if np.random.random() < epsilon else best_a(state)",
    "        nobs, r, ter, tru, _ = env.step(action)",
    "        done   = ter or tru",
    "        ns     = discretize(nobs)",
    "        old_q  = get_q(state, action)",
    "        nmax   = max(get_q(ns, a) for a in range(2))",
    "        Q[(state, action)] = old_q + alpha * (r + gamma * nmax - old_q)",
    "        state, total, steps = ns, total + r, steps + 1",
    "    episode_rewards.append(total)",
    "    episode_lengths.append(steps)",
    "",
    "window = 30",
    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4))",
    "ax1.plot(np.convolve(episode_rewards, np.ones(window)/window, mode='valid'), lw=2)",
    "ax1.axhline(195, color='red', linestyle='--', label='Solved threshold (195)')",
    "ax1.set(title=f'CartPole Reward | alpha={alpha} gamma={gamma} epsilon={epsilon}',",
    "        xlabel='Episode', ylabel='Total Reward (max 200)')",
    "ax1.legend(); ax1.grid(alpha=0.3)",
    "ax2.plot(np.convolve(episode_lengths, np.ones(window)/window, mode='valid'), color='orange', lw=2)",
    "ax2.set(title='Episode Length  (longer = better balance)',",
    "        xlabel='Episode', ylabel='Steps')",
    "ax2.grid(alpha=0.3)",
    "plt.tight_layout(); plt.show()",
    "print(f'Q-table entries used : {len(Q):,} / {10**4*2:,} possible')",
    "print(f'Avg reward (last 50) : {np.mean(episode_rewards[-50:]):.1f} / 200')"
]),

md([
    "---",
    "## Part 2 · FrozenLake — Slippery vs. Non-Slippery",
    "",
    "Previously: `is_slippery=False` — agent moves exactly where intended.",
    "Now: `is_slippery=True` — agent sometimes slides sideways.",
    "",
    "### 🔧 Your task",
    "Compare the two curves:",
    "- Which converges faster?",
    "- Which is more stable (less bouncing)?",
    "- What does this tell you about learning in unpredictable environments?"
]),

code([
    "alpha, gamma, epsilon, n_episodes = 0.8, 0.95, 0.1, 3000",
    "window = 100",
    "",
    "def run_frozenlake(slippery):",
    "    env = gym.make('FrozenLake-v1', is_slippery=slippery)",
    "    Q   = np.zeros([env.observation_space.n, env.action_space.n])",
    "    rewards = []",
    "    for _ in range(n_episodes):",
    "        state, _ = env.reset()",
    "        total, done = 0, False",
    "        while not done:",
    "            action = env.action_space.sample() if np.random.random() < epsilon else np.argmax(Q[state])",
    "            ns, r, ter, tru, _ = env.step(action)",
    "            done = ter or tru",
    "            Q[state, action] += alpha * (r + gamma * np.max(Q[ns]) - Q[state, action])",
    "            state, total = ns, total + r",
    "        rewards.append(total)",
    "    return rewards",
    "",
    "print('Training both environments... (~15 seconds)')",
    "r_det  = run_frozenlake(slippery=False)",
    "r_slip = run_frozenlake(slippery=True)",
    "",
    "plt.figure(figsize=(12, 4))",
    "for rewards, label, color in [",
    "    (r_det,  'Non-slippery (deterministic)', 'steelblue'),",
    "    (r_slip, 'Slippery (stochastic)',         'coral'),",
    "]:",
    "    s = np.convolve(rewards, np.ones(window)/window, mode='valid')",
    "    plt.plot(s, label=label, color=color, lw=2)",
    "plt.title('FrozenLake: Deterministic vs. Stochastic')",
    "plt.xlabel('Episode'); plt.ylabel('Success Rate (smoothed)')",
    "plt.legend(); plt.grid(alpha=0.3); plt.show()",
    "print(f'Non-slippery success (last 500): {np.mean(r_det[-500:]):.1%}')",
    "print(f'Slippery     success (last 500): {np.mean(r_slip[-500:]):.1%}')"
]),

]

with open("notebooks/RL_Day2.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb(day2_cells), f, ensure_ascii=False, indent=1)
print("✅ RL_Day2.ipynb written")
print("\nDone! Both notebooks saved to notebooks/")
