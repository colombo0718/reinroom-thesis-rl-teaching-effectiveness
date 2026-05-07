"""
extract_data.py — 從 C.數據收集/ 的 CSV 抽取所有圖表所需資料，輸出為 figures/data.js

執行：
    cd C:\\Users\\USER\\論文 - RL平台教學成效
    python figures/extract_data.py
"""

import csv
import io
import json
import re
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


def match_pairs(pre, post):
    pairs = []
    for pid, pre_sc in pre.items():
        for poid in post:
            if normalize_id(pid) == normalize_id(poid):
                pairs.append({"pre": pre_sc, "post": post[poid]["score"], "id": poid})
                break
    return pairs


# === 載入四份 CSV ===
pre_a = load_pre("RL Lab — Pre-Test (Group A) (回覆) - 表單回覆 1.csv")
pre_b = load_pre("RL Lab — Pre-Test (Group B) (回覆) - 表單回覆 1.csv")
post_a = load_post("RL Lab — Post-Test (Group A) (回覆) - 表單回覆 1.csv")
post_b = load_post("RL Lab — Post-Test (Group B) (回覆) - 表單回覆 1.csv")

# === 整理為各圖表所需資料 ===
data = {
    # 概念測驗分數（用於圖 5-1 箱型圖）
    "concept_test": {
        "A_pre_all": list(pre_a.values()),
        "A_post_all": [v["score"] for v in post_a.values()],
        "B_pre_all": list(pre_b.values()),
        "B_post_all": [v["score"] for v in post_b.values()],
        "A_paired": match_pairs(pre_a, post_a),
        "B_paired": match_pairs(pre_b, post_b),
    },

    # 五任務完成率（用於圖 5-3）
    "task_completion": {
        "tasks": ["T1 MAB", "T2 Maze1D", "T3 Maze2D", "T4 Heli", "T5 Fighter"],
        "A_completed": [11, 16, 8, 10, 11],
        "A_total": [26, 26, 18, 18, 18],
        "B_completed": [8, 8, 8, 6, 3],
        "B_total": [15, 15, 12, 12, 12],
        "A_rate": [11/26, 16/26, 8/18, 10/18, 11/18],
        "B_rate": [8/15, 8/15, 8/12, 6/12, 3/12],
    },

    # Section 3 平台回饋（用於圖 5-4）
    "section3": {
        "items": [
            "3-1 介面易用",
            "3-2 參數信心",
            "3-3 視覺化幫助",
            "3-4 學習動機",
            "3-5 推薦意願",
        ],
        "A": [
            sum(v["sec3"][i] for v in post_a.values()) / len(post_a)
            for i in range(5)
        ],
        "B": [
            sum(v["sec3"][i] for v in post_b.values()) / len(post_b)
            for i in range(5)
        ],
    },

    # SUS 易用性（用於圖 5-5 箱型圖 + 平均條）
    "sus": {
        "A_all": [v["sus"] for v in post_a.values()],
        "A_clean": [
            v["sus"] for sid, v in post_a.items()
            if sid not in {s.upper() for s in STRAIGHTLINERS}
        ],
        "B": [v["sus"] for v in post_b.values()],
    },

    # NASA-TLX 心智負荷（用於圖 5-5 補充）
    "nasa_tlx": {
        "A_all": [sum(v["nasa"]) / 6 for v in post_a.values()],
        "B": [sum(v["nasa"]) / 6 for v in post_b.values()],
    },

    # 統計檢定結果（圖表標題用）
    "stats": {
        "concept_paired_A": {"t": 1.170, "p": 0.28, "sig": "n.s.", "n": 10,
                             "pre_M": 5.60, "post_M": 6.70, "gain": 1.10},
        "concept_paired_B": {"t": 3.086, "p": 0.01, "sig": "*", "n": 12,
                             "pre_M": 5.00, "post_M": 6.92, "gain": 1.92},
        "concept_class_A": {"t": 1.116, "p": 0.27, "sig": "n.s.",
                            "pre_M": 5.54, "post_M": 6.22, "gain": 0.68},
        "concept_class_B": {"t": 3.344, "p": 0.003, "sig": "**",
                            "pre_M": 4.87, "post_M": 6.92, "gain": 2.05},
        "gain_AvsB": {"t": -1.642, "p": 0.12, "sig": "n.s."},
        "sus_AvsB": {"t": -2.188, "p": 0.037, "sig": "*"},
        "sec3_4_motivation_AvsB": {"t": 1.761, "p": 0.089, "sig": "n.s.（趨近顯著）"},
    },

    # 描述性元數據
    "meta": {
        "groups": {
            "A": "實驗組（RL Lab，大二，n=18 後測）",
            "B": "對照組（Colab，碩一，n=12 後測）",
        },
    },
}


def write_js():
    js_content = "// figures/data.js — 由 extract_data.py 自動產生\n"
    js_content += "// 資料來源：C.數據收集/ 四份問卷 CSV\n"
    js_content += "// 排除測試帳號 S1136103\n\n"
    js_content += "window.DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    OUT_FILE.write_text(js_content, encoding="utf-8")
    print(f"✅ 寫入 {OUT_FILE}")
    print(f"   - concept_test: A 班全 n={len(data['concept_test']['A_pre_all'])} pre, n={len(data['concept_test']['A_post_all'])} post")
    print(f"   - concept_test: B 班全 n={len(data['concept_test']['B_pre_all'])} pre, n={len(data['concept_test']['B_post_all'])} post")
    print(f"   - 配對：A n={len(data['concept_test']['A_paired'])}, B n={len(data['concept_test']['B_paired'])}")
    print(f"   - task_completion: T5 A={data['task_completion']['A_rate'][4]:.0%} vs B={data['task_completion']['B_rate'][4]:.0%}")


if __name__ == "__main__":
    write_js()
