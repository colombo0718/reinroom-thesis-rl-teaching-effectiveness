"""
generate_survey_charts.py
產生問卷 Section 2 三張圖表題用圖，輸出到 survey_charts/
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

np.random.seed(42)
OUT = Path(__file__).parent / "survey_charts"
OUT.mkdir(exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# ─────────────────────────────────────────────────────────────
# Chart 1 — Reward curve: flat then rising then plateau
# Question: "stays flat first 100 episodes, then rises"
# ─────────────────────────────────────────────────────────────

n = 400
ep = np.arange(n)

flat    = np.random.normal(1.0, 0.6, 120)
rising  = np.linspace(1.0, 9.0, 160) + np.random.normal(0, 0.7, 160)
plateau = np.random.normal(9.0, 0.4, 120)
raw     = np.concatenate([flat, rising, plateau])

# smoothing
w = 15
smooth = np.convolve(raw, np.ones(w) / w, mode="valid")
ep_s   = ep[:len(smooth)]

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(ep_s, smooth, color="#1565C0", linewidth=2.2)
ax.axvline(120, color="#999", linewidth=1.2, linestyle="--", alpha=0.7)
ax.text(125, 1.5, "episode ~120", color="#666", fontsize=10)
ax.set_xlabel("Episode", fontsize=13)
ax.set_ylabel("Average Reward", fontsize=13)
ax.set_title("Training Reward Curve", fontsize=14, fontweight="bold")
ax.set_ylim(-1, 12)
ax.set_xlim(0, n)
ax.grid(True, alpha=0.25)
fig.tight_layout()
fig.savefig(OUT / "chart_q2_1.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("✅ chart_q2_1.png saved")

# ─────────────────────────────────────────────────────────────
# Chart 2 — Two curves: A fast+noisy, B slow+smooth
# Question: "Curve A high learning rate vs Curve B"
# ─────────────────────────────────────────────────────────────

n = 350
ep = np.arange(n)

# Curve A: high LR → rises fast but noisy
a_true  = 9.5 * (1 - np.exp(-ep / 40))
noise_a = np.random.normal(0, 1.6, n)
curve_a = a_true + noise_a

# Curve B: low LR → rises slowly but smooth
b_true  = 9.5 * (1 - np.exp(-ep / 180))
noise_b = np.random.normal(0, 0.25, n)
curve_b = b_true + noise_b

# light smoothing on A only
w = 4
a_s = np.convolve(curve_a, np.ones(w)/w, mode="valid")
ep_a = ep[:len(a_s)]

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(ep_a,  a_s,           color="#E53935", linewidth=1.4, alpha=0.85, label="Curve A")
ax.plot(ep[:n], curve_b,      color="#2E7D32", linewidth=2.2, label="Curve B")
ax.set_xlabel("Episode", fontsize=13)
ax.set_ylabel("Average Reward", fontsize=13)
ax.set_title("Reward Curves: A vs B", fontsize=14, fontweight="bold")
ax.legend(fontsize=12, framealpha=0.8)
ax.set_ylim(-4, 13)
ax.set_xlim(0, n)
ax.grid(True, alpha=0.25)
fig.tight_layout()
fig.savefig(OUT / "chart_q2_2.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("✅ chart_q2_2.png saved")

# ─────────────────────────────────────────────────────────────
# Chart 3 — Q-table heatmap (Maze 2D, goal at top-right)
# Question: "cells near goal = strong color, cells far = weak"
# ─────────────────────────────────────────────────────────────

BINS = 8
action_sym = {0: "", 1: "↑", 2: "↓", 3: "←", 4: "→"}

grid   = np.zeros((BINS, BINS))
arrows = [["" for _ in range(BINS)] for _ in range(BINS)]

for bx in range(BINS):
    for by in range(BINS):
        dist = np.sqrt((bx - (BINS-1))**2 + (by - (BINS-1))**2)
        max_dist = np.sqrt(2) * (BINS - 1)
        # Q-value decreases with distance; far cells get extra noise
        q = max(0, 10 * (1 - dist / max_dist) + np.random.normal(0, dist * 0.45))
        grid[BINS - 1 - by, bx] = q

        # Best action pointing roughly toward goal
        if bx == BINS-1 and by == BINS-1:
            arrows[BINS-1-by][bx] = "★"
        elif bx < BINS-1 and by < BINS-1:
            arrows[BINS-1-by][bx] = "→" if (BINS-1-bx) > (BINS-1-by) else "↑"
        elif bx < BINS-1:
            arrows[BINS-1-by][bx] = "→"
        else:
            arrows[BINS-1-by][bx] = "↑"

fig, ax = plt.subplots(figsize=(6.5, 5.8))
im = ax.imshow(grid, cmap="YlOrRd", aspect="equal", vmin=0, vmax=10)
cbar = plt.colorbar(im, ax=ax, shrink=0.85)
cbar.set_label("Max Q-value (confidence)", fontsize=11)

for r in range(BINS):
    for c in range(BINS):
        ax.text(c, r, arrows[r][c], ha="center", va="center",
                fontsize=13, color="#222" if grid[r, c] < 6 else "#fff")

ax.set_xticks(range(BINS))
ax.set_yticks(range(BINS))
ax.set_xticklabels(range(BINS))
ax.set_yticklabels(range(BINS - 1, -1, -1))
ax.set_xlabel("X  (→ East)", fontsize=12)
ax.set_ylabel("Y  (↑ North)", fontsize=12)
ax.set_title("Maze Q-Table Heatmap\n(★ = goal, arrow = best direction)", fontsize=13, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT / "chart_q2_3.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("✅ chart_q2_3.png saved")

print(f"\n📁 All charts saved to: {OUT.resolve()}")
