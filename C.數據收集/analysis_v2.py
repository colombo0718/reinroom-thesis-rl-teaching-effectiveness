"""analysis_v2.py — 對齊 6/10 口委（吳穎沺、周志岳）意見之重新分析

吳老師明確要求：
1. 樣本限定為「兩天都到、能配對」之有效樣本：RR n=10、Colab n=12
2. n<30 改用無母數檢定（Wilcoxon、Mann-Whitney U）
3. 加 effect size（r）讓人判斷實際差距大小
4. 沒顯著就是沒顯著，不要用「勝出」這類字眼

原 analysis.py 保留不動作為對照。
"""
import csv
import os
import math
import numpy as np
from scipy import stats

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_ID = "S1136103"
STRAIGHTLINERS_A = {"1123505", "DH10"}


# ────── 資料載入（同 analysis.py） ──────────────────────────────────────

def parse_score(s):
    return int(s.split("/")[0].strip())

def get_section_keys(row, prefix):
    keys = [k for k in row if k.startswith(prefix)]
    return sorted(keys, key=lambda k: int(k.split(".")[0].split("-")[1]))

def calc_sus(items):
    odd  = [items[i] - 1 for i in [0, 2, 4, 6, 8]]
    even = [5 - items[i] for i in [1, 3, 5, 7, 9]]
    return sum(odd + even) * 2.5

def load_pre(filename):
    students = {}
    with open(os.path.join(DATA_DIR, filename), encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            sid = row["Student ID"].strip().upper()
            if sid == TEST_ID:
                continue
            students[sid] = parse_score(row["分數"])
    return students

def load_post(filename, straightliners=None):
    students = {}
    with open(os.path.join(DATA_DIR, filename), encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            sid = row["Student ID"].strip().upper()
            if sid == TEST_ID:
                continue
            sec3_keys = get_section_keys(row, "3-")
            nasa_keys = get_section_keys(row, "4-")
            sus_keys  = get_section_keys(row, "5-")
            students[sid] = {
                "score": parse_score(row["分數"]),
                "sec3":  [int(row[k]) for k in sec3_keys],
                "nasa":  [int(row[k]) for k in nasa_keys],
                "sus":   [int(row[k]) for k in sus_keys],
                "sl":    straightliners and sid in {s.upper() for s in straightliners},
            }
    return students

def normalize_id(s):
    return s.lstrip("S").replace("-", "").replace(" ", "")

def matched_pairs_full(pre, post):
    """回傳配對成功之 (sid, pre_score, post_score, post_dict)"""
    pairs = []
    for pid, pre_sc in pre.items():
        for poid, pdata in post.items():
            if normalize_id(pid) == normalize_id(poid):
                pairs.append((poid, pre_sc, pdata["score"], pdata))
                break
    return pairs


# ────── 統計工具：無母數檢定 + effect size ──────────────────────────────

def sig_star(p):
    if p < 0.001: return "***"
    if p < 0.01:  return "**"
    if p < 0.05:  return "*"
    if p < 0.10:  return "†"
    return "n.s."

def wilcoxon_r(x, y):
    """配對樣本 Wilcoxon signed-rank + r = |Z| / sqrt(N)
    回傳 (W, p, r, n_pairs, interp)
    """
    n = len(x)
    diffs = [b - a for a, b in zip(x, y)]
    nz = sum(1 for d in diffs if d != 0)
    if nz < 2:
        return None, None, None, n, "樣本不足"
    try:
        res = stats.wilcoxon(x, y, method='approx')
        W = res.statistic
        p = res.pvalue
        z = res.zstatistic if hasattr(res, 'zstatistic') else None
        if z is None:
            # 退而求其次：用 W 反推 z
            mean_w = nz * (nz + 1) / 4
            sd_w   = math.sqrt(nz * (nz + 1) * (2 * nz + 1) / 24)
            z = (W - mean_w) / sd_w if sd_w > 0 else 0
        r = abs(z) / math.sqrt(nz)  # 用 nz 而非 n (去除 tie pairs)
        interp = "小" if r < 0.3 else "中" if r < 0.5 else "大"
        return W, p, r, nz, interp
    except Exception as e:
        return None, None, None, n, str(e)

def mannwhitney_r(x, y):
    """獨立樣本 Mann-Whitney U + r = |Z| / sqrt(N1+N2)
    回傳 (U, p, r, n1, n2, interp)
    """
    n1, n2 = len(x), len(y)
    try:
        res = stats.mannwhitneyu(x, y, method='asymptotic', alternative='two-sided')
        U = res.statistic
        p = res.pvalue
        # 計算 Z
        mean_u = n1 * n2 / 2
        sd_u   = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
        z = (U - mean_u) / sd_u if sd_u > 0 else 0
        r = abs(z) / math.sqrt(n1 + n2)
        interp = "小" if r < 0.3 else "中" if r < 0.5 else "大"
        return U, p, r, n1, n2, interp
    except Exception as e:
        return None, None, None, n1, n2, str(e)


# ────── 載入資料 ───────────────────────────────────────────────────

pre_a  = load_pre("RL Lab — Pre-Test (Group A) (回覆) - 表單回覆 1.csv")
pre_b  = load_pre("RL Lab — Pre-Test (Group B) (回覆) - 表單回覆 1.csv")
post_a = load_post("RL Lab — Post-Test (Group A) (回覆) - 表單回覆 1.csv", STRAIGHTLINERS_A)
post_b = load_post("RL Lab — Post-Test (Group B) (回覆) - 表單回覆 1.csv")

# 配對樣本：兩天都到、能配對
pairs_a = matched_pairs_full(pre_a, post_a)   # n=10
pairs_b = matched_pairs_full(pre_b, post_b)   # n=12

print("═" * 75)
print(f"資料載入摘要")
print("═" * 75)
print(f"  RR 組（A）：前測 {len(pre_a)} 人、後測 {len(post_a)} 人、可配對 {len(pairs_a)} 人")
print(f"  Colab 組（B）：前測 {len(pre_b)} 人、後測 {len(post_b)} 人、可配對 {len(pairs_b)} 人")
print()
print(f"  本次分析依吳老師意見：限定可配對樣本")
print(f"  → RR 組 n={len(pairs_a)}, Colab 組 n={len(pairs_b)}")
print()

# 抽出配對樣本的分數與後測量表資料
pre_a_v  = [p[1] for p in pairs_a]
post_a_v = [p[2] for p in pairs_a]
pre_b_v  = [p[1] for p in pairs_b]
post_b_v = [p[2] for p in pairs_b]

post_a_dicts = [p[3] for p in pairs_a]
post_b_dicts = [p[3] for p in pairs_b]

sus_a  = [calc_sus(v["sus"]) for v in post_a_dicts]
sus_b  = [calc_sus(v["sus"]) for v in post_b_dicts]
nasa_a_byq = [v["nasa"] for v in post_a_dicts]  # 6 個分項
nasa_b_byq = [v["nasa"] for v in post_b_dicts]
sec3_a_byq = [v["sec3"] for v in post_a_dicts]  # 5 題
sec3_b_byq = [v["sec3"] for v in post_b_dicts]

gains_a = [b - a for a, b in zip(pre_a_v, post_a_v)]
gains_b = [b - a for a, b in zip(pre_b_v, post_b_v)]


# ────── 結果輸出 helper ────────────────────────────────────────────

def hr(title, width=75):
    print()
    print("═" * width)
    print(title)
    print("═" * width)

def print_within(label, x, y):
    """組內前後測 Wilcoxon"""
    W, p, r, n, interp = wilcoxon_r(x, y)
    if W is None:
        print(f"  {label}: {interp}")
        return
    star = sig_star(p)
    mean_x, mean_y = np.mean(x), np.mean(y)
    md_x, md_y = np.median(x), np.median(y)
    print(f"  {label}")
    print(f"    pre  M={mean_x:.2f} Mdn={md_x:.1f}  → post M={mean_y:.2f} Mdn={md_y:.1f}")
    print(f"    Wilcoxon W={W:.1f}, p={p:.4f} {star}, r={r:.3f}（效果量{interp}）, n={n} 配對")

def print_between(label, x, y, low_better=False):
    """組間 Mann-Whitney U"""
    U, p, r, n1, n2, interp = mannwhitney_r(x, y)
    if U is None:
        print(f"  {label}: {interp}")
        return
    star = sig_star(p)
    print(f"  {label}")
    print(f"    A: M={np.mean(x):.2f} SD={np.std(x,ddof=1):.2f} Mdn={np.median(x):.2f} (n={n1})")
    print(f"    B: M={np.mean(y):.2f} SD={np.std(y,ddof=1):.2f} Mdn={np.median(y):.2f} (n={n2})")
    print(f"    Mann-Whitney U={U:.1f}, p={p:.4f} {star}, r={r:.3f}（效果量{interp}）")

def chi2_completion(succ_a, n_a, succ_b, n_b, label):
    """完成率：卡方 + Cramer's V"""
    fail_a, fail_b = n_a - succ_a, n_b - succ_b
    table = np.array([[succ_a, fail_a], [succ_b, fail_b]])
    try:
        chi2, p, dof, exp = stats.chi2_contingency(table)
        n_total = n_a + n_b
        # Cramer's V for 2x2
        v = math.sqrt(chi2 / n_total)
        # 若期望次數有 <5 改用 Fisher
        use_fisher = (exp < 5).any()
        if use_fisher:
            _, p_fisher = stats.fisher_exact(table)
            p = p_fisher
    except Exception as e:
        print(f"  {label}: {e}")
        return
    star = sig_star(p)
    method = "Fisher's exact" if use_fisher else "Chi-square"
    print(f"  {label}")
    print(f"    A: {succ_a}/{n_a} = {succ_a/n_a*100:.1f}%   B: {succ_b}/{n_b} = {succ_b/n_b*100:.1f}%")
    print(f"    {method}: p={p:.4f} {star}, Cramer's V={v:.3f}")


# ────── 分析開始 ────────────────────────────────────────────────────

hr("1. 前測同質性檢驗（兩組起點是否可比）")
print_between("前測分數 A vs B", pre_a_v, pre_b_v)

hr("2. 組內前後測比較（Wilcoxon signed-rank）")
print_within("RR 組（A）前 → 後", pre_a_v, post_a_v)
print()
print_within("Colab 組（B）前 → 後", pre_b_v, post_b_v)

hr("3. 組間 Gain Score 比較（Mann-Whitney U）")
print_between("Gain (post-pre) A vs B", gains_a, gains_b)

hr("4. 系統易用性量表 (SUS)")
print_between("SUS A vs B", sus_a, sus_b)

hr("5. 心智負荷量表（NASA-TLX）整體與各分項")
nasa_labels = ["心智需求", "體力需求", "時間壓力", "努力", "挫折感", "表現"]
nasa_a_overall = [np.mean(v) for v in nasa_a_byq]
nasa_b_overall = [np.mean(v) for v in nasa_b_byq]
print_between("心智負荷量表 整體 A vs B", nasa_a_overall, nasa_b_overall)
print()
for i, name in enumerate(nasa_labels):
    a_i = [v[i] for v in nasa_a_byq]
    b_i = [v[i] for v in nasa_b_byq]
    print_between(f"NASA-{i+1} {name} A vs B", a_i, b_i)
    print()

hr("6. 平台回饋量表（Section 3 五題）")
sec3_labels = ["介面易用", "參數信心", "視覺化幫助", "課後學習動機", "推薦意願"]
sec3_a_overall = [np.mean(v) for v in sec3_a_byq]
sec3_b_overall = [np.mean(v) for v in sec3_b_byq]
print_between("Sec3 整體 A vs B", sec3_a_overall, sec3_b_overall)
print()
for i, name in enumerate(sec3_labels):
    a_i = [v[i] for v in sec3_a_byq]
    b_i = [v[i] for v in sec3_b_byq]
    print_between(f"Q{i+1} {name} A vs B", a_i, b_i)
    print()

hr("7. 任務完成率（卡方 + Cramer's V）")
# T4 Heli, T5 Fighter 完成率
# 注意：完成率原資料記錄全班 18 / 12，但分析應用配對樣本
# 這裡先用論文原本記錄的 n=18 vs 12 → 待覆核後改為配對樣本
print("  ⚠ 完成率原使用全班樣本 (n_A=18, n_B=12)，需覆核完成記錄是否能對應配對樣本後再重跑")
print()
# 範例（依原數據估算配對樣本完成率，待人工覆核）
# T4: A 56% × 18 ≈ 10, B 50% × 12 = 6
# T5: A 61% × 18 ≈ 11, B 25% × 12 = 3
print("  以下為「假設配對樣本完成率與全班一致」的估算（需覆核）：")
chi2_completion(succ_a=int(round(0.556 * 10)), n_a=10, succ_b=int(round(0.500 * 12)), n_b=12, label="T4 Heli")
print()
chi2_completion(succ_a=int(round(0.611 * 10)), n_a=10, succ_b=int(round(0.250 * 12)), n_b=12, label="T5 Fighter")

hr("8. 對照組：t 檢定結果（吳老師建議改無母數，此處保留作對比）")
t, p = stats.ttest_rel(pre_a_v, post_a_v)
print(f"  A 配對 t（n=10）：t={t:+.3f}, p={p:.4f}  {sig_star(p)}")
t, p = stats.ttest_rel(pre_b_v, post_b_v)
print(f"  B 配對 t（n=12）：t={t:+.3f}, p={p:.4f}  {sig_star(p)}")
t, p = stats.ttest_ind(gains_a, gains_b, equal_var=False)
print(f"  Gain Welch t：t={t:+.3f}, p={p:.4f}  {sig_star(p)}")

hr("9. 配對樣本 Student ID 清單")
print("  RR 組（A）配對 ID：")
for sid, pre, post, _ in pairs_a:
    print(f"    {sid}  pre={pre}, post={post}, gain={post-pre:+d}")
print()
print("  Colab 組（B）配對 ID：")
for sid, pre, post, _ in pairs_b:
    print(f"    {sid}  pre={pre}, post={post}, gain={post-pre:+d}")
