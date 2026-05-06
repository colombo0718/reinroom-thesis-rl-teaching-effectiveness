import csv
import os
from scipy import stats
import numpy as np

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_ID = "S1136103"
STRAIGHTLINERS_A = {"1123505", "DH10"}

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
            nasa_keys  = get_section_keys(row, "4-")
            sus_keys   = get_section_keys(row, "5-")
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

def match_pairs(pre, post):
    pairs = []
    for pid, pre_sc in pre.items():
        for poid, pdata in post.items():
            if normalize_id(pid) == normalize_id(poid):
                pairs.append((pre_sc, pdata["score"]))
                break
    return pairs

def matched_post_ids(pre, post):
    ids = []
    for pid in pre:
        for poid in post:
            if normalize_id(pid) == normalize_id(poid):
                ids.append(poid)
                break
    return ids

pre_a  = load_pre("RL Lab — Pre-Test (Group A) (回覆) - 表單回覆 1.csv")
pre_b  = load_pre("RL Lab — Pre-Test (Group B) (回覆) - 表單回覆 1.csv")
post_a = load_post("RL Lab — Post-Test (Group A) (回覆) - 表單回覆 1.csv", STRAIGHTLINERS_A)
post_b = load_post("RL Lab — Post-Test (Group B) (回覆) - 表單回覆 1.csv")

pairs_a = match_pairs(pre_a, post_a)
pairs_b = match_pairs(pre_b, post_b)

gains_a = [post - pre for pre, post in pairs_a]
gains_b = [post - pre for pre, post in pairs_b]
pre_a_v  = [p[0] for p in pairs_a]; post_a_v = [p[1] for p in pairs_a]
pre_b_v  = [p[0] for p in pairs_b]; post_b_v = [p[1] for p in pairs_b]

sus_a_all   = [calc_sus(v["sus"]) for v in post_a.values()]
sus_a_clean = [calc_sus(v["sus"]) for v in post_a.values() if not v["sl"]]
sus_b       = [calc_sus(v["sus"]) for v in post_b.values()]

nasa_a_all   = [np.mean(v["nasa"]) for v in post_a.values()]
nasa_a_clean = [np.mean(v["nasa"]) for v in post_a.values() if not v["sl"]]
nasa_b       = [np.mean(v["nasa"]) for v in post_b.values()]

sec3_a = [np.mean(v["sec3"]) for v in post_a.values()]
sec3_b = [np.mean(v["sec3"]) for v in post_b.values()]
mot_a  = [v["sec3"][3] for v in post_a.values()]
mot_b  = [v["sec3"][3] for v in post_b.values()]
par_a  = [v["sec3"][1] for v in post_a.values()]
par_b  = [v["sec3"][1] for v in post_b.values()]
vis_a  = [v["sec3"][2] for v in post_a.values()]
vis_b  = [v["sec3"][2] for v in post_b.values()]

post_a_all = [v["score"] for v in post_a.values()]
post_b_all = [v["score"] for v in post_b.values()]

def row(label, t, p, n1, n2=None):
    sig = "***" if p<0.001 else "**" if p<0.01 else "*" if p<0.05 else "n.s."
    n = f"n={n1}" if n2 is None else f"n={n1},{n2}"
    print(f"  {label:<42} t={t:+.3f}  p={p:.4f}  {sig}  ({n})")

sep = "=" * 72

print(sep)
print("1. 組內配對 t-test（前後測）")
print(sep)
t,p = stats.ttest_rel(post_a_v, pre_a_v); row("Group A  pre→post", t, p, len(pairs_a))
t,p = stats.ttest_rel(post_b_v, pre_b_v); row("Group B  pre→post", t, p, len(pairs_b))

print(f"\n{sep}")
print("2. 組間 t-test：Gain Score")
print(sep)
t,p = stats.ttest_ind(gains_a, gains_b); row("Gain A vs B", t, p, len(gains_a), len(gains_b))

print(f"\n{sep}")
print("3. 組間 t-test：後測分數（全部）")
print(sep)
t,p = stats.ttest_ind(post_a_all, post_b_all); row("Post-test A vs B", t, p, len(post_a_all), len(post_b_all))

print(f"\n{sep}")
print("4. 組間 t-test：SUS 易用性")
print(sep)
t,p = stats.ttest_ind(sus_a_all, sus_b);   row("SUS  A(all) vs B",          t, p, len(sus_a_all), len(sus_b))
t,p = stats.ttest_ind(sus_a_clean, sus_b); row("SUS  A(excl.straightliner) vs B", t, p, len(sus_a_clean), len(sus_b))

print(f"\n{sep}")
print("5. 組間 t-test：NASA-TLX")
print(sep)
t,p = stats.ttest_ind(nasa_a_all, nasa_b);   row("NASA-TLX  A(all) vs B",   t, p, len(nasa_a_all), len(nasa_b))
t,p = stats.ttest_ind(nasa_a_clean, nasa_b); row("NASA-TLX  A(excl.) vs B", t, p, len(nasa_a_clean), len(nasa_b))

print(f"\n{sep}")
print("6. 組間 t-test：Section 3 分項")
print(sep)
t,p = stats.ttest_ind(sec3_a, sec3_b); row("Sec3 整體 A vs B",          t, p, len(sec3_a), len(sec3_b))
t,p = stats.ttest_ind(par_a,  par_b);  row("Sec3-2 參數信心 A vs B",    t, p, len(par_a),  len(par_b))
t,p = stats.ttest_ind(vis_a,  vis_b);  row("Sec3-3 視覺化理解 A vs B",  t, p, len(vis_a),  len(vis_b))
t,p = stats.ttest_ind(mot_a,  mot_b);  row("Sec3-4 學習動機 A vs B",    t, p, len(mot_a),  len(mot_b))

print(f"\n{sep}")
print("描述統計摘要")
print(sep)
print(f"  Gain A:  M={np.mean(gains_a):.2f}  SD={np.std(gains_a,ddof=1):.2f}  n={len(gains_a)}")
print(f"  Gain B:  M={np.mean(gains_b):.2f}  SD={np.std(gains_b,ddof=1):.2f}  n={len(gains_b)}")
print(f"  SUS A(all):   M={np.mean(sus_a_all):.1f}  SD={np.std(sus_a_all,ddof=1):.1f}  n={len(sus_a_all)}")
print(f"  SUS A(clean): M={np.mean(sus_a_clean):.1f}  SD={np.std(sus_a_clean,ddof=1):.1f}  n={len(sus_a_clean)}")
print(f"  SUS B:        M={np.mean(sus_b):.1f}  SD={np.std(sus_b,ddof=1):.1f}  n={len(sus_b)}")
print(f"  NASA A(all):  M={np.mean(nasa_a_all):.2f}  SD={np.std(nasa_a_all,ddof=1):.2f}  n={len(nasa_a_all)}")
print(f"  NASA A(clean):M={np.mean(nasa_a_clean):.2f}  SD={np.std(nasa_a_clean,ddof=1):.2f}  n={len(nasa_a_clean)}")
print(f"  NASA B:       M={np.mean(nasa_b):.2f}  SD={np.std(nasa_b,ddof=1):.2f}  n={len(nasa_b)}")
print(f"  Sec3-4 A: M={np.mean(mot_a):.2f}  SD={np.std(mot_a,ddof=1):.2f}")
print(f"  Sec3-4 B: M={np.mean(mot_b):.2f}  SD={np.std(mot_b,ddof=1):.2f}")


# ============================================================
# 只看配對樣本（前後測都有作答的人）
# ============================================================
print(f"\n{sep}")
print("7. 配對樣本限定分析（A 縮小至前後測都做的人）")
print(sep)

matched_a_ids = matched_post_ids(pre_a, post_a)
matched_b_ids = matched_post_ids(pre_b, post_b)

post_a_m = {sid: post_a[sid] for sid in matched_a_ids}
post_b_m = {sid: post_b[sid] for sid in matched_b_ids}

sus_a_m  = [calc_sus(v["sus"]) for v in post_a_m.values()]
nasa_a_m = [np.mean(v["nasa"]) for v in post_a_m.values()]
sec3_a_m = [np.mean(v["sec3"]) for v in post_a_m.values()]
mot_a_m  = [v["sec3"][3] for v in post_a_m.values()]
par_a_m  = [v["sec3"][1] for v in post_a_m.values()]
vis_a_m  = [v["sec3"][2] for v in post_a_m.values()]

t,p = stats.ttest_ind(sus_a_m, sus_b);   row("SUS  A(matched) vs B(matched)",   t, p, len(sus_a_m), len(sus_b))
t,p = stats.ttest_ind(nasa_a_m, nasa_b); row("NASA A(matched) vs B(matched)",   t, p, len(nasa_a_m), len(nasa_b))
t,p = stats.ttest_ind(sec3_a_m, sec3_b); row("Sec3 整體 A(matched) vs B",      t, p, len(sec3_a_m), len(sec3_b))
t,p = stats.ttest_ind(par_a_m,  par_b);  row("Sec3-2 參數信心 A(matched) vs B", t, p, len(par_a_m),  len(par_b))
t,p = stats.ttest_ind(vis_a_m,  vis_b);  row("Sec3-3 視覺化 A(matched) vs B",   t, p, len(vis_a_m),  len(vis_b))
t,p = stats.ttest_ind(mot_a_m,  mot_b);  row("Sec3-4 動機 A(matched) vs B",     t, p, len(mot_a_m),  len(mot_b))

print()
print(f"  SUS A(matched):     M={np.mean(sus_a_m):.1f}  SD={np.std(sus_a_m,ddof=1):.1f}  n={len(sus_a_m)}")
print(f"  NASA A(matched):    M={np.mean(nasa_a_m):.2f}  SD={np.std(nasa_a_m,ddof=1):.2f}  n={len(nasa_a_m)}")
print(f"  Sec3 整體 A(m): M={np.mean(sec3_a_m):.2f}  Sec3-2 A(m): M={np.mean(par_a_m):.2f}  Sec3-3 A(m): M={np.mean(vis_a_m):.2f}  Sec3-4 A(m): M={np.mean(mot_a_m):.2f}")
print(f"  配對 A 學生 ID（n={len(matched_a_ids)}）：{matched_a_ids}")
print(f"  配對 B 學生 ID（n={len(matched_b_ids)}）：{matched_b_ids}")


# ============================================================
# 班級整體比較（不要求個人配對，獨立樣本 t-test）
# ============================================================
print(f"\n{sep}")
print("8. 班級整體前後測比較（獨立樣本 t-test）")
print(sep)

pre_a_all  = list(pre_a.values())
pre_b_all  = list(pre_b.values())

t,p = stats.ttest_ind(post_a_all, pre_a_all)
row("Group A  班級整體 pre vs post", t, p, len(pre_a_all), len(post_a_all))
t,p = stats.ttest_ind(post_b_all, pre_b_all)
row("Group B  班級整體 pre vs post", t, p, len(pre_b_all), len(post_b_all))

print()
print(f"  Group A pre  (n={len(pre_a_all)}):  M={np.mean(pre_a_all):.2f}  SD={np.std(pre_a_all,ddof=1):.2f}")
print(f"  Group A post (n={len(post_a_all)}):  M={np.mean(post_a_all):.2f}  SD={np.std(post_a_all,ddof=1):.2f}")
print(f"  Group B pre  (n={len(pre_b_all)}):  M={np.mean(pre_b_all):.2f}  SD={np.std(pre_b_all,ddof=1):.2f}")
print(f"  Group B post (n={len(post_b_all)}):  M={np.mean(post_b_all):.2f}  SD={np.std(post_b_all,ddof=1):.2f}")
