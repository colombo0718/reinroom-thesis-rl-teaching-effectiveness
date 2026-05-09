#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
migrate_md_format.py — 把所有論文 md 檔對齊 v1 寫作規約

規約對應表：
  第N節 (X.Y)     → ## X.Y 標題
  壹、(X.Y.Z)     → ### X.Y.Z 標題
  一、(X.Y.Z.W)   → #### X.Y.Z.W 標題
  修辭分項        → **（一）標題** 純 bold（不動）

只動：
  - 行首標題的 # 數量、** 包覆
  - 行首章名（## 第N章 ...）刪除
  - 純 bold 假標題（**X.Y.Z xxx**）改成正規 heading
  - caption 標點：圖/表 N：xxx → 圖/表 N　xxx

不動：
  - 任何句子字詞
  - 行內 bold（如句中的 **RL Lab**）
  - 列表、表格內容、圖片路徑
  - 程式碼區塊（``` ... ```）

執行：
  python migrate_md_format.py --dry-run    # 只列出將要做的改動
  python migrate_md_format.py              # 實際寫入
"""

import re
import sys
from pathlib import Path

MD_DIR = Path(__file__).parent / "md"

# 行首標題 / bold 偽標題的識別
RE_HEADING_LINE   = re.compile(r'^(#{1,6})\s+(.*?)\s*$')
RE_BOLD_ONLY_LINE = re.compile(r'^\*\*(.+?)\*\*\s*$')

# 章名（## 第三章 ...）— 需刪除
RE_CHAPTER_NAME   = re.compile(r'^第[一二三四五六七八九十百]+章')

# 編號模式
RE_NUM_DEEPEST = re.compile(r'^(\d+\.\d+\.\d+\.\d+)\s+(.*)$')   # 4 級 X.Y.Z.W
RE_NUM_SUB     = re.compile(r'^(\d+\.\d+\.\d+)\s+(.*)$')         # 3 級 X.Y.Z
RE_NUM_SEC     = re.compile(r'^(\d+\.\d+)\s+(.*)$')               # 2 級 X.Y

# 修辭分項（無編號的 **（X）xxx**）
RE_RHETORICAL  = re.compile(r'^[（(][一二三四五六七八九十1-9]+[）)]')

# caption 標點：圖 X-Y[:：\s]+title → 圖 X-Y　title
RE_CAP_PUNCT_FIG = re.compile(r'(圖\s*\d+(?:[-−–]\d+)?[a-z]?)[\s::]+(?=\S)')
RE_CAP_PUNCT_TBL = re.compile(r'(表\s*\d+(?:[-−–]\d+)?[a-z]?)[\s::]+(?=\S)')


def normalize_title_text(s):
    """去除外層 ** 包覆。"""
    s = s.strip()
    m = re.match(r'^\*\*(.+?)\*\*\s*$', s)
    if m:
        s = m.group(1).strip()
    return s


def classify_numbered(text):
    """回傳 (level, normalized_text)。level: 'deepest' / 'sub' / 'sec' / None"""
    if RE_NUM_DEEPEST.match(text):
        return 'deepest', text
    if RE_NUM_SUB.match(text):
        return 'sub', text
    if RE_NUM_SEC.match(text):
        return 'sec', text
    return None, text


def normalize_caption_punct(text):
    """圖/表編號與標題之間用全形空格分隔。"""
    text = RE_CAP_PUNCT_FIG.sub(r'\1　', text)
    text = RE_CAP_PUNCT_TBL.sub(r'\1　', text)
    return text


# md image: ![alt](path)
RE_MD_IMAGE_LINE = re.compile(r'^(\s*!\[)(.*?)(\]\([^)]*\)\s*)$')


def transform_line(line, in_code_block):
    """處理單行，回傳 (new_line, did_change)。在 code block 中不處理。"""
    if in_code_block:
        return line, False

    stripped = line.strip()
    if not stripped:
        return line, False

    # === 1) Markdown heading 行 (## ...) ===
    m = RE_HEADING_LINE.match(line)
    if m:
        hashes = m.group(1)
        raw_content = m.group(2)
        content = normalize_title_text(raw_content)

        # 1a) 章名行 → 刪除
        if RE_CHAPTER_NAME.match(content):
            return None, True

        # 1b) 依編號層次重定 H 級
        level, _ = classify_numbered(content)
        if level == 'sec':
            new_line = f'## {content}\n'
        elif level == 'sub':
            new_line = f'### {content}\n'
        elif level == 'deepest':
            new_line = f'#### {content}\n'
        else:
            new_line = f'{hashes} {content}\n'

        return new_line, new_line != line

    # === 2) 純 bold 行 ===
    m = RE_BOLD_ONLY_LINE.match(stripped)
    if m:
        content = m.group(1).strip()

        # 2a) 章名 → 刪除
        if RE_CHAPTER_NAME.match(content):
            return None, True

        # 2b) 編號 bold → 對應 heading 級
        level, _ = classify_numbered(content)
        if level == 'sec':
            return f'## {content}\n', True
        if level == 'sub':
            return f'### {content}\n', True
        if level == 'deepest':
            return f'#### {content}\n', True

        # 2c) 圖/表 caption（純 bold 形式）→ 標點正規化
        if re.match(r'^(圖|表)\s*\d+', content):
            new_content = normalize_caption_punct(content)
            if new_content != content:
                return f'**{new_content}**\n', True

        # 2d) 修辭分項 / 無編號 bold → 不動
        return line, False

    # === 3) Markdown image：normalize alt 文字內的 caption 標點 ===
    m = RE_MD_IMAGE_LINE.match(line)
    if m:
        prefix, alt, suffix = m.group(1), m.group(2), m.group(3)
        new_alt = normalize_caption_punct(alt)
        if new_alt != alt:
            return f'{prefix}{new_alt}{suffix}', True
        return line, False

    # === 4) 其他正文行：不動（避免誤改「見圖 X-Y」「如表 X-Y」這類引用）===
    return line, False


def transform_file(fpath, dry_run=True):
    text = fpath.read_text(encoding='utf-8')
    lines = text.splitlines(keepends=True)
    new_lines = []
    in_code = False
    changes = []

    for i, line in enumerate(lines, 1):
        # code block toggle
        if line.lstrip().startswith('```'):
            in_code = not in_code
            new_lines.append(line)
            continue

        new_line, changed = transform_line(line, in_code)
        if changed:
            changes.append((i, line.rstrip('\n'), (new_line or '').rstrip('\n') or '<刪除>'))
        if new_line is not None:
            new_lines.append(new_line)

    if changes and not dry_run:
        fpath.write_text(''.join(new_lines), encoding='utf-8')

    return changes


def main():
    dry_run = '--dry-run' in sys.argv

    files = sorted(MD_DIR.glob('*.md'))
    total_changes = 0

    for f in files:
        changes = transform_file(f, dry_run=dry_run)
        if not changes:
            continue
        total_changes += len(changes)
        print(f'\n=== {f.name} ({len(changes)} 處) ===')
        for ln, before, after in changes[:20]:
            print(f'  L{ln}:')
            print(f'    - {before}')
            print(f'    + {after}')
        if len(changes) > 20:
            print(f'  ... 還有 {len(changes) - 20} 處')

    print(f'\n總計：{len(files)} 檔，{total_changes} 處改動。')
    if dry_run:
        print('（dry-run 模式，未寫入。加 --commit 或移除 --dry-run 才會實際寫入。）')
    else:
        print('✅ 已寫入。')


if __name__ == '__main__':
    main()
