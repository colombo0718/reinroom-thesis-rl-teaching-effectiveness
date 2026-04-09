#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_thesis.py — 元智大學碩士論文組裝腳本（格式A）

輸入：md/ 資料夾的章節 md 檔 + images/ 資料夾的圖片
輸出：論文_組裝.docx

圖片命名規則：images/fig{章}-{圖號}.png
  例：圖 3-1 → images/fig3-1.png
  目前提取的圖片（3.1 RL Lab 平台架構__image1.png 等）
  請手動重新命名為 fig3-1.png, fig3-2.png, fig3-3.png, fig3-4.png
"""

import re
from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE    = Path(__file__).parent
MD_DIR  = BASE / "md"
IMG_DIR = BASE / "images"
OUTPUT  = BASE / "論文_組裝.docx"

FONT_CN = '標楷體'
FONT_EN = 'Times New Roman'

# ── 章節順序（可自行調整章名與檔案清單） ────────────────────────────────
CHAPTERS = [
    ("第一章　緒論", [
        "第一章 緒論.md",
    ]),
    ("第二章　文獻探討", [
        "2.1 強化學習基本概念與教育潛力.md",
        "2.2 中小學生 RL 教學案例分析.md",
        "2.3 Gymnasium 平台與標準化環境簡介.md",
        "2.4 圖形化介面（UI-driven）與低門檻 RL 教學.md",
        "2.5 本研究切入點與創新定位.md",
    ]),
    ("第三章　Rein Room 平台設計", [
        "3.1 RL Lab 平台架構.md",
        "3.2 演算法設計.md",
        "3.3 視覺化模組.md",
        "3.4 遊戲環境.md",
    ]),
    ("第四章　研究設計", [
        "4.1 研究假設與實驗目標.md",
        "4.2 A_B 教學實驗流程設計.md",
        "4.3 實驗對象與分組方式說明.md",
        "4.4 教學流程與教材使用說明.md",
        "4.5 評估工具設計.md",
        "4.6 數據分析方法.md",
    ]),
    ("第五章　研究結果與分析", [
        "5.1 RL 概念理解測驗分析_.md",
        "5.2 任務完成成效與策略發展比較.md",
        "5.3 學習參與度與平台使用回饋.md",
        "5.4 錯誤行為觀察與平台改進討論.md",
    ]),
    ("第六章　結論與建議", [
        "6.1 研究成果總結.md",
        "6.2 平台與教材之教育應用潛力_.md",
    ]),
]

# ── 正則式 ───────────────────────────────────────────────────────────────
RE_HEADING    = re.compile(r'^(#{1,4})\s+(.*)')
RE_BOLD_ONLY  = re.compile(r'^\*\*(.+?)\*\*\s*$')
RE_FIG_CAP    = re.compile(r'^圖\s*\d+[-−–]\d+')
RE_FIG_DESC   = re.compile(r'^[（(]圖\s*\d+')
RE_SUBSEC     = re.compile(r'^\d+\.\d+\.\d+')   # X.X.X
RE_SEC        = re.compile(r'^\d+\.\d+\s')       # X.X<空格>
RE_CHAPTER_NO = re.compile(r'^第[一二三四五六七八九十百]+章')
RE_CN_SUB     = re.compile(r'^[一二三四五六七八九十]+[、．]')
RE_LIST       = re.compile(r'^[-*+]\s+(.*)')
RE_TABLE_ROW  = re.compile(r'^\|')
RE_TABLE_SEP  = re.compile(r'^\|[\s\-:]+\|')
RE_HR         = re.compile(r'^-{3,}$|^\*{3,}$')

# ── 字型 / 段落格式函數 ──────────────────────────────────────────────────

def set_font(run, size_pt, bold=False):
    run.bold = bold
    run.font.size = Pt(size_pt)
    run.font.name = FONT_EN
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:eastAsia'), FONT_CN)
    rFonts.set(qn('w:ascii'),    FONT_EN)
    rFonts.set(qn('w:hAnsi'),   FONT_EN)

def set_spacing(para, line_mult=1.2, before_pt=0, after_pt=0):
    pPr = para._p.get_or_add_pPr()
    for old in pPr.findall(qn('w:spacing')):
        pPr.remove(old)
    sp = OxmlElement('w:spacing')
    sp.set(qn('w:line'),     str(int(240 * line_mult)))
    sp.set(qn('w:lineRule'), 'auto')
    if before_pt:
        sp.set(qn('w:before'), str(int(before_pt * 20)))
    if after_pt:
        sp.set(qn('w:after'), str(int(after_pt * 20)))
    pPr.append(sp)

def add_runs(para, text, size_pt, default_bold=False):
    """拆解 **bold** 標記，加入 runs。"""
    parts = re.split(r'\*\*(.+?)\*\*', text)
    for i, part in enumerate(parts):
        if not part:
            continue
        run = para.add_run(part)
        set_font(run, size_pt, bold=default_bold or (i % 2 == 1))

# ── 段落類型函數 ─────────────────────────────────────────────────────────

def add_chapter_title(doc, title):
    """章名：標楷體 20pt 置中 1.2x 前後留雙倍行距。"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_spacing(p, 1.2, before_pt=28, after_pt=28)
    run = p.add_run(title)
    set_font(run, 20, bold=True)

def add_section(doc, text):
    """X.X 節名：16pt 靠左。"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_spacing(p, 1.2, before_pt=14, after_pt=0)
    run = p.add_run(text)
    set_font(run, 16, bold=True)

def add_subsection(doc, text):
    """X.X.X 節名：14pt 靠左。"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_spacing(p, 1.2, before_pt=10, after_pt=0)
    run = p.add_run(text)
    set_font(run, 14, bold=True)

def add_subhead(doc, text):
    """一、 層次：14pt 靠左 粗體。"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_spacing(p, 1.2)
    run = p.add_run(text)
    set_font(run, 14, bold=True)

def add_body(doc, text):
    """正文：14pt justified 1.2x。"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    set_spacing(p, 1.2)
    add_runs(p, text, 14)

def add_list_item(doc, text):
    """清單項目：• 開頭，14pt。"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    set_spacing(p, 1.2)
    run = p.add_run('• ')
    set_font(run, 14)
    add_runs(p, text, 14)

def add_fig_placeholder(doc, caption_text):
    """圖片不存在時的佔位文字。"""
    p = doc.add_paragraph(f'【圖片待補：{caption_text}】')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_spacing(p, 1.2, before_pt=8, after_pt=4)
    for run in p.runs:
        set_font(run, 12)
        run.font.color.rgb = None  # 用預設色

def add_fig_caption(doc, text):
    """圖說：12pt 置中。"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_spacing(p, 1.2, before_pt=4, after_pt=8)
    run = p.add_run(text)
    set_font(run, 12, bold=True)

def add_image(doc, img_path, width_cm=14):
    """插入圖片，置中。"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_spacing(p, 1.0, before_pt=8)
    run = p.add_run()
    run.add_picture(str(img_path), width=Cm(width_cm))

def add_page_break(doc):
    p = doc.add_paragraph()
    run = p.add_run()
    run.add_break(WD_BREAK.PAGE)

def add_table(doc, raw_rows):
    """從 md 表格列插入 Word 表格。"""
    rows = [r for r in raw_rows if not RE_TABLE_SEP.match(r.strip())]
    if not rows:
        return
    cols = max(len(r.strip('|').split('|')) for r in rows)
    if cols <= 0:
        return
    tbl = doc.add_table(rows=len(rows), cols=cols)
    tbl.style = 'Table Grid'
    for ri, row_line in enumerate(rows):
        cells = [c.strip() for c in row_line.strip('|').split('|')]
        for ci in range(cols):
            cell_text = cells[ci].strip('*').strip() if ci < len(cells) else ''
            cell = tbl.rows[ri].cells[ci]
            cell.text = ''
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_spacing(p, 1.2)
            add_runs(p, cell_text, 12)

# ── 圖片查找 ─────────────────────────────────────────────────────────────

def find_image(caption):
    """從圖說文字找對應圖片，例：圖 3-1 → images/fig3-1.png，圖 3-11a → images/fig3-11a.png。"""
    m = re.search(r'圖\s*(\d+)\s*[-−–]\s*(\d+)([a-z]?)', caption)
    if not m:
        return None
    ch, num, letter = m.group(1), m.group(2), m.group(3)
    for ext in ('png', 'jpg', 'jpeg'):
        p = IMG_DIR / f"fig{ch}-{num}{letter}.{ext}"
        if p.exists():
            return p
    return None

# ── MD 解析 ──────────────────────────────────────────────────────────────

def normalize(text):
    """去除 ** 標記並 strip。"""
    return text.replace('**', '').strip()

def classify_bold_line(content):
    """判斷純 bold 行的段落類型。"""
    if RE_FIG_CAP.match(content):
        return 'figcaption'
    if RE_CHAPTER_NO.match(content):
        return 'chapter'
    if RE_SUBSEC.match(content):
        return 'subsection'
    if RE_SEC.match(content):
        return 'section'
    if RE_CN_SUB.match(content):
        return 'subhead'
    # 短純粗體行（無標點在中間）→ 當作 subhead
    if len(content) < 30 and '，' not in content and '。' not in content:
        return 'subhead'
    return 'body'

def parse_md(filepath, chapter_title):
    """逐行解析 md，yield (kind, content)。"""
    lines = filepath.read_text(encoding='utf-8').splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        stripped = line.strip()

        # 空行、分隔線
        if not stripped or RE_HR.match(stripped):
            continue

        # 圖描述 （圖 X-X ...） → 跳過（不出現在論文）
        if RE_FIG_DESC.match(stripped):
            continue

        # 表格
        if RE_TABLE_ROW.match(stripped):
            rows = [line]
            while i < len(lines) and RE_TABLE_ROW.match(lines[i].strip()):
                rows.append(lines[i])
                i += 1
            yield ('table', rows)
            continue

        # Markdown heading (#, ##, ###, ####)
        m = RE_HEADING.match(line)
        if m:
            content = normalize(m.group(2))
            if not content:
                continue
            # 跳過與章名相同的行
            if content.replace('　', ' ') == chapter_title.replace('　', ' '):
                continue
            if RE_CHAPTER_NO.match(content):
                yield ('chapter_skip', content)
            elif RE_SUBSEC.match(content):
                yield ('subsection', content)
            elif RE_SEC.match(content):
                yield ('section', content)
            elif RE_CN_SUB.match(content):
                yield ('subhead', content)
            else:
                yield ('section', content)
            continue

        # 純 **bold** 行
        m = RE_BOLD_ONLY.match(stripped)
        if m:
            content = m.group(1).strip()
            kind = classify_bold_line(content)
            if kind == 'chapter':
                if content.replace('　', ' ') == chapter_title.replace('　', ' '):
                    continue
                yield ('chapter_skip', content)
            else:
                yield (kind, content)
            continue

        # 清單
        m = RE_LIST.match(stripped)
        if m:
            yield ('list', m.group(1))
            continue

        # 正文
        yield ('body', stripped)

# ── 主程式 ───────────────────────────────────────────────────────────────

def build():
    doc = Document()

    # 頁面邊距
    for sec in doc.sections:
        sec.top_margin    = Cm(3.5)
        sec.bottom_margin = Cm(2.0)
        sec.left_margin   = Cm(4.0)
        sec.right_margin  = Cm(2.0)

    # 清除預設段落間距
    normal = doc.styles['Normal']
    normal.paragraph_format.space_after  = Pt(0)
    normal.paragraph_format.space_before = Pt(0)

    first_chapter = True
    missing_images = []

    for chapter_title, files in CHAPTERS:
        # 每章從新頁開始
        if not first_chapter:
            add_page_break(doc)
        first_chapter = False

        print(f'\n▶ {chapter_title}')
        add_chapter_title(doc, chapter_title)

        for fname in files:
            fpath = MD_DIR / fname
            if not fpath.exists():
                print(f'  ⚠  找不到：{fname}')
                continue
            print(f'  ✓  {fname}')

            for kind, content in parse_md(fpath, chapter_title):
                if kind == 'chapter_skip':
                    pass  # 章名已在上面加過
                elif kind == 'section':
                    add_section(doc, content)
                elif kind == 'subsection':
                    add_subsection(doc, content)
                elif kind == 'subhead':
                    add_subhead(doc, content)
                elif kind == 'figcaption':
                    img = find_image(content)
                    if img:
                        add_image(doc, img)
                    else:
                        add_fig_placeholder(doc, content)
                        missing_images.append(content)
                    add_fig_caption(doc, content)
                elif kind == 'list':
                    add_list_item(doc, content)
                elif kind == 'table':
                    add_table(doc, content)
                elif kind == 'body':
                    if content:
                        add_body(doc, content)

    doc.save(str(OUTPUT))
    print(f'\n✅ 輸出：{OUTPUT}')

    if missing_images:
        print(f'\n⚠  以下 {len(missing_images)} 張圖片未找到，已插入佔位文字：')
        for caption in missing_images:
            print(f'   - {caption}')
        print(f'\n   圖片請命名為 images/fig{{章}}-{{號}}.png')
        print(f'   例：圖 3-1 → images/fig3-1.png')

if __name__ == '__main__':
    build()
