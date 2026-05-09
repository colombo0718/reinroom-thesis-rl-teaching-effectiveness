#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unify_terminology_cleanup.py — 第一輪批次替換後的 cleanup

修補：
- Colab Colab 組 → Colab 組（原本「Colab 對照組」被翻譯產生）
- RR 組（A）（RR）→ RR 組（A）（原本「實驗組 A（RL Lab）」翻譯）
- Colab 組（B）（Gymnasium + Colab）→ Colab 組（B）
- 中英文之間缺空格（之RR、於RR、之Colab 等）
"""

import re
import sys
from pathlib import Path

MD_DIR = Path(__file__).parent / "md"

CLEANUP_RULES = [
    # 雙重命名清除
    ('Colab Colab 組',                    'Colab 組'),
    ('RR RR 組',                          'RR 組'),
    ('RR 組（A）（RR）',                  'RR 組（A）'),
    ('Colab 組（B）（Gymnasium + Colab）',  'Colab 組（B）'),
    ('Colab 組（B）（Gym + Colab）',        'Colab 組（B）'),
    ('RR 組（A）（RL Lab）',               'RR 組（A）'),
    # 三層巢狀（保險）
    ('Colab Colab Colab',                'Colab'),
    ('RR RR RR',                         'RR'),
]

# 正則修補：中文字 + RR/Colab/Group 之間缺空格
SPACE_PATTERNS = [
    (re.compile(r'([一-鿿])(RR\s)'),     r'\1 \2'),
    (re.compile(r'(RR)([一-鿿])'),       r'\1 \2'),
    (re.compile(r'([一-鿿])(Colab\s)'),  r'\1 \2'),
    (re.compile(r'(Colab)(組)'),                  r'\1 \2'),  # 「Colab組」→「Colab 組」
]


def transform(text):
    out_lines = []
    in_code = False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith('```'):
            in_code = not in_code
            out_lines.append(line)
            continue
        if in_code:
            out_lines.append(line)
            continue

        new_line = line
        for old, new in CLEANUP_RULES:
            new_line = new_line.replace(old, new)
        for pat, repl in SPACE_PATTERNS:
            new_line = pat.sub(repl, new_line)
        out_lines.append(new_line)
    return ''.join(out_lines)


def main():
    dry_run = '--dry-run' in sys.argv
    files = sorted(MD_DIR.glob('*.md'))
    total = 0
    for f in files:
        original = f.read_text(encoding='utf-8')
        migrated = transform(original)
        if original == migrated:
            continue
        diffs = sum(1 for a, b in zip(original.splitlines(), migrated.splitlines()) if a != b)
        total += diffs
        print(f'✓ {f.name}  ({diffs} 行受影響)')
        if not dry_run:
            f.write_text(migrated, encoding='utf-8')
    print(f'\n總計 {total} 行受影響。{"dry-run" if dry_run else "已寫入"}.')


if __name__ == '__main__':
    main()
