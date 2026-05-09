#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nasa_tlx_breakdown.py — NASA-TLX 6 項分量表 t-test

從後測 CSV 讀 NASA-TLX 6 題（Section 4: 4-1~4-6），對 RR vs Colab 做獨立樣本 t-test。

NASA-TLX 6 項：
1. Mental Demand 心智需求
2. Physical Demand 體力需求
3. Temporal Demand 時間壓力
4. Performance 表現自評（反向）
5. Effort 努力
6. Frustration 挫折感
"""

import csv
import os
from scipy import stats
import numpy as np

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_ID = "S1136103"
STRAIGHTLINERS_A = {"1123505", "DH10"}

DIMS = ["心智需求", "體力需求", "時間壓力", "表現自評", "努力", "挫折感"]


def load_nasa(filename, straightliners=None):
    """回傳 list of (sid, [6 項分數], is_straightline)"""
    rows = []
    with open(os.path.join(DATA_DIR, filename), encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            sid = row["Student ID"].strip().upper()
            if sid == TEST_ID:
                continue
            keys = sorted([k for k in row if k.startswith("4-")],
                          key=lambda k: int(k.split(".")[0].split("-")[1]))
            scores = [int(row[k]) for k in keys]
            sl = straightliners and (sid in {s.upper() for s in straightliners})
            rows.append((sid, scores, sl))
    return rows


def main():
    a = load_nasa("RL Lab — Post-Test (Group A) (回覆) - 表單回覆 1.csv", STRAIGHTLINERS_A)
    b = load_nasa("RL Lab — Post-Test (Group B) (回覆) - 表單回覆 1.csv")

    print(f"RR (A) n = {len(a)}, 排除直線式後 n = {sum(1 for r in a if not r[2])}")
    print(f"Colab (B) n = {len(b)}\n")

    # 整體平均
    a_overall_all = [np.mean(r[1]) for r in a]
    a_overall_clean = [np.mean(r[1]) for r in a if not r[2]]
    b_overall = [np.mean(r[1]) for r in b]

    t_all, p_all = stats.ttest_ind(a_overall_all, b_overall, equal_var=False)
    t_clean, p_clean = stats.ttest_ind(a_overall_clean, b_overall, equal_var=False)

    print(f"整體平均  RR(全部, n={len(a_overall_all)})  M={np.mean(a_overall_all):.2f} SD={np.std(a_overall_all, ddof=1):.2f}")
    print(f"整體平均  RR(排除直線, n={len(a_overall_clean)})  M={np.mean(a_overall_clean):.2f} SD={np.std(a_overall_clean, ddof=1):.2f}")
    print(f"整體平均  Colab(n={len(b_overall)})  M={np.mean(b_overall):.2f} SD={np.std(b_overall, ddof=1):.2f}")
    print(f"  t(全部 vs Colab) = {t_all:+.3f}, p = {p_all:.3f}")
    print(f"  t(排除直線 vs Colab) = {t_clean:+.3f}, p = {p_clean:.3f}\n")

    # 6 項分項
    print("=" * 90)
    print(f"{'分項':<12}{'RR M(SD)':<18}{'RR排除 M(SD)':<18}{'Colab M(SD)':<18}{'t (全部)':<12}{'p':<10}{'sig'}")
    print("=" * 90)

    rows_md = []
    for i, dim in enumerate(DIMS):
        a_all = [r[1][i] for r in a]
        a_clean = [r[1][i] for r in a if not r[2]]
        b_v = [r[1][i] for r in b]

        a_m, a_sd = np.mean(a_all), np.std(a_all, ddof=1)
        a_cm, a_csd = np.mean(a_clean), np.std(a_clean, ddof=1)
        b_m, b_sd = np.mean(b_v), np.std(b_v, ddof=1)

        t, p = stats.ttest_ind(a_all, b_v, equal_var=False)
        sig = '***' if p < .001 else '**' if p < .01 else '*' if p < .05 else 'n.s.'

        print(f"{dim:<10}  {a_m:.2f}({a_sd:.2f})    {a_cm:.2f}({a_csd:.2f})    {b_m:.2f}({b_sd:.2f})    {t:+.3f}     {p:.3f}    {sig}")

        rows_md.append((dim, a_m, a_sd, a_cm, a_csd, b_m, b_sd, t, p, sig))

    # Markdown 表
    print("\n\n## Markdown 合併表（整體 + 6 項分項）\n")
    print("| 構面 | RR 全部 (n=18) M (SD) | RR 排除直線 (n=16) M (SD) | Colab (n=12) M (SD) | t（全部 vs Colab）| p | 顯著性 |")
    print("|------|--------------------|---------------------------|---------------------|------|---|--------|")
    print(f"| **整體平均** | {np.mean(a_overall_all):.2f} ({np.std(a_overall_all, ddof=1):.2f}) | {np.mean(a_overall_clean):.2f} ({np.std(a_overall_clean, ddof=1):.2f}) | {np.mean(b_overall):.2f} ({np.std(b_overall, ddof=1):.2f}) | {t_all:+.3f} | {p_all:.3f} | {'\\*'*(1 if p_all<.05 else 0) if p_all<.05 else 'n.s.'} |")
    for row in rows_md:
        dim, a_m, a_sd, a_cm, a_csd, b_m, b_sd, t, p, sig = row
        sig_md = '\\*\\*\\*' if p < .001 else '\\*\\*' if p < .01 else '\\*' if p < .05 else 'n.s.'
        print(f"| {dim} | {a_m:.2f} ({a_sd:.2f}) | {a_cm:.2f} ({a_csd:.2f}) | {b_m:.2f} ({b_sd:.2f}) | {t:+.3f} | {p:.3f} | {sig_md} |")


if __name__ == '__main__':
    main()
