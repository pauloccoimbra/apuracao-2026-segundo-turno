#!/usr/bin/env python3
"""Gera pag_perfil.html, pag_participacao.html e pag_governadores.html a partir das páginas do 1º turno (leitura apenas),
preservando o conteúdo do 1º turno e acrescentando um bloco com os dados ao vivo do 2º turno.
Uso: python3 gerar_pag_apoio.py <pasta do site do 1º turno>"""
import sys, os, re
D1 = sys.argv[1]
AQUI = os.path.dirname(os.path.abspath(__file__))
extras = open(os.path.join(AQUI, 'extras.css'), encoding='utf8').read()
COMUM = open(os.path.join(AQUI, 'live_comum.js'), encoding='utf8').read()

def base(nome):
    s = open(os.path.join(D1, nome + '.html'), encoding='utf8').read()
    s = R(s, '--bg:#f3f4f6; --surface:#ffffff', '--bg:#ffffff; --surface:#ffffff')
    s = R(s, '</style>', extras + '\n.live-h{margin:0 0 6px}.lv{margin-bottom:14px}\n</style>')
    return s, None

def R(s, a, b):
    assert a in s, a[:70]
    return s.replace(a, b, 1)

def fim(s, nome, live_html, live_js):
    # bloco ao vivo logo depois do texto de abertura (antes da primeira seção)
    i = s.index('<section class="card"')
    s = s[:i] + live_html + '\n' + s[i:]
    # biblioteca depois dos dados do 1º turno e das utilidades, antes do script principal da página
    j = s.index('<script>\n', s.index('function pager(){}'))
    s = s[:j] + '<script>/*@LIB*/</script>\n' + s[j:]
    k = s.rindex('</body>')
    s = s[:k] + '<script>\n(function(){\n\'use strict\';\n' + COMUM + '\n' + live_js + '\n})();\n</script>\n' + s[k:]
    open(os.path.join(AQUI, 'pag_' + nome + '.html'), 'w', encoding='utf8').write(s)
    print('ok', nome, len(s))

LIVE = lambda tit, sub: f'<section class="card lv" id="live2t"><h2>{tit}<span class="sub">{sub}</span></h2><div id="status" class="status" style="margin-bottom:8px"></div><div id="codesbox"></div><div id="l2"></div></section>'

# ---------------- Perfil ----------------
s, sub = base('perfil')
s = R(s, '<title>Perfil do voto · Apuração 2026 · 1º turno</title><meta name="description" content="Polarização, fragmentação e geografia dos votos do 1º turno de 2026 por estado.">',
    '<title>Perfil do voto · Apuração 2026 · 2º turno</title><meta name="description" content="Perfil do voto presidencial: polarização, fragmentação e geografia do 1º turno, e a mudança do 1º para o 2º turno por UF, com dados do TSE.">')
s = R(s, '<div class="brand">Perfil do voto<small>Presidente · 1º turno 2026 · polarização, fragmentação e geografia</small></div>', '<div class="brand">Perfil do voto · Apuração 2026 · 2º turno<small>Presidente · 1º turno como base e mudança no 2º turno</small></div>')
s = R(s, '<h1 class="page-h">Perfil do voto no 1º turno</h1>', '<h1 class="page-h">Perfil do voto: do 1º ao 2º turno</h1>')
s = R(s, 'Todos os números são dos votos válidos (nominais) de cada estado, a partir do resultado final do TSE.</p></div>', 'Os cartões após o bloco do 2º turno descrevem o 1º turno (resultado final do TSE, votos válidos); o primeiro bloco usa os arquivos do 2º turno lidos pelo seu navegador.</p></div>')
s = R(s, '<p class="fonte-pg"><b>Fonte desta página:</b> TSE, resultado final do 1º turno de 04/10/2026', '<p class="fonte-pg"><b>Fonte desta página:</b> 1º turno: TSE, resultado final de 04/10/2026; 2º turno: arquivos públicos do TSE lidos ao vivo; cálculos próprios. TSE, 1º turno, de 04/10/2026')
js = r'''
const root=$('#l2');
function draw(){
  const rows=[];let sx=[],sy=[];
  for(const u of ALLU){const d=D.pres[u];if(!d||!d.v.vv)continue;const p=pctSec(u);if(p<.02)continue;const k=1/p,x=U1(u);
    const l=(fin(d,'13')||{vap:0}).vap*k,f=(fin(d,'22')||{vap:0}).vap*k,Eu=U1vv(u)-x.v[IL]-x.v[IF],g=(l-x.v[IL])+(f-x.v[IF]);
    rows.push({u,p,f1:x.v[IF]/(x.v[IF]+x.v[IL])*100,f2:f/(f+l)*100,r:Eu>0?g/Eu:NaN,fim:p>=.999,vv:f+l,m1:(x.v[IF]-x.v[IL])/(x.v[IF]+x.v[IL])*100,m2:(f-l)/(f+l)*100})}
  if(!rows.length){root.innerHTML='<div class="empty-msg">Aguardando dados do 2º turno.</div>';return}
  const mean=a=>a.reduce((x,y)=>x+y,0)/a.length;
  const cor=(a,b)=>{const ma=mean(a),mb=mean(b);let sa=0,sb=0,sab=0;for(let i=0;i<a.length;i++){sa+=(a[i]-ma)**2;sb+=(b[i]-mb)**2;sab+=(a[i]-ma)*(b[i]-mb)}return sab/Math.sqrt(sa*sb)};
  const c=rows.length>2?cor(rows.map(r=>r.m1),rows.map(r=>r.m2)):NaN;
  const dm=rows.map(r=>r.m2-r.m1);
  const W=640,H=360,l=46,r=14,t=12,b=38,lo=-60,hi=60,X=v=>l+(v-lo)/(hi-lo)*(W-l-r),Y=v=>t+(1-(v-lo)/(hi-lo))*(H-t-b);
  let g='';for(let v=lo;v<=hi;v+=20)g+=`<line x1="${l}" x2="${W-r}" y1="${Y(v)}" y2="${Y(v)}" stroke="var(--line)" stroke-width=".7"/><line x1="${X(v)}" x2="${X(v)}" y1="${t}" y2="${H-b}" stroke="var(--line)" stroke-width=".7"/><text x="${l-5}" y="${Y(v)+4}" text-anchor="end" font-size="10.5" fill="var(--muted)">${fs(v,0)}</text><text x="${X(v)}" y="${H-b+15}" text-anchor="middle" font-size="10.5" fill="var(--muted)">${fs(v,0)}</text>`;
  g+=`<line x1="${X(lo)}" y1="${Y(lo)}" x2="${X(hi)}" y2="${Y(hi)}" stroke="var(--fg2)" stroke-dasharray="5 4"/><text x="${W-r-4}" y="${t+12}" text-anchor="end" font-size="10.5" fill="var(--fg2)">linha de igualdade</text>`;
  rows.forEach(q=>{g+=`<circle cx="${X(q.m1)}" cy="${Y(q.m2)}" r="${3+Math.sqrt(q.vv/3e6)*3}" style="fill:${q.m2>=0?'var(--c2)':'var(--c1)'}" fill-opacity=".55" stroke="var(--surface)"><title>${q.u.toUpperCase()}: 1º turno ${fs(q.m1,1)} p.p.; 2º turno ${fs(q.m2,1)} p.p.</title></circle><text x="${X(q.m1)}" y="${Y(q.m2)+3}" text-anchor="middle" font-size="8.5" fill="var(--fg)" pointer-events="none">${q.u.toUpperCase()}</text>`});
  g+=`<text x="${(l+W-r)/2}" y="${H-3}" text-anchor="middle" font-size="11" fill="var(--fg2)">Flávio − Lula no 1º turno (p.p., só os dois finalistas)</text><text transform="translate(11 ${(t+H-b)/2}) rotate(-90)" text-anchor="middle" font-size="11" fill="var(--fg2)">Flávio − Lula no 2º turno (p.p.)</text>`;
  rows.sort((a,b)=>a.u.localeCompare(b.u));
  root.innerHTML=`<p class="note" style="margin:0 0 8px">Cada UF com ao menos 2% das seções totalizadas entra com os votos extrapolados pela fração totalizada (${rows.filter(r=>r.fim).length} concluídas, ${rows.filter(r=>!r.fim).length} projetadas). Percentuais entre Lula e Flávio Bolsonaro, para comparar com o 1º turno sem os demais candidatos.</p>
  <div class="stats" style="margin-bottom:10px"><div class="stat"><div class="lab">UFs com leitura</div><div class="val">${rows.length}</div><div class="pc">de 28 (27 UFs + Exterior)</div></div>
  <div class="stat"><div class="lab">Variação média da margem</div><div class="val">${fs(mean(dm),1)} p.p.</div><div class="pc">2º turno − 1º turno, Flávio − Lula</div></div>
  <div class="stat"><div class="lab">Correlação 1º × 2º turno</div><div class="val">${isFinite(c)?fd(c,2):'–'}</div><div class="pc">margens por UF (Pearson)</div></div></div>
  <div class="chart"><svg style="max-width:640px" viewBox="0 0 ${W} ${H}" role="img" aria-label="Margem Flávio menos Lula por UF no 1º e no 2º turno">${g}</svg></div>
  <div class="tw" style="margin-top:10px"><table><thead><tr><th>UF</th><th class="n">Seções</th><th class="n">Flávio, 1º turno</th><th class="n">Flávio, 2º turno</th><th class="n">Variação (p.p.)</th><th class="n">r da UF</th><th>Base</th></tr></thead><tbody>${rows.map(q=>`<tr><td><b>${q.u.toUpperCase()}</b> ${esc(UFN[q.u])}</td><td class="n">${fp(q.p*100,1)}</td><td class="n">${fp(q.f1,1)}</td><td class="n">${fp(q.f2,1)}</td><td class="n">${fs(q.f2-q.f1,1)}</td><td class="n">${isFinite(q.r)?fd(q.r,2):'–'}</td><td style="color:var(--muted)">${q.fim?'observado':'projetado'}</td></tr>`).join('')}</tbody></table></div>
  <p class="note">r da UF = ganho líquido de Lula + Flávio Bolsonaro em relação ao 1º turno, dividido pelos votos dos eliminados na UF. Correlação e variação descrevem a UF como agregado, não o comportamento individual (limite da inferência ecológica).</p>`;
}
AP.S.onUpdate=draw;wire({pres:true,gov:false});draw();
'''
fim(s, 'perfil', LIVE('Mudança do 1º para o 2º turno', 'dados do 2º turno ao vivo'), js)

# ---------------- Participação ----------------
s, sub = base('participacao')
s = R(s, '<title>Participação · Apuração 2026 · 1º turno</title><meta name="description" content="Abstenção por estado, valor de mobilizar eleitores e voto cruzado entre presidente e governador no 1º turno de 2026.">',
    '<title>Participação · Apuração 2026 · 2º turno</title><meta name="description" content="Comparecimento, abstenção, brancos e nulos no 2º turno de 2026 em comparação com o 1º turno, e a análise de participação e voto cruzado do 1º turno.">')
s = R(s, '<div class="brand">Participação e voto cruzado<small>Abstenção, brancos, nulos e coerência presidente × governador · 1º turno 2026</small></div>', '<div class="brand">Participação · Apuração 2026 · 2º turno<small>Comparecimento, abstenção, brancos e nulos · 2º turno e 1º turno</small></div>')
s = R(s, '<h1 class="page-h">Participação, brancos, nulos e voto cruzado</h1>', '<h1 class="page-h">Participação, brancos, nulos e voto cruzado</h1>')
s = R(s, 'Os dados descrevem o 1º turno e não indicam como os abstencionistas votariam.</p></div>', 'O primeiro bloco mostra o 2º turno ao vivo, nas seções já totalizadas; os demais descrevem o 1º turno e não indicam como os abstencionistas votariam.</p></div>')
s = R(s, '<p class="fonte-pg"><b>Fonte desta página:</b> TSE, resultado final do 1º turno de 04/10/2026', '<p class="fonte-pg"><b>Fonte desta página:</b> 2º turno: arquivos públicos do TSE lidos ao vivo, nas seções totalizadas; cálculos próprios. 1º turno: TSE, resultado final de 04/10/2026')
js = r'''
const root=$('#l2');
function draw(){
  const rows=[];
  for(const u of ALLU){const d=D.pres[u];if(!d||!d.v.tv)continue;const x=U1(u),e=d.e,v=d.v,est=e.est||0;if(!est)continue;
    rows.push({u,p:pctSec(u),c2:e.c/est*100,a2:e.a/est*100,b2:v.vb/v.tv*100,n2:v.vn/v.tv*100,c1:x.comp/x.el*100,a1:(x.el-x.comp)/x.el*100,b1:x.vb/x.comp*100,n1:x.vn/x.comp*100,tv:v.tv})}
  const b=D.pres.br;
  if(!rows.length||!b){root.innerHTML='<div class="empty-msg">Aguardando dados do 2º turno.</div>';return}
  let t1c=0,t1e=0,t1b=0,t1n=0;for(const u of ALLU){const x=U1(u);t1c+=x.comp;t1e+=x.el;t1b+=x.vb;t1n+=x.vn}
  const e=b.e,v=b.v,est=e.est||1;
  const k=(lab,a,bb,det)=>`<div class="stat"><div class="lab">${lab}</div><div class="val">${a}</div><div class="pc">${det}</div></div>`;
  rows.sort((a,b)=>a.u.localeCompare(b.u));
  root.innerHTML=`<p class="note" style="margin:0 0 8px">Seções totalizadas no país: ${fp(b.s.p*100,2)}. Percentuais de comparecimento e abstenção sobre o eleitorado apto das seções já totalizadas; brancos e nulos sobre o total de votos. Seções que chegam depois podem ter perfil diferente (por exemplo, mais urbanas ou mais distantes), então o parcial pode mudar.</p>
  <div class="stats" style="margin-bottom:10px">${k('Comparecimento',fp(e.c/est*100,2),0,'1º turno: '+fp(t1c/t1e*100,2))}${k('Abstenção',fp(e.a/est*100,2),0,'1º turno: '+fp((t1e-t1c)/t1e*100,2))}${k('Brancos',fp(v.vb/(v.tv||1)*100,2),0,'1º turno: '+fp(t1b/t1c*100,2)+' dos votos')}${k('Nulos',fp(v.vn/(v.tv||1)*100,2),0,'1º turno: '+fp(t1n/t1c*100,2)+' dos votos')}${k('Eleitorado apto',fi(e.te),0,'seções totalizadas: '+fi(e.est))}</div>
  <div class="tw"><table><thead><tr><th>UF</th><th class="n">Seções</th><th class="n">Comparec. 2º</th><th class="n">Comparec. 1º</th><th class="n">Variação (p.p.)</th><th class="n">Abstenção 2º</th><th class="n">Brancos 2º</th><th class="n">Nulos 2º</th><th class="n">Brancos+nulos 1º</th></tr></thead><tbody>${rows.map(q=>`<tr><td><b>${q.u.toUpperCase()}</b> ${esc(UFN[q.u])}</td><td class="n">${fp(q.p*100,1)}</td><td class="n">${fp(q.c2,1)}</td><td class="n">${fp(q.c1,1)}</td><td class="n">${fs(q.c2-q.c1,1)}</td><td class="n">${fp(q.a2,1)}</td><td class="n">${fp(q.b2,1)}</td><td class="n">${fp(q.n2,1)}</td><td class="n">${fp(q.b1+q.n1,1)}</td></tr>`).join('')}</tbody></table></div>
  <p class="note">A comparação de comparecimento entre turnos usa, no 2º turno, só as seções já totalizadas e, no 1º turno, o total final: enquanto a apuração não termina, a diferença mistura variação real e composição das seções. Não se infere desta tabela como os abstencionistas votariam.</p>`;
}
AP.S.onUpdate=draw;wire({pres:true,gov:false});draw();
'''
fim(s, 'participacao', LIVE('Participação no 2º turno', 'dados do 2º turno ao vivo'), js)

# ---------------- Governadores ----------------
s, sub = base('governadores')
s = R(s, '<title>Governadores · Apuração 2026 · 1º turno</title><meta name="description" content="Governadores eleitos no 1º turno de 2026, coligações e simulador dos seis segundos turnos estaduais.">',
    '<title>Governadores · Apuração 2026 · 2º turno</title><meta name="description" content="Os seis segundos turnos estaduais de 2026 (RN, AM, AC, ES, TO e DF) com apuração ao vivo e simulador, e os 21 governadores eleitos no 1º turno.">')
s = R(s, '<div class="brand">Governadores<small>1º turno e segundos turnos estaduais · 2026</small></div>', '<div class="brand">Governadores · Apuração 2026 · 2º turno<small>Seis segundos turnos estaduais e 21 eleitos no 1º turno</small></div>')
s = R(s, '<h1 class="page-h">Governadores: eleitos e segundos turnos</h1>', '<h1 class="page-h">Governadores: segundos turnos e eleitos</h1>')
s = R(s, '<p class="fonte-pg"><b>Fonte desta página:</b> TSE, resultado final do 1º turno de 04/10/2026', '<p class="fonte-pg"><b>Fonte desta página:</b> segundos turnos: arquivos públicos do TSE lidos ao vivo; cálculos próprios. 1º turno: TSE, resultado final de 04/10/2026')
s = R(s, '<p>A apuração dos segundos turnos de 25 de outubro será acompanhada no <a href="https://pauloccoimbra.github.io/apuracao-2026-segundo-turno/" rel="noopener">site do 2º turno ↗</a>.</p>', '<p>Os segundos turnos estaduais deste dia 25 de outubro são lidos acima, ao vivo; o simulador abaixo usa só o 1º turno e não é previsão.</p>')
js = r'''
const root=$('#l2'),GU=['rn','am','ac','es','to','df'];
const nm=s=>String(s||'').normalize('NFD').replace(/[̀-ͯ]/g,'').toUpperCase().replace(/[^A-Z]/g,'');
function card(uf){
  const r=D26.runoff.find(x=>x.uf===uf),d=D.gov[uf],ab=D.ab.est[uf],p=ab?ab.s.p:(d?d.s.p:0);
  let h=`<div class="card" style="box-shadow:none"><h2 style="margin-bottom:6px">${uf.toUpperCase()} · ${esc(UFN[uf])}<span class="sub">${fp(p*100,1)} das seções</span></h2>`;
  if(!d||!d.v.vv){return h+`<div class="empty-msg">Aguardando dados do 2º turno.</div><p class="note">1º turno: ${esc(r.l[0])} (${esc(r.l[1])}) ${fd(r.l[3],1)}% · ${esc(r.d[0])} (${esc(r.d[1])}) ${fd(r.d[3],1)}%.</p></div>`}
  const find=n=>d.cands.find(c=>nm(c.nmu)===nm(n)||nm(c.nm)===nm(n)),a=find(r.l[0])||d.cands[0],b=find(r.d[0])||d.cands[1]||d.cands[0],vv=d.v.vv,sa=a.vap/vv*100,sb=b.vap/vv*100;
  const lead=a.vap>=b.vap?a:b,oth=lead===a?b:a,dif=lead.vap-oth.vap;
  h+=`<div class="strip" style="height:30px"><div style="width:${sa/(sa+sb)*100}%;background:var(--fg2);color:var(--bg);display:flex;align-items:center;padding-left:8px;font-weight:600;font-size:12px;white-space:nowrap;overflow:hidden">${esc(a.nmu)} ${fp(sa,1)}</div><div style="flex:1;background:var(--accent);color:#fff;display:flex;align-items:center;justify-content:flex-end;padding-right:8px;font-weight:600;font-size:12px;white-space:nowrap;overflow:hidden">${esc(b.nmu)} ${fp(sb,1)}</div></div>`;
  h+=`<div class="tw" style="margin-top:6px"><table><tbody><tr><td>${esc(a.nmu)} <small style="color:var(--muted)">${esc(a.party)}</small></td><td class="n">${fi(a.vap)}</td><td class="n">${fp(sa)}</td></tr><tr><td>${esc(b.nmu)} <small style="color:var(--muted)">${esc(b.party)}</small></td><td class="n">${fi(b.vap)}</td><td class="n">${fp(sb)}</td></tr></tbody></table></div>`;
  h+=`<p style="margin:6px 0 2px"><span class="pill" style="background:var(--surface2)">${dif===0?'empate':esc(lead.nmu)+' à frente'}</span> <span class="num" style="color:var(--fg2)">margem ${fi(dif)} votos (${fd(dif/vv*100,2)} p.p.)</span></p>`;
  if(p>=.02&&p<.999){const k=1/p,pa=a.vap*k,pb=b.vap*k;h+=`<p class="note" style="margin:2px 0">Projeção aritmética (votos ÷ fração de seções): ${esc(a.nmu)} ${fp(pa/(pa+pb)*100,1)} · ${esc(b.nmu)} ${fp(pb/(pa+pb)*100,1)}. Hipótese, não previsão.</p>`}
  const e=d.e;if(e.est)h+=`<p class="note" style="margin:2px 0">Comparecimento nas seções totalizadas: ${fp(e.c/e.est*100,1)} · brancos ${fp(d.v.vb/(d.v.tv||1)*100,1)} · nulos ${fp(d.v.vn/(d.v.tv||1)*100,1)}.</p>`;
  h+=`<p class="note" style="margin:2px 0">1º turno: ${esc(r.l[0])} ${fd(r.l[3],1)}% · ${esc(r.d[0])} ${fd(r.d[3],1)}%.</p></div>`;return h;
}
function draw(){root.innerHTML=`<div class="cols2">${GU.map(card).join('')}</div><p class="note">Cada governo é uma disputa independente, sem agregado nacional. Votos <i>sub judice</i> ficam fora dos válidos. O resultado oficial é o do TSE.</p>`}
AP.S.onUpdate=draw;wire({pres:false,gov:true});draw();
'''
fim(s, 'governadores', LIVE('Apuração dos seis segundos turnos', 'RN, AM, AC, ES, TO e DF · dados ao vivo'), js)
