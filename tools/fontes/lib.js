'use strict';
/* ===== Biblioteca comum: leitura dos arquivos públicos do TSE (2º turno), formatação e histórico local ===== */
const UFS=['ac','al','ap','am','ba','ce','df','es','go','ma','mt','ms','mg','pa','pb','pr','pe','pi','rj','rn','rs','ro','rr','sc','sp','se','to'];
const ALLU=UFS.concat('zz');
const UFN={ac:'Acre',al:'Alagoas',ap:'Amapá',am:'Amazonas',ba:'Bahia',ce:'Ceará',df:'Distrito Federal',es:'Espírito Santo',go:'Goiás',ma:'Maranhão',mt:'Mato Grosso',ms:'Mato Grosso do Sul',mg:'Minas Gerais',pa:'Pará',pb:'Paraíba',pr:'Paraná',pe:'Pernambuco',pi:'Piauí',rj:'Rio de Janeiro',rn:'Rio Grande do Norte',rs:'Rio Grande do Sul',ro:'Rondônia',rr:'Roraima',sc:'Santa Catarina',sp:'São Paulo',se:'Sergipe',to:'Tocantins',zz:'Exterior',br:'Brasil'};
const TILE={rr:[1,0],ap:[3,0],am:[1,1],pa:[2,1],ma:[3,1],ce:[4,1],rn:[5,1],ac:[0,2],ro:[1,2],mt:[2,2],to:[3,2],pi:[4,2],pb:[5,2],ms:[1,3],go:[2,3],df:[3,3],ba:[4,3],pe:[5,3],al:[6,3],sp:[2,4],mg:[3,4],es:[4,4],se:[5,4],pr:[2,5],rj:[3,5],sc:[2,6],rs:[2,7],zz:[5,7]};
const GOVUF=['rn','am','ac','es','to','df']; // conferir com o TSE: UFs com governador em 2º turno
const REGN={N:'Norte',NE:'Nordeste',CO:'Centro-Oeste',SE:'Sudeste',S:'Sul',EX:'Exterior'};
const ROOT_PAD='https://resultados.tse.jus.br/oficial/ele2026/';
const DIA_2T='2026-10-25';

/* ---------- utilidades ---------- */
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const num=v=>{if(v==null||v==='')return 0;if(typeof v==='number')return v;const n=parseFloat(String(v).replace(/\./g,'').replace(',','.'));return isFinite(n)?n:0};
const fi=n=>(isFinite(n)?Math.round(n):0).toLocaleString('pt-BR');
const fd=(x,d=2)=>(isFinite(x)?x:0).toLocaleString('pt-BR',{minimumFractionDigits:d,maximumFractionDigits:d});
const fp=(x,d=2)=>fd(x,d)+'%';
const MINUS='−';
const fs=(x,d=2)=>{if(!isFinite(x))return '–';const v=Math.round(x*Math.pow(10,d))/Math.pow(10,d);return (v>0?'+':v<0?MINUS:'')+fd(Math.abs(v),d)};
const fsi=n=>{n=Math.round(n);return (n>0?'+':n<0?MINUS:'')+Math.abs(n).toLocaleString('pt-BR')};
const pad=(n,w)=>String(n).padStart(w,'0');
const tzf=new Intl.DateTimeFormat('pt-BR',{timeZone:'America/Sao_Paulo',hour:'2-digit',minute:'2-digit',second:'2-digit'});
const tzm=new Intl.DateTimeFormat('pt-BR',{timeZone:'America/Sao_Paulo',hour:'2-digit',minute:'2-digit'});
const fTime=ms=>tzf.format(new Date(ms)), fTimeM=ms=>tzm.format(new Date(ms));
const LS=(()=>{try{localStorage.setItem('_t','1');localStorage.removeItem('_t');return localStorage}catch(e){return null}})();
const store={get(k,d){try{const v=LS&&LS.getItem(k);return v==null?d:JSON.parse(v)}catch(e){return d}},set(k,v){try{LS&&LS.setItem(k,JSON.stringify(v))}catch(e){}},del(k){try{LS&&LS.removeItem(k)}catch(e){}}};

/* ---------- dados do 1º turno (embutidos) ---------- */
const D26=window.D26;
const CIDX=Object.fromEntries(D26.cands.map((c,i)=>[c[0],i]));
const CNAME=Object.fromEntries(D26.cands.map(c=>[c[0],c[1]]));
const IL=CIDX['13'], IF=CIDX['22'];
const U1=u=>D26.ufs[u];
const U1vv=u=>U1(u).v.reduce((a,b)=>a+b,0);
const T1=(()=>{ // totais nacionais do 1º turno, recalculados dos dados embutidos
  let vv=0,L=0,F=0,vb=0,vn=0,el=0,comp=0;
  for(const u of ALLU){const x=U1(u);vv+=U1vv(u);L+=x.v[IL];F+=x.v[IF];vb+=x.vb;vn+=x.vn;el+=x.el;comp+=x.comp}
  const E=vv-L-F, M=F-L;
  return{vv,L,F,E,M,vb,vn,el,comp,abst:el-comp,sec:ALLU.reduce((a,u)=>a+U1(u).sec,0)};
})();

/* ---------- códigos de eleição (dependem do TSE; informados na página ou por ?fed=&est=) ---------- */
const Q=new URLSearchParams(location.search);
['fed','est','root'].forEach(k=>{const v=Q.get(k);if(v!==null&&v!=='')store.set('ap26s.'+k,v.trim())});
if(Q.get('limpar')!==null){['fed','est','root'].forEach(k=>store.del('ap26s.'+k))}
const CODE={
  get fed(){return String(store.get('ap26s.fed','')||'').replace(/\D/g,'')},
  get est(){return String(store.get('ap26s.est','')||'').replace(/\D/g,'')},
  get root(){const r=String(store.get('ap26s.root','')||'')||ROOT_PAD;return r.endsWith('/')?r:r+'/'}
};
const urlCargo=(uf,cargo,e)=>`${CODE.root}${e}/dados/${uf}/${uf}-c${pad(cargo,4)}-e${pad(e,6)}-u.json`;
const urlAb=e=>`${CODE.root}${e}/dados/br/br-e${pad(e,6)}-ab.json`;

/* ---------- parsers (mesmo formato do 1º turno) ---------- */
const parseS=s=>{s=s||{};const ts=num(s.ts),st=num(s.st);return{ts,st,p:ts?st/ts:0}};
const parseV=v=>{v=v||{};return{tv:num(v.tv),vv:num(v.vv),vnom:num(v.vnom),van:num(v.van),vansj:num(v.vansj),vb:num(v.vb),vn:num(v.vn)}};
function parseCargo(j){
  const car=(j&&j.carg||[])[0]; if(!car)return null;
  const cands=[];
  for(const a of car.agr||[]) for(const p of a.par||[]) for(const c of p.cand||[]){
    cands.push({n:String(c.n),nm:c.nm,nmu:c.nmu||c.nm,seq:num(c.seq),party:p.sg||'',agr:a.com||a.nm||'',vap:num(c.vap),e:c.e==='s',st:c.st||'',pvap:num(c.pvap)});
  }
  const v=parseV(j.v), vsum=cands.reduce((a,c)=>a+c.vap,0);
  if(!v.vv)v.vv=vsum;
  cands.sort((a,b)=>b.vap-a.vap||a.seq-b.seq);
  return{cd:num(car.cd),cands,s:parseS(j.s),v,hg:j.hg||'',dg:j.dg||'',tf:j.tf==='s',t:Date.now()};
}
function parseAb(j){const m={};for(const a of (j&&j.abr)||[])m[String(a.cdabr).toLowerCase()]={s:parseS(a.s)};return m}

/* ---------- estado e leitura ---------- */
const D={pres:{},gov:{},ab:{fed:{},est:{}},seen:{}};
const S={paused:false,pollMs:60000,tickN:0,busy:false,lastOk:0,lastErr:'',need:{pres:true,gov:true},onUpdate:null,timer:null,anyData:false};
const cool={};
async function getJSON(url){
  if(cool[url]&&cool[url]>S.tickN)return null;
  const ctl=new AbortController(),to=setTimeout(()=>ctl.abort(),25000);
  try{
    const r=await fetch(url,{cache:'no-cache',signal:ctl.signal});
    if(r.status===404){cool[url]=S.tickN+5;return null}
    if(!r.ok)throw new Error('HTTP '+r.status+' em '+url);
    return await r.json();
  }catch(e){ if(e&&e.name==='AbortError')throw new Error('tempo esgotado em '+url); throw e }
  finally{clearTimeout(to)}
}
async function pool(jobs,n=6){
  const out=[];let i=0;
  await Promise.all(Array.from({length:n},async()=>{while(i<jobs.length){const k=i++;try{out[k]=await jobs[k]()}catch(e){out[k]={error:e}}}}));
  return out;
}
const codesOk=()=>!!(CODE.fed&&(CODE.est||!S.need.gov));
async function tick(force){
  if(S.busy)return;
  if(!codesOk()){S.lastErr='codigos';render();return}
  S.busy=true;S.tickN++;
  const errs=[];
  try{
    const jobs=[];
    if(S.need.pres){
      const abF=await getJSON(urlAb(CODE.fed)).catch(e=>{errs.push(e);return null});
      if(abF)D.ab.fed=parseAb(abF);
      const want=(uf)=>{
        const a=D.ab.fed[uf], st=a?a.s.st:-1, key='pres'+uf, prev=D.seen[key];
        if(D.pres[uf]&&st>=0&&st===prev&&!force&&S.tickN%5!==0)return;
        jobs.push(async()=>{const j=await getJSON(urlCargo(uf,1,CODE.fed));if(!j)return;const p=parseCargo(j);if(!p)return;D.pres[uf]=p;D.seen[key]=st});
      };
      jobs.push(async()=>{const j=await getJSON(urlCargo('br',1,CODE.fed));if(j){const p=parseCargo(j);if(p)D.pres.br=p}});
      ALLU.forEach(want);
    }
    if(S.need.gov&&CODE.est){
      const abE=await getJSON(urlAb(CODE.est)).catch(e=>{errs.push(e);return null});
      if(abE)D.ab.est=parseAb(abE);
      for(const uf of GOVUF){
        const a=D.ab.est[uf], st=a?a.s.st:-1, key='gov'+uf, prev=D.seen[key];
        if(D.gov[uf]&&st>=0&&st===prev&&!force&&S.tickN%5!==0)continue;
        jobs.push(async()=>{const j=await getJSON(urlCargo(uf,3,CODE.est));if(!j)return;const p=parseCargo(j);if(!p)return;D.gov[uf]=p;D.seen[key]=st});
      }
    }
    const res=await pool(jobs);
    res.forEach(r=>{if(r&&r.error)errs.push(r.error)});
    S.anyData=!!(D.pres.br||Object.keys(D.pres).length||Object.keys(D.gov).length);
    if(S.anyData)recordHistory();
    S.lastOk=Date.now();S.lastErr=errs.length?String(errs[0].message||errs[0]):'';
  }catch(e){S.lastErr=String(e.message||e)}
  finally{S.busy=false}
  render();
}
function schedule(){clearTimeout(S.timer);if(S.paused)return;S.timer=setTimeout(async()=>{await tick();schedule()},S.pollMs)}
function render(){mountStatus();if(S.onUpdate)S.onUpdate()}

/* ---------- agregados ---------- */
const fin=(d,n)=>d?d.cands.find(c=>c.n===n):null;
const pctSec=uf=>{const a=D.ab.fed[uf];if(a)return a.s.p;const d=D.pres[uf];return d?d.s.p:0};
function nacional(incluiExt){ // soma das UFs (com ou sem Exterior)
  let L=0,F=0,vv=0,wp=0,ws=0,n=0;
  for(const u of ALLU){
    if(u==='zz'&&!incluiExt)continue;
    const d=D.pres[u]; if(!d)continue; n++;
    L+=(fin(d,'13')||{vap:0}).vap;F+=(fin(d,'22')||{vap:0}).vap;vv+=d.v.vv;
    const w=U1(u).sec;wp+=pctSec(u)*w;ws+=w;
  }
  const wall=ALLU.filter(u=>incluiExt||u!=='zz').reduce((a,u)=>a+U1(u).sec,0);
  return{L,F,vv,n,p:wall?wp/wall:0};
}
/* projeção aritmética: em cada UF, votos atuais ÷ fração de seções totalizadas; sem dados, usa a proporção nacional entre os finalistas */
function projecao(incluiExt=true){
  const nat=nacional(incluiExt); if(!nat.vv)return null;
  const shL=nat.L/(nat.L+nat.F||1);
  let L=0,F=0,tot=0,cov=0,nu=0;
  for(const u of ALLU){
    if(u==='zz'&&!incluiExt)continue;
    const d=D.pres[u],p=d?pctSec(u):0;
    if(d&&d.v.vv>0&&p>=0.02){const k=1/p,l=(fin(d,'13')||{vap:0}).vap*k,f=(fin(d,'22')||{vap:0}).vap*k;L+=l;F+=f;tot+=d.v.vv*k;cov+=d.v.vv;nu++}
    else{const base=U1vv(u); L+=base*shL;F+=base*(1-shL);tot+=base}
  }
  return{L,F,tot,cov,nu,mL:L/(L+F)*100,mF:F/(L+F)*100};
}

/* ---------- histórico local (ritmo de apuração) ---------- */
let H=store.get('ap26s.hist',null); if(!H||!H.t)H={t:[],u:[]};
function recordHistory(){
  const t=Date.now(),n=H.t.length;
  if(n&&t-H.t[n-1]<5000)return;
  const row={};
  for(const u of ALLU){const d=D.pres[u];if(!d)continue;row[u]=[(fin(d,'13')||{vap:0}).vap,(fin(d,'22')||{vap:0}).vap,d.v.vv,Math.round(pctSec(u)*10000)/10000]}
  if(!Object.keys(row).length)return;
  H.t.push(t);H.u.push(row);
  if(H.t.length>1500){const c=H.t.length-1500;H.t.splice(0,c);H.u.splice(0,c)}
  store.set('ap26s.hist',H);
}
function clearHist(){H={t:[],u:[]};store.del('ap26s.hist')}

/* ---------- cabeçalho de estado e códigos de eleição ---------- */
function statusText(){
  if(!codesOk())return{c:'wait',t:'Aguardando os códigos de eleição do 2º turno (veja “Códigos de eleição”).'};
  if(S.busy&&!S.lastOk)return{c:'wait',t:'Lendo os arquivos do TSE…'};
  if(S.lastErr&&!S.anyData)return{c:'err',t:'Sem dados do TSE: '+S.lastErr+'. Se o erro for 403/404, confira os códigos de eleição.'};
  if(!S.anyData)return{c:'wait',t:'Conectado ao TSE, ainda sem dados do 2º turno (a apuração começa às 17h de Brasília).'};
  return{c:S.lastErr?'wait':'live',t:'Última leitura às '+fTime(S.lastOk)+(S.lastErr?' · aviso: '+S.lastErr:'')+(S.paused?' · pausado':'')};
}
function mountStatus(){
  const el=$('#status'); if(!el)return;
  const s=statusText();
  el.innerHTML=`<span><span class="dot ${s.c}"></span>${esc(s.t)}</span>`;
}
function codesCard(){
  return `<details class="card" id="codes"><summary><h2>Códigos de eleição <span class="sub">necessários para ler o 2º turno</span></h2></summary>
  <p class="note" style="margin-top:6px">O TSE publica o 2º turno sob códigos de eleição próprios (no 1º turno, 6257 para presidente e 6259 para governador). Informe aqui os códigos do 2º turno, que aparecem nos endereços do <a class="ext" href="https://resultados.tse.jus.br/oficial/app/index.html" target="_blank" rel="noopener">aplicativo do TSE</a>. Também vale <code>?fed=…&amp;est=…</code> no endereço. Ficam só no seu navegador.</p>
  <div class="codes"><label>Eleição federal (presidente)<input id="c_fed" inputmode="numeric" value="${esc(CODE.fed)}"></label><label>Eleição estadual (governadores)<input id="c_est" inputmode="numeric" value="${esc(CODE.est)}"></label><label>Endereço-base (opcional)<input id="c_root" value="${esc(store.get('ap26s.root',''))}" placeholder="${ROOT_PAD}"></label><button class="btn" id="c_ok">Salvar e ler</button></div></details>`;
}
function bindCodes(){
  const b=$('#c_ok'); if(!b)return;
  b.onclick=()=>{store.set('ap26s.fed',$('#c_fed').value.trim());store.set('ap26s.est',$('#c_est').value.trim());const r=$('#c_root').value.trim();if(r)store.set('ap26s.root',r);else store.del('ap26s.root');for(const k in cool)delete cool[k];tick(true)};
}
function startLive(opts){
  Object.assign(S.need,opts||{});
  const ctl=$('#ctl');
  if(ctl){ctl.innerHTML=`<select id="poll" aria-label="Intervalo de leitura"><option value="30000">30 s</option><option value="60000" selected>60 s</option><option value="120000">2 min</option></select><button id="pau">Pausar</button><button id="upd">Atualizar</button>`;
    $('#poll').onchange=e=>{S.pollMs=+e.target.value;schedule()};
    $('#pau').onclick=e=>{S.paused=!S.paused;e.target.textContent=S.paused?'Retomar':'Pausar';if(!S.paused){tick();schedule()}else clearTimeout(S.timer);mountStatus()};
    $('#upd').onclick=()=>tick(true);}
  mountStatus();tick().then(schedule);
}
