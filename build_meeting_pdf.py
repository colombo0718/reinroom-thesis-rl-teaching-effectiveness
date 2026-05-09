#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_meeting_pdf.py — 產生 5/9 開會用精簡 PDF
僅含：第四章、第五章、6.1 研究成果總結

執行：python build_meeting_pdf.py
產出：開會討論_第四五章_6.1.pdf
"""

import sys
from pathlib import Path

BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))

import build_thesis as bt
from docx2pdf import convert

# 覆寫章節清單（只保留要討論的）
bt.CHAPTERS = [
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
    ]),
]

# 覆寫輸出檔名
DOCX_OUT = BASE / "開會討論_第四五章_6.1.docx"
PDF_OUT  = BASE / "開會討論_第四五章_6.1.pdf"
bt.OUTPUT = DOCX_OUT

print("▶ 組裝精簡版 docx ...")
bt.build()

print(f"\n▶ 轉 PDF：{PDF_OUT.name}")
convert(str(DOCX_OUT), str(PDF_OUT))
print(f"\n✅ PDF 完成：{PDF_OUT}")
