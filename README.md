# 🌡️ 냉온수 배관 관경 산정 시스템 [MANMIN-Ver2.0]

> 기계설비 기술기준 국토교통부 고시 제2021-851호 기반  
> William-Hazen / Darcy-Weisbach 방정식 자동 산정 PWA

---

## 📁 파일 구성

```
/
├── index.html              ← 메인 앱 (Single HTML)
├── manifest.json           ← PWA 매니페스트
├── sw.js                   ← Service Worker (오프라인 캐시)
├── favicon.ico             ← 파비콘
├── 404.html                ← GitHub Pages SPA 리다이렉트
├── .nojekyll               ← GitHub Pages Jekyll 비활성화
└── icons/
    ├── icon-16x16.png
    ├── icon-32x32.png
    ├── icon-48x48.png
    ├── icon-72x72.png
    ├── icon-96x96.png
    ├── icon-128x128.png
    ├── icon-144x144.png      ← Windows 타일
    ├── icon-152x152.png      ← iPad
    ├── icon-192x192.png      ← Android Chrome (필수)
    ├── icon-384x384.png
    ├── icon-512x512.png      ← Splash Screen (필수)
    └── apple-touch-icon.png  ← iOS 홈 화면 (180×180)
```

---

## 🚀 GitHub Pages 배포 방법

### 1단계 — 레포지토리 생성
```bash
# GitHub에서 새 레포 생성 후
git init
git add .
git commit -m "feat: PWA 냉온수 배관 관경 산정 시스템 v2.0"
git branch -M main
git remote add origin https://github.com/[유저명]/[레포명].git
git push -u origin main
```

### 2단계 — GitHub Pages 활성화
1. GitHub 레포 → **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **main** / **/ (root)**
4. **Save** 클릭

### 3단계 — 배포 확인
```
https://[유저명].github.io/[레포명]/
```

> ⏱ 배포까지 약 1~3분 소요

---

## 📲 PWA 설치 방법

### Android (Chrome)
- 브라우저 접속 후 **하단 배너 「설치하기」** 버튼 탭
- 또는 헤더의 **📲 앱 설치** 버튼 클릭

### iPhone / iPad (Safari)
1. Safari로 접속
2. 하단 **공유 버튼 (↑)** 탭
3. **「홈 화면에 추가」** 탭
4. **「추가」** 탭

### PC (Chrome / Edge)
- 주소창 우측 **⊕ 설치** 아이콘 클릭
- 또는 헤더 **📲 앱 설치** 버튼 클릭

---

## ⚙️ 기능

| 기능 | 설명 |
|------|------|
| 관경 자동 산정 | W-H 공식 / D-W 방정식 |
| 오프라인 지원 | Service Worker 캐시 |
| PWA 설치 | Android/iOS/PC 모두 지원 |
| A4 출력 | PDF·JPG 내보내기 |
| 반응형 | 모바일·태블릿·데스크탑 |

---

## 📜 라이선스

개인 사용 및 업무 참고용 — MANMIN Engineering  
© 2024 Engineer KIM MANMIN
