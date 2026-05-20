# 論文_組裝.docx 元智格式 A 檢驗報告（Claude 自查版）

檢驗日期：2026-05-10
檢驗對象：`論文_組裝.docx`（Codex 第一輪報告 `codex-report_2026-05-10_01.md` 之 6 項修補後版本）
來源程式：`build_thesis.py`
檢驗者：Claude（與 Codex 平行盲審，使用相同 prompt 模板）

檢驗方法：
- 直接解壓 docx → 讀 `word/document.xml` / `word/footer1.xml` / `word/styles.xml`
- 抽樣 OOXML 結構（`pgSz` / `pgMar` / `sectPr` / `pgNumType` / `rFonts` / `spacing` / `ind`）
- 對「圖 N」「表 N」字串做 regex 計數比對 caption 與文字參照數
- 對照 `元智格式規範/md/R-G-A00-new.md`、`CLAUDE.md` 摘要

整體結論：
- 本輪改善幅度大：圖去重、表號分流、目錄順序、深層章節辨識、list item 行距 context — 五項已修好。
- 但 **頁碼羅馬數字 / 阿拉伯數字切換實際沒套上**（兩個 sectPr 都是 decimal）— 重大缺陷未修好。
- caption 全形冒號 `：` 未被正規化（regex 內仍只放半形 `:`）— 小缺陷殘留。
- 表號跨檔同編號（如多檔都用「表 5-6」）會經 first-seen 機制把所有正文參照導到首見序號，可能造成「不同章節的 表 X-Y 在正文皆被引用為同一個全文號」— 結構性議題未根除。
- 前置頁版型（封面 / 書名頁 / 審定書 / 中英摘要 / 誌謝 / 符號說明）仍是 placeholder（已知議題）。

---

## 1. 頁面邊距
- 規範要求：上 3.5cm、左 4cm、右 2cm、下 2cm。
- docx 實際呈現：`pgMar top=1984 bottom=1134 left=2268 right=1134` twips ≈ 上 3.50 / 下 2.00 / 左 4.00 / 右 2.00 cm。
- 是否符合：✅
- build_thesis.py 對應：`build_thesis.py:639-647`，無需修法。

## 2. 紙張尺寸
- 規範要求：A4。
- docx 實際呈現：`pgSz w=11906 h=16838` twips = 21.0 × 29.7 cm。
- 是否符合：✅

## 3. 字型
- 規範要求：中文標楷體、英文 Times New Roman。
- docx 實際呈現：抽樣 3,126 個 rFonts 標籤，全為 `eastAsia=標楷體, ascii/hAnsi=Times New Roman`。
- 是否符合：✅

## 4. 字級
- 規範要求：章名 20pt、節名 16pt、小節 14pt 粗體、正文 14pt。
- docx 實際呈現：經樣本驗證，章名 20pt、節名 16pt、subhead 14pt 粗體、正文 14pt、圖說/表說/表格內文 12pt。
- 是否符合：⚠️ 部分符合（caption 與表格內文 12pt 為設計選擇，規範未明文）。
- build_thesis.py 對應：`add_chapter_title/section/subsection/subhead/body` 一致；`add_fig_caption/table_caption/add_table` 硬寫 12pt。

## 5. 行距
- 規範要求：正文 1.2x、摘要/誌謝/參考文獻 1.5x。
- docx 實際呈現：`w:line` 分布為 `288` (=1.2x) × 2,232、`360` (=1.5x) × 54、`240` (=1.0x) × 21（圖片段落）。
- 是否符合：✅
- build_thesis.py 對應：`add_body / add_body_15x / add_list_item(line_mult=...)` 已正確切換。

## 6. 章節編號層次
- 規範要求：第一章 → 第一節 → 壹 → 一 → 1。
- docx 實際呈現：
  - 第一章 / 第一節 / 壹、皆已正確生成。
  - `（一）...` / `1、...` 已正確被歸為 subhead（14pt 粗體），非升為 Heading 2。
  - 但仍有部分純文字標題如「本節小結」「研究範圍」未走標準層次序列。
- 是否符合：⚠️ 部分符合
- build_thesis.py 對應：`RE_CN_PAREN` / `RE_NUM_SUB` 已新增（`build_thesis.py:121-122`），但 `本節小結` 這類仍因不符合任何深層 regex 而落到 fallback `'section'`（`parse_md` 末段）。
- 建議：若要完全符合，可在 `parse_md` 對「短標題且無編號」加 `subhead` fallback。

## 7. 圖編號
- 規範要求：全文連續編號、圖片下方擺圖說。
- docx 實際呈現：21 個 `<w:drawing>` 元素，每張對應一個圖說，無重複輸出。
- 是否符合：✅
- build_thesis.py 對應：`parse_md` 已恢復 `last_md_img_key` 去重（`build_thesis.py:530-535`, `573-580`）。

## 8. 表編號
- 規範要求：全文連續編號、表格上方擺表說。
- docx 實際呈現：表編號 1–28 連續，但有以下隱性議題——
  - 同一原始號碼（如 `表 5-6`）在不同 md 檔中重用時，每張會獲得獨立的全文序號（已修），但**正文中「見表 5-6」之類的文字參照仍經由 first-seen 機制全部指向首見序號**。
  - 抽樣：「表 16」在 docx 出現 3 次，其中 1 次是表說、2 次是來自不同章節的「如表 16　所示」文字參照。這 2 個參照在 md 原文都是「表 5-6」，但其實指涉的是兩張不同表（5.2 章與 5.3 章各有一張原號 5-6）。
- 是否符合：⚠️ 部分符合
- build_thesis.py 對應：`TableRegistry.first_seen`（`build_thesis.py:170-175`）。文字參照不可能完美還原，因 md 原始號碼本身已不唯一；建議的根治路徑是 md 原始號碼避免跨檔重用，或把文字參照同樣改寫成 `表 X-Ya/b` 等明確 suffix。

## 9. 圖說 / 表說位置與標點
- 規範要求：表號表名置於表上方、圖號圖名置於圖下方；編號與標題之間用全形空格。
- docx 實際呈現：
  - 位置正確（圖在上、圖說在下；表說在上、表在下）。
  - **caption 標點仍有 12 處全形冒號未被正規化**：例「圖 16：研究流程圖」「表 8：…」「表 9：…」「圖 17：…」「圖 18：…」等。
- 是否符合：❌
- build_thesis.py 對應：`normalize_caption_punct`（`build_thesis.py:182-191`）的 regex `[\s::　]+` 內兩個 `:` 都是 **ASCII 半形冒號**，沒有包含全形 `：`（U+FF1A）。已用本機 Python 實測：`re.sub(r'[\s::　]+', ..., '圖 16：標題')` 不會替換 `：`。
- 建議修法：把 regex 改為 `[\s::：　]+`（顯式列入全形 `：`），或更穩當地用 `[\s　:：]+`。

## 10. 段落首行縮排
- 規範要求：中文正文首行縮排 2 字元。
- docx 實際呈現：788 個 `<w:ind>` 段落全部設為 `firstLineChars=200, firstLine=560`（= 2 字 × 14pt × 20twips）。
- 是否符合：✅
- build_thesis.py 對應：`set_first_line_indent_chars`（`build_thesis.py:221-232`），無需修法。

## 11. 頁碼位置與格式
- 規範要求：版面底端 1cm 處中央；前置頁小寫羅馬數字（i, ii, iii）、正文阿拉伯數字（1, 2, 3）；書名頁/審定書計入但不印頁碼。
- docx 實際呈現：
  - footer 距離 = `567` twips ≈ 1.0cm ✅
  - footer 中央對齊 + PAGE field ✅
  - **section 頁碼格式檢查**：trailing sectPr × 2、inline sectPr × 1，**三者全部都是 `<w:pgNumType w:fmt="decimal" w:start="1"/>`**。羅馬數字 `lowerRoman` **完全沒套上**。
  - 結構中沒有 `titlePg` 或頁碼抑制設定，書名頁 / 審定書頁碼會直接印出。
- 是否符合：❌
- build_thesis.py 對應：`build():`
  ```
  add_front_matter(doc)
  add_section_break(doc, page_fmt='lowerRoman', start=1)
  set_section_page_format(doc.sections[0], fmt='decimal', start=1)
  ```
  問題在 `add_section_break` 插入 inline sectPr 後，python-docx 的 `doc.sections` 可能只回傳一個 section（trailing sectPr），所以 `set_section_page_format(doc.sections[0], 'decimal')` 把唯一可改的那個改成 decimal；inline sectPr 雖原本帶 lowerRoman，但 builder 內某處（疑似 `add_section_break` 把 `pgNumType` 從 last_sect 一併深拷貝過來再覆蓋）導致最終全部 decimal。
- 建議修法：
  1. 確認 `doc.sections[-1]` vs `doc.sections[0]` 在 inline sectPr 插入後的對應關係，將 decimal 設定明確指向「最後一個 section」。
  2. `add_section_break` 不要 deepcopy `pgNumType`（只 copy pgSz / pgMar / cols / docGrid）。
  3. 若 python-docx 版本不友善，改用「先建文件、走完正文、再 prepend 前置部分為新 section」的順序，避免 sectPr 順序錯亂。

## 12. 目錄 / 表目錄 / 圖目錄
- 規範要求：依 R-G-A9 順序為「目錄 → 表目錄 → 圖目錄」。
- docx 實際呈現：三個 TOC field 順序為 `TOC \\o "1-3"`（目錄）→ `TOC \\h \\z \\c "表"`（表目錄）→ `TOC \\h \\z \\c "圖"`（圖目錄）✅
- 是否符合：✅（順序已修正）
- 注意：TOC field 在 docx 內仍是空欄位，需於 Word 中按 F9 才會生成實際條目；此為 python-docx 限制，建議在繳交前的最後一步以 Word 自動更新後再另存一份。

## 13. 前置頁完整性
- 規範要求：封面 / 書名頁 / 審定書 / 中文摘要 / 英文摘要 / 誌謝 / 目錄 / 表目錄 / 圖目錄 / 符號說明 / 本文 / 參考文獻。
- docx 實際呈現（前置文字節錄）：
  - 「【封面：請依元智規範手動製作或由系所提供範本】」← placeholder
  - 「【書名頁：中英文題目 + 研究生 / 指導教授姓名】」← placeholder
  - 「【論文口試委員審定書：口試後由系所提供】」← placeholder
  - 中文摘要 / 英文摘要 / 誌謝 已有實質內容但**未排官方範本版型**（無題目 / 學號 / 指導教授 metadata 區塊）。
  - 完全沒有「符號說明」頁。
- 是否符合：❌
- build_thesis.py 對應：`add_front_matter()`（`build_thesis.py:594-633`）目前只插入 generic chapter title。
- 建議：此項屬「結構性議題」，需另行決定要 code 化專屬版型函式（`add_cover_page` / `add_title_page` / `add_abstract_with_metadata`）還是另作一份手作 docx 在交件前合併。

## 14. Heading style 套用
- 規範要求（隱含）：為了讓 TOC field 能抓到目錄條目，章 / 節 / 小節需套用 Heading 1/2/3 樣式。
- docx 實際呈現：Heading1 = 13、Heading2 = 35、Heading3 = 97 — 已正確套用。
- 是否符合：✅
- build_thesis.py 對應：`_apply_heading_style`（`build_thesis.py:269-273`）。

---

## 與 Codex 第一輪報告的對照

| 項次 | Codex 第一輪 | 本輪修補後 | 本次驗證 |
|------|-------------|-----------|---------|
| 頁邊距 | ✅ | — | ✅ |
| 字型 | ✅ | — | ✅ |
| 字級 | ⚠️ | — | ⚠️ |
| 行距 | ⚠️（list item 1.2x） | 已修 context-aware | ✅ |
| 章節層次 | ❌（（一）誤升為 H2） | 已修 | ⚠️（仍有「本節小結」類 fallback） |
| 圖編號 | ❌（重複） | 已修去重 | ✅ |
| 表編號 | ❌（碰撞） | 已修分流 | ⚠️（文字參照 first-seen 副作用） |
| caption 標點 | ⚠️（全形冒號） | **未修好**（regex 仍只半形） | ❌ |
| 首行縮排 | ✅ | — | ✅ |
| 頁碼 section | ❌ | **未修好**（仍全 decimal） | ❌ |
| 目錄順序 | ❌ | 已修 | ✅ |
| 前置頁完整性 | ❌ | placeholder（已知） | ❌ |

---

## 結論

本輪修補解決了 Codex 第一輪指出的 **6 項中的 4 項**：
- ✅ 圖去重、表號分流、目錄順序、深層章節辨識（含 list item 行距 context）

**仍未解決的 2 項**：
- ❌ **caption 全形冒號**：regex 寫錯（兩個都是半形 `:`），實測無效
- ❌ **頁碼 section 切換**：實際輸出中 inline + trailing sectPr 全為 decimal，羅馬數字未套上

**結構性議題**（非本輪範圍）：
- 前置頁版型（封面 / 書名頁 / 審定書 / 摘要 metadata / 符號說明）仍 placeholder
- 表號跨檔重用導致文字參照 first-seen 失準

若以「現在這份 `論文_組裝.docx` 能否視為元智格式 A 合格稿」判斷：**仍不能**，但離合格更近一步。
