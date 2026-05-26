/**
 * 從論文 ../images/ 同步圖片到 public/images/
 * dev / build 前自動執行，確保簡報拿到最新圖
 */
import { mkdirSync, readdirSync, copyFileSync, statSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const HERE = dirname(fileURLToPath(import.meta.url))
const SRC = resolve(HERE, '../images')
const DST = resolve(HERE, 'public/images')

mkdirSync(DST, { recursive: true })
let n = 0
for (const f of readdirSync(SRC)) {
  if (!/\.(png|jpe?g|gif|svg|webp)$/i.test(f)) continue
  const s = resolve(SRC, f)
  const d = resolve(DST, f)
  copyFileSync(s, d)
  n++
}
console.log(`✓ 同步 ${n} 張圖：${SRC} → ${DST}`)
