#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
strip_fig_titles.py — 移除 fig5-X HTML 內的 title/subtitle/footnote/stats-line

依元智規範，圖標題與圖說由 docx 腳本（build_thesis.py 的 add_fig_caption）負責，
HTML 圖檔本身只應包含「圖表本身」，不該含「圖 5-X xxx」這種重複標題。

只動 fig5-1 ~ fig5-5，不動 fig3-2、fig4-1（fig4-1 已手動重寫）。
"""

import re
from pathlib import Path

FIGURES = [
    "fig5-1-pretest-posttest-box.html",
    "fig5-2-gain-comparison.html",
    "fig5-3-task-completion.html",
    "fig5-4-section3-comparison.html",
    "fig5-5-sus-comparison.html",
]

DIR = Path(__file__).parent

# 要移除的 div 類型
DIV_CLASSES_TO_REMOVE = ['title', 'subtitle', 'footnote', 'stats-line']

# 要移除的 CSS rule 類別
CSS_CLASSES_TO_REMOVE = ['.title', '.subtitle', '.footnote', '.stats-line']


def remove_divs(html, class_name):
    """移除 <div class="class_name">...</div>，可能跨多行。"""
    # 簡單版：以非貪婪匹配找 <div class="X">...</div>
    pattern = re.compile(
        r'<div\s+class="' + re.escape(class_name) + r'"[^>]*>.*?</div>\s*',
        re.DOTALL
    )
    return pattern.sub('', html)


def remove_css_rule(css, selector):
    """移除指定 selector 的 CSS rule。"""
    # 匹配 selector { ... } 含換行
    pattern = re.compile(
        r'\s*' + re.escape(selector) + r'\s*\{[^}]*\}\s*',
        re.DOTALL
    )
    return pattern.sub('\n  ', css)


def process(fpath):
    text = fpath.read_text(encoding='utf-8')
    original = text

    # 先移除 div
    for cls in DIV_CLASSES_TO_REMOVE:
        text = remove_divs(text, cls)

    # 移除對應 CSS rules
    for cls in CSS_CLASSES_TO_REMOVE:
        text = remove_css_rule(text, cls)

    # body height 縮減（從 800px → 640px，因為去掉 title/subtitle/footnote 後高度變小）
    text = re.sub(r'(\s+height:\s*)800px\s*;', r'\g<1>640px;', text)
    # 有些可能是 700/900 等，先不動

    if text != original:
        fpath.write_text(text, encoding='utf-8')
        return True
    return False


def main():
    for name in FIGURES:
        fpath = DIR / name
        if not fpath.exists():
            print(f'❌ 找不到 {name}')
            continue
        changed = process(fpath)
        marker = '✓' if changed else '—'
        print(f'{marker} {name}')


if __name__ == '__main__':
    main()
