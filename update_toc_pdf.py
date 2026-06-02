"""
update_toc_pdf.py — 用 LibreOffice + UNO 自動更新所有目錄欄位 + 匯出 PDF

問題背景：build_thesis.py 用 Word TOC field 寫進 docx，但 LibreOffice
headless 模式不會自動更新 field，所以匯出的 PDF 目錄頁是空的。

本腳本：
1. 啟動 LibreOffice headless + UNO socket
2. Python 透過 UNO 連線開檔
3. 對所有 DocumentIndexes 呼叫 update()（含目錄、表目錄、圖目錄）
4. refresh() 更新所有 field
5. 匯出 PDF

執行：
    python update_toc_pdf.py
"""
import os
import sys
import time
import subprocess
import socket
from pathlib import Path

BASE = Path(__file__).parent
DOCX = BASE / "論文_組裝.docx"
PDF  = BASE / "論文_組裝.pdf"

SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"
UNO_PORT = 2202


def url(path):
    return "file:///" + str(path).replace("\\", "/")


def wait_port(port, timeout=20):
    for _ in range(timeout * 4):
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.25)
    return False


def main():
    if not DOCX.exists():
        print(f"❌ 找不到 {DOCX}")
        sys.exit(1)

    # 把 LibreOffice 自帶 python 的 site-packages 加入路徑（含 uno）
    lo_program = Path(SOFFICE).parent
    sys.path.insert(0, str(lo_program))

    try:
        import uno
        from com.sun.star.beans import PropertyValue
    except ImportError as e:
        print(f"❌ 無法 import uno：{e}")
        print(f"   嘗試改用 LibreOffice 自帶 python：")
        print(f"   {lo_program / 'python.exe'} {__file__}")
        sys.exit(1)

    # 啟動 LibreOffice headless + UNO socket
    print("▶ 啟動 LibreOffice headless…")
    proc = subprocess.Popen([
        SOFFICE,
        "--headless", "--nologo", "--norestore", "--nofirststartwizard",
        f"--accept=socket,host=127.0.0.1,port={UNO_PORT};urp;",
    ])

    try:
        if not wait_port(UNO_PORT, 30):
            print("❌ LibreOffice UNO socket 沒起來")
            return

        print(f"▶ 連線 UNO（port {UNO_PORT}）…")
        ctx = uno.getComponentContext()
        resolver = ctx.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", ctx)
        remote_ctx = resolver.resolve(
            f"uno:socket,host=127.0.0.1,port={UNO_PORT};urp;StarOffice.ComponentContext"
        )
        smgr = remote_ctx.ServiceManager
        desktop = smgr.createInstanceWithContext(
            "com.sun.star.frame.Desktop", remote_ctx)

        print(f"▶ 開檔：{DOCX.name}（強制更新所有欄位）")
        # UpdateDocMode: 0=ACCORDING_TO_CONFIG, 1=NO_UPDATE, 2=QUIET_UPDATE, 3=FULL_UPDATE
        open_props = (
            PropertyValue("Hidden", 0, True, 0),
            PropertyValue("UpdateDocMode", 0, 3, 0),
        )
        doc = desktop.loadComponentFromURL(url(DOCX), "_blank", 0, open_props)

        if doc is None:
            print("❌ 開檔失敗")
            return

        print(f"▶ DocumentIndexes.Count = {doc.DocumentIndexes.Count}")
        for i in range(doc.DocumentIndexes.Count):
            idx = doc.DocumentIndexes.getByIndex(i)
            idx.update()
            print(f"   ✓ index #{i}: {idx.Title or '(無標題)'}")

        # 用 UNO dispatch 觸發內建命令（會處理 Word TOC field）
        print("▶ dispatch UpdateAllIndexes / UpdateFields / UpdateAll…")
        dispatcher = smgr.createInstanceWithContext(
            "com.sun.star.frame.DispatchHelper", remote_ctx)
        frame = doc.getCurrentController().getFrame()
        for cmd in (".uno:UpdateAllIndexes", ".uno:UpdateFields", ".uno:UpdateAll"):
            try:
                dispatcher.executeDispatch(frame, cmd, "", 0, ())
                print(f"   ✓ {cmd}")
            except Exception as e:
                print(f"   ⚠ {cmd}: {e}")

        # 再 refresh 一次（dispatch 可能改了 index 內容）
        doc.refresh()
        # 等 LibreOffice 處理完 index 計算
        time.sleep(2)
        print(f"▶ 處理後 DocumentIndexes.Count = {doc.DocumentIndexes.Count}")

        print(f"▶ 匯出 PDF：{PDF.name}")
        pdf_props = (PropertyValue("FilterName", 0, "writer_pdf_Export", 0),)
        doc.storeToURL(url(PDF), pdf_props)

        doc.close(False)
        print(f"\n✅ 完成！PDF 已產出含目錄填好的版本：{PDF}")

    finally:
        print("▶ 關閉 LibreOffice…")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    main()
