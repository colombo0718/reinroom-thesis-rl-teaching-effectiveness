"""
rr_envs.py — RR Platform Custom Gymnasium Environments
=======================================================
Five environments that exactly replicate the reward functions of
Rein Room (reinroom.leaflune.org). Visualization may differ
(this is the control group's Colab version), but game logic and
reward values are identical to the RR JavaScript source code.

Environments:
    MABEnv       — Multi-Armed Bandit (MAB.html)
    Maze1DEnv    — 1D Maze            (Maze1D.html)
    Maze2DEnv    — 2D Maze            (Maze2D.html)
    HeliEnv      — Helicopter Flappy  (heli.html)
    FighterEnv   — Fighter Plane      (fighter.html)

Usage:
    from rr_envs import MABEnv, Maze1DEnv, Maze2DEnv, HeliEnv, FighterEnv
"""

import gymnasium as gym
from gymnasium import spaces
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from IPython.display import clear_output


# ─────────────────────────────────────────────────────────────
# 1. Multi-Armed Bandit
# ─────────────────────────────────────────────────────────────

class MABEnv(gym.Env):
    """
    Multi-Armed Bandit — 5 machines, episode = 10 pulls.

    Reward pools match RR MAB.html exactly:
        ❌ = 0 pts  |  🍬 = 1 pt  |  🪙 = 3 pts  |  💎 = 10 pts

    Modes (same as RR):
        'same'    — all machines share the same pool
        'fixed'   — two 0s, two 1s, one 3
        'slight'  — slight expected-value differences between machines
        'jackpot' — one machine hides a 💎 pool
    """

    _POOLS = {
        "same": [
            [0,0,0,1,1,1,1,1,3,3],
            [0,0,0,1,1,1,1,1,3,3],
            [0,0,0,1,1,1,1,1,3,3],
            [0,0,0,1,1,1,1,1,3,3],
            [0,0,0,1,1,1,1,1,3,3],
        ],
        "fixed": [
            [0]*10, [0]*10,
            [1]*10, [1]*10,
            [3]*10,
        ],
        "slight": [
            [0,0,0,1,1,1,1,1,3,3],
            [0,0,0,1,1,1,1,1,3,3],
            [1,1,1,1,1,1,1,1,3,3],
            [1,1,1,1,1,1,1,1,3,3],
            [1,1,1,1,1,1,3,3,3,3],
        ],
        "jackpot": [
            [0,0,0,1,1,1,1,1,3,3],
            [0,0,0,1,1,1,1,1,3,3],
            [0,0,0,1,1,1,1,1,3,3],
            [0,0,0,1,1,1,1,1,3,3],
            [0,0,0,0,0,0,0,0,10,10],
        ],
    }

    def __init__(self, mode: str = "slight"):
        super().__init__()
        assert mode in self._POOLS, f"mode must be one of {list(self._POOLS)}"
        self.mode = mode
        self.n_machines = 5
        self.episode_step_limit = 10          # 10 pulls per episode (matches RR)

        self.observation_space = spaces.Box(
            low=np.array([0], dtype=np.float32),
            high=np.array([4], dtype=np.float32),
        )
        self.action_space = spaces.Discrete(self.n_machines)

    def _setup_pools(self):
        pools = self._POOLS[self.mode]
        idx = self.np_random.permutation(len(pools))
        self.machine_pools = [pools[i] for i in idx]

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._setup_pools()
        self.selected = 0
        self.step_count = 0
        return np.array([self.selected], dtype=np.float32), {}

    def step(self, action: int):
        self.selected = int(action)
        pool = self.machine_pools[self.selected]
        reward = float(self.np_random.choice(pool))
        self.step_count += 1
        done = self.step_count >= self.episode_step_limit
        return np.array([self.selected], dtype=np.float32), reward, done, False, {}


# ─────────────────────────────────────────────────────────────
# 2. Maze 1D
# ─────────────────────────────────────────────────────────────

class Maze1DEnv(gym.Env):
    """
    1D Maze — 10 cells (0–9). Bomb at cell 0, Goal at cell 9.

    Reward (matches RR Maze1D.html):
        Reach Goal  🏆 : +10, done
        Reach Bomb  💣 : -10, done
        Pie mode    🍕 : goal gives +2 instead of +10
        Positive feedback: +1 moving right (not at goal), -1 moving left
        Negative feedback: -1 moving right, +1 moving left

    Actions:
        0 = stay  |  1 = right  |  2 = left
    """

    def __init__(self, start_pos: int = 4, feedback_mode: str = "none"):
        super().__init__()
        assert 1 <= start_pos <= 8, "start_pos must be between 1 and 8"
        assert feedback_mode in ("none", "positive", "negative", "pie")
        self.grid_size = 10
        self.start_pos = start_pos
        self.feedback_mode = feedback_mode

        self.observation_space = spaces.Discrete(self.grid_size)
        self.action_space = spaces.Discrete(3)   # 0=stay, 1=right, 2=left

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.pos = self.start_pos
        return int(self.pos), {}

    def step(self, action: int):
        prev = self.pos

        if action == 1 and self.pos < self.grid_size - 1:
            self.pos += 1
        elif action == 2 and self.pos > 0:
            self.pos -= 1

        reward = 0.0

        # Step feedback
        if self.feedback_mode == "positive":
            if self.pos > prev and self.pos < 9:
                reward += 1.0
            elif self.pos < prev and self.pos > 0:
                reward -= 1.0
        elif self.feedback_mode in ("negative", "pie"):
            if self.pos > prev and self.pos < 9:
                reward -= 1.0
            elif self.pos < prev and self.pos > 0:
                reward += 1.0

        done = False
        if self.pos == 0:                  # bomb
            reward -= 10.0
            done = True
        elif self.pos == self.grid_size - 1:   # goal
            reward += 2.0 if self.feedback_mode == "pie" else 10.0
            done = True

        return int(self.pos), reward, done, False, {}


# ─────────────────────────────────────────────────────────────
# 3. Maze 2D
# ─────────────────────────────────────────────────────────────

class Maze2DEnv(gym.Env):
    """
    2D Maze — 10×10 grid. Start: (0, 0). Goal: (9, 9).

    Reward (matches RR Maze2D.html):
        Reach (9,9) : +10, done
        All other steps : 0

    State: [x, y] grid coordinates (0–9 each).

    Actions:
        0 = stay  |  1 = up  |  2 = down  |  3 = left  |  4 = right
    """

    def __init__(self):
        super().__init__()
        self.grid_size = 10

        self.observation_space = spaces.Box(
            low=np.array([0, 0], dtype=np.float32),
            high=np.array([9, 9], dtype=np.float32),
        )
        self.action_space = spaces.Discrete(5)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.x, self.y = 0, 0
        return np.array([self.x, self.y], dtype=np.float32), {}

    def step(self, action: int):
        if action == 1 and self.y < self.grid_size - 1:
            self.y += 1
        elif action == 2 and self.y > 0:
            self.y -= 1
        elif action == 3 and self.x > 0:
            self.x -= 1
        elif action == 4 and self.x < self.grid_size - 1:
            self.x += 1

        done = (self.x == 9 and self.y == 9)
        reward = 10.0 if done else 0.0
        return np.array([self.x, self.y], dtype=np.float32), reward, done, False, {}


# ─────────────────────────────────────────────────────────────
# 4. Heli (Flappy Helicopter)
# ─────────────────────────────────────────────────────────────

class HeliEnv(gym.Env):
    """
    Helicopter Flappy Bird — matches RR heli.html exactly.

    Reward:
        Survive each step  : +0.01
        Pass a wall        : +1.0
        Crash (wall/edge)  : -10.0, done

    State (3D, normalized to [-1, 1]):
        heliY        — helicopter vertical position
        wallDistance — horizontal distance to next wall
        gapCenterY   — vertical center of next gap

    Actions:
        0 = fall (gravity)  |  1 = flap (move up)

    Modes (match RR):
        'fixed' — gap always at center height
        'small' — gap center ± 100 px random
        'large' — gap center ± 200 px random
    """

    # Constants from heli.html
    CANVAS_W      = 500
    CANVAS_H      = 500
    HELI_X        = 120
    HELI_SIZE     = 34
    WALL_WIDTH    = 44
    WALL_SPACING  = 220
    GAP_HEIGHT    = 170
    FLY_SPEED     = 2.0
    WALL_SPEED    = 1.8
    FIXED_GAP_CTR = 250
    SURVIVAL_R    = 0.01
    PASS_R        = 1.0
    CRASH_P       = -10.0

    def __init__(self, mode: str = "fixed"):
        super().__init__()
        assert mode in ("fixed", "small", "large")
        self.mode = mode

        self.observation_space = spaces.Box(
            low=np.full(3, -1.0, dtype=np.float32),
            high=np.full(3,  1.0, dtype=np.float32),
        )
        self.action_space = spaces.Discrete(2)

    # ----------------------------------------------------------
    def _make_wall(self, x: float) -> dict:
        if self.mode == "fixed":
            center = self.FIXED_GAP_CTR
        elif self.mode == "small":
            center = self.np_random.uniform(
                self.FIXED_GAP_CTR - 100, self.FIXED_GAP_CTR + 100
            )
        else:
            center = self.np_random.uniform(
                self.FIXED_GAP_CTR - 200, self.FIXED_GAP_CTR + 200
            )
        lo = self.GAP_HEIGHT / 2 + 20
        hi = self.CANVAS_H - self.GAP_HEIGHT / 2 - 20
        center = float(np.clip(center, lo, hi))
        gap_top = center - self.GAP_HEIGHT / 2
        return {"x": x, "gap_top": gap_top, "gap_bottom": gap_top + self.GAP_HEIGHT, "passed": False}

    def _obs(self) -> np.ndarray:
        nw = next((w for w in self.walls if w["x"] + self.WALL_WIDTH >= self.HELI_X), self.walls[0])
        gap_center = (nw["gap_top"] + nw["gap_bottom"]) / 2
        wall_dist   = nw["x"] + self.WALL_WIDTH - self.HELI_X
        # normalize each to [-1, 1]
        hy  = self.heli_y / self.CANVAS_H * 2 - 1
        wd  = wall_dist  / self.CANVAS_W * 2 - 1
        gc  = gap_center / self.CANVAS_H * 2 - 1
        return np.array([hy, wd, gc], dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.heli_y   = float(self.CANVAS_H / 2)
        self.heli_dir = 1        # 1 = falling, -1 = rising
        self.walls = [
            self._make_wall(self.CANVAS_W + 120),
            self._make_wall(self.CANVAS_W + 120 + self.WALL_SPACING),
            self._make_wall(self.CANVAS_W + 120 + self.WALL_SPACING * 2),
        ]
        self.score = 0
        return self._obs(), {}

    def step(self, action: int):
        self.heli_dir = -1 if action == 1 else 1
        self.heli_y  += self.heli_dir * self.FLY_SPEED
        reward        = self.SURVIVAL_R

        # Move walls, check pass
        for w in self.walls:
            w["x"] -= self.WALL_SPEED
            if not w["passed"] and w["x"] + self.WALL_WIDTH < self.HELI_X:
                w["passed"] = True
                self.score += 1
                reward += self.PASS_R

        # Recycle wall
        if self.walls[0]["x"] + self.WALL_WIDTH < -10:
            self.walls.pop(0)
            self.walls.append(self._make_wall(self.walls[-1]["x"] + self.WALL_SPACING))

        # Collision — boundary
        r = self.HELI_SIZE * 0.28   # ≈ 9.52
        if self.heli_y - r <= 0 or self.heli_y + r >= self.CANVAS_H:
            return self._obs(), reward + self.CRASH_P, True, False, {}

        # Collision — walls
        for w in self.walls:
            hit_x = self.HELI_X + r > w["x"] and self.HELI_X - r < w["x"] + self.WALL_WIDTH
            hit_y = self.heli_y - r < w["gap_top"] or self.heli_y + r > w["gap_bottom"]
            if hit_x and hit_y:
                return self._obs(), reward + self.CRASH_P, True, False, {}

        return self._obs(), reward, False, False, {}


# ─────────────────────────────────────────────────────────────
# 5. Fighter Plane
# ─────────────────────────────────────────────────────────────

class FighterEnv(gym.Env):
    """
    Fighter Plane — matches RR fighter.html exactly.

    Reward:
        Hit rock (bullet hits rock)  : +10
        Miss (bullet exits top)      : -1
        Rock crashes into player     : -100, done
        Clear (10 hits)              : done (success)

    State (5D, normalized to [-1, 1]):
        playerX, rockX, rockY, rockVX, rockVY

    Actions:
        0 = none  |  1 = left  |  2 = right  |  3 = shoot

    Modes (match RR 5 levels):
        'fixed'    — rock stationary at center top
        'randomX'  — rock random X each episode
        'randomXY' — rock random X and Y
        'falling'  — rock falls from top (moving target)
        'drifting' — falling + horizontal drift
    """

    CANVAS_W    = 500
    CANVAS_H    = 600
    LANE_MIN    = 36
    LANE_MAX    = 464          # 500 - 36
    PLAYER_Y    = 528          # 600 - 72
    MAX_SPEED   = 12.0
    ACCEL       = 2.5
    FRICTION    = 0.82
    BULLET_SPD  = 20.0
    HIT_R       = 10.0
    MISS_P      = -1.0
    CRASH_P     = -100.0
    CLEAR_HITS  = 10
    COOLDOWN    = 20           # frames

    def __init__(self, mode: str = "fixed"):
        super().__init__()
        assert mode in ("fixed", "randomX", "randomXY", "falling", "drifting")
        self.mode = mode

        self.observation_space = spaces.Box(
            low=np.full(5, -1.0, dtype=np.float32),
            high=np.full(5,  1.0, dtype=np.float32),
        )
        self.action_space = spaces.Discrete(4)

    # ----------------------------------------------------------
    def _spawn_rock(self) -> dict:
        cx = self.CANVAS_W / 2
        if self.mode == "fixed":
            return {"x": cx, "y": 60.0, "vx": 0.0, "vy": 0.0}
        if self.mode == "randomX":
            return {"x": float(self.np_random.uniform(self.LANE_MIN, self.LANE_MAX)),
                    "y": 60.0, "vx": 0.0, "vy": 0.0}
        if self.mode == "randomXY":
            return {"x": float(self.np_random.uniform(self.LANE_MIN, self.LANE_MAX)),
                    "y": float(self.np_random.uniform(30, 200)),
                    "vx": 0.0, "vy": 0.0}
        if self.mode == "falling":
            return {"x": float(self.np_random.uniform(self.LANE_MIN, self.LANE_MAX)),
                    "y": -20.0, "vx": 0.0,
                    "vy": float(self.np_random.uniform(1.5, 3.0))}
        # drifting
        return {"x": float(self.np_random.uniform(self.LANE_MIN, self.LANE_MAX)),
                "y": -20.0,
                "vx": float(self.np_random.uniform(-2.0, 2.0)),
                "vy": float(self.np_random.uniform(1.5, 3.0))}

    def _normalize(self) -> np.ndarray:
        cx = self.CANVAS_W / 2
        cy = self.CANVAS_H / 2
        px  = (self.player_x          - cx) / cx
        rx  = (self.rock["x"]         - cx) / cx
        ry  = (cy - self.rock["y"])         / cy   # positive = above center
        rvx = self.rock["vx"]               / self.MAX_SPEED
        rvy = self.rock["vy"]               / self.MAX_SPEED
        return np.clip(np.array([px, rx, ry, rvx, rvy], dtype=np.float32), -1.0, 1.0)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.player_x   = float(self.CANVAS_W / 2)
        self.player_vx  = 0.0
        self.bullet     = None
        self.rock       = self._spawn_rock()
        self.hits       = 0
        self.cooldown   = 0
        return self._normalize(), {}

    def step(self, action: int):
        reward = 0.0

        if self.cooldown > 0:
            self.cooldown -= 1

        # Action
        if action == 1:
            self.player_vx -= self.ACCEL
        elif action == 2:
            self.player_vx += self.ACCEL
        elif action == 3 and self.bullet is None and self.cooldown == 0:
            self.bullet   = {"x": self.player_x, "y": float(self.PLAYER_Y)}
            self.cooldown = self.COOLDOWN

        # Physics — player
        self.player_vx  *= self.FRICTION
        self.player_vx   = float(np.clip(self.player_vx, -self.MAX_SPEED, self.MAX_SPEED))
        self.player_x   += self.player_vx
        self.player_x    = float(np.clip(self.player_x, self.LANE_MIN, self.LANE_MAX))

        # Physics — rock (cylindrical X wrap, same as RR)
        self.rock["x"] += self.rock["vx"]
        self.rock["y"] += self.rock["vy"]
        if self.rock["x"] < self.LANE_MIN:
            self.rock["x"] = float(self.LANE_MAX)
        elif self.rock["x"] > self.LANE_MAX:
            self.rock["x"] = float(self.LANE_MIN)

        # Rock exits bottom (falling/drifting modes) → respawn
        if self.rock["y"] > self.CANVAS_H + 20:
            self.rock = self._spawn_rock()

        # Bullet movement & hit detection
        if self.bullet is not None:
            self.bullet["y"] -= self.BULLET_SPD
            rock_r = 20
            if (abs(self.bullet["x"] - self.rock["x"]) < rock_r and
                    abs(self.bullet["y"] - self.rock["y"]) < rock_r):
                reward     += self.HIT_R
                self.hits  += 1
                self.bullet = None
                self.rock   = self._spawn_rock()
                if self.hits >= self.CLEAR_HITS:
                    return self._normalize(), reward, True, False, {"result": "clear"}
            elif self.bullet["y"] < 0:
                reward     += self.MISS_P
                self.bullet = None

        # Rock crashes into player
        player_r = 20
        if (abs(self.rock["x"] - self.player_x) < player_r and
                abs(self.rock["y"] - self.PLAYER_Y) < player_r):
            reward += self.CRASH_P
            return self._normalize(), reward, True, False, {"result": "crash"}

        return self._normalize(), reward, False, False, {}


# ─────────────────────────────────────────────────────────────
# Shared Q-Learning Runner (for Colab use)
# ─────────────────────────────────────────────────────────────

def run_q_learning(env, alpha=0.5, gamma=0.95, epsilon=0.2,
                   n_episodes=500, bins=None, verbose=True):
    """
    Run tabular Q-learning on any rr_envs environment.

    For continuous state environments (Maze2D, Heli, Fighter),
    pass bins=N to discretize each dimension into N buckets.
    Discrete-state envs (MAB, Maze1D) ignore bins.

    Returns:
        episode_rewards  — list of total reward per episode
        episode_lengths  — list of steps per episode
        Q                — final Q-table (dict)
    """
    is_discrete = isinstance(env.observation_space, spaces.Discrete)
    obs_dim     = 1 if is_discrete else env.observation_space.shape[0]
    n_actions   = env.action_space.n

    if is_discrete:
        n_states = env.observation_space.n
        def to_key(obs):
            return int(obs)
    else:
        if bins is None:
            bins = 6
        low   = env.observation_space.low
        high  = env.observation_space.high
        edges = [np.linspace(low[i], high[i], bins + 1) for i in range(obs_dim)]
        def to_key(obs):
            return tuple(
                int(np.clip(np.digitize(obs[i], edges[i]) - 1, 0, bins - 1))
                for i in range(obs_dim)
            )

    Q = {}
    get_q  = lambda s, a: Q.get((s, a), 0.0)
    best_a = lambda s: max(range(n_actions), key=lambda a: get_q(s, a))

    episode_rewards, episode_lengths = [], []

    for ep in range(n_episodes):
        obs, _ = env.reset()
        state   = to_key(obs)
        total_r = 0.0
        steps   = 0
        done    = False

        while not done:
            if np.random.random() < epsilon:
                action = env.action_space.sample()
            else:
                action = best_a(state)

            obs, reward, terminated, truncated, _ = env.step(action)
            done       = terminated or truncated
            next_state = to_key(obs)

            old_q   = get_q(state, action)
            next_q  = max(get_q(next_state, a) for a in range(n_actions)) if not done else 0.0
            Q[(state, action)] = old_q + alpha * (reward + gamma * next_q - old_q)

            state   = next_state
            total_r += reward
            steps   += 1

        episode_rewards.append(total_r)
        episode_lengths.append(steps)

        if verbose and (ep + 1) % max(1, n_episodes // 10) == 0:
            avg = np.mean(episode_rewards[-50:])
            print(f"  Episode {ep+1:>5} / {n_episodes}  |  avg reward (last 50): {avg:.2f}")

    return episode_rewards, episode_lengths, Q


def plot_training(episode_rewards, episode_lengths,
                  label="", window=30):
    """Plot reward curve + episode length curve."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4))

    smooth_r = np.convolve(episode_rewards, np.ones(window) / window, mode="valid")
    ax1.plot(smooth_r, linewidth=2, label=label)
    ax1.set_title(f"Episode Reward  (smoothed, window={window})")
    ax1.set_xlabel("Episode")
    ax1.set_ylabel("Total Reward")
    ax1.grid(True, alpha=0.3)

    smooth_l = np.convolve(episode_lengths, np.ones(window) / window, mode="valid")
    ax2.plot(smooth_l, color="coral", linewidth=2)
    ax2.set_title("Episode Length (steps)")
    ax2.set_xlabel("Episode")
    ax2.set_ylabel("Steps")
    ax2.grid(True, alpha=0.3)

    plt.suptitle(label, fontsize=13)
    plt.tight_layout()
    plt.show()


def plot_maze2d_qtable(Q, bins=6):
    """Visualize Q-table for Maze2D as a heatmap with arrows."""
    import matplotlib.patches as mpatches

    action_arrows = {0: "", 1: "↑", 2: "↓", 3: "←", 4: "→"}
    grid = np.zeros((bins, bins))
    arrows = [["" for _ in range(bins)] for _ in range(bins)]

    for bx in range(bins):
        for by in range(bins):
            vals = [Q.get(((bx, by), a), 0.0) for a in range(5)]
            grid[bins - 1 - by, bx] = max(vals)
            arrows[bins - 1 - by][bx] = action_arrows[int(np.argmax(vals))]

    fig, ax = plt.subplots(figsize=(7, 7))
    im = ax.imshow(grid, cmap="YlOrRd", aspect="equal")
    plt.colorbar(im, ax=ax, label="Max Q-value (confidence)")

    for r in range(bins):
        for c in range(bins):
            ax.text(c, r, arrows[r][c], ha="center", va="center", fontsize=14)

    ax.set_xticks(range(bins))
    ax.set_yticks(range(bins))
    ax.set_xlabel("X bin (→ east)")
    ax.set_ylabel("Y bin (↑ north)")
    ax.set_title("Maze2D Q-Table — Best Action per State\n(color = confidence, arrow = preferred direction)")
    plt.tight_layout()
    plt.show()
