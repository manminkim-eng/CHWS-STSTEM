#!/bin/bash
# 매뉴얼 전체 재생성: 캡처 → WebP → HTML → PDF → 좁은 화면 점검   usage: bash build.sh <repoDir> <rawDir>
# 환경: MM_PW(playwright 경로) · MM_VENDOR(CDN 로컬 사본 — html2canvas · @fontsource/* · pretendard, npm pack)
# 계산 대조(독립 구현 3,000건)는 버전s-5.0.10\_검증\ (run_app.js · indep.py)
set -e; REPO="$(cd "$1" && pwd)"; RAW="$2"; mkdir -p "$RAW"; RAW="$(cd "$RAW" && pwd)"; cd "$(dirname "$0")"; M="$REPO/manual"; mkdir -p "$M/images"
node capture_chws.js "$REPO" "$RAW" > "$RAW/_log.json"
python3 - "$RAW" "$M" <<'PY'
import sys,glob,os,shutil
from PIL import Image
raw,M=sys.argv[1],sys.argv[2]
for f in sorted(glob.glob(raw+'/s*.png')): Image.open(f).convert('RGB').save(M+'/images/'+os.path.basename(f)[:-4]+'.webp',quality=82,method=6)
shutil.copy(raw+'/_marks.json',M+'/images/_marks.json'); shutil.copy(raw+'/_example.json',M+'/_tools/_example.json')
PY
MANUAL_DIR="$M" python3 gen_manual_chws.py
node pdf_chws.js "$M" CHWS_사용자매뉴얼_Ver-5.0.pdf "냉온수 배관 관경 산정 시스템 사용자 매뉴얼 Ver-5.0"
node audit_responsive.js "$M/index.html" > "$RAW/_audit.json"
