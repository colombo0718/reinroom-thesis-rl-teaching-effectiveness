# 口試簡報

**口試時間：** 2026/6/10（三）13:00–14:00
**口試地點：** 元智一館 1311 教室
**口試委員：**
- 黃怡錚教授（指導教授）
- 吳穎沺教授（校外，中央大學網路學習科技研究所）
- 周志岳教授（校內）

**簡報時間：** 15–20 分鐘
**問答時間：** 約 40 分鐘

---

## 技術選型

採用 **Slidev**（Vue/Vite-based 簡報框架），以 Markdown 撰寫，可即時預覽、轉 PDF。

選 Slidev 而非 PowerPoint 的理由：
- 內容以 Markdown 寫，git 友善（diff 可讀）
- 內建 KaTeX / Mermaid，數學與流程圖原生漂亮
- 圖直接用論文 `images/*.png`，不需重做
- 同樣的 dev workflow（VSCode + git）

---

## 快速開始

```bash
# 安裝依賴（首次）
npm install

# 啟動 dev server（hot reload）
npm run dev
# 瀏覽器自動打開 http://localhost:3030

# 匯出 PDF（口試前最終定稿）
npm run export:pdf
```

---

## 檔案結構

```
口試簡報/
├── README.md          ← 本檔
├── 簡報大綱.md         ← 22 頁簡版大綱（參考用）
├── 簡報大綱_40頁版.md  ← 40 頁完整大綱（slides.md 依此寫）
├── slides.md          ← Slidev 主檔，實際簡報內容
├── package.json       ← 依賴
└── .gitignore
```

圖片直接從 `../images/` 引用，無需複製。

---

## 進度

- [x] 大綱（22 頁版 + 40 頁版）
- [x] Slidev 專案結構
- [x] slides.md 全 40 頁骨架
- [ ] 套主題微調（seriph）
- [ ] 5/26 帶去與老師討論
- [ ] 依老師意見刪減/重排
- [ ] 補逐頁講稿（`<!-- ... -->` 已預埋）
- [ ] 自我排練 ×3，控時 ≤ 18 分鐘
- [ ] 模擬問答（與助教 / 同學）
- [ ] 匯出最終 PDF

---

## 演講時注意事項

詳見 [簡報大綱_40頁版.md](簡報大綱_40頁版.md) 末段
