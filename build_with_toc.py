"""
build_with_toc.py — 2-pass build：填好目錄頁碼

流程：
  1. 第一次 build → docx with '—' 頁碼
  2. LibreOffice → PDF (1st)
  3. 掃 PDF 抓真實頁碼，寫入 toc_pages.json
  4. 第二次 build → docx with 真實頁碼
  5. LibreOffice → PDF (final)

執行：
    python build_with_toc.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent
DOCX = BASE / "論文_組裝.docx"
PDF  = BASE / "論文_組裝.pdf"
TOC_JSON = BASE / "toc_pages.json"
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"
PDFTOTEXT = r"C:\Program Files\Git\mingw64\bin\pdftotext.exe"


def run_build():
    print("▶ python build_thesis.py")
    env = {**__import__('os').environ, 'PYTHONUTF8': '1'}
    r = subprocess.run(
        [sys.executable, "build_thesis.py"],
        cwd=BASE, capture_output=True, text=True, encoding='utf-8', env=env
    )
    if r.returncode != 0:
        print(r.stderr)
        sys.exit(1)


def run_libreoffice():
    PDF.unlink(missing_ok=True)
    print("▶ LibreOffice → PDF")
    r = subprocess.run([
        SOFFICE, "--headless", "--convert-to", "pdf",
        "--outdir", str(BASE), str(DOCX)
    ], capture_output=True, text=True)
    if not PDF.exists():
        print("❌ PDF 轉換失敗")
        print(r.stderr)
        sys.exit(1)
    print(f"   {PDF.name} ({PDF.stat().st_size:,} bytes)")


def extract_pdf_pages():
    """回傳 [(pdf_seq, visible_page_str, text)]
    用 PyMuPDF (fitz) 抽中文 — pdftotext 對 LibreOffice 標楷體 PDF
    抽不出中文（沒 ToUnicode CMap）。
    visible_page 從頁尾 footer 抓（阿拉伯 = body / 羅馬 = 前置）。
    """
    import fitz
    doc = fitz.open(str(PDF))
    pages_text = [doc[i].get_text() for i in range(len(doc))]
    doc.close()

    ROMAN = {'i','ii','iii','iv','v','vi','vii','viii','ix','x',
             'xi','xii','xiii','xiv','xv','xvi','xvii','xviii','xix','xx',
             'xxi','xxii','xxiii','xxiv','xxv'}
    out = []
    for idx, text in enumerate(pages_text, start=1):
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        visible = str(idx)
        # 從尾端找 1-3 字元的數字或羅馬
        for line in reversed(lines[-5:]):
            if re.fullmatch(r'\d{1,3}', line):
                visible = line
                break
            if line.lower() in ROMAN:
                visible = line
                break
        out.append((idx, visible, text))
    return out


def normalize(s):
    """忽略所有空格/全形空格，讓 layout 上的空白差異不影響搜尋。"""
    return re.sub(r'[\s　]+', '', s)


def collect_toc_entries():
    """import build_thesis，呼叫 collect_events + registries + _collect_toc_entries。"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("build_thesis", BASE / "build_thesis.py")
    bt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bt)
    events = bt.collect_events()
    fr = bt.build_fig_registry(events)
    tr = bt.build_table_registry(events)
    return bt._collect_toc_entries(events, fr, tr)


def build_search_index():
    """條目 → 搜尋字串 + 對應的 JSON key。
    回傳 list of (key, search_text) 保持目錄順序，
    讓 scan_for_entries 可按順序遞進搜尋（避免重名 sub-subsection 抓錯位置）。
    """
    chap_e, fig_e, table_e = collect_toc_entries()
    index = []   # [(json_key, search_text)]
    for level, text, seq in chap_e:
        index.append((f'CHAP::{seq}::{text}', text))
    for num, caption in fig_e:
        index.append((f'FIG::{caption[:40]}', caption[:20]))
    for num, caption in table_e:
        index.append((f'TABLE::{caption[:40]}', caption[:20]))
    return index


def scan_for_entries(pages, index_ordered):
    """掃 PDF，按目錄順序循序搜尋每個條目。
    重點：每個條目從「上一個條目找到的頁」之後開始找，避免重名
    （例如多章節都有「伍、小結」）抓到錯誤位置。

    index_ordered: list of (key, search_text)，順序需與目錄順序一致
    """
    body_start = 0
    for idx, vis, text in pages:
        if '第一章' in text and '.....' not in text:
            body_start = idx
            break
    print(f"   本文起始：PDF seq {body_start}（本文頁碼 1）")

    body_pages = [(idx, normalize(text))
                  for idx, vis, text in pages
                  if idx >= body_start]

    found = {}
    # 三個類別各自循序搜尋（每個類別有自己的 cursor）：
    # 章節依目錄順序在本文出現；圖、表也各自依編號順序出現。
    for category in ('CHAP', 'FIG', 'TABLE'):
        cursor = 0
        for key, search_text in index_ordered:
            if not key.startswith(f'{category}::'):
                continue
            if not search_text:
                continue
            target = normalize(search_text)
            if not target:
                continue
            hit = None
            for i in range(cursor, len(body_pages)):
                idx, ntext = body_pages[i]
                if target in ntext:
                    hit = (i, idx)
                    break
            if hit is None:
                # fallback：從頭找（理論上不該發生，遇到代表搜尋字串對不上）
                for i in range(0, cursor):
                    idx, ntext = body_pages[i]
                    if target in ntext:
                        hit = (i, idx)
                        break
            if hit is not None:
                i, idx = hit
                found[key] = str(idx - body_start + 1)
                cursor = i  # 下一條目從這頁起（允許同頁多條目）
    return found


def main():
    # Pass 1: 清掉舊頁碼，產生 docx (頁碼 '—') → PDF
    print("=" * 60)
    print("Pass 1：產生含『—』頁碼的初版 docx + PDF")
    print("=" * 60)
    TOC_JSON.unlink(missing_ok=True)
    run_build()
    run_libreoffice()

    # 掃 PDF 抓頁碼
    print("\n" + "=" * 60)
    print("掃 PDF 抓真實頁碼")
    print("=" * 60)
    pages = extract_pdf_pages()
    index = build_search_index()
    pages_map = scan_for_entries(pages, index)
    print(f"▶ 條目總數 {len(index)}，找到頁碼 {len(pages_map)}")

    if len(pages_map) < len(index):
        missing = [(k, s) for k, s in index if k not in pages_map]
        print(f"⚠ 缺 {len(missing)} 條，前 5 個：")
        for k, s in missing[:5]:
            print(f"   {k}  →  搜：{s!r}")

    with open(TOC_JSON, 'w', encoding='utf-8') as f:
        json.dump(pages_map, f, ensure_ascii=False, indent=2)
    print(f"▶ 寫入 {TOC_JSON.name}")

    # Pass 2: 用真頁碼再 build 一次
    print("\n" + "=" * 60)
    print("Pass 2：用真實頁碼產生最終 docx + PDF")
    print("=" * 60)
    run_build()
    run_libreoffice()
    print("\n✅ 完成：論文_組裝.pdf 含真實頁碼目錄")


if __name__ == "__main__":
    main()
