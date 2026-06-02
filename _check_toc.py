"""快速檢查 PDF 內目錄頁的實際內容（前 15 頁）"""
import subprocess

for p in range(1, 16):
    txt = subprocess.run(
        [r"C:\Program Files\Git\mingw64\bin\pdftotext.exe", "-layout",
         "-f", str(p), "-l", str(p), "論文_組裝.pdf", "-"],
        capture_output=True, text=True, encoding='utf-8'
    ).stdout
    # 找含關鍵字的頁
    if any(k in txt for k in ['目錄', '請於 Word', '表目錄', '圖目錄', 'F9 更新']):
        print(f'=== 第 {p} 頁 ===')
        print(txt[:300])
        print('...')
