#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_thesis.py — 元智大學碩士論文組裝腳本（格式A）

輸入：md/ 資料夾的章節 md 檔 + images/ 資料夾的圖片
輸出：論文_組裝.docx

【格式對齊原則】md 不管正式格式，腳本負責對齊學校規範。
  - 章節編號：md 的「X.X」「X.X.X」由腳本轉成「第N節」「壹、」
  - 圖表編號：md 的「圖 3-1」依出現順序連續編號為「圖 1」、「圖 2」...
  - 文內圖片參照：「見圖 3-1」也會同步轉換
  - 圖片語法：支援 markdown 的 ![caption](path) 語法

圖片命名規則：images/fig{章}-{圖號}.png
  例：圖 3-1 → images/fig3-1.png
  支援字尾：圖 3-11a → images/fig3-11a.png
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

# ── 格式轉換開關（對齊元智格式A） ─────────────────────────────────────────
CONVERT_SECTION_NUMBERING    = True   # 5.1 → 第一節
CONVERT_SUBSECTION_NUMBERING = True   # 5.1.1 → 壹、
CONVERT_FIGURE_NUMBERING     = True   # 圖 3-1 → 圖 1（全文連續編號）
CONVERT_TABLE_NUMBERING      = True   # 表 3-1 → 表 1（全文連續編號）
NORMALIZE_CAPTION_PUNCT      = True   # 圖 1：xxx / 圖 1 xxx → 圖 1　xxx（全形空格）
ADD_PAGE_NUMBER              = True   # footer 中央阿拉伯數字頁碼
BODY_FIRST_LINE_INDENT_CHARS = 2      # 正文首行縮排字元數

# ── 中文數字對照表 ───────────────────────────────────────────────────────
NUM_CN_SIMPLE = ['', '一','二','三','四','五','六','七','八','九','十',
                 '十一','十二','十三','十四','十五','十六','十七','十八','十九','二十']
NUM_CN_FORMAL = ['', '壹','貳','參','肆','伍','陸','柒','捌','玖','拾',
                 '拾壹','拾貳','拾參','拾肆','拾伍','拾陸','拾柒','拾捌','拾玖','貳拾']

def num_to_cn(n, formal=False):
    table = NUM_CN_FORMAL if formal else NUM_CN_SIMPLE
    return table[n] if 0 < n < len(table) else str(n)

def convert_section_text(text):
    """5.1 RL 概念理解測驗分析 → 第一節　RL 概念理解測驗分析"""
    m = re.match(r'^\d+\.(\d+)\s+(.*)$', text)
    if not m:
        return text
    return f'第{num_to_cn(int(m.group(1)))}節　{m.group(2).strip()}'

def convert_subsection_text(text):
    """4.2.1 實驗設計型態 → 壹、實驗設計型態"""
    m = re.match(r'^\d+\.\d+\.(\d+)\s+(.*)$', text)
    if not m:
        return text
    return f'{num_to_cn(int(m.group(1)), formal=True)}、{m.group(2).strip()}'

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
        "6.3 未來擴充建議.md",
        "6.4 發表與推廣建議.md",
        "6.5 給未來平台設計者的建議.md",
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
RE_MD_IMAGE   = re.compile(r'^!\[(.*?)\]\((.*?)\)\s*$')   # ![caption](path)
RE_FIG_KEY    = re.compile(r'圖\s*(\d+)[-−–](\d+)([a-z]?)')   # 圖 3-1 / 圖 3-11a
RE_TABLE_CAP  = re.compile(r'^表\s*\d+[-−–]\d+')   # 表說起始：表 5-5
RE_TABLE_KEY  = re.compile(r'表\s*(\d+)[-−–](\d+)([a-z]?)')   # 表 5-5 / 表 5-5a

# ── 圖表編號管理 ─────────────────────────────────────────────────────────

class FigureRegistry:
    """蒐集所有圖標籤並依出現順序給予全文連續編號。"""
    def __init__(self):
        self.mapping = {}   # (chapter, num, letter) → 連續號

    def register(self, caption_text):
        m = RE_FIG_KEY.search(caption_text)
        if not m:
            return
        key = (m.group(1), m.group(2), m.group(3))
        if key not in self.mapping:
            self.mapping[key] = len(self.mapping) + 1

    def convert(self, text):
        """將文字中所有「圖 X-Y」替換為「圖 N」（依登記表）。"""
        if not text:
            return text
        def repl(m):
            key = (m.group(1), m.group(2), m.group(3))
            if key in self.mapping:
                return f'圖 {self.mapping[key]}'
            return m.group(0)
        return RE_FIG_KEY.sub(repl, text)


class TableRegistry:
    """蒐集所有表標籤並依出現順序給予全文連續編號（同 FigureRegistry）。"""
    def __init__(self):
        self.mapping = {}

    def register(self, caption_text):
        m = RE_TABLE_KEY.search(caption_text)
        if not m:
            return
        key = (m.group(1), m.group(2), m.group(3))
        if key not in self.mapping:
            self.mapping[key] = len(self.mapping) + 1

    def convert(self, text):
        if not text:
            return text
        def repl(m):
            key = (m.group(1), m.group(2), m.group(3))
            if key in self.mapping:
                return f'表 {self.mapping[key]}'
            return m.group(0)
        return RE_TABLE_KEY.sub(repl, text)


def normalize_caption_punct(text):
    """統一圖/表 caption 的編號與標題之間用全形空格分隔。
    「圖 1：xxx」「圖 1 xxx」「表 5  xxx」 → 「圖 1　xxx」「表 5　xxx」
    """
    if not text:
        return text
    # 「圖 N」或「表 N」 後若接 半形空格/冒號/全形冒號 + 標題文字 → 替換成全形空格
    text = re.sub(r'(圖\s*\d+[a-z]?)[\s::]+(?=\S)', r'\1　', text)
    text = re.sub(r'(表\s*\d+[a-z]?)[\s::]+(?=\S)', r'\1　', text)
    return text

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

def set_first_line_indent_chars(para, chars):
    """中文段落首行縮排 N 字元（firstLineChars 以百分位寫入）。"""
    if chars <= 0:
        return
    pPr = para._p.get_or_add_pPr()
    for old in pPr.findall(qn('w:ind')):
        pPr.remove(old)
    ind = OxmlElement('w:ind')
    ind.set(qn('w:firstLineChars'), str(chars * 100))
    # fallback: 14pt × N 字 × 20 twips/pt
    ind.set(qn('w:firstLine'), str(int(14 * chars * 20)))
    pPr.append(ind)

def add_page_number_field(footer_para):
    """在 footer 段落加入 PAGE field（顯示當前頁碼）。"""
    footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = footer_para.add_run()
    set_font(run, 12)
    fld_begin = OxmlElement('w:fldChar')
    fld_begin.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText')
    instr.set(qn('xml:space'), 'preserve')
    instr.text = 'PAGE'
    fld_end = OxmlElement('w:fldChar')
    fld_end.set(qn('w:fldCharType'), 'end')
    run._r.append(fld_begin)
    run._r.append(instr)
    run._r.append(fld_end)

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
    """正文：14pt justified 1.2x，首行縮排 2 字元。"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    set_spacing(p, 1.2)
    set_first_line_indent_chars(p, BODY_FIRST_LINE_INDENT_CHARS)
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
    """圖說：12pt 置中，置於圖下方。"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_spacing(p, 1.2, before_pt=4, after_pt=8)
    run = p.add_run(text)
    set_font(run, 12, bold=True)

def add_table_caption(doc, text):
    """表說：12pt 粗體置中，置於表上方（規範要求表號表名列於表上方）。"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_spacing(p, 1.2, before_pt=8, after_pt=4)
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

def add_table(doc, raw_rows, fig_registry=None, table_registry=None):
    """從 md 表格列插入 Word 表格；registry 提供時，cell 內圖/表參照會轉成新編號。"""
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
            if fig_registry is not None:
                cell_text = fig_registry.convert(cell_text)
            if table_registry is not None:
                cell_text = table_registry.convert(cell_text)
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

def resolve_md_image(path_str):
    """解析 markdown 圖片相對路徑。md 在 MD_DIR/，所以 ../images/x.png → IMG_DIR/x.png。"""
    p = (MD_DIR / path_str).resolve()
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
    if RE_TABLE_CAP.match(content):
        return 'tablecaption'
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
    """逐行解析 md，yield (kind, content)。

    去重：若 ![圖 X-Y](path) 後緊接著 **圖 X-Y　...** 的 bold figcaption，
    視為同一張圖的重複標註（既有 md 的混用慣例），跳過第二次。
    """
    lines = filepath.read_text(encoding='utf-8').splitlines()
    i = 0
    last_md_img_key = None  # 上一個 md_image 的圖編號 (ch, num, letter)，遇任何非空非 figcaption 內容即清除
    while i < len(lines):
        line = lines[i]
        i += 1
        stripped = line.strip()

        # 空行、分隔線：不清除 last_md_img_key（允許段落間有空白行）
        if not stripped or RE_HR.match(stripped):
            continue

        # 圖描述 （圖 X-X ...） → 跳過（不出現在論文）
        if RE_FIG_DESC.match(stripped):
            continue

        # Markdown 圖片語法 ![caption](path)
        m = RE_MD_IMAGE.match(stripped)
        if m:
            caption = m.group(1).strip()
            path    = m.group(2).strip()
            mk = RE_FIG_KEY.search(caption)
            last_md_img_key = (mk.group(1), mk.group(2), mk.group(3)) if mk else None
            yield ('md_image', (caption, path))
            continue

        # 表格
        if RE_TABLE_ROW.match(stripped):
            rows = [line]
            while i < len(lines) and RE_TABLE_ROW.match(lines[i].strip()):
                rows.append(lines[i])
                i += 1
            last_md_img_key = None
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
            last_md_img_key = None
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
            # 去重：md_image 後緊接同編號 figcaption → 跳過
            if kind == 'figcaption' and last_md_img_key is not None:
                mk = RE_FIG_KEY.search(content)
                if mk and (mk.group(1), mk.group(2), mk.group(3)) == last_md_img_key:
                    last_md_img_key = None
                    continue
            last_md_img_key = None
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
            last_md_img_key = None
            yield ('list', m.group(1))
            continue

        # 正文
        last_md_img_key = None
        yield ('body', stripped)

# ── 主程式 ───────────────────────────────────────────────────────────────

def collect_events():
    """Pass 1：掃描所有 md，收集 (chapter_title, kind, content) 序列。"""
    events = []
    for chapter_title, files in CHAPTERS:
        events.append((chapter_title, '__chapter_start__', None))
        for fname in files:
            fpath = MD_DIR / fname
            if not fpath.exists():
                events.append((chapter_title, '__missing_file__', fname))
                continue
            events.append((chapter_title, '__file_start__', fname))
            for kind, content in parse_md(fpath, chapter_title):
                events.append((chapter_title, kind, content))
    return events

def build_fig_registry(events):
    """Pass 2：依出現順序登記所有圖標籤。"""
    reg = FigureRegistry()
    for _, kind, content in events:
        if kind == 'figcaption':
            reg.register(content)
        elif kind == 'md_image':
            caption, _ = content
            reg.register(caption)
    return reg

def build_table_registry(events):
    """Pass 2b：依出現順序登記所有表標籤。"""
    reg = TableRegistry()
    for _, kind, content in events:
        if kind == 'tablecaption':
            reg.register(content)
    return reg

def build():
    doc = Document()

    # 頁面設定（A4 + 邊距 + footer 距離）
    for sec in doc.sections:
        sec.page_width      = Cm(21.0)   # A4 寬
        sec.page_height     = Cm(29.7)   # A4 高
        sec.top_margin      = Cm(3.5)
        sec.bottom_margin   = Cm(2.0)
        sec.left_margin     = Cm(4.0)
        sec.right_margin    = Cm(2.0)
        sec.footer_distance = Cm(1.0)    # 規範：版面底端 1cm 處中央繕打頁次

    # footer 中央阿拉伯數字頁碼
    if ADD_PAGE_NUMBER:
        for sec in doc.sections:
            footer_para = sec.footer.paragraphs[0]
            footer_para.text = ''
            add_page_number_field(footer_para)

    # 清除預設段落間距
    normal = doc.styles['Normal']
    normal.paragraph_format.space_after  = Pt(0)
    normal.paragraph_format.space_before = Pt(0)

    # Pass 1: 收集事件
    events = collect_events()

    # Pass 2: 建立圖/表編號對照
    fig_registry   = build_fig_registry(events)   if CONVERT_FIGURE_NUMBERING else None
    table_registry = build_table_registry(events) if CONVERT_TABLE_NUMBERING  else None

    # Pass 3: 渲染 docx
    first_chapter = True
    missing_images = []

    def maybe_convert_refs(text):
        """文內若有圖/表參照，依登記表替換；並統一 caption 標點。"""
        if not text:
            return text
        if fig_registry is not None:
            text = fig_registry.convert(text)
        if table_registry is not None:
            text = table_registry.convert(text)
        if NORMALIZE_CAPTION_PUNCT:
            text = normalize_caption_punct(text)
        return text

    for chapter_title, kind, content in events:
        if kind == '__chapter_start__':
            if not first_chapter:
                add_page_break(doc)
            first_chapter = False
            print(f'\n▶ {chapter_title}')
            add_chapter_title(doc, chapter_title)
        elif kind == '__missing_file__':
            print(f'  ⚠  找不到：{content}')
        elif kind == '__file_start__':
            print(f'  ✓  {content}')
        elif kind == 'chapter_skip':
            pass
        elif kind == 'section':
            text = convert_section_text(content) if CONVERT_SECTION_NUMBERING else content
            add_section(doc, text)
        elif kind == 'subsection':
            text = convert_subsection_text(content) if CONVERT_SUBSECTION_NUMBERING else content
            add_subsection(doc, text)
        elif kind == 'subhead':
            add_subhead(doc, content)
        elif kind == 'figcaption':
            display = maybe_convert_refs(content)
            img = find_image(content)
            if img:
                add_image(doc, img)
            else:
                add_fig_placeholder(doc, display)
                missing_images.append(content)
            add_fig_caption(doc, display)
        elif kind == 'md_image':
            caption, path = content
            display = maybe_convert_refs(caption)
            img = resolve_md_image(path) or find_image(caption)
            if img:
                add_image(doc, img)
            else:
                add_fig_placeholder(doc, display)
                missing_images.append(caption)
            add_fig_caption(doc, display)
        elif kind == 'tablecaption':
            display = maybe_convert_refs(content)
            add_table_caption(doc, display)
        elif kind == 'list':
            add_list_item(doc, maybe_convert_refs(content))
        elif kind == 'table':
            add_table(doc, content, fig_registry, table_registry)
        elif kind == 'body':
            if content:
                add_body(doc, maybe_convert_refs(content))

    doc.save(str(OUTPUT))
    print(f'\n✅ 輸出：{OUTPUT}')

    # 摘要報告
    if fig_registry is not None and fig_registry.mapping:
        print(f'\n📊 圖編號對照（共 {len(fig_registry.mapping)} 張）：')
        for (ch, num, letter), new_n in sorted(fig_registry.mapping.items(), key=lambda x: x[1]):
            old = f'圖 {ch}-{num}{letter}'
            print(f'   {old:>12s}  →  圖 {new_n}')

    if table_registry is not None and table_registry.mapping:
        print(f'\n📋 表編號對照（共 {len(table_registry.mapping)} 張）：')
        for (ch, num, letter), new_n in sorted(table_registry.mapping.items(), key=lambda x: x[1]):
            old = f'表 {ch}-{num}{letter}'
            print(f'   {old:>12s}  →  表 {new_n}')

    if missing_images:
        print(f'\n⚠  以下 {len(missing_images)} 張圖片未找到，已插入佔位文字：')
        for caption in missing_images:
            print(f'   - {caption}')
        print(f'\n   圖片請命名為 images/fig{{章}}-{{號}}.png')
        print(f'   例：圖 3-1 → images/fig3-1.png')

if __name__ == '__main__':
    build()
