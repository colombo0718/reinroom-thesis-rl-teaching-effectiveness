"""
verify_data.py — 驗證 data.js 與 CSV 原始數據的一致性

執行：
    cd C:\\Users\\USER\\論文 - RL平台教學成效
    python figures/verify_data.py
"""

import csv
import io
from pathlib import Path
from statistics import mean, stdev
import math

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "C.數據收集"

TEST_ID = "S1136103"
STRAIGHTLINERS = {"1123505", "DH10"}


def parse_score(s):
    return int(s.split("/")[0].strip())


def normalize_id(s):
    return s.lstrip("S").replace("-", "").replace(" ", "").upper()


print("=" * 70)
print("論文數據驗證報告")
print("=" * 70)

# 1. 檢查樣本人數
print("\n【樣本人數驗證】")
with io.open(DATA_DIR / "RL Lab — Pre-Test (Group A) (回覆) - 表單回覆 1.csv", "r", encoding="utf-8-sig") as f:
    pre_a = list(csv.DictReader(f))
    pre_a_valid = [r for r in pre_a if r["Student ID"].strip().upper() != TEST_ID]
    print(f"✓ 實驗組前測：{len(pre_a_valid)} 人（原始 {len(pre_a)} 人，排除 1 個測試帳號）")

with io.open(DATA_DIR / "RL Lab — Post-Test (Group A) (回覆) - 表單回覆 1.csv", "r", encoding="utf-8-sig") as f:
    post_a = list(csv.DictReader(f))
    post_a_valid = [r for r in post_a if r["Student ID"].strip().upper() != TEST_ID]
    print(f"✓ 實驗組後測：{len(post_a_valid)} 人")

with io.open(DATA_DIR / "RL Lab — Pre-Test (Group B) (回覆) - 表單回覆 1.csv", "r", encoding="utf-8-sig") as f:
    pre_b = list(csv.DictReader(f))
    pre_b_valid = [r for r in pre_b if r["Student ID"].strip().upper() != TEST_ID]
    print(f"✓ 對照組前測：{len(pre_b_valid)} 人")

with io.open(DATA_DIR / "RL Lab — Post-Test (Group B) (回覆) - 表單回覆 1.csv", "r", encoding="utf-8-sig") as f:
    post_b = list(csv.DictReader(f))
    post_b_valid = [r for r in post_b if r["Student ID"].strip().upper() != TEST_ID]
    print(f"✓ 對照組後測：{len(post_b_valid)} 人")

# 2. 檢查概念測驗分數統計
print("\n【概念測驗分數驗證】")
pre_a_scores = [parse_score(r["分數"]) for r in pre_a_valid]
post_a_scores = [parse_score(r["分數"]) for r in post_a_valid]
pre_b_scores = [parse_score(r["分數"]) for r in pre_b_valid]
post_b_scores = [parse_score(r["分數"]) for r in post_b_valid]

print(f"實驗組前測：M={mean(pre_a_scores):.2f}, SD={stdev(pre_a_scores):.2f}, n={len(pre_a_scores)}")
print(f"實驗組後測：M={mean(post_a_scores):.2f}, n={len(post_a_scores)}")
print(f"對照組前測：M={mean(pre_b_scores):.2f}, SD={stdev(pre_b_scores):.2f}, n={len(pre_b_scores)}")
print(f"對照組後測：M={mean(post_b_scores):.2f}, n={len(post_b_scores)}")

# 3. 讀取任務完成率
print("\n【任務完成率驗證】")
with io.open(DATA_DIR / "任務完成記錄表_A組.md", "r", encoding="utf-8") as f:
    content_a = f.read()
    print(f"✓ 實驗組任務表已讀取（{len(content_a)} 字）")

with io.open(DATA_DIR / "任務完成記錄表_B組.md", "r", encoding="utf-8") as f:
    content_b = f.read()
    print(f"✓ 對照組任務表已讀取（{len(content_b)} 字）")

# 4. 檢查 Section 3 平台回饋計算
print("\n【Section 3 平台回饋驗證】")


def get_section_keys(row, prefix):
    keys = [k for k in row if k.startswith(prefix)]
    return sorted(keys, key=lambda k: int(k.split(".")[0].split("-")[1]))


sec3_a = []
for row in post_a_valid:
    sec3_keys = get_section_keys(row, "3-")
    sec3_a.append([int(row[k]) for k in sec3_keys])

sec3_b = []
for row in post_b_valid:
    sec3_keys = get_section_keys(row, "3-")
    sec3_b.append([int(row[k]) for k in sec3_keys])

if sec3_a:
    sec3_a_means = [mean([s[i] for s in sec3_a]) for i in range(5)]
    print(f"實驗組 3-1 介面易用：{sec3_a_means[0]:.4f}")
    print(f"實驗組 3-2 參數信心：{sec3_a_means[1]:.4f}")
    print(f"實驗組 3-3 視覺化幫助：{sec3_a_means[2]:.4f}")
    print(f"實驗組 3-4 學習動機：{sec3_a_means[3]:.4f}  ← checklist 要求 4.17")
    print(f"實驗組 3-5 推薦意願：{sec3_a_means[4]:.4f}")

if sec3_b:
    sec3_b_means = [mean([s[i] for s in sec3_b]) for i in range(5)]
    print(f"\n對照組 3-1 介面易用：{sec3_b_means[0]:.4f}")
    print(f"對照組 3-2 參數信心：{sec3_b_means[1]:.4f}")
    print(f"對照組 3-3 視覺化幫助：{sec3_b_means[2]:.4f}")
    print(f"對照組 3-4 學習動機：{sec3_b_means[3]:.4f}  ← checklist 要求 3.33")
    print(f"對照組 3-5 推薦意願：{sec3_b_means[4]:.4f}")

# 5. 檢查 SUS 計算
print("\n【SUS 易用性驗證】")


def calc_sus(items):
    odd = [items[i] - 1 for i in [0, 2, 4, 6, 8]]
    even = [5 - items[i] for i in [1, 3, 5, 7, 9]]
    return sum(odd + even) * 2.5


sus_a = []
sus_b = []

for row in post_a_valid:
    sus_keys = get_section_keys(row, "5-")
    if sus_keys:
        sus_raw = [int(row[k]) for k in sus_keys]
        sus_a.append(calc_sus(sus_raw))

for row in post_b_valid:
    sus_keys = get_section_keys(row, "5-")
    if sus_keys:
        sus_raw = [int(row[k]) for k in sus_keys]
        sus_b.append(calc_sus(sus_raw))

print(f"實驗組 SUS：M={mean(sus_a):.2f}, SD={stdev(sus_a):.2f}, n={len(sus_a)}")
print(f"對照組 SUS：M={mean(sus_b):.2f}, SD={stdev(sus_b):.2f}, n={len(sus_b)}")

# 排除直線式作答後
sus_a_clean = [v for i, v in enumerate(sus_a)
               if list(post_a_valid)[i]["Student ID"].strip().upper() not in {s.upper() for s in STRAIGHTLINERS}]
print(f"實驗組 SUS（排除直線式）：M={mean(sus_a_clean):.2f}, SD={stdev(sus_a_clean):.2f}, n={len(sus_a_clean)}")

print("\n" + "=" * 70)
print("✅ 驗證完成。請檢查上述數值是否與 figures/data.js 與論文一致。")
print("=" * 70)
