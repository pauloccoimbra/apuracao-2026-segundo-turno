/* ===== MODO DEMONSTRAÇÃO: dados SIMULADOS no lugar do TSE. Nada abaixo é resultado eleitoral. ===== */
const DEMO=true;
{
  const DUR=240; // segundos reais até o fim (1 s ≈ 1 minuto simulado, 17h às 21h)
  const hs=(s)=>{let h=2166136261;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619)}return ((h>>>0)%100000)/100000};
  const tp=Q.get('t'); if(tp!==null&&tp!==''){store.set('ap26s.demo0',Date.now()-Math.max(0,+tp)*1000);clearHist()}
  if(Q.get('reiniciar')!==null){store.del('ap26s.demo0');clearHist()}
  if((tp!==null&&tp!=='')||Q.get('reiniciar')!==null){W.st=null;W.act=false;W.gaps=[];W.flash='';store.del('ap26s.watch')}
  let t0=store.get('ap26s.demo0',null); if(!t0){t0=Date.now();store.set('ap26s.demo0',t0);clearHist()}
  Object.defineProperty(CODE,'fed',{get(){return '9001'}});Object.defineProperty(CODE,'est',{get(){return '9002'}});
  S.pollMs=3000;
  const INT=Q.get('interrupcao')!==null; if(INT)W.thr=0.25;
  const simMin=()=>{let e=(Date.now()-t0)/1000;if(INT)e=e<120?e:e<160?120:e-40;return Math.min(240,e*(240/DUR))};
  const prog=(u,m)=>{const a=u==='zz'?60:10+hs('a'+u)*55, d=55+hs('d'+u)*70+(U1(u).r==='N'?25:0);
    const x=Math.min(1,Math.max(0,(m-a)/d));return x*x*(3-2*x)};
  const fim=u=>{const x=U1(u),vv=U1vv(u),L=x.v[IL],F=x.v[IF],E=vv-L-F;
    const g=0.72*E*(1+(hs('g'+u)-.5)*.3), s=0.47+(hs('s'+u)-.5)*.16;
    return{L:L+g*s,F:F+g*(1-s)}};
  const bias=u=>(hs('b'+u)-.5)*.06;
  function votos(u,p){const f=fim(u),T=f.L+f.F,sh=f.L/T+bias(u)*(1-p),n=T*p;return[Math.round(n*sh),Math.round(n*(1-sh))]}
  const cand=(n,nm,v)=>({n,nm:nm.toUpperCase(),nmu:nm,seq:'1',vap:String(v),e:'n'});
  const mk=(L,F,p,ts,te)=>{const vv=L+F,c=Math.round(vv/0.965),br=c-vv,est=Math.round(te*p);
    return{carg:[{cd:'1',agr:[{n:'13',nm:'Lula',com:'PT',par:[{sg:'PT',cand:[cand('13','Lula',L)]}]},{n:'22',nm:'Flávio Bolsonaro',com:'PL',par:[{sg:'PL',cand:[cand('22','Flávio Bolsonaro',F)]}]}]}],
    s:{ts:String(ts),st:String(Math.round(ts*p))},
    v:{tv:String(c),vv:String(vv),vnom:String(vv),van:String(Math.round(br*.65)),vansj:'0',vb:String(Math.round(br*.35)),vn:String(Math.round(br*.65))},
    e:{te:String(te),est:String(est),c:String(c),a:String(Math.max(0,est-c))}}};
  const FR={rn:.55,am:.30,ac:.35,es:.40,to:.50,df:.38};
  function gov(uf,p){const r=D26.runoff.find(x=>x.uf===uf),v2=r.l[2]+r.d[2]+r.pool*.9,a=r.l[2]+r.pool*.9*FR[uf],b=v2-a;
    const j=mk(Math.round(a*p),Math.round(b*p),p,U1(uf).sec,U1(uf).el),c=j.carg[0].agr;
    const set=(k,n,nm,sg,v)=>{c[k].n=n;c[k].par[0].sg=sg;Object.assign(c[k].par[0].cand[0],{n,nm:nm.toUpperCase(),nmu:nm,vap:String(v)})};
    set(0,GNUM[uf][0],r.l[0],r.l[1],Math.round(a*p));set(1,GNUM[uf][1],r.d[0],r.d[1],Math.round(b*p));return j}
  getJSON=async function(url){
    const m=url.match(/\/ele2026\/(\d+)\/dados\/([a-z]+)\/(.+)\.json/);if(!m)return null;
    const e=m[1],uf=m[2],nome=m[3],mn=simMin();
    if(e==='6257'&&U1(uf)&&!nome.endsWith('-ab')){const x=U1(uf),vv=x.v.reduce((a,b)=>a+b,0),c=vv+x.vb+x.vn;
      return{carg:[{cd:'1',agr:D26.cands.map((k,i)=>({n:k[0],nm:k[1],com:k[2],par:[{sg:k[2],cand:[cand(k[0],k[1],x.v[i])]}]}))}],s:{ts:String(x.sec),st:String(x.sec)},v:{tv:String(c),vv:String(vv),vnom:String(vv),van:String(x.vn),vansj:'0',vb:String(x.vb),vn:'0'},e:{te:String(x.el),est:String(x.el),c:String(x.comp),a:String(x.el-x.comp)}}}
    if(nome.endsWith('-ab')){const lista=e==='9001'?ALLU:GOVUF;return{abr:lista.map(u=>({cdabr:u.toUpperCase(),s:{ts:String(U1(u).sec),st:String(Math.round(U1(u).sec*prog(u,mn)))}}))}}
    if(e==='9001'){
      if(uf==='br'){let L=0,F=0,ts=0,st=0,te=0;for(const u of ALLU){const p=prog(u,mn),v=votos(u,p);L+=v[0];F+=v[1];ts+=U1(u).sec;st+=U1(u).sec*p;te+=U1(u).el}
        const j=mk(L,F,st/ts,ts,te);let est=0;for(const u of ALLU)est+=Math.round(U1(u).el*prog(u,mn));j.e.est=String(est);j.e.a=String(Math.max(0,est-(+j.e.c)));return j}
      const p=prog(uf,mn),v=votos(uf,p);return mk(v[0],v[1],p,U1(uf).sec,U1(uf).el)}
    if(e==='9002')return gov(uf,prog(uf,mn));
    return null};
  let lastK=-1;
  recordHistory=function(){
    const K=Math.floor(simMin());
    for(let k=Math.max(0,lastK+1);k<=K;k++){const row={};
      for(const u of ALLU){const p=prog(u,k),v=votos(u,p);if(p>0)row[u]=[v[0],v[1],v[0]+v[1],Math.round(p*10000)/10000]}
      H.t.push(T0+k*60000);H.u.push(row)}
    lastK=K;store.set('ap26s.hist',H)};
  window.__demo={simMin,prog,fim,votos,gov,T0,get:u=>getJSON(u)};
  const css=document.createElement('style');css.textContent='.demo-banner{background:#b3261e;color:#fff;padding:8px 16px;font:600 13px/1.35 var(--sans);text-align:center}.demo-banner a{color:#fff}.demo-tag{position:fixed;left:8px;bottom:8px;z-index:200;background:#b3261e;color:#fff;font:700 12px var(--sans);padding:4px 8px;border-radius:6px;opacity:.92;pointer-events:none}';document.head.appendChild(css);
  const b=document.createElement('div');b.className='demo-banner';
  b.innerHTML='DEMONSTRAÇÃO: todos os números de apuração desta cópia são SIMULADOS e não são resultado eleitoral. A contagem simulada avança em ritmo acelerado (4 minutos reais = 17h às 21h). <a href="?reiniciar">Reiniciar</a> · <a href="?t=60">1 min</a> · <a href="?t=120">2 min</a> · <a href="?t=180">3 min</a> · <a href="?t=240">fim</a> · <a href="?reiniciar&amp;interrupcao">simular interrupção</a>';
  document.body.insertBefore(b,document.body.firstChild);
  const tag=document.createElement('div');tag.className='demo-tag';tag.textContent='DADOS SIMULADOS';document.body.appendChild(tag);
  document.title='DEMO · '+document.title;
}
