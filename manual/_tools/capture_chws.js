// 냉온수 배관 관경 산정 시스템 매뉴얼 화면 캡처 — usage: node capture_chws.js <repoDir> <outDir>
// 규격: 1440×900 · DSF 1.25 · _marks.json(번호 배지 % 좌표) · _example.json(예제 검증값 — 앱에서 읽음)
const {chromium}=require(process.env.MM_PW||'playwright');const fs=require('fs');const path=require('path');const {setup,server}=require('./serve');
const repo=path.resolve(process.argv[2]),out=path.resolve(process.argv[3]);fs.mkdirSync(out,{recursive:true});
const VW=1440,VH=900,DSF=1.25,PORT=8899;
/* 예제 A = 냉수 주관 · 강관 SGP · 부하 350 kW · 냉방 냉수 7/12℃ · 허용 압력강하 30 mmAq/m · 설계 유속 2.0 m/s · 10층 × 3.6 m
   예제 B = 온수 분기관 · 동관 · 유량 50 LPM · 허용 압력강하 20 mmAq/m · 설계 유속 1.5 m/s · 5층 × 3.3 m */
const FREEZE=`(()=>{const T=new Date(2026,9,13,10,0,0).getTime();const D=Date;class F extends D{constructor(...a){if(a.length)super(...a);else super(T);}static now(){return T;}}window.Date=F;window.alert=()=>{};window.confirm=()=>true;try{localStorage.clear();localStorage.setItem('pwa-banner-dismissed','1')}catch(e){}})()`;
const HIDE='#pwa-banner,#pwa-install-banner,#ios-modal,#toast,.toast,#toastMsg{display:none!important}';
const FLAT='.calc-col-right{position:static!important;max-height:none!important;overflow:visible!important}';
const HELP=`window.__vis=e=>e&&e.getClientRects().length>0;
window.__card=t=>{const h=[...document.querySelectorAll('.card-tit')].find(e=>__vis(e)&&e.textContent.trim().startsWith(t));return h?h.closest('.card'):null;};
window.__find=sel=>{if(sel.startsWith('card:'))return __card(sel.slice(5));
 if(sel.startsWith('a4sub:'))return document.querySelectorAll('#a4Page .a4-sub')[+sel.slice(6)]||null;
 if(sel.startsWith('sec:'))return [...document.querySelectorAll('#panel-calc .pipe-result-section')].filter(__vis)[+sel.slice(4)]||null;
 if(sel.startsWith('up:')){const [a,b]=sel.slice(3).split('|');const e=document.querySelector(a);return e?e.closest(b):null;}
 for(const s of sel.split(',')){const e=[...document.querySelectorAll(s)].find(__vis);if(e)return e;}return null;};
window.__tab=t=>switchTab(t,[...document.querySelectorAll('.tab-bar .tb')].find(e=>(e.getAttribute('onclick')||'').includes("'"+t+"'")));
window.__set=(id,v)=>{document.getElementById(id).value=v;};
window.__flat=on=>{let s=document.getElementById('__flat');if(on&&!s){s=document.createElement('style');s.id='__flat';s.textContent='${FLAT}';document.head.appendChild(s);}if(!on&&s)s.remove();};
window.__A=()=>{resetAll();__tab('calc');__set('sel-flow-unit','kgh');onFlowUnitChange();selectMat('steel_sgp');__set('sel-sch','normal');__set('sel-purpose','cold');__set('sel-pdrop','30');onPdropChange();
  setInputMode('load',document.getElementById('mode-load'));__set('sel-sys-preset','cold');onSysPresetChange();__set('sel-load-unit','kw');onLoadUnitChange();__set('inp-load','350');onLoadInput();
  __set('sel-vel','2.0');onVelChange();__set('inp-floors','10');__set('inp-floorht','3.6');liveCalc();window.scrollTo(0,0);};
window.__B=()=>{resetAll();__tab('calc');selectMat('copper');__set('sel-purpose','hot');__set('sel-pdrop','20');onPdropChange();
  setInputMode('flow',document.getElementById('mode-flow'));__set('sel-flow-unit','lpm');onFlowUnitChange();__set('inp-flow','50');onFlowInput();
  __set('sel-vel','1.5');onVelChange();__set('inp-floors','5');__set('inp-floorht','3.3');liveCalc();window.scrollTo(0,0);};
window.__ex=()=>{const R=STATE.result;return {mat:R.mat.id,matNm:R.mat.nm,cat:R.mat.cat,C:R.C,Ca:R.mat.Ca,sch:R.schLabel,matLabel:R.matLabel,purpose:document.getElementById('sel-purpose').value,
  mode:INPUT_MODE,loadUnit:document.getElementById('sel-load-unit').value,loadIn:+document.getElementById('inp-load').value,ts:+document.getElementById('inp-ts').value,tr:+document.getElementById('inp-tr').value,
  flowUnit:document.getElementById('sel-flow-unit').value,flowIn:+document.getElementById('inp-flow').value,
  loadKcalh:STATE.loadKcalh,dt:STATE.dt,flowKgh:R.flowKgh,lpm:R.flowKgh/60,pdrop:STATE.pdrop,pdPa:STATE.pdrop*9.80665,vel:STATE.vel,vmax:R.vmax,vrec:R.mat.vrec,floors:STATE.floors,ht:STATE.floorHt,totalH:R.totalH,staticKpa:R.staticKpa,prv:R.prvAlert,pdropRec:R.pdropRec,pdropOverRec:R.pdropOverRec,
  sel:{s:R.selected.s,od:R.selected.od,t:R.selected.t,id:R.selected.id,vel:R.selected.vel,pd:R.selected.actualPdrop,maxq:R.selected.maxQ_kgh,ok:R.selected.ok},minIdByVel:R.minIdByVel,
  cands:R.candidates.map(c=>({s:c.s,id:c.id,vel:c.vel,pd:c.actualPdrop,maxq:c.maxQ_kgh,ok:c.ok,over:c.overAbsMax})),
  sum:[...document.querySelectorAll('.sum-bar .sum-item,.sum-bar span')].map(e=>e.textContent.trim()).filter(Boolean).slice(0,12)};};
window.__tables=()=>({types:PIPE_TYPES,steel:STEEL_PIPES,sch40:SCH40_PIPES,sch80:SCH80_PIPES,cu:COPPER_PIPES});`;
const SHOTS=[
 {id:'s01_overview',pre:"__A()",clip:'viewport',m:[['.tab-bar-inner','작업 탭'],['.sum-bar','요약 스트립'],['#panel-calc .step-bar','진행 단계'],['card:STEP 1','STEP 1 배관 재질'],['card:STEP 2','STEP 2 유량 / 부하'],['card:STEP 4','STEP 4 산정 결과'],['.fab-wrap','초기화 · 설계기준 안내']]},
 {id:'s02_tabs',clip:'.hdr-shell',m:[['.tab-bar .tb:nth-child(1)','관경 산정'],['.tab-bar .tb:nth-child(2)','관경 표준표'],['.tab-bar .tb:nth-child(3)','배관 규격표'],['.tab-bar .tb:nth-child(4)','설계 기준'],['.tab-bar .tb:nth-child(5)','A4 미리보기'],['.tb-manual','매뉴얼'],['.hdr-right','근거 기준']]},
 {id:'s03_project',clip:'card:공사 정보',m:[['#inp-project-name','공사명'],['#inp-project-date','작성일'],['#inp-project-author','작성자']]},
 {id:'s04_material',clip:'card:STEP 1',m:[['#ptypeGrid .ptype-card.sel','배관 재질 4종'],['#sel-purpose','배관 용도'],['#sel-sch','강관 스케줄'],['#sel-pdrop','허용 압력강하'],['#disp-pdrop','적용 단위 마찰손실']]},
 {id:'s05_load',clip:'card:STEP 2',m:[['#mode-load','입력 방식 — 유량 / 부하'],['#sel-sys-preset','시스템 종류(온도 프리셋)'],['#sel-load-unit','부하 단위'],['#inp-load','부하량'],['#inp-ts','공급 · 환수 온도'],['#load-conv-box','부하 전환산 결과'],['#sync-indicator','유량 · 부하 연동']]},
 {id:'s06_param',clip:'card:STEP 3',m:[['#sel-vel','설계 목표 유속'],['#inp-floors','총 층수'],['#inp-floorht','층 높이'],['up:#p-pdrop|.crow','압력강하 기준(Pa/m 환산)'],['up:#p-vmax|.crow','최대 유속'],['up:#p-static|.crow','정수두']]},
 {id:'s07_result',pre:"__flat(true);scrollTo(0,0)",clip:'#pipeHero',union:'#flowDiagram',m:[['#pipeHero','채택 관경 · 실제 유속'],['#statGrid','내경 · 유속 · 압력강하'],['#vel-bar','유속 적정성 게이지'],['#flowDiagram','배관 계통 흐름도']]},
 {id:'s08_table',clip:'up:#tbl-pipes|.pipe-result-section',m:[['#tbl-pipes thead','관경 · 내경 · 유속 · 압력강하 · 최대유량'],['#tbl-pipes tr.highlight','채택 관경 행']]},
 {id:'s09_summary',clip:'up:#res-flow|.cbox',union:'#panel-calc .ref-box',m:[['up:#res-pipe|.crow','채택 관경'],['up:#res-pdrop|.crow','압력강하(실제)'],['up:#res-formula|.crow','적용 공식'],['#tbl-alt','대안 관경 비교'],['#panel-calc .ref-box','적용 기준']]},
 {id:'s10_history',pre:"__flat(false);saveHistory&&saveHistory();",wait:500,clip:'card:산정 이력',m:[['#historyList','저장된 산정 결과'],['up:#historyList|.card','현재 결과 저장']]},
 {id:'s11_flow_b',pre:"__B()",wait:700,clip:'card:STEP 2',m:[['#mode-flow','유량 직접 입력'],['#sel-flow-unit','유량 단위'],['#inp-flow','유량'],['#sync-indicator','KG/H · LPM · ㎥/H · ㎥/s 연동']]},
 {id:'s12_result_b',pre:"__flat(true);scrollTo(0,0)",clip:'#pipeHero',union:'up:#tbl-pipes|.pipe-result-section',post:"__flat(false);__A()",m:[['#pipeHero','동관 40A'],['#tbl-pipes','32A — 압력강하 초과']]},
 {id:'s13_std',pre:"__tab('stdtable');showStdTable(30,document.getElementById('seg-30'));scrollTo(0,0)",wait:700,clip:'card:압력강하별',m:[['#seg-30','기준 선택 — 20 · 30 mmAq/m · 유속 2 · 3 m/s'],['#stdTblMain tbody tr:nth-child(9)','100A'],['#stdTblMain tbody tr:nth-child(10)','125A']]},
 {id:'s14_ctable',clip:'card:재질별 Hazen',m:[['in:재질별 Hazen>>.gtbl thead','C 계수 · 권장 · 최대 유속'],['in:재질별 Hazen>>.nb-txt','MANMIN 참고값 근거']]},
 {id:'s15_spec_sgp',pre:"__tab('spec');scrollTo(0,0)",wait:700,clip:'card:강관 일반',m:[]},
 {id:'s16_spec_cu',clip:'card:동관',m:[]},
 {id:'s17_support',clip:'card:배관 지지 간격',m:[]},
 {id:'s18_guide_judge',pre:"__tab('guide');scrollTo(0,0)",wait:800,clip:'card:현재 산정 결과',m:[['#guide-floor-analysis','층수 · 층높이 연동 분석']]},
 {id:'s19_guide_vel',clip:'card:유속 기준',union:'card:단위 마찰손실',m:[]},
 {id:'s20_guide_floor',clip:'card:총 층수',m:[]},
 {id:'s21_guide_formula',clip:'card:관경 산정 공식',m:[]},
 {id:'s22_modal',pre:"__tab('calc');openGuideModal();switchGuideTab(0)",wait:800,fixed:true,clip:'#guideModal .modal-box',m:[]},
 {id:'s23_modal_vel',pre:"switchGuideTab(1)",wait:500,fixed:true,post:"closeGuideModal()",clip:'#guideModal .modal-box',m:[]},
 {id:'s24_a4',pre:"__A();__tab('a4');scrollTo(0,0)",wait:1500,clip:'viewport',m:[['.a4-export-bar .btn-export','인쇄 / PDF'],['.btn-jpg','JPG 저장'],['#a4Page','A4 관경 산정서']]},
 {id:'s25_a4page',clip:'#a4Page',m:[['a4sub:0','1. 설계 입력 조건'],['a4sub:1','2. 관경 산정 결과'],['a4sub:2','3. 인접 관경 비교표'],['a4sub:3','4. 적용 기준 및 계산 공식']]},
];
(async()=>{
 const s=await server(repo,PORT);const b=await chromium.launch();
 const ctx=await b.newContext({viewport:{width:VW,height:VH},deviceScaleFactor:DSF,serviceWorkers:'block'});await setup(ctx);
 const pg=await ctx.newPage();const errs=[];pg.on('pageerror',e=>errs.push(e.message));
 await pg.addInitScript(FREEZE);
 await pg.goto(`http://127.0.0.1:${PORT}/index.html`);await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(2500);
 await pg.addStyleTag({content:HIDE});
 await pg.evaluate(HELP);
 const ex={};const meta={};
 for(const S of SHOTS){
  if(S.pre){try{await pg.evaluate(S.pre);}catch(e){errs.push(S.id+' pre '+e.message);}}
  await pg.waitForTimeout(S.wait||600);
  if(S.id==='s01_overview'){ex.A=await pg.evaluate('__ex()');ex.tables=await pg.evaluate('__tables()');}
  if(S.id==='s11_flow_b')ex.B=await pg.evaluate('__ex()');
  if(S.id==='s13_std')ex.std30=await pg.evaluate(()=>[...document.querySelectorAll('#stdTblMain tbody tr')].map(tr=>[...tr.cells].map(c=>c.textContent.trim())));
  if(S.id==='s25_a4page')ex.A_a4=await pg.evaluate(()=>document.getElementById('a4Page').innerText.replace(/\s+/g,' '));
  const info=await pg.evaluate(({S,VW,VH})=>{
   const abs=e=>{const r=e.getBoundingClientRect();return {x:r.left+scrollX,y:r.top+scrollY,w:r.width,h:r.height};};
   const F=sel=>{if(sel.startsWith('in:')){const [t,q]=sel.slice(3).split('>>');const c=__card(t);return c?c.querySelector(q):null;}return __find(sel);};
   let clip;
   if(S.clip==='viewport'){clip={x:0,y:scrollY,width:VW,height:VH};}
   else{const el=__find(S.clip);if(!el)return {err:'clip '+S.clip};const a=abs(el);clip={x:a.x,y:a.y,width:a.w,height:a.h};
     if(S.union){const e2=__find(S.union);if(e2){const a2=abs(e2);const x0=Math.min(clip.x,a2.x),y0=Math.min(clip.y,a2.y),x1=Math.max(clip.x+clip.width,a2.x+a2.w),y1=Math.max(clip.y+clip.height,a2.y+a2.h);clip={x:x0,y:y0,width:x1-x0,height:y1-y0};}}
     const P=12;clip={x:Math.max(0,clip.x-P),y:Math.max(0,clip.y-P),width:clip.width+2*P,height:clip.height+2*P};}
   const marks=[];(S.m||[]).forEach(([sel,label],i)=>{const e=F(sel);if(!e){marks.push({n:i+1,label,miss:sel});return;}const a=abs(e);
     marks.push({n:i+1,label,x:+((a.x-clip.x)/clip.width*100).toFixed(2),y:+((a.y-clip.y)/clip.height*100).toFixed(2),w:+(Math.min(a.w,clip.x+clip.width-a.x)/clip.width*100).toFixed(2),h:+(Math.min(a.h,clip.y+clip.height-a.y)/clip.height*100).toFixed(2)});});
   return {clip,marks};},{S,VW,VH});
  if(info.err){errs.push(S.id+' '+info.err);continue;}
  const c=info.clip;const cl={x:Math.max(0,c.x),y:Math.max(0,c.y),width:Math.min(c.width,VW-Math.max(0,c.x)),height:c.height};
  if(S.clip==='viewport'){await pg.screenshot({path:path.join(out,S.id+'.png'),clip:{x:0,y:0,width:VW,height:VH}});}
  else if(S.fixed){const sx=await pg.evaluate(()=>scrollX),sy=await pg.evaluate(()=>scrollY);await pg.screenshot({path:path.join(out,S.id+'.png'),clip:{x:c.x-sx,y:c.y-sy,width:Math.min(c.width,VW),height:Math.min(c.height,VH)}});}
  else{await pg.screenshot({path:path.join(out,S.id+'.png'),clip:cl,fullPage:true});}
  meta[S.id]={w:Math.round(cl.width),h:Math.round(Math.min(cl.height,S.fixed?VH:1e9)),marks:info.marks};
  if(S.post){try{await pg.evaluate(S.post);}catch(e){errs.push(S.id+' post '+e.message);}await pg.waitForTimeout(400);}
 }
 await pg.evaluate('__A()');await pg.waitForTimeout(500);ex.after=await pg.evaluate('__ex()');
 const mctx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:2,serviceWorkers:'block',isMobile:true,hasTouch:true});await setup(mctx);
 const mp=await mctx.newPage();await mp.addInitScript(FREEZE);
 await mp.goto(`http://127.0.0.1:${PORT}/index.html`);await mp.waitForTimeout(2500);
 await mp.addStyleTag({content:HIDE});await mp.evaluate(HELP);await mp.evaluate('__A()');await mp.waitForTimeout(600);
 await mp.screenshot({path:path.join(out,'s26_mobile_main.png')});meta['s26_mobile_main']={w:390,h:844,marks:[]};
 await mp.evaluate(()=>{document.getElementById('pipeHero').scrollIntoView({block:'start'});});await mp.waitForTimeout(500);
 await mp.screenshot({path:path.join(out,'s27_mobile_result.png')});meta['s27_mobile_result']={w:390,h:844,marks:[]};
 await mp.evaluate(()=>{__tab('a4');window.scrollTo(0,0);});await mp.waitForTimeout(1200);
 await mp.screenshot({path:path.join(out,'s28_mobile_a4.png')});meta['s28_mobile_a4']={w:390,h:844,marks:[]};
 ex.mobile=await mp.evaluate(()=>({page:document.documentElement.scrollWidth,tabbar:document.querySelector('.tab-bar-inner').scrollWidth,vw:innerWidth}));
 fs.writeFileSync(path.join(out,'_marks.json'),JSON.stringify(meta,null,1));fs.writeFileSync(path.join(out,'_example.json'),JSON.stringify(ex,null,1));
 const miss=[];Object.entries(meta).forEach(([k,v])=>v.marks.forEach(m=>{if(m.miss)miss.push(k+':'+m.miss);else if(m.x<0||m.y<0||m.x+m.w>100.5||m.y+m.h>100.5)miss.push(k+':OUT '+m.label+' '+m.x+','+m.y+','+m.w+','+m.h);}));
 const pick=e=>e&&[e.flowKgh,e.sel.s,+e.sel.vel.toFixed(3),+e.sel.pd.toFixed(2)];
 console.log(JSON.stringify({A:pick(ex.A),B:pick(ex.B),same:JSON.stringify(ex.A)===JSON.stringify(ex.after),mobile:ex.mobile,sizes:Object.fromEntries(Object.entries(meta).map(([k,v])=>[k,v.w+'x'+v.h])),miss,errs:errs.slice(0,15)},null,1));
 await b.close();s.close();
})();
