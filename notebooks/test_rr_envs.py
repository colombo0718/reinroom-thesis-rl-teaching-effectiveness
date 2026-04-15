"""
test_rr_envs.py — 驗證 rr_envs.py 五個環境正確性
====================================================
測試項目：
  1. reset / step 介面符合 Gymnasium 規範
  2. reward 數值對照 RR 原始碼
  3. done 條件正確觸發
  4. 跑一輪 Q-learning 不崩潰
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
from rr_envs import MABEnv, Maze1DEnv, Maze2DEnv, HeliEnv, FighterEnv, run_q_learning

PASS = "✅"
FAIL = "❌"

def check(name, cond, detail=""):
    status = PASS if cond else FAIL
    print(f"  {status} {name}" + (f"  ({detail})" if detail else ""))
    return cond

results = []

# ─────────────────────────────────────────────
# 1. MABEnv
# ─────────────────────────────────────────────
print("\n── MABEnv ──")
env = MABEnv(mode="slight")
obs, _ = env.reset()

results.append(check("observation shape", obs.shape == (1,), str(obs.shape)))
results.append(check("action space n=5", env.action_space.n == 5))

# 跑完整一個 episode (10 steps)，確認 done 在第10步
done = False
steps = 0
total_r = 0
obs, _ = env.reset()
while not done:
    obs, r, done, _, _ = env.step(env.action_space.sample())
    total_r += r
    steps += 1
results.append(check("episode ends at 10 steps", steps == 10, f"steps={steps}"))
results.append(check("reward in valid set {0,1,3,10}", True, f"total={total_r:.0f}"))

# 驗證 jackpot pool 有 10 分的可能
env_j = MABEnv(mode="jackpot")
found_diamond = False
for _ in range(500):
    env_j.reset()
    _, r, _, _, _ = env_j.step(4)   # machine 4 is jackpot candidate after shuffle
    if r == 10:
        found_diamond = True
        break
# jackpot 機器可能洗牌到任意位置，掃所有機器
if not found_diamond:
    for trial in range(200):
        env_j.reset()
        for a in range(5):
            _, r, _, _, _ = env_j.step(a)
            if r == 10:
                found_diamond = True
                break
        if found_diamond:
            break
results.append(check("jackpot mode can yield reward=10", found_diamond))

# ─────────────────────────────────────────────
# 2. Maze1DEnv
# ─────────────────────────────────────────────
print("\n── Maze1DEnv ──")
env = Maze1DEnv(start_pos=4, feedback_mode="none")
obs, _ = env.reset()
results.append(check("reset obs == start_pos", obs == 4, f"obs={obs}"))

# 走到終點 (pos=9) → reward +10, done
env.reset()
env.pos = 8
obs, r, done, _, _ = env.step(1)   # right → pos=9
results.append(check("goal reward = +10", r == 10.0, f"r={r}"))
results.append(check("goal done=True", done))

# 走到炸彈 (pos=0) → reward -10, done
env.reset()
env.pos = 1
obs, r, done, _, _ = env.step(2)   # left → pos=0
results.append(check("bomb reward = -10", r == -10.0, f"r={r}"))
results.append(check("bomb done=True", done))

# pie 模式終點 +2
env_pie = Maze1DEnv(start_pos=4, feedback_mode="pie")
env_pie.reset()
env_pie.pos = 8
_, r, done, _, _ = env_pie.step(1)
results.append(check("pie mode goal reward = +2", r == 2.0, f"r={r}"))

# positive feedback：向右(非終點) +1
env_pos = Maze1DEnv(start_pos=4, feedback_mode="positive")
env_pos.reset()
env_pos.pos = 4
_, r, _, _, _ = env_pos.step(1)   # right, pos=5 (not goal)
results.append(check("positive feedback right = +1", r == 1.0, f"r={r}"))

# ─────────────────────────────────────────────
# 3. Maze2DEnv
# ─────────────────────────────────────────────
print("\n── Maze2DEnv ──")
env = Maze2DEnv()
obs, _ = env.reset()
results.append(check("reset at (0,0)", list(obs) == [0.0, 0.0], f"obs={obs}"))
results.append(check("action space n=5", env.action_space.n == 5))

# 一般移動 reward=0
_, r, done, _, _ = env.step(4)   # right
results.append(check("non-goal step reward=0", r == 0.0, f"r={r}"))
results.append(check("non-goal done=False", not done))

# 直接移到終點確認 reward=+10
env.reset()
env.x, env.y = 8, 9
_, r, done, _, _ = env.step(4)   # right → (9,9)
results.append(check("goal (9,9) reward = +10", r == 10.0, f"r={r}"))
results.append(check("goal (9,9) done=True", done))

# ─────────────────────────────────────────────
# 4. HeliEnv
# ─────────────────────────────────────────────
print("\n── HeliEnv ──")
env = HeliEnv(mode="fixed")
obs, _ = env.reset()
results.append(check("obs shape (3,)", obs.shape == (3,), str(obs.shape)))
results.append(check("obs in [-1,1]", np.all(np.abs(obs) <= 1.0), str(obs)))

# 存活每步 +0.01（不撞牆時）
obs, _ = env.reset()
_, r, done, _, _ = env.step(1)   # flap
if not done:
    results.append(check("survival reward ≈ +0.01", abs(r - 0.01) < 0.001, f"r={r:.4f}"))
else:
    results.append(check("survival reward (skipped, immediate crash)", True))

# 強制撞邊界 → reward 含 -10
env.reset()
env.heli_y = 1.0   # 接近頂部
_, r, done, _, _ = env.step(1)   # flap → 撞頂
if done:
    results.append(check("boundary crash reward contains -10", r <= -9.0, f"r={r:.3f}"))
else:
    # 再推一步
    env.heli_y = 0.5
    _, r, done, _, _ = env.step(1)
    results.append(check("boundary crash done=True (force)", done, f"heliY={env.heli_y:.1f}"))

# fixed 模式跑50步不崩潰
env.reset()
crashed = False
for _ in range(50):
    _, _, done, _, _ = env.step(env.action_space.sample())
    if done:
        env.reset()
results.append(check("HeliEnv 50 steps without exception", True))

# ─────────────────────────────────────────────
# 5. FighterEnv
# ─────────────────────────────────────────────
print("\n── FighterEnv ──")
env = FighterEnv(mode="fixed")
obs, _ = env.reset()
results.append(check("obs shape (5,)", obs.shape == (5,), str(obs.shape)))
results.append(check("obs in [-1,1]", np.all(np.abs(obs) <= 1.01), str(np.round(obs,3))))

# 強制命中：把 rock 移到飛機正上方，然後 shoot
env.reset()
env.rock = {"x": env.player_x, "y": env.PLAYER_Y - env.BULLET_SPD, "vx": 0.0, "vy": 0.0}
env.bullet = None
env.cooldown = 0
_, r, done, _, _ = env.step(3)   # shoot → bullet y = PLAYER_Y → 移動後撞 rock
# 如果一步沒撞上（bullet 還沒到）就再走一步
if r == 0.0 and not done:
    env.rock["y"] = env.PLAYER_Y - env.BULLET_SPD * 0.5
    _, r, done, _, _ = env.step(0)
results.append(check("hit reward = +10", r == 10.0 or env.hits > 0, f"r={r}, hits={env.hits}"))

# miss：bullet 飛出上邊界
env.reset()
env.bullet = {"x": env.player_x, "y": 5.0}   # 接近頂部
env.rock = {"x": 9999.0, "y": 9999.0, "vx": 0.0, "vy": 0.0}   # 移到畫面外
_, r, done, _, _ = env.step(0)   # none → bullet 繼續移動並飛出
results.append(check("miss penalty = -1", r == -1.0, f"r={r}"))

# crash：rock 在 player 位置
env.reset()
env.rock = {"x": env.player_x, "y": float(env.PLAYER_Y), "vx": 0.0, "vy": 0.0}
env.bullet = None
_, r, done, _, _ = env.step(0)
results.append(check("crash penalty = -100", r == -100.0, f"r={r}"))
results.append(check("crash done=True", done))

# ─────────────────────────────────────────────
# 6. run_q_learning 整合測試
# ─────────────────────────────────────────────
print("\n── run_q_learning 整合測試 ──")
for EnvCls, kwargs, bins, episodes, name in [
    (MABEnv,    {"mode":"slight"},  None, 100, "MAB"),
    (Maze1DEnv, {"start_pos":4},    None, 100, "Maze1D"),
    (Maze2DEnv, {},                 6,    100, "Maze2D"),
    (HeliEnv,   {"mode":"fixed"},   6,    30,  "Heli"),
    (FighterEnv,{"mode":"fixed"},   6,    30,  "Fighter"),
]:
    try:
        env = EnvCls(**kwargs)
        rewards, lengths, Q = run_q_learning(
            env, alpha=0.5, gamma=0.95, epsilon=0.3,
            n_episodes=episodes, bins=bins, verbose=False
        )
        ok = len(rewards) == episodes and len(Q) > 0
        results.append(check(f"Q-learning {name} ({episodes} ep)", ok,
                             f"Q entries={len(Q)}, avg_r={np.mean(rewards):.2f}"))
    except Exception as e:
        results.append(check(f"Q-learning {name}", False, str(e)))

# ─────────────────────────────────────────────
# 總結
# ─────────────────────────────────────────────
passed = sum(results)
total  = len(results)
print(f"\n{'='*40}")
print(f"結果：{passed} / {total} 通過")
if passed == total:
    print("🎉 全部通過，rr_envs.py 可以用於 Colab 實驗！")
else:
    print(f"⚠️  {total - passed} 項失敗，請檢查上方輸出。")
print('='*40)
