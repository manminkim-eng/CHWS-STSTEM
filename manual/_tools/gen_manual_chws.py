# -*- coding: utf-8 -*-
"""냉온수 배관 관경 산정 시스템 사용자 매뉴얼 생성기 (MANMIN 매뉴얼 공통 엔진 사용)
   실행: MANUAL_DIR=<manual 폴더> python gen_manual_chws.py  →  <manual>/index.html
   근거(원문 대조 2026-10-13):
     기계설비 기술기준 국토교통부 고시 제2021-851호(제2026-360호로 타법개정, 2026.7.8. 시행) 별표 5 · 8 — LawMCP
     KDS 31 25 25:2021 배관설비 — 국토교통부고시 「설비(기계) 설계기준(KDS 31 00 00)…」 제2026-92호(2026.3.1. 시행) 첨부 원문(hwp)
     KS D 3507 · KS D 3562 치수 — 공개 자료 교차 대조(버전s-5.0.10\\참고자료\\KS_강관치수_출처대조.md)
   예제 수치·관 규격·비교표는 캡처 때 앱에서 읽어 기록한 _example.json 에서 가져온다(손으로 옮겨 적지 않는다)."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manual_engine import fig, T, render, B
HERE = os.path.dirname(os.path.abspath(__file__))
EX = json.load(open(os.path.join(HERE, '_example.json'), encoding='utf-8'))
A, Bx, TB = EX['A'], EX['B'], EX['tables']

VER = 'Ver-5.0'
REL = 'v5.0.11'
DATE = '2026-10-13'
PDF = 'CHWS_사용자매뉴얼_Ver-5.0.pdf'
APP_URL = 'https://manminkim-eng.github.io/CHWS-STSTEM/'
KDS = 'KDS 31 25 25:2021 배관설비'
GOSI = '기계설비 기술기준 국토교통부 고시 제2021-851호(제2026-360호로 타법개정, 2026. 7. 8. 시행)'
KGOSI = '국토교통부고시 제2026-92호(2026. 3. 1. 시행, 현행)'

def n(x, d=2):
    s = f'{x:,.{d}f}'
    return s.rstrip('0').rstrip('.') if '.' in s else s
def i0(x): return f'{round(x):,}'
PUR = {'cold': '냉수 배관(냉방)', 'hot': '온수 배관(난방)', 'chiller': '냉각수 배관(냉동기)', 'general': '일반 냉온수'}
MATNM = {'steel_sgp': '강관', 'copper': '동관', 'stainless': '스테인리스', 'pvc': 'PVC/PE'}
def cand(e, s): return next(c for c in e['cands'] if c['s'] == s)
def prev(e):
    k = [c['s'] for c in e['cands']].index(e['sel']['s']); return e['cands'][k - 1]
def nxt(e):
    k = [c['s'] for c in e['cands']].index(e['sel']['s']); return e['cands'][k + 1]
SA, SB = A['sel'], Bx['sel']
PA, PB = prev(A), prev(Bx)
KW = A['loadIn']

FLOW_SVG = r"""<svg viewBox="0 0 900 200" role="img" aria-label="냉온수 관경 산정 흐름: 부하와 온도차로 유량을 구하고, 관경 후보마다 Hazen-Williams 식으로 허용 압력강하 안의 최대 유량과 연속방정식의 유속을 구해 두 조건을 모두 만족하는 가장 작은 관경을 고른다">
<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2D3A8C"/></marker></defs>
<style>.b{fill:#E9ECF8;stroke:#2D3A8C;stroke-width:1.5}.o{fill:#FDF1E7;stroke:#C97A3A;stroke-width:1.5}.t{font:600 14px 'Noto Sans KR','Noto Sans KR Local',sans-serif;fill:#1A1A2E}.s{font:12px 'Noto Sans KR','Noto Sans KR Local',sans-serif;fill:#4A4F66}.l{stroke:#2D3A8C;stroke-width:1.6;fill:none;marker-end:url(#ar)}</style>
<rect class="b" x="10" y="20" width="190" height="72" rx="10"/><text class="t" x="22" y="48">① 유량</text><text class="s" x="22" y="72">Q = H ÷ (Cp × ΔT)</text>
<rect class="b" x="230" y="20" width="200" height="72" rx="10"/><text class="t" x="242" y="48">② 압력강하 조건</text><text class="s" x="242" y="72">Hazen-Williams · I ≤ 허용값</text>
<rect class="b" x="460" y="20" width="190" height="72" rx="10"/><text class="t" x="472" y="48">③ 유속 조건</text><text class="s" x="472" y="72">V = Q ÷ (πd²/4) ≤ 목표</text>
<rect class="o" x="680" y="20" width="210" height="72" rx="10"/><text class="t" x="692" y="48">④ 관경 채택</text><text class="s" x="692" y="72">②·③ 모두 만족하는 최소</text>
<path class="l" d="M200,56 L228,56"/><path class="l" d="M430,56 L458,56"/><path class="l" d="M650,56 L678,56"/>
<rect class="b" x="230" y="118" width="420" height="62" rx="10"/><text class="t" x="242" y="144">관 규격표 — 내경 d = 외경 − 2 × 두께</text><text class="s" x="242" y="166">강관 KS D 3507 · 3562(Sch 40 · 80) · 동관 KS D 5301</text>
<path class="l" d="M440,118 L440,96"/>
</svg>"""

EXTRA_CSS = """<style>
#fig-s04_material{max-width:360px}
#fig-s05_load,#fig-s06_param,#fig-s11_flow_b,#fig-s10_history{max-width:520px}
#fig-s07_result,#fig-s08_table,#fig-s09_summary,#fig-s12_result_b{max-width:500px}
#fig-s25_a4page{max-width:560px}
#fig-s15_spec_sgp,#fig-s16_spec_cu,#fig-s17_support,#fig-s19_guide_vel,#fig-s20_guide_floor,#fig-s21_guide_formula{max-width:620px}
#fig-s22_modal,#fig-s23_modal_vel{max-width:600px}
.k1 td:first-child,.k1 th:first-child{white-space:nowrap}
@media (max-width:1240px){.eq{white-space:pre-wrap;word-break:keep-all}}
.eq .c{display:block;margin-top:2px}
.pair>div{min-width:0}
.tri{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;align-items:start}
@media (max-width:760px){.tri{grid-template-columns:1fr}}
@media print{
  figure.shot{max-width:none!important}
  figure.shot .frame{width:fit-content;max-width:100%}
  figure.shot img{width:auto;height:auto;max-width:100%;max-height:118mm}
  #fig-s25_a4page img,#fig-s08_table img,#fig-s12_result_b img,#fig-s17_support img,#fig-s19_guide_vel img{max-height:215mm}
  figure.narrow img{max-height:105mm}
  .pair{grid-template-columns:1fr 1fr}.tri{grid-template-columns:repeat(3,1fr)}
  .brk .tbl{break-inside:auto}.brk tr{break-inside:avoid}.brk thead{display:table-header-group}
}
</style>"""
K = lambda t: '<div class="k1">' + t + '</div>'
BR = lambda t: '<div class="brk">' + t + '</div>'

def res_rows(e):
    s = e['sel']
    return [
        ['설계 유량', f"{i0(e['flowKgh'])} kg/h ({n(e['lpm'], 1)} L/min)"],
        ['채택 관경', f"<b>{s['s']}</b> — 내경 {n(s['id'])} mm (외경 {n(s['od'])} · 두께 {n(s['t'])} mm)"],
        ['실제 유속', f"<b>{n(s['vel'], 3)} m/s</b> (목표 {n(e['vel'])} m/s 이하)"],
        ['실제 압력강하', f"<b>{n(s['pd'])} mmAq/m</b> (허용 {n(e['pdrop'])} mmAq/m 이하)"],
        ['최대 허용 유량', f"{i0(s['maxq'])} kg/h — 여유율 {n((s['maxq'] / e['flowKgh'] - 1) * 100, 1)} %"],
    ]

def cmp_rows(e, lo, hi):
    ss = [c['s'] for c in e['cands']]
    rows = []
    for c in e['cands'][max(0, ss.index(e['sel']['s']) - lo): ss.index(e['sel']['s']) + hi + 1]:
        mark = '◀ 채택' if c['s'] == e['sel']['s'] else ('적합' if c['ok'] else '부적합')
        rows.append([c['s'], n(c['id']), n(c['vel'], 3), n(c['pd']), i0(c['maxq']), mark])
    return rows

TOC = [
 ('ch0', '0. 이 매뉴얼에 대하여', []),
 ('ch1', '1. 한눈에 보기', [('s1-1', '화면 구성'), ('s1-2', '작업 탭·근거 표시'), ('s1-3', '설치·보관·매뉴얼')]),
 ('ch2', '2. 1분 따라하기', []),
 ('ch3', '3. 화면별 기능 상세', [('s3-1', '공사 정보'), ('s3-2', '배관 재질'), ('s3-3', '유량·부하 입력'), ('s3-4', '설계 파라미터'), ('s3-5', '산정 결과'), ('s3-6', '관경별 비교표'), ('s3-7', '핵심 수치·적용 기준'), ('s3-8', '산정 이력'), ('s3-9', '관경 표준표 탭'), ('s3-10', '배관 규격표 탭'), ('s3-11', '설계 기준 탭'), ('s3-12', '설계기준 안내 창'), ('s3-13', 'A4 미리보기·출력'), ('s3-14', '휴대전화 화면')]),
 ('ch4', '4. 기술기준 해설', [('s4-1', '근거 체계'), ('s4-2', '부하 → 유량'), ('s4-3', 'Hazen-Williams 식'), ('s4-4', '유속과 관경 채택'), ('s4-5', '단위 압력손실'), ('s4-6', 'C 계수·유속'), ('s4-7', '강관·동관 규격'), ('s4-8', '정수두·최고 사용압력'), ('s4-9', '배관 지지 간격'), ('s4-10', '계산 범위·한계'), ('s4-11', 'v5.0.10 근거·계산 정정')]),
 ('ch5', '5. 실무 작업 방법', [('s5-1', '단계별 절차'), ('s5-2', '도면 반영 전 확인'), ('s5-3', '예제 B — 동관 온수 분기관')]),
 ('ch6', '6. 문제 해결·FAQ', []),
 ('ch7', '부록', [('a1', '예제 입력값'), ('a2', '관경 표준표(30 mmAq/m)'), ('a3', '버전 변경 내역'), ('a4', '용어')]),
]
S = []
# ───────────── 0
S.append(f"""{EXTRA_CSS}<section class="ch" id="ch0"><h2><span class="n">00</span>이 매뉴얼에 대하여</h2>
<p class="lead">냉온수 배관 관경 산정 시스템은 냉 · 온수 유량(또는 냉난방 부하와 공급 · 환수 온도)을 넣으면 <b>Hazen-Williams 식</b>으로 허용 압력강하를, <b>연속방정식</b>으로 유속을 검토해 두 조건을 모두 만족하는 가장 작은 호칭지름을 고르고 A4 관경 산정서를 만듭니다.</p>
{K(T([
 ['대상 프로그램', f'냉온수 배관 관경 산정 시스템 <b>MANMIN {VER}</b>({REL}) — 탭 막대 「📘 매뉴얼」 버튼으로 이 문서가 열립니다'],
 ['접속 주소', f'<a href="{APP_URL}" target="_blank" rel="noopener">manminkim-eng.github.io/CHWS-STSTEM</a>'],
 ['매뉴얼 판', f'<b>{VER}</b> (화면 표기와 같은 판 번호, 초판) · {DATE} · 작성 김만민 건축사(㈜대성건축사사무소)'],
 ['내려받기', f'<a href="{PDF}" download>PDF(A4)</a> · <a href="../index.html">냉온수 배관 관경 산정 시스템 열기</a>'],
 ['예제', f'본문 그림은 예제 A(강관 SGP · 냉방 냉수 7/12℃ · 부하 {KW} kW · 허용 {A["pdrop"]} mmAq/m · 목표 유속 {n(A["vel"])} m/s · {A["floors"]}층 × {n(A["ht"])} m)로 캡처했습니다. 결과 <b>{SA["s"]}</b> · 유속 <b>{n(SA["vel"], 2)} m/s</b> · 압력강하 <b>{n(SA["pd"], 1)} mmAq/m</b>. 예제 B(동관 온수 50 L/min → {SB["s"]})는 <a href="#s5-3">5-3</a>'],
 ['근거 기준', f'{GOSI} [별표 8] 2.1.5 · 3.1.4 / {KDS} 1.6(4) · 4.1.5 — {KGOSI} 첨부 원문과 대조({DATE}) / 강관 치수 KS D 3507 · 3562'],
 ['읽는 순서', '처음이면 1장 → 2장(따라하기) → 필요할 때 3장(화면별 상세). 도면에 관경을 옮기기 전에는 4장(기술기준) · 5장(작업 방법)'],
], ['항목', '내용']))}
<div class="note"><b>표기</b>그림 위 주황색 번호(①②…)는 그림 아래 범례 번호와 같습니다. 그림을 누르면 크게 볼 수 있습니다. 「mmAq/m」는 배관 1 m당 압력강하(1 mmAq = 9.80665 Pa), 「A」는 호칭지름, 「C」는 Hazen-Williams 유량계수입니다.</div>
<div class="warn"><b>책임 한계</b>이 도구는 <b>배관 한 구간의 유량</b>으로 그 구간의 관경을 고릅니다. 계통 전체 마찰손실 · 펌프 양정 · 국부저항 · 팽창탱크는 계산하지 않습니다(<a href="#s4-10">4-10</a>). C 계수 · 재질별 유속은 기술기준에 수치가 없어 설비공학편람 · ASHRAE 값을 정리한 <b>MANMIN 참고값</b>입니다. 최종 관경은 설계자가 판단합니다.</div>
</section>""")

# ───────────── 1
S.append(f"""<section class="ch" id="ch1"><h2><span class="n">01</span>한눈에 보기</h2>
<p class="lead">설치 없이 브라우저에서 바로 실행되는 단일 페이지 앱(PWA)입니다. 입력한 내용은 내 PC 브라우저 안에서만 계산되며 서버로 전송되지 않습니다.</p>
<div class="cards">
<div class="card"><h5>무엇을 산정하나</h5><p>냉수 · 온수 · 냉각수 배관 한 구간의 호칭지름 — 유속 · 압력강하 · 최대 허용 유량 · 정수두</p></div>
<div class="card"><h5>배관 재질</h5><p>강관(SGP · Sch 40 · Sch 80) · 동관 · 스테인리스 · PVC/PE</p></div>
<div class="card"><h5>근거</h5><p>기계설비 기술기준 별표 8 · {KDS}</p></div>
</div>
<h3 id="s1-1">1-1. 화면 구성</h3>
{fig('s01_overview', '전체 화면 — 관경 산정 탭(예제 A)', ['작업 탭: 관경 산정 · 관경 표준표 · 배관 규격표 · 설계 기준 · A4 미리보기 · 매뉴얼', '요약 스트립: 유량 · 채택 관경 · 유속 · 압력강하 · 재질', '진행 단계: 배관 조건 → 유량 입력 → 설계 파라미터 → 산정 결과', 'STEP 1 배관 재질 · 용도 · 스케줄 · 허용 압력강하', 'STEP 2 유량 직접 입력 / 부하로 유량 환산', 'STEP 4 산정 결과 — 채택 관경 · 실제 유속', '오른쪽 아래 「초기화」 · 「설계기준 안내」'])}
{K(T([
 ['왼쪽 — 입력', 'STEP 1 배관 재질 → STEP 2 유량 · 부하 → STEP 3 설계 파라미터(목표 유속 · 층수). 값을 바꾸면 바로 다시 계산합니다(계산 버튼 없음)'],
 ['오른쪽 — 결과', '채택 관경 · 실제 유속(큰 숫자) → 내경 · 유속 · 압력강하 → 유속 게이지 → 계통 흐름도 → 관경별 비교표 → 핵심 수치 · 인접 관경 · 적용 기준'],
 ['요약 스트립', '헤더 아래 띠에 핵심 결과 5개가 늘 보입니다. 다른 탭에서도 확인할 수 있습니다'],
], ['영역', '내용']))}
<h3 id="s1-2">1-2. 작업 탭·근거 표시</h3>
{fig('s02_tabs', '헤더 — 작업 탭과 근거 표시', ['관경 산정', '관경 표준표 — 압력강하 · 유속별 관경당 유량', '배관 규격표 — 강관 · 동관 치수, 지지 간격', '설계 기준 — 산정 결과 판정 · 유속 · 마찰손실 · 층수 연동', 'A4 미리보기 — 관경 산정서 · 인쇄 · JPG', '매뉴얼(이 문서)', '근거: 기계설비 기술기준 고시 제2021-851호 · 제2026-360호 타법개정 · 2026.7.8. 시행'])}
<h3 id="s1-3">1-3. 설치·보관·매뉴얼</h3>
{K(T([
 ['설치', '주소창의 설치 아이콘 또는 휴대전화 「홈 화면에 추가」로 앱처럼 쓸 수 있습니다. 한 번 연 뒤에는 인터넷 없이도 계산됩니다'],
 ['입력값 보관', '「💾 현재 결과 저장」으로 산정 이력에 남길 수 있습니다(이 브라우저 안). 문서로 남기려면 A4 산정서(PDF · JPG)를 쓰십시오'],
 ['매뉴얼', '탭 막대 오른쪽 끝 「📘 매뉴얼」 — 인터넷 연결 시 새 창으로 열립니다'],
 ['업데이트', '새 버전이 올라오면 다음 접속 때 자동으로 바뀝니다. 화면이 예전 그대로면 새로 고침(Ctrl+F5)'],
], ['항목', '내용']))}
</section>""")

# ───────────── 2
S.append(f"""<section class="ch" id="ch2"><h2><span class="n">02</span>1분 따라하기</h2>
<p class="lead">예제 A로 6단계를 따라 하면 냉수 주관 <b>{SA['s']}</b> · 유속 <b>{n(SA['vel'], 2)} m/s</b> · 압력강하 <b>{n(SA['pd'], 1)} mmAq/m</b>가 나옵니다.</p>
<ol class="steps">
<li><b class="t">① 배관 재질</b>STEP 1에서 「강관 KS D 3507」을 누르고 배관 용도 「냉수 배관(냉방)」, 강관 스케줄 「일반(SGP)」, 허용 압력강하 「{A['pdrop']} mmAq/m — 표준」을 고릅니다(<a href="#s3-2">3-2</a>).</li>
<li><b class="t">② 부하로 유량 환산</b>STEP 2에서 「🌡️ 부하로 유량 환산」을 누르고 시스템 종류 「냉방 냉수(7℃ / 12℃)」, 부하 단위 「kW」, 부하량 {KW}을 넣습니다. 유량이 <b>{i0(A['flowKgh'])} kg/h</b>로 바뀝니다(<a href="#s3-3">3-3</a>).</li>
<li><b class="t">③ 설계 파라미터</b>STEP 3에서 설계 목표 유속 「{n(A['vel'])} m/s — 강관 권장」, 총 층수 {A['floors']}, 층 높이 {n(A['ht'])} m를 넣습니다(<a href="#s3-4">3-4</a>).</li>
<li><b class="t">④ 결과 확인</b>오른쪽 큰 숫자로 채택 관경 <b>{SA['s']}</b>(내경 {n(SA['id'])} mm) · 실제 유속 <b>{n(SA['vel'], 2)} m/s</b>를 확인합니다(<a href="#s3-5">3-5</a>).</li>
<li><b class="t">⑤ 비교표로 근거 확인</b>「관경별 유량 · 유속 비교표」에서 한 치수 아래 {PA['s']}는 유속 {n(PA['vel'], 2)} m/s로 목표 안이지만 압력강하 {n(PA['pd'], 1)} mmAq/m가 허용 {A['pdrop']}을 넘어 「부적합」임을 봅니다(<a href="#s3-6">3-6</a>).</li>
<li><b class="t">⑥ A4 산정서</b>「📄 A4 미리보기」에서 「🖨️ 인쇄 / PDF 저장」 또는 「🖼️ JPG 저장」으로 관경 산정서를 남깁니다(<a href="#s3-13">3-13</a>).</li>
</ol>
{K(T(res_rows(A), ['항목', '예제 A 결과']))}
<div class="tip"><b>확인</b>따라 한 결과가 위 표와 같으면 준비가 끝난 것입니다. 파라미터 상자의 「⚠ 10층 → 20 mmAq/m 이하 권장」과 「300 kPa 초과 — 구간별 감압밸브 검토」는 MANMIN 참고값에 따른 주의 표시입니다(<a href="#s4-8">4-8</a>). 예제 A의 실제 압력강하 {n(SA['pd'], 1)} mmAq/m는 이 권고치(20)보다도 낮습니다.</div>
</section>""")

# ───────────── 3
S.append(f"""<section class="ch" id="ch3"><h2><span class="n">03</span>화면별 기능 상세</h2>
<h3 id="s3-1">3-1. 공사 정보</h3>
{fig('s03_project', '공사 정보 — A4 산정서 표제', ['공사명', '작성일', '작성자'])}
<h3 id="s3-2">3-2. 배관 재질 (STEP 1)</h3>
{fig('s04_material', 'STEP 1 — 배관 재질 · 용도 · 허용 압력강하', ['배관 재질 4종 — 강관 · 동관 · 스테인리스 · PVC/PE', '배관 용도 — 냉수 · 온수 · 냉각수 · 일반', '강관 스케줄 — 일반(SGP) · Sch 40 · Sch 80', '허용 압력강하 — 20 · 30 · 50 mmAq/m · 직접 입력', '적용 단위 마찰손실(현재값)'])}
{K(T([
 ['배관 재질', f'C 계수와 관 규격표를 정합니다 — 강관 C {TB["types"][0]["C"]} · 동관 {TB["types"][1]["C"]} · 스테인리스 {TB["types"][2]["C"]} · PVC/PE {TB["types"][3]["C"]}. 재질을 누르면 설계 목표 유속이 그 재질의 권장 상한으로 바뀝니다'],
 ['강관 스케줄', '일반(SGP, KS D 3507) · Sch 40 · Sch 80(KS D 3562)에 따라 내경과 최대 유속(SGP 2.0 · Sch 2.5 m/s)이 바뀝니다'],
 ['스테인리스 · PVC/PE', 'SGP 호칭지름 · 내경으로 계산합니다(전용 규격표 없음 — <a href="#s4-7">4-7</a>)'],
 ['허용 압력강하', f'배관 1 m당 허용 마찰손실. {KDS} 4.1.5는 75~400 Pa/m(약 7.6~40.8 mmAq/m)를 권장합니다. 50 mmAq/m(약 490 Pa/m)는 이 범위를 넘어 「KDS 권장 초과」로 표시됩니다'],
 ['배관 용도', 'A4 산정서와 흐름도 표기용입니다. 관경 계산에는 영향이 없습니다'],
], ['항목', '내용']))}
<h3 id="s3-3">3-3. 유량·부하 입력 (STEP 2)</h3>
{fig('s05_load', 'STEP 2 — 부하로 유량 환산(예제 A)', ['입력 방식 — 유량 직접 입력 / 부하로 유량 환산', '시스템 종류 — 냉방 냉수 · 난방 온수 · 냉각수 · 고온 온수(온도 자동 설정)', '부하 단위 — kcal/h · kW · 냉동톤', '부하량', '공급 · 환수 온도 → ΔT', '부하 전환산 결과 — kcal/h · kW · 냉동톤 · 유량', '유량 · 부하 실시간 연동'])}
{K(T([
 ['부하로 유량 환산', f'유량 = 부하(kcal/h) ÷ (비열 1 kcal/kg·℃ × ΔT). 예제 A: {KW} kW × 860 = {i0(A["loadKcalh"])} kcal/h ÷ {n(A["dt"])} ℃ = <b>{i0(A["flowKgh"])} kg/h</b>'],
 ['유량 직접 입력', 'kg/h · L/min · ㎥/h 가운데 하나로 넣습니다. 나머지 단위와 역산 부하가 함께 표시됩니다(<a href="#s5-3">5-3</a>)'],
 ['시스템 종류', '냉방 냉수 7/12℃ · 난방 온수 45/40℃ · 냉각수 32/37℃ · 고온 온수 60/50℃. 「직접 설정」이면 온도를 손으로 넣습니다'],
 ['냉동톤', '3,024 kcal/h(미국 냉동톤, USRT)로 환산합니다'],
], ['항목', '내용']))}
<h3 id="s3-4">3-4. 설계 파라미터 (STEP 3)</h3>
{fig('s06_param', 'STEP 3 — 설계 목표 유속 · 층수 · 연동 파라미터', ['설계 목표 유속', '총 층수', '층 높이', '압력강하 기준 — Pa/m 환산 · KDS 범위 · 층수 권고', '최대 유속(MANMIN 참고 상한)', '정수두 — 300 kPa 참고 경고'])}
{K(T([
 ['설계 목표 유속', '이 유속 이하가 되는 관경을 고릅니다. 낮출수록 관경이 커집니다. 재질 최대 유속보다 높게 넣으면 경고가 뜹니다'],
 ['압력강하 기준', f'입력값을 Pa/m로 함께 보여 줍니다(예제 A {A["pdrop"]} mmAq/m = {i0(A["pdPa"])} Pa/m). 75~400 Pa/m 밖이면 「KDS 31 25 25 권장 75~400 Pa/m 밖」 경고'],
 ['층수 · 층 높이', '정수두(층수 × 층 높이 × 9.81 kPa/m)와 층수별 압력강하 권고(10층 이상 20 · 15층 이상 15 mmAq/m, MANMIN 참고값)에 씁니다. 관경 계산에는 영향이 없습니다'],
], ['항목', '내용']))}
<h3 id="s3-5">3-5. 산정 결과 (STEP 4)</h3>
{fig('s07_result', '산정 결과 — 예제 A', ['채택 관경 · 실제 유속', '내경 · 유속 · 압력강하', '유속 적정성 게이지 — 실제 / 목표 / 최대', '배관 계통 흐름도'])}
<p>유속 게이지는 권장 범위(강관 1~2 m/s) 안이면 「✅ 정상 범위」, 하한 미만이면 「🔵 퇴적 주의」, 상한 초과면 「🟡 수격방지 검토」를 표시합니다. 채택 관경 배지는 두 조건을 모두 만족하면 초록, 하나라도 못 맞추면 주황 · 빨강입니다.</p>
<h3 id="s3-6">3-6. 관경별 유량·유속 비교표</h3>
{fig('s08_table', '관경별 유량 · 유속 비교표 — 예제 A', ['관경 · 내경 · 유속 · 압력강하 · 최대 허용 유량 · 판정', '채택 관경 행(◀)'])}
{BR(T(cmp_rows(A, 2, 2), ['관경', '내경 mm', '유속 m/s', '압력강하 mmAq/m', '최대유량 kg/h', '판정'], (1, 2, 3, 4)))}
<p>「적합」은 <b>설계 유량 ≤ 최대 허용 유량</b>(= 실제 압력강하 ≤ 허용값)과 <b>실제 유속 ≤ 목표 유속</b>을 모두 만족한다는 뜻입니다. 예제 A의 {PA['s']}는 유속은 목표 안이지만 압력강하가 허용값을 넘어 부적합입니다 — 이 예제에서는 압력강하가 관경을 정했습니다.</p>
<h3 id="s3-7">3-7. 핵심 수치·적용 기준</h3>
{fig('s09_summary', '관경 산정 핵심 수치 · 인접 관경 비교 · 적용 기준', ['채택 관경', '압력강하(실제)', '적용 공식 — Q = 0.27853 × C × d²·⁶³ × I⁰·⁵⁴', '인접 관경 비교', '적용 기준 — 별표 8 2.1.5 · KDS 31 25 25 4.1.5'])}
<h3 id="s3-8">3-8. 산정 이력</h3>
{fig('s10_history', '산정 이력 — 「💾 현재 결과 저장」', ['저장된 결과 — 관경 · 재질 · 유량 · 유속 · 압력강하', '현재 결과 저장 · 전체삭제'])}
<p>구간마다 결과를 저장해 두면 주관 · 분기관을 차례로 비교할 수 있습니다. 이력은 이 브라우저에만 남습니다.</p>
<h3 id="s3-9">3-9. 관경 표준표 탭</h3>
{fig('s13_std', '압력강하별 관경 선정표(강관 SGP, C = 120)', ['기준 선택 — 20 · 30 mmAq/m · 유속 2 · 3 m/s', '100A', '125A'])}
{fig('s14_ctable', '재질별 Hazen-Williams C 계수 및 권장 유속', ['C 계수 · 권장 · 최대 유속', 'MANMIN 참고값 근거'])}
<p>표준표는 관경마다 허용 압력강하(또는 유속) 안에서 흘릴 수 있는 최대 유량입니다. 예제 A({i0(A['flowKgh'])} kg/h)는 30 mmAq/m 표에서 100A(48,639)를 넘고 125A(86,036) 안이므로 125A입니다 — 3-6의 결과와 같습니다. 전체 표는 <a href="#a2">부록 A2</a>.</p>
<h3 id="s3-10">3-10. 배관 규격표 탭</h3>
<div class="pair"><div>{fig('s15_spec_sgp', '강관 일반(KS D 3507) — 외경 · 두께 · 내경 · 단면적')}</div><div>{fig('s16_spec_cu', '동관(KS D 5301) — 외경 · 두께 · 내경 · 단면적')}</div></div>
{fig('s17_support', '배관 지지 간격(별표 8 3.1.4 표 1)')}
<h3 id="s3-11">3-11. 설계 기준 탭</h3>
{fig('s18_guide_judge', '현재 산정 결과 종합 판정 — 예제 A', ['층수 · 층높이 연동 분석 — 정수두 · 압력강하 권고 · 감압 예비판정'])}
<div class="pair"><div>{fig('s19_guide_vel', '유속 기준 · 단위 마찰손실 기준')}</div><div>{fig('s20_guide_floor', '총 층수 · 층높이 연동 로직')}{fig('s21_guide_formula', '관경 산정 공식 해설')}</div></div>
<h3 id="s3-12">3-12. 설계기준 안내 창</h3>
<div class="pair"><div>{fig('s22_modal', '오른쪽 아래 「설계기준 안내」 — 이용방법')}</div><div>{fig('s23_modal_vel', '유속 기준 탭')}</div></div>
<h3 id="s3-13">3-13. A4 미리보기·출력</h3>
{fig('s24_a4', 'A4 미리보기 탭', ['인쇄 / PDF 저장', 'JPG 저장', 'A4 관경 산정서'])}
{fig('s25_a4page', 'A4 관경 산정서 — 예제 A', ['1. 설계 입력 조건', '2. 관경 산정 결과', '3. 인접 관경 비교표', '4. 적용 기준 및 계산 공식'])}
{K(T([
 ['인쇄 / PDF', '브라우저 인쇄 창에서 「PDF로 저장」을 고르면 PDF가 됩니다. 배경색 인쇄를 켜 두십시오'],
 ['JPG 저장', 'A4 쪽 단위 그림으로 저장합니다. 미리보기 창에서 쪽마다 확인 후 저장합니다'],
 ['4. 적용 기준', 'Hazen-Williams 식 · 연속방정식 · C 계수 · 채택 원칙 · 적용 기술기준(별표 8 2.1.5) · 설계기준(KDS 31 25 25 4.1.5)'],
], ['항목', '내용']))}
<h3 id="s3-14">3-14. 휴대전화 화면</h3>
<div class="tri"><div>{fig('s26_mobile_main', '입력', narrow=True)}</div><div>{fig('s27_mobile_result', '결과', narrow=True)}</div><div>{fig('s28_mobile_a4', 'A4 미리보기', narrow=True)}</div></div>
<p>좁은 화면에서는 입력 → 결과가 한 줄로 쌓입니다. 탭 막대는 화면 폭보다 길어 좌우로 밀어서 「설계 기준」 · 「A4 미리보기」 · 「매뉴얼」을 엽니다.</p>
</section>""")

# ───────────── 4
pa_chk = A['flowKgh'] / 3.6e6
S.append(f"""<section class="ch" id="ch4"><h2><span class="n">04</span>기술기준 해설</h2>
<h3 id="s4-1">4-1. 근거 체계</h3>
{K(T([
 [f'기계설비 기술기준 [별표 8] 2.1.5', '냉 · 온수 배관 「단위마찰손실과 유속을 기준으로 배관 호칭지름을 결정한다」 — 판단 기준(수치 없음)'],
 [f'{KDS} 4.1.5', '단위 압력손실과 유속을 기준으로 관경을 결정하고, 초기투자비와 운영비를 고려하여 <b>75~400 Pa/m</b> 압력손실을 권장. 배관마찰 저항선도 또는 식은 설비공학편람 제1권 제17장 또는 ASHRAE Handbook Fundamentals Ch.22 참조'],
 [f'{KDS} 4.2.2', '냉각수배관 관지름 선정은 4.1(냉온수 배관)에 따름'],
 [f'{KDS} 1.6(4)', '배관계통 최고 사용압력은 1 MPa 이하가 바람직, 부득이 초과 시 그 압력에 맞는 재료 사용'],
 ['기계설비 기술기준 [별표 8] 3.1.4 표 1', '배관 지지 간격(KCS 31 20 15 표 3.4-1 · 3.12-1 준용)'],
 ['KS D 3507 · 3562 · 5301', '강관(SGP · Sch 40 · Sch 80) · 동관 치수 — 내경 = 외경 − 2 × 두께'],
 ['MANMIN 참고값', 'C 계수 · 재질별 권장 · 최대 유속 · 층수별 압력강하 권고 · 정수두 300 kPa 경고 — 기술기준에 수치가 없는 값'],
], ['근거', '내용']))}
<p class="mono" style="font-size:13px;color:var(--text2)">기계설비 기술기준: 국토교통부 고시 제2021-851호(2021.6.7. 제정 시행), 제2026-360호(2026.7.8. 타법개정 · 시행) · KDS 31 25 25:2021(2021.2.19. 개정) — {KGOSI} 첨부 전문</p>
<h3 id="s4-2">4-2. 부하 → 유량</h3>
<div class="eq">G = H ÷ (Cp × ΔT)<span class="c">G 유량(kg/h) · H 부하(kcal/h) · Cp 물의 비열 1 kcal/kg·℃ · ΔT 공급 · 환수 온도차(℃)</span></div>
<div class="eq">{KW} kW × 860 = {i0(A['loadKcalh'])} kcal/h &nbsp;→&nbsp; {i0(A['loadKcalh'])} ÷ (1 × {n(A['dt'])}) = {i0(A['flowKgh'])} kg/h = {n(A['lpm'], 1)} L/min<span class="c">예제 A — 냉방 냉수 7℃ / 12℃</span></div>
<p>1 kW = 860 kcal/h, 1 냉동톤(USRT) = 3,024 kcal/h로 환산합니다. 물의 밀도는 1,000 kg/㎥로 보고 kg/h를 ㎥/s로 바꿉니다.</p>
<h3 id="s4-3">4-3. Hazen-Williams 식</h3>
<div class="eq">Q = 0.27853 × C × d<sup>2.63</sup> × I<sup>0.54</sup><span class="c">Q 유량(㎥/s) · C 유량계수 · d 내경(m) · I 동수경사(m/m) = 압력강하(mmAq/m) ÷ 1,000</span></div>
<div class="eq">V = 0.35464 × C × d<sup>0.63</sup> × I<sup>0.54</sup> &nbsp;·&nbsp; Q = V × πd²/4 &nbsp;→&nbsp; 0.35464 × π/4 = 0.27853<span class="c">유속식과 유량식의 관계</span></div>
<p>관경 후보마다 허용 압력강하에서의 <b>최대 허용 유량</b>을 구하고, 설계 유량을 넣어 <b>실제 압력강하</b>를 역산합니다.</p>
<div class="eq">I = [ Q ÷ (0.27853 × C × d<sup>2.63</sup>) ]<sup>1/0.54</sup><span class="c">실제 압력강하(역산)</span></div>
<div class="eq">{SA['s']}: Q<sub>max</sub> = 0.27853 × {A['C']} × {n(SA['id'] / 1000, 4)}<sup>2.63</sup> × 0.0{A['pdrop']}<sup>0.54</sup> = {n(SA['maxq'] / 3.6e6, 5)} ㎥/s = {i0(SA['maxq'])} kg/h ≥ {i0(A['flowKgh'])} ✓<span class="c">예제 A — 실제 압력강하 {n(SA['pd'])} mmAq/m</span></div>
<h3 id="s4-4">4-4. 유속과 관경 채택</h3>
<div class="eq">V = Q ÷ (πd²/4) &nbsp;·&nbsp; d<sub>min</sub> = √(4Q ÷ πV<sub>목표</sub>)<span class="c">연속방정식</span></div>
<div class="eq">d<sub>min</sub> = √(4 × {n(pa_chk, 5)} ÷ (π × {n(A['vel'])})) = {n(A['minIdByVel'], 1)} mm<span class="c">예제 A — 유속만 보면 내경 {n(A['minIdByVel'], 1)} mm 이상(100A 내경 105.3 mm로 충분)</span></div>
{K(T([
 ['① 채택', '압력강하 조건(설계 유량 ≤ 최대 허용 유량)과 유속 조건(실제 유속 ≤ 목표 유속)을 모두 만족하는 가장 작은 관경'],
 ['② 없으면', '재질 최대 유속을 넘지 않는 가장 작은 관경(주황 배지 — 압력강하 또는 목표 유속 초과)'],
 ['③ 그래도 없으면', '목록의 가장 큰 관경(빨강 배지 — 최대 유속 초과)'],
], ['순서', '내용']))}
<p>예제 A는 유속 조건만이면 100A지만 100A의 압력강하가 {n(PA['pd'], 1)} mmAq/m로 허용 {A['pdrop']}을 넘어 125A가 됩니다.</p>
<h3 id="s4-5">4-5. 단위 압력손실</h3>
{BR(T([
 ['20', i0(20 * 9.80665), '권장 범위 안 — 고층 · 장거리'],
 ['30', i0(30 * 9.80665), '권장 범위 안 — 표준'],
 ['40.8', '400', 'KDS 권장 상한'],
 ['50', i0(50 * 9.80665), '권장 범위 초과 — 「KDS 권장 초과」 표시'],
], ['mmAq/m', 'Pa/m', 'KDS 31 25 25 4.1.5(75~400 Pa/m)'], (0, 1)))}
<p>층수별 권고(10층 이상 20 · 15층 이상 15 mmAq/m)는 입상관이 길어 누적 손실이 커지는 것을 줄이려는 MANMIN 참고값입니다.</p>
<h3 id="s4-6">4-6. C 계수·유속 (MANMIN 참고값)</h3>
{BR(T([[t['nm'], str(t['C']), str(t['Ca']), f"{t['vrec'][0]:.1f} ~ {t['vrec'][1]:.1f}", ('2.0 (Sch 2.5)' if t['id'] == 'steel_sgp' else f"{t['vmax']:.1f}")] for t in TB['types']],
 ['재질', 'C 신설', 'C 노후', '권장 유속 m/s', '최대 유속 m/s'], (1, 2, 3)))}
<div class="note"><b>근거</b>기계설비 기술기준 별표 8과 {KDS}에는 C 계수와 재질별 유속 수치가 없습니다. KDS 31 25 25 4.1.5가 참조하도록 정한 설비공학편람 · ASHRAE 값을 정리한 것이며, 계산은 신설 C를 씁니다. 노후 C는 20년 뒤 성능을 볼 때 참고합니다.</div>
<h3 id="s4-7">4-7. 강관·동관 규격</h3>
{BR(T([[p['s'], f"{p['od']:.1f}", f"{p['t']:.1f}", f"{p['id']:.2f}"] + [f"{next(q['t'] for q in TB['sch40'] if q['s'] == p['s']):.1f}"] for p in TB['steel'] if p['s'] in ('15A','25A','50A','80A','100A','125A','150A','200A','300A')],
 ['호칭', '외경 mm', 'SGP 두께', 'SGP 내경', 'Sch 40 두께'], (1, 2, 3, 4)))}
<p>강관은 KS D 3507(SGP) · KS D 3562(Sch 40 · 80) 외경 · 두께에서 내경을 계산합니다(JIS G 3452 · 3454와 같은 값). 400A 이상 SGP 두께는 KS 원문 확인 전 JIS 값 7.9 mm를 씁니다. 동관은 KS D 5301 L형, 스테인리스 · PVC/PE는 SGP 호칭지름 · 내경으로 계산합니다(전용 규격표 추가는 향후 과제).</p>
<h3 id="s4-8">4-8. 정수두·최고 사용압력</h3>
<div class="eq">정수두 = 층수 × 층 높이 × 9.81 kPa/m &nbsp;→&nbsp; {A['floors']} × {n(A['ht'])} × 9.81 = {n(A['staticKpa'], 1)} kPa<span class="c">예제 A</span></div>
{K(T([
 [f'{KDS} 1.6(4)', '배관계통 최고 사용압력 1 MPa 이하 권장 — 초과 시 그 압력에 맞는 재료'],
 ['정수두 300 kPa 경고', 'MANMIN 참고값 — 구간별 감압 · 압력 등급 검토를 알리는 표시'],
 ['별표 5 2.1.7(550 kPa)', '<b>위생기구 급수압</b> 기준(감압밸브 또는 급수 조닝)입니다. 냉 · 온수 밀폐계에는 적용하지 않습니다'],
], ['기준', '내용']))}
<h3 id="s4-9">4-9. 배관 지지 간격 (별표 8 3.1.4 표 1)</h3>
{BR(T([
 ['강관', '20A 이하 1.8 · 25~40A 2.0 · 50~80A 3.0 · 100~150A 4.0 · 200A 이상 5.0 m 이내'],
 ['동관 · 스테인리스관', '20A 이하 1.0 · 25~40A 1.5 · 50A 2.0 · 65~100A 2.5 · 125A 이상 3.0 m 이내'],
 ['경질 염화 비닐관', '16A 이하 0.75 · 20~40A 1.0 · 50A 1.2 · 65~125A 1.5 · 150A 이상 2.0 m 이내'],
 ['수직관', '각 층에 1개소 이상 · 실내 수직관은 각 층 흔들림 방지철물(3.1.4(2)) · 동관 · 스테인리스강관은 절연조치(3.1.4(3))'],
], ['배관', '지지 간격']))}
<h3 id="s4-10">4-10. 계산 범위·한계</h3>
{K(T([
 ['계산하는 것', '배관 한 구간의 관경 · 유속 · 단위 압력강하 · 최대 허용 유량 · 정수두'],
 ['계산하지 않는 것', '계통 전체 마찰손실(직관 길이 · 국부저항) · 펌프 양정 · 팽창탱크 · 유체 온도에 따른 점도 보정 · 부동액'],
 ['유량 기준', '열원회로 · 주배관은 건축물 부하의 최댓값, 가지배관은 각 존의 시간대별 최대부하 기준(KDS 31 25 25 4.1.1(3))'],
 ['Darcy-Weisbach', '공식 해설에만 소개합니다. 계산은 Hazen-Williams 식입니다'],
], ['항목', '내용']))}
<h3 id="s4-11">4-11. v5.0.10 근거·계산 정정 (2026-10-13)</h3>
{BR(K(T([
 ['Hazen-Williams 상수', '유량식에 유속식 상수 0.35464를 쓰고 있었음 → 최대 허용 유량 1.27배 과대 · 압력강하 표시 1/1.57 과소', '0.27853으로 정정 — 무작위 3,000건 독립 구현 대조 불일치 0'],
 ['강관 규격표', 'SGP 내경 칸에 동관 내경 · Sch 표에 ASME 외경', 'KS D 3507 · 3562 외경 · 두께로 내경 재계산'],
 ['개정 구분', '「제2026-360호 일부개정」', '「타법개정」'],
 ['근거 표기', '유속 · C 계수 · 압력강하를 별표 8 근거로 표기 · 550 kPa 감압 「의무」', '별표 8 2.1.5 + KDS 31 25 25 4.1.5 · MANMIN 참고값 표기 · 1 MPa(1.6(4))'],
 ['지지 간격', '구간 · 수직관 값이 원문과 다름', '별표 8 3.1.4 표 1 원문'],
], ['항목', '기존', '정정'])))}
<p>정정 전 판으로 고른 관경은 무작위 3,000건 가운데 약 16 %가 바뀝니다. 이전 산정서가 있으면 다시 확인하십시오.</p>
</section>""")

# ───────────── 5
S.append(f"""<section class="ch" id="ch5"><h2><span class="n">05</span>실무 작업 방법</h2>
<h3 id="s5-1">5-1. 단계별 절차</h3>
<div class="svgbox">{FLOW_SVG}</div>
{K(T([
 ['① 구간 나누기', '열원 출구 → 주관 → 입상관 → 층 분기관 → 터미널 순으로 구간을 나누고 구간마다 담당 부하(또는 유량)를 정합니다'],
 ['② 조건 정하기', '재질 · 스케줄 · 허용 압력강하(KDS 75~400 Pa/m 안) · 목표 유속을 정합니다. 고층이면 압력강하를 낮춥니다'],
 ['③ 구간별 산정', '구간마다 유량을 넣고 결과를 「💾 현재 결과 저장」으로 남깁니다'],
 ['④ 대조', '관경 표준표 탭과 비교표로 근거를 확인합니다. 흐름 방향으로 관경이 커지지 않는지 봅니다'],
 ['⑤ 출력', '주관 · 대표 구간의 A4 산정서를 PDF로 남겨 설계도서에 붙입니다'],
], ['단계', '내용']))}
<h3 id="s5-2">5-2. 도면 반영 전 확인</h3>
{K(T([
 ['유량', '부하 단위(kW · kcal/h · 냉동톤)와 공급 · 환수 온도가 장비 사양과 같은가'],
 ['압력강하', f'실제 압력강하가 KDS 권장(75~400 Pa/m) 안인가 — 예제 A {n(SA["pd"], 1)} mmAq/m ≈ {i0(SA["pd"] * 9.80665)} Pa/m'],
 ['유속', '권장 범위 하한(퇴적) · 상한(소음 · 수격)을 벗어나지 않는가'],
 ['압력', '정수두 + 펌프 양정이 배관 · 밸브 최고 사용압력(1 MPa 권장) 안인가'],
 ['지지', '지지 간격 · 신축이음 · 공기빼기 · 물빼기 밸브(별표 8 2.1 · 3.1)'],
], ['항목', '확인']))}
<h3 id="s5-3">5-3. 예제 B — 동관 온수 분기관</h3>
<div class="pair"><div>{fig('s11_flow_b', 'STEP 2 — 유량 직접 입력(예제 B)', ['유량 직접 입력', '유량 단위 L/min', '유량 50', 'kg/h · L/min · ㎥/h · ㎥/s · 역산 부하'])}</div><div>{fig('s12_result_b', '산정 결과 — 예제 B', [f'동관 {SB["s"]} · 유속 {n(SB["vel"], 2)} m/s(권장 하한 미만 — 퇴적 주의)', f'관경별 비교표 — {PB["s"]}는 압력강하 {n(PB["pd"], 1)} mmAq/m로 부적합'])}</div></div>
{K(T([
 ['조건', f'동관(C {Bx["C"]}) · 온수 · 유량 {n(Bx["flowIn"])} L/min({i0(Bx["flowKgh"])} kg/h) · 허용 {Bx["pdrop"]} mmAq/m · 목표 유속 {n(Bx["vel"])} m/s · {Bx["floors"]}층 × {n(Bx["ht"])} m'],
 ['결과', f'<b>{SB["s"]}</b>(내경 {n(SB["id"])} mm) · 유속 {n(SB["vel"], 3)} m/s · 압력강하 {n(SB["pd"])} mmAq/m · 최대 유량 {i0(SB["maxq"])} kg/h'],
 ['판단', f'{PB["s"]}는 유속 {n(PB["vel"], 3)} m/s로 목표 안이지만 압력강하 {n(PB["pd"], 1)} mmAq/m가 허용 {Bx["pdrop"]}을 넘습니다. {SB["s"]}의 유속 {n(SB["vel"], 2)} m/s는 권장 하한 1.0 m/s보다 낮아 「퇴적 주의」가 뜹니다 — 허용 압력강하를 높이거나(KDS 범위 안) 그대로 둘지 설계자가 판단합니다'],
], ['항목', '내용']))}
{BR(T(cmp_rows(Bx, 2, 1), ['관경', '내경 mm', '유속 m/s', '압력강하 mmAq/m', '최대유량 kg/h', '판정'], (1, 2, 3, 4)))}
</section>""")

# ───────────── 6
S.append(f"""<section class="ch" id="ch6"><h2><span class="n">06</span>문제 해결·FAQ</h2>
{K(T([
 ['결과가 「대기」로 남아요', '유량이 0입니다. STEP 2에서 유량을 넣거나 부하 · 온도를 넣으십시오. 공급 · 환수 온도를 같게 넣으면 ΔT를 1 ℃로 보고 계산하므로 유량이 크게 나옵니다 — 온도를 확인하십시오'],
 ['채택 관경이 주황 · 빨강이에요', '두 조건을 동시에 만족하는 관경이 목록에 없습니다. 목표 유속을 높이거나(재질 최대 안) 허용 압력강하를 조정하거나 재질 · 스케줄을 바꾸십시오'],
 ['압력강하 「KDS 권장 범위 밖」 경고', '입력한 허용 압력강하가 75~400 Pa/m(약 7.6~40.8 mmAq/m) 밖입니다. 계산은 그대로 진행되며 설계자가 판단합니다'],
 ['예전 산정서와 관경이 달라요', 'v5.0.10(2026-10-13)에서 Hazen-Williams 상수와 강관 내경을 정정했습니다(<a href="#s4-11">4-11</a>). 새 판 결과를 쓰십시오'],
 ['감압밸브 경고가 떠요', '정수두 300 kPa 이상일 때의 MANMIN 참고 경고입니다. 배관 · 밸브 압력 등급과 계통 분리를 검토하십시오(<a href="#s4-8">4-8</a>)'],
 ['스테인리스 관경이 강관과 같아요', '스테인리스 · PVC/PE는 SGP 호칭지름 · 내경으로 계산합니다. C 계수만 다릅니다'],
 ['휴대전화에서 탭이 다 안 보여요', '탭 막대를 좌우로 밀면 나머지 탭과 「📘 매뉴얼」이 나옵니다'],
 ['화면이 예전 판이에요', '새로 고침(Ctrl+F5) 또는 앱을 닫았다 다시 여십시오'],
], ['증상', '해결']))}
</section>""")

# ───────────── 부록
std = EX['std30']
S.append(f"""<section class="ch" id="ch7"><h2><span class="n">부록</span></h2>
<h3 id="a1">A1. 예제 입력값</h3>
{K(T([
 ['배관', f"강관 SGP(C {A['C']}) · {PUR[A['purpose']]}", f"동관 KS D 5301(C {Bx['C']}) · {PUR[Bx['purpose']]}"],
 ['유량', f"부하 {KW} kW · {n(A['ts'])}/{n(A['tr'])}℃ → {i0(A['flowKgh'])} kg/h", f"{n(Bx['flowIn'])} L/min → {i0(Bx['flowKgh'])} kg/h"],
 ['조건', f"허용 {A['pdrop']} mmAq/m · 목표 {n(A['vel'])} m/s · {A['floors']}층 × {n(A['ht'])} m", f"허용 {Bx['pdrop']} mmAq/m · 목표 {n(Bx['vel'])} m/s · {Bx['floors']}층 × {n(Bx['ht'])} m"],
 ['결과', f"{SA['s']} · {n(SA['vel'], 3)} m/s · {n(SA['pd'])} mmAq/m", f"{SB['s']} · {n(SB['vel'], 3)} m/s · {n(SB['pd'])} mmAq/m"],
], ['항목', '예제 A', '예제 B']))}
<h3 id="a2">A2. 관경 표준표 — 강관 SGP · C 120 · 30 mmAq/m</h3>
{BR(T([[r[0], r[1], r[2], r[3]] for r in std], ['관경', '내경 mm', '최대유량 kg/h', '최대유량 L/min'], (1, 2, 3)))}
<h3 id="a3">A3. 버전 변경 내역</h3>
{K(T([
 ['Ver-5.0 · v5.0.11 (2026-10-13)', '사용자 매뉴얼 연결(탭 막대 「📘 매뉴얼」) · 유속 기준 카드 · A4 적용 기술기준 표기 정정 · 부하 단위 표시 · 표준표 첫 버튼 · 부하 입력 모드 유량 반올림 재계산 정정'],
 ['Ver-5.0 · v5.0.10 (2026-10-13)', 'Hazen-Williams 유량식 상수 0.27853 · 강관 규격 KS D 3507 · 3562 · 「타법개정」 · KDS 31 25 25 4.1.5 표기 · 지지 간격 원문 · 위생배관 차용 문구 삭제(<a href="#s4-11">4-11</a>)'],
 ['Ver-5.0 · v5.0.0 ~ v5.0.9 (2026-08 ~ 09)', '디자인 통일(헤더 · 탭 막대 · 요약 스트립), A4 미리보기 · JPG 저장, 오프라인 캐시 개선'],
], ['버전', '내용']))}
<h3 id="a4">A4. 용어</h3>
{BR(K(T([
 ['Hazen-Williams 식', '물 배관의 마찰손실을 유량 · 내경 · 유량계수(C)로 나타낸 경험식'],
 ['C 계수', '관 내면 거칠기를 나타내는 유량계수 — 클수록 매끄러움'],
 ['동수경사(I)', '배관 1 m당 수두 손실(m/m) — 압력강하(mmAq/m) ÷ 1,000'],
 ['단위 압력손실', '배관 1 m당 압력강하 — mmAq/m 또는 Pa/m'],
 ['ΔT', '공급 · 환수 온도차(℃)'],
 ['SGP · Sch', 'SGP = 배관용 탄소강관(KS D 3507), Sch 40 · 80 = 압력배관용 탄소강관(KS D 3562) 두께 계열'],
 ['정수두', '배관 높이차에 따른 정지 수압(kPa) — 높이(m) × 9.81'],
 ['USRT', '미국 냉동톤 — 3,024 kcal/h'],
], ['용어', '뜻'])))}
</section>""")

html = render(title=f'냉온수 배관 관경 산정 시스템 사용자 매뉴얼 {VER} · MANMIN',
              desc=f'냉온수 배관 관경 산정 시스템 MANMIN {VER} 사용자 매뉴얼 — 화면 기능, 기술기준(기계설비 기술기준 별표 8 · KDS 31 25 25), 실무 작업 방법',
              eyebrow='MANMIN ENGINEERING · USER MANUAL', h1='냉온수 배관 관경 산정 시스템 사용자 매뉴얼',
              sub='냉 · 온수 유량(부하 · 온도차) → Hazen-Williams 압력강하 · 연속방정식 유속 → 호칭지름 → A4 관경 산정서', ver=VER, date=DATE, app_name='냉온수 배관 관경 산정 시스템',
              pdf=PDF, toc=TOC, sections=S, foot_note='기계설비 기술기준 별표 8 · KDS 31 25 25:2021')
html = html.replace('화면 대응 개정 2026-10-12', '화면 대응 개정 ' + DATE)
open(os.path.join(B, 'index.html'), 'w', encoding='utf-8').write(html)
print('manual ok', len(html))
