# 🌡️ 냉온수 배관 관경 산정 시스템 [MANMIN-Ver2.0]

**Engineer KIM MANMIN** | 기계설비 기술기준 기반 냉온수 배관 관경 자동 산정 PWA

---

## 📦 파일 구조

```
/
├── index.html          ← 메인 앱 (PWA 완전 통합)
├── manifest.json       ← PWA 매니페스트
├── sw.js               ← 서비스 워커 (오프라인 캐시)
├── favicon.ico         ← 브라우저 파비콘
├── .nojekyll           ← GitHub Pages Jekyll 비활성화
├── README.md           ← 이 파일
└── icons/
    ├── icon-16x16.png
    ├── icon-32x32.png
    ├── icon-48x48.png
    ├── icon-72x72.png
    ├── icon-96x96.png
    ├── icon-128x128.png
    ├── icon-144x144.png
    ├── icon-152x152.png
    ├── icon-192x192.png    ← PWA 필수
    ├── icon-384x384.png
    ├── icon-512x512.png    ← PWA 필수 (maskable)
    └── apple-touch-icon.png ← iOS 홈화면
```

---

## 🚀 GitHub Pages 배포 방법

### 1단계 — 레포지토리 생성
```
GitHub → New repository
이름: manmin-pipe (또는 원하는 이름)
Public 선택 → Create repository
```

### 2단계 — 파일 업로드
```
이 폴더의 모든 파일을 레포지토리 루트에 업로드
(icons 폴더 포함, .nojekyll 포함)
```

### 3단계 — GitHub Pages 활성화
```
레포지토리 → Settings → Pages
Source: Deploy from a branch
Branch: main / (root)
Save
```

### 4단계 — 배포 완료
```
약 1~2분 후 https://{username}.github.io/{repo-name}/ 에서 접속 가능
```

---

## 📱 PWA 설치 방법

| 기기 | 방법 |
|------|------|
| **Android Chrome** | 화면 하단 "앱 설치" 배너 또는 ⋮ 메뉴 → "앱 설치" |
| **iOS Safari** | 공유 버튼(□↑) → "홈 화면에 추가" |
| **Chrome PC** | 주소창 우측 ⊕ 아이콘 클릭 |
| **Edge PC** | 주소창 우측 앱 아이콘 또는 ⋯ 메뉴 → "이 사이트를 앱으로 설치" |

---

## ⚙️ 기술 스택

- **PWA**: Service Worker (Cache First), Web App Manifest
- **산정 공식**: William-Hazen + 연속방정식 + Darcy-Weisbach
- **적용 기준**: 기계설비 기술기준 [별표 8] 국토교통부 고시 제2021-851호
- **아이콘**: Engineer KIM MANMIN 로고 (512×512 기반 자동 리사이즈)
- **오프라인**: Service Worker 캐시로 인터넷 없이도 완전 작동

---

## 📌 주요 기능

- ✅ 강관(SGP·SCH40·SCH80) · 동관 · 스테인리스 · PVC/PE 전 재질
- ✅ 유량 직접 입력 또는 냉난방 부하 → 유량 역산 (kcal/h · kW · RT)
- ✅ 실시간 자동 산정 (입력 즉시 결과 갱신)
- ✅ A4 산정서 자동 생성 (인쇄·PDF·JPG)
- ✅ Samsung Galaxy S24 Ultra 모바일 미리보기 + 공유
- ✅ 오프라인 완전 지원 (PWA)

---

*Engineer KIM MANMIN · MANMIN-Ver2.0*
