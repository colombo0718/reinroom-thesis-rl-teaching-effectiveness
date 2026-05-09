#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unify_terminology.py — 批次統一論文用詞

依 5/9 老師會議要求 + 4.1 命名宣告：
  - 平台名稱舊稱：RL Lab → RR
  - 視覺化用詞：可視化 → 視覺化、圖形化互動 → 視覺化互動
  - 組別命名：實驗組 → RR 組、對照組 → Colab 組
  - Group A/B → (A)/(B)（已少用，保險處理）

只動 md/ 內論文檔，不動程式碼路徑、變數名、檔名。

執行：
  python unify_terminology.py --dry-run    # 預覽
  python unify_terminology.py              # 實際寫入
"""

import re
import sys
from pathlib import Path

MD_DIR = Path(__file__).parent / "md"

# 替換規則 (按執行順序，注意先後關係)
RULES = [
    # 平台舊稱清除
    (r'\bRL Lab\b',     'RR'),
    (r'\bRL lab\b',     'RR'),
    (r'\bRL_Lab\b',     'RR'),
    (r'\bRLLab\b',      'RR'),

    # 視覺化用詞
    ('可視化',           '視覺化'),
    ('圖形化互動',        '視覺化互動'),
    ('圖形化介面',        '視覺化介面'),
    ('圖像化呈現',        '視覺化呈現'),

    # 組別命名（小心：先改長詞、再改短詞）
    ('實驗組學生',        'RR 組學生'),
    ('對照組學生',        'Colab 組學生'),
    ('實驗組（A）',       'RR 組（A）'),
    ('對照組（B）',       'Colab 組（B）'),
    ('實驗組（Group A）', 'RR 組（A）'),
    ('對照組（Group B）', 'Colab 組（B）'),
    ('實驗組（A 組）',    'RR 組（A）'),
    ('對照組（B 組）',    'Colab 組（B）'),
    ('實驗組 A',         'RR 組（A）'),
    ('對照組 B',         'Colab 組（B）'),
    ('A 組（實驗組）',    'RR 組（A）'),
    ('B 組（對照組）',    'Colab 組（B）'),
    ('Group A',          'A 組'),
    ('Group B',          'B 組'),

    # 一般「實驗組」「對照組」單獨出現 → 替換
    # （「準實驗設計」「兩組前後測準實驗設計」「實驗設計」不含「實驗組」三字，安全）
    ('實驗組',           'RR 組'),
    ('對照組',           'Colab 組'),
]

# 內容保全：strip structural markers, then count chars
def content_signature(text):
    """剝結構標記與替換目標，留下純內容字元供比對。"""
    s = text
    # 剝 # 標記
    s = re.sub(r'^#{1,6}\s+', '', s, flags=re.MULTILINE)
    # 剝 ** **
    s = s.replace('**', '')
    # 剝 RR / RL Lab / 實驗組 / 對照組 / 可視化 / 視覺化 / 圖形化 / 圖像化 / Group / A 組 / B 組 / Colab
    for token in ['RL Lab', 'RR', '實驗組', '對照組', 'Colab', '可視化', '視覺化', '圖形化', '圖像化', 'Group', 'A 組', 'B 組']:
        s = s.replace(token, '')
    # 剝空白
    s = re.sub(r'\s+', '', s)
    return s


def transform(text):
    new_text = text
    in_code = False
    out_lines = []
    for line in new_text.splitlines(keepends=True):
        if line.lstrip().startswith('```'):
            in_code = not in_code
            out_lines.append(line)
            continue
        if in_code:
            out_lines.append(line)
            continue
        # 對 line 套用所有規則
        new_line = line
        for pat, repl in RULES:
            if pat.startswith('\\b') or '\\' in pat:
                new_line = re.sub(pat, repl, new_line)
            else:
                new_line = new_line.replace(pat, repl)
        out_lines.append(new_line)
    return ''.join(out_lines)


def main():
    dry_run = '--dry-run' in sys.argv
    files = sorted(MD_DIR.glob('*.md'))
    total = 0
    failed_preserve = []

    for f in files:
        original = f.read_text(encoding='utf-8')
        migrated = transform(original)
        if original == migrated:
            continue

        # 計算變化量
        diffs = sum(1 for a, b in zip(original.splitlines(), migrated.splitlines()) if a != b)
        total += diffs
        print(f'✓ {f.name}  ({diffs} 行受影響)')

        if not dry_run:
            f.write_text(migrated, encoding='utf-8')

    print(f'\n總計 {total} 行受影響。{"dry-run（未寫入）" if dry_run else "已寫入。請用 git diff 檢視變化"}.')


if __name__ == '__main__':
    main()
