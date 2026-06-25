# 附錄 A　量表完整題項與信度分析

本附錄補充第四章評估工具設計與第五章學習參與度分析所使用之三份量表之完整題項、計分方式、原始量表之文獻信度（Cronbach's α），以及本研究實測之信度資料。依吳穎沺老師（中央大學）口試意見補充，使讀者可完整檢視量表內容與心理計量品質。

---

## A.1　平台回饋量表（自行設計，Likert 1–5）

本量表為本研究自行設計之 5 題量表，依組別分流，題項中之「本系統」分別指涉 RR 或 Colab + the course notebooks。每題採 Likert 1–5 評分（1 = strongly disagree、5 = strongly agree）。本量表為自行設計量表，無原始文獻信度資料；本研究將以本實測樣本之 Cronbach's α 作為內部一致性參考。

### A.1.1　完整題項（原文）

| 題號 | 構面 | 原文題目（依組別微調平台名稱） |
|------|------|-------------------------------|
| 3-1 | 介面易用 | The Rein Room / Colab interface was easy to use. |
| 3-2 | 參數調整信心 | I felt confident adjusting the parameters (α, γ, ε) using the sliders / in the code. |
| 3-3 | 視覺化幫助理解 | The visualizations / charts helped me understand what the agent was learning. |
| 3-4 | 課後學習動機 | I am interested in learning more about reinforcement learning after this class. |
| 3-5 | 推薦意願 | I would recommend Rein Room / Colab + the course notebooks to someone who wants to learn about RL. |

### A.1.2　計分方式

各題以原始 Likert 1–5 分為原始分數，五題平均作為整體平台回饋分數。本量表無反向題。

### A.1.3　本研究實測信度

| 樣本範圍 | n | Cronbach's α |
|---------|---|--------------|
| RR 組（後測有效樣本） | 18 | .885 |
| Colab 組（後測有效樣本） | 12 | .825 |
| **兩組合併（全部後測有效樣本）** | **30** | **.848** |
| 兩組合併（配對樣本） | 22 | .831 |

依 Nunnally（1978）之經驗準則，α > .70 為可接受、α > .80 為良好。本量表於全部後測樣本與配對樣本下皆達 α > .80，內部一致性良好。

---

## A.2　心智負荷量表（NASA-TLX，Likert 1–10）

採用 NASA Task Load Index（Hart & Staveland, 1988; Hart, 2006）之六項分量表。原始量表為 0–100 連續刻度，本研究依教學情境調整為 1–10 之 Likert 量表，1 分代表負擔最輕、10 分代表負擔最重，俾便學生於課後問卷情境下作答。

### A.2.1　完整題項與構面定義（原文）

| 題號 | 構面（中／英）| 構面定義（原文） |
|------|-------------|------------------|
| 4-1 | 心智需求 / Mental Demand | How much mental and perceptual activity was required (e.g., thinking, deciding, calculating, remembering, looking, searching, etc.)? Was the task easy or demanding, simple or complex, exacting or forgiving? |
| 4-2 | 體力需求 / Physical Demand | How much physical activity was required (e.g., pushing, pulling, turning, controlling, activating, etc.)? Was the task easy or demanding, slow or brisk, slack or strenuous, restful or laborious? |
| 4-3 | 時間壓力 / Temporal Demand | How much time pressure did you feel due to the rate or pace at which the tasks or task elements occurred? Was the pace slow and leisurely or rapid and frantic? |
| 4-4 | 表現自評 / Performance | How successful do you think you were in accomplishing the goals of the task set by the experimenter (or yourself)? How satisfied were you with your performance in accomplishing these goals? |
| 4-5 | 努力 / Effort | How hard did you have to work (mentally and physically) to accomplish your level of performance? |
| 4-6 | 挫折感 / Frustration | How insecure, discouraged, irritated, stressed and annoyed versus secure, gratified, content, relaxed and complacent did you feel during the task? |

### A.2.2　計分方式

本研究採用「未加權版本」（Raw TLX, RTLX）——六項分項分數直接平均作為整體心智負荷指標（Byers, Bittner, & Hill, 1989; Hart, 2006）。本研究未採用原始 NASA-TLX 之兩兩配對權重程序。

### A.2.3　原始量表之文獻信度

NASA-TLX 為廣泛使用之心智負荷量表，跨研究之 Cronbach's α 報告值分佈於 .70–.85 區間（Cao et al., 2009; Hart, 2006 中提及之多項研究綜述）。

### A.2.4　本研究實測信度

| 樣本範圍 | n | Cronbach's α |
|---------|---|--------------|
| RR 組（後測有效樣本） | 18 | .727 |
| Colab 組（後測有效樣本） | 12 | .329 |
| **兩組合併（全部後測有效樣本）** | **30** | **.644** |
| 兩組合併（配對樣本） | 22 | .188 |

**信度結果說明**：

本研究於 NASA-TLX 之 Cronbach's α 結果偏低，原因可能包括：

1. **六項分項本質上量測不同向度之心智負荷**：NASA-TLX 之六項分項（心智、體力、時間、表現、努力、挫折）為設計上即為多向度（multidimensional）之構念，原始研究亦未強調其單一向度之內部一致性（Hart, 2006）。整體量表分數之效度更多依賴內容效度而非內部一致性。
2. **「表現自評」分項與其他分項方向可能相反**：高表現自評（成功完成任務）通常與低負荷相關，於本研究情境下此題與其他負荷題之相關可能為負，拉低整體 α。
3. **本研究樣本規模較小**：n = 22 至 30 之樣本規模下，Cronbach's α 估計值之穩定性受限。

實務上 NASA-TLX 較常用之分析方式為「整體分數作描述用、分項分數作推論用」。本研究於 5.3.5 即採用此模式：呈現六項分項與整體平均，並以各分項分別進行 Mann-Whitney U 檢定。

---

## A.3　系統易用性量表（SUS，Likert 1–5）

採用 Brooke（1996）之 System Usability Scale 標準十題量表，依組別微調系統名稱。題項正反向交替排列。

### A.3.1　完整題項（原文）

| 題號 | 方向 | 原文題目（依組別微調系統名稱） |
|------|------|-------------------------------|
| 5-1 | 正向 | I think that I would like to use Rein Room / Colab + notebooks frequently. |
| 5-2 | 反向 | I found Rein Room / Colab + notebooks unnecessarily complex. |
| 5-3 | 正向 | I thought Rein Room / Colab + notebooks was easy to use. |
| 5-4 | 反向 | I think that I would need the support of a technical person to be able to use Rein Room / Colab + notebooks. |
| 5-5 | 正向 | I found the various functions in Rein Room / Colab + notebooks were well integrated. |
| 5-6 | 反向 | I thought there was too much inconsistency in Rein Room / Colab + notebooks. |
| 5-7 | 正向 | I would imagine that most people would learn to use Rein Room / Colab + notebooks very quickly. |
| 5-8 | 反向 | I found Rein Room / Colab + notebooks very cumbersome to use. |
| 5-9 | 正向 | I felt very confident using Rein Room / Colab + notebooks. |
| 5-10 | 反向 | I needed to learn a lot of things before I could get going with Rein Room / Colab + notebooks. |

### A.3.2　計分方式

依 Brooke（1996）標準計分方式：
- 正向題（1、3、5、7、9）：原始分數 − 1
- 反向題（2、4、6、8、10）：5 − 原始分數
- 十題加總後乘以 2.5，得到 0–100 之百分制

### A.3.3　解讀基準

依 Bangor、Kortum 與 Miller（2009）提出之解讀標準：
- 0–50：Not Acceptable（不可接受）
- 50–70：Marginal（邊際可接受）
- 70–85：Good（好）
- 85 以上：Excellent（極佳）

### A.3.4　原始量表之文獻信度

Bangor、Kortum 與 Miller（2008）整理 2,324 份問卷之大樣本研究，報告 SUS 之 Cronbach's α = .91；Lewis 與 Sauro（2009）跨研究綜述報告 α 多分佈於 .85–.91 區間。SUS 為國際公認之高內部一致性系統易用性量表。

### A.3.5　本研究實測信度

| 樣本範圍 | n | Cronbach's α |
|---------|---|--------------|
| RR 組（後測有效樣本） | 18 | .870 |
| Colab 組（後測有效樣本） | 12 | .743 |
| **兩組合併（全部後測有效樣本）** | **30** | **.853** |
| 兩組合併（配對樣本） | 22 | .899 |

本研究實測 SUS 之 α 接近文獻報告值，內部一致性良好。

---

## A.4　開放題

三題開放式回答，作為質性補充：

| 題號 | 原文題目 |
|------|---------|
| 6-1 | What was the most helpful part of today's class? |
| 6-2 | What was the most confusing or difficult part? |
| 6-3 | Any other comments or suggestions? (optional) |

開放題回應於第 5.3.7 節以主題歸納法整理，依出現於各組之比例呈現，並於 5.3.7（三）討論兩組描述語言風格差異。

---

## A.5　量表信度彙整表

**表 A-1　本研究三份量表信度彙整**

| 量表 | 題數 | 文獻 α | 本研究 α（全部後測，n=30）| 本研究 α（配對，n=22）|
|------|------|--------|---------------------------|------------------------|
| 平台回饋量表（自行設計）| 5 | — | **.848** | .831 |
| NASA-TLX（Hart & Staveland, 1988）| 6 | .70–.85 | **.644** | .188 |
| SUS（Brooke, 1996）| 10 | .85–.91 | **.853** | .899 |

**信度評估**：

- **平台回饋量表**：本研究自行設計，全部後測樣本下 α = .848，內部一致性良好。
- **SUS**：實測值與文獻報告值接近，內部一致性良好。
- **NASA-TLX**：實測值低於文獻典型區間。如 A.2.4 所述，此一現象與 NASA-TLX 設計為多向度量表、配對樣本規模較小等因素相關。整體分數之解讀於本研究中採描述用途，分項分數則分別進行推論統計檢定（5.3.5），符合 NASA-TLX 之常見分析慣例。

---

## A.6　本附錄參考文獻

本附錄所引文獻於〈參考文獻〉一節中收錄，並列出於下：

- Bangor, A., Kortum, P., & Miller, J. T. (2008). An empirical evaluation of the System Usability Scale. *International Journal of Human-Computer Interaction*, 24(6), 574–594.
- Bangor, A., Kortum, P., & Miller, J. (2009). Determining what individual SUS scores mean: Adding an adjective rating scale. *Journal of Usability Studies*, 4(3), 114–123.
- Brooke, J. (1996). SUS: A "quick and dirty" usability scale. In P. W. Jordan, B. Thomas, B. A. Weerdmeester, & I. L. McClelland (Eds.), *Usability Evaluation in Industry* (pp. 189–194). Taylor & Francis.
- Byers, J. C., Bittner, A. C., & Hill, S. G. (1989). Traditional and raw task load index (TLX) correlations: Are paired comparisons necessary? *Advances in Industrial Ergonomics and Safety I*, 481–485.
- Cao, A., Chintamani, K. K., Pandya, A. K., & Ellis, R. D. (2009). NASA TLX: Software for assessing subjective mental workload. *Behavior Research Methods*, 41(1), 113–117.
- Hart, S. G. (2006). NASA-Task Load Index (NASA-TLX); 20 years later. *Proceedings of the Human Factors and Ergonomics Society Annual Meeting*, 50(9), 904–908.
- Hart, S. G., & Staveland, L. E. (1988). Development of NASA-TLX (Task Load Index): Results of empirical and theoretical research. In P. A. Hancock & N. Meshkati (Eds.), *Advances in Psychology* (Vol. 52, pp. 139–183). North-Holland.
- Lewis, J. R., & Sauro, J. (2009). The factor structure of the System Usability Scale. In *Human Centered Design* (pp. 94–103). Springer.
- Nunnally, J. C. (1978). *Psychometric Theory* (2nd ed.). McGraw-Hill.
