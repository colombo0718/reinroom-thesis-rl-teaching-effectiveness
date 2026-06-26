"""
extract_data.py — 從 C.數據收集/ 的 CSV 抽取所有圖表所需資料，輸出為 figures/data.js

修訂版（2026/6/26）：依吳穎沺老師意見，所有量表分析以配對樣本為主要範圍，
                  並改用無母數檢定 + effect size。

執行：
    cd C:\\Users\\USER\\論文 - RL平台教學成效
    python figures/extract_data.py
"""

import csv
import io
import json
import math
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "C.數據收集"
OUT_FILE = Path(__file__).parent / "data.js"

TEST_ID = "S1136103"
STRAIGHTLINERS = {"1123505", "DH10"}


def parse_score(s):
    return int(s.split("/")[0].strip())


def normalize_id(s):
    return s.lstrip("S").replace("-", "").replace(" ", "").upper()


def load_pre(fname):
    students = {}
    with io.open(DATA_DIR / fname, "r", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            sid = row["Student ID"].strip().upper()
            if sid == TEST_ID:
                continue
            students[sid] = parse_score(row["分數"])
    return students


def get_section_keys(row, prefix):
    keys = [k for k in row if k.startswith(prefix)]
    return sorted(keys, key=lambda k: int(k.split(".")[0].split("-")[1]))


def calc_sus(items):
    odd = [items[i] - 1 for i in [0, 2, 4, 6, 8]]
    even = [5 - items[i] for i in [1, 3, 5, 7, 9]]
    return sum(odd + even) * 2.5


def load_post(fname):
    students = {}
    with io.open(DATA_DIR / fname, "r", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            sid = row["Student ID"].strip().upper()
            if sid == TEST_ID:
                continue
            sec3_keys = get_section_keys(row, "3-")
            nasa_keys = get_section_keys(row, "4-")
            sus_keys = get_section_keys(row, "5-")
            students[sid] = {
                "score": parse_score(row["分數"]),
                "sec3": [int(row[k]) for k in sec3_keys],
                "nasa": [float(row[k]) for k in nasa_keys],
                "sus_raw": [int(row[k]) for k in sus_keys],
                "sus": calc_sus([int(row[k]) for k in sus_keys]),
            }
    return students


def match_pair_ids(pre, post):
    """回傳成功配對之 (pre_id, post_id) tuples"""
    pairs = []
    for pid in pre:
        for poid in post:
            if normalize_id(pid) == normalize_id(poid):
                pairs.append((pid, poid))
                break
    return pairs


# === 載入四份 CSV ===
pre_a = load_pre("RL Lab — Pre-Test (Group A) (回覆) - 表單回覆 1.csv")
pre_b = load_pre("RL Lab — Pre-Test (Group B) (回覆) - 表單回覆 1.csv")
post_a = load_post("RL Lab — Post-Test (Group A) (回覆) - 表單回覆 1.csv")
post_b = load_post("RL Lab — Post-Test (Group B) (回覆) - 表單回覆 1.csv")

# 配對學生 ID
pairs_a = match_pair_ids(pre_a, post_a)  # [(pre_id, post_id), ...]
pairs_b = match_pair_ids(pre_b, post_b)

# 配對學生之前後測分數
A_pre_paired = [pre_a[pid] for pid, _ in pairs_a]
A_post_paired = [post_a[poid]["score"] for _, poid in pairs_a]
B_pre_paired = [pre_b[pid] for pid, _ in pairs_b]
B_post_paired = [post_b[poid]["score"] for _, poid in pairs_b]

# 配對學生之後測量表回應
A_post_paired_dicts = [post_a[poid] for _, poid in pairs_a]
B_post_paired_dicts = [post_b[poid] for _, poid in pairs_b]


def mean(lst):
    return sum(lst) / len(lst) if lst else 0


# === 整理為各圖表所需資料 ===
data = {
    # 概念測驗分數（圖 5-1 箱型圖 / 圖 5-2 增益圖）
    "concept_test": {
        # 全班（保留作為對照）
        "A_pre_all": list(pre_a.values()),
        "A_post_all": [v["score"] for v in post_a.values()],
        "B_pre_all": list(pre_b.values()),
        "B_post_all": [v["score"] for v in post_b.values()],
        # 配對樣本（主要分析）
        "A_pre_paired": A_pre_paired,
        "A_post_paired": A_post_paired,
        "B_pre_paired": B_pre_paired,
        "B_post_paired": B_post_paired,
        # 增益
        "A_gain": [b - a for a, b in zip(A_pre_paired, A_post_paired)],
        "B_gain": [b - a for a, b in zip(B_pre_paired, B_post_paired)],
    },

    # 五任務完成率（圖 5-3）
    "task_completion": {
        "tasks": ["T1 MAB", "T2 Maze1D", "T3 Maze2D", "T4 Heli", "T5 Fighter"],
        "A_completed": [11, 16, 8, 10, 11],
        "A_total": [26, 26, 18, 18, 18],
        "B_completed": [8, 8, 8, 6, 3],
        "B_total": [15, 15, 12, 12, 12],
        "A_rate": [11/26, 16/26, 8/18, 10/18, 11/18],
        "B_rate": [8/15, 8/15, 8/12, 6/12, 3/12],
    },

    # Section 3 平台回饋（圖 5-4）— 配對樣本為主要分析
    "section3": {
        "items": [
            "3-1 介面易用",
            "3-2 參數信心",
            "3-3 視覺化幫助",
            "3-4 學習動機",
            "3-5 推薦意願",
        ],
        # 全部後測樣本（保留作為對照）
        "A_all": [mean([v["sec3"][i] for v in post_a.values()]) for i in range(5)],
        "B_all": [mean([v["sec3"][i] for v in post_b.values()]) for i in range(5)],
        # 配對樣本
        "A_paired": [mean([v["sec3"][i] for v in A_post_paired_dicts]) for i in range(5)],
        "B_paired": [mean([v["sec3"][i] for v in B_post_paired_dicts]) for i in range(5)],
    },

    # 系統易用性量表（圖 5-5 箱型圖）
    "sus": {
        # 全部後測樣本
        "A_all": [v["sus"] for v in post_a.values()],
        "A_clean": [
            v["sus"] for sid, v in post_a.items()
            if sid not in {s.upper() for s in STRAIGHTLINERS}
        ],
        "B_all": [v["sus"] for v in post_b.values()],
        # 配對樣本（主要分析）
        "A_paired": [v["sus"] for v in A_post_paired_dicts],
        "B_paired": [v["sus"] for v in B_post_paired_dicts],
    },

    # 心智負荷量表（補充）
    "nasa_tlx": {
        "A_all": [mean(v["nasa"]) for v in post_a.values()],
        "B_all": [mean(v["nasa"]) for v in post_b.values()],
        "A_paired": [mean(v["nasa"]) for v in A_post_paired_dicts],
        "B_paired": [mean(v["nasa"]) for v in B_post_paired_dicts],
    },

    # 統計檢定結果（圖表標題用，依 6/10 口委意見之修訂版）
    "stats": {
        # 配對樣本（主要分析）
        "concept_wilcoxon_A": {
            "n": len(A_pre_paired), "W": 3.0, "p": 0.113, "r": 0.647, "sig": "n.s.",
            "pre_M": mean(A_pre_paired), "post_M": mean(A_post_paired),
        },
        "concept_wilcoxon_B": {
            "n": len(B_pre_paired), "W": 5.0, "p": 0.012, "r": 0.756, "sig": "*",
            "pre_M": mean(B_pre_paired), "post_M": mean(B_post_paired),
        },
        "gain_MW_AvsB": {"U": 43.0, "p": 0.268, "r": 0.239, "sig": "n.s."},
        "pretest_MW_AvsB": {"U": 77.0, "p": 0.265, "r": 0.239, "sig": "n.s."},
        # 完成率（卡方 / Fisher exact + Cramer's V）
        "completion_chi2": {
            "T1": {"p": 0.721, "V": 0.056, "sig": "n.s."},
            "T2": {"p": 0.854, "V": 0.029, "sig": "n.s."},
            "T3": {"p": 0.411, "V": 0.150, "sig": "n.s."},
            "T4": {"p": 1.000, "V": 0.000, "sig": "n.s."},
            "T5": {"p": 0.117, "V": 0.286, "sig": "n.s."},
        },
        # SUS（配對 Mann-Whitney U）
        "sus_MW_AvsB": {"U": 37.0, "p": 0.136, "r": 0.323, "sig": "n.s."},
        # Section 3 五題（配對 Mann-Whitney U）
        "sec3_MW": [
            {"U": 49.0, "p": 0.465, "r": 0.155, "sig": "n.s."},   # 3-1
            {"U": 71.0, "p": 0.471, "r": 0.155, "sig": "n.s."},   # 3-2
            {"U": 70.0, "p": 0.494, "r": 0.141, "sig": "n.s."},   # 3-3
            {"U": 71.0, "p": 0.475, "r": 0.155, "sig": "n.s."},   # 3-4
            {"U": 45.0, "p": 0.308, "r": 0.211, "sig": "n.s."},   # 3-5
        ],
    },

    # 描述性元數據
    "meta": {
        "groups": {
            "A": "RR 組（A），配對 n=10",
            "B": "Colab 組（B），配對 n=12",
        },
        "note": "圖表分析依 2026/6/10 口委（吳穎沺、周志岳）意見之修訂版："
                "量表以配對樣本為主，採無母數檢定（Wilcoxon / Mann-Whitney U）"
                "並報告效果量 r；完成率採卡方檢定 + Cramer's V。",
    },
}


def write_js():
    js_content = "// figures/data.js — 由 extract_data.py 自動產生\n"
    js_content += "// 資料來源：C.數據收集/ 四份問卷 CSV；排除測試帳號 S1136103\n"
    js_content += "// 6/10 口委意見後修訂：配對樣本 + 無母數 + effect size\n\n"
    js_content += "window.DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    OUT_FILE.write_text(js_content, encoding="utf-8")
    print(f"✅ 寫入 {OUT_FILE}")
    print(f"   全班 A pre={len(data['concept_test']['A_pre_all'])}, "
          f"post={len(data['concept_test']['A_post_all'])}")
    print(f"   全班 B pre={len(data['concept_test']['B_pre_all'])}, "
          f"post={len(data['concept_test']['B_post_all'])}")
    print(f"   配對：A n={len(data['concept_test']['A_pre_paired'])}, "
          f"B n={len(data['concept_test']['B_pre_paired'])}")
    print(f"   T5 完成率：A={data['task_completion']['A_rate'][4]:.1%} "
          f"vs B={data['task_completion']['B_rate'][4]:.1%}")
    print(f"   配對樣本 Q4 動機：A={data['section3']['A_paired'][3]:.2f} "
          f"vs B={data['section3']['B_paired'][3]:.2f}")
    print(f"   配對樣本 SUS：A M={mean(data['sus']['A_paired']):.2f}, "
          f"B M={mean(data['sus']['B_paired']):.2f}")


if __name__ == "__main__":
    write_js()
