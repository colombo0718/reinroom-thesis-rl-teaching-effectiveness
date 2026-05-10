#!/usr/bin/env bash
# download_papers.sh — 批次下載開放存取文獻 PDF 到 references/PDFs/
# 用法：bash download_papers.sh

set +e  # 個別失敗不終止其餘下載
cd "$(dirname "$0")"
mkdir -p PDFs

download() {
  local out="$1"
  local url="$2"
  local desc="$3"

  if [ -f "PDFs/$out" ] && [ -s "PDFs/$out" ]; then
    echo "✓ 已存在：$out"
    return
  fi

  echo "▶ 抓取：$desc"
  echo "  URL：$url"
  curl -L --max-time 90 -A "Mozilla/5.0" -fsS -o "PDFs/$out" "$url"
  if [ $? -eq 0 ] && [ -s "PDFs/$out" ]; then
    local size=$(du -h "PDFs/$out" | cut -f1)
    # 檢查是否真的是 PDF（前 4 bytes 應為 %PDF）
    local magic=$(head -c 4 "PDFs/$out" 2>/dev/null)
    if [ "$magic" = "%PDF" ]; then
      echo "  ✅ 成功（$size）"
    else
      echo "  ⚠️  下載成功但不是 PDF（可能是 HTML 錯誤頁），保留檔案供檢查"
    fi
  else
    echo "  ❌ 下載失敗"
    rm -f "PDFs/$out"
  fi
  echo
}

echo "=== arXiv 系列（高成功率）==="

download "Brockman_2016_OpenAI_Gym.pdf" \
  "https://arxiv.org/pdf/1606.01540.pdf" \
  "Brockman et al. (2016) OpenAI Gym"

download "Silver_2018_AlphaZero.pdf" \
  "https://arxiv.org/pdf/1712.01815.pdf" \
  "Silver et al. (2018) AlphaZero arXiv version"

download "Sallab_2017_DRL_Autonomous_Driving.pdf" \
  "https://arxiv.org/pdf/1704.02532.pdf" \
  "Sallab et al. (2017) DRL for autonomous driving"

echo "=== 開放存取期刊與會議 ==="

download "Bangor_2009_SUS_Adjective_Rating.pdf" \
  "https://uxpajournal.org/wp-content/uploads/sites/8/pdf/JUS_Bangor_May2009.pdf" \
  "Bangor et al. (2009) Determining what individual SUS scores mean"

download "Brooke_1996_SUS_Quick_Dirty.pdf" \
  "https://hell.meiert.org/core/pdf/sus.pdf" \
  "Brooke (1996) SUS: A quick and dirty usability scale"

download "Touretzky_2019_AI_for_K12.pdf" \
  "https://ojs.aaai.org/index.php/AAAI/article/view/5054/4932" \
  "Touretzky et al. (2019) Envisioning AI for K-12 (AAAI)"

download "Long_Magerko_2020_AI_Literacy.pdf" \
  "https://dl.acm.org/doi/pdf/10.1145/3313831.3376727" \
  "Long & Magerko (2020) AI Literacy CHI 2020"

echo "=== K-12 RL 教學系列（references/ 內已有解析，這裡抓原文 PDF）==="

download "Dietz_2022_ARtonomous_IDC.pdf" \
  "https://dl.acm.org/doi/pdf/10.1145/3501712.3535293" \
  "Dietz et al. (2022) ARtonomous IDC 2022"

download "Mnih_2015_DQN_Atari.pdf" \
  "https://arxiv.org/pdf/1312.5602.pdf" \
  "Mnih et al. (2015) Playing Atari with Deep RL（額外加碼）"

echo "=========================================="
echo "下載完成。結果："
ls -lh PDFs/ 2>/dev/null
