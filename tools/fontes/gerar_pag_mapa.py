#!/usr/bin/env python3
"""Gera pag_mapa.html a partir do mapa.html do 1º turno (leitura apenas), trocando os códigos de eleição,
o texto e restringindo governador aos 6 estados com 2º turno. Uso: python3 gerar_pag_mapa.py <mapa.html do 1T>"""
import sys, os, re
src = open(sys.argv[1], encoding='utf8').read()
def sub(a, b, n=1):
    global src
    assert src.count(a) >= 1, a[:60]
    src = src.replace(a, b) if n == 0 else src.replace(a, b, n)
sub('<title>Mapa · Apuração 2026 · 1º turno</title>', '<title>Mapa · Apuração 2026 · 2º turno</title>')
sub('Mapa da apuração do 1º turno de 2026 para presidente e governador: país, regiões, estados, municípios e zonas eleitorais, com dados públicos do TSE.',
    'Mapa da apuração do 2º turno de 2026: presidente (país, regiões, estados, municípios e zonas) e os seis governos estaduais, com dados públicos do TSE.')
sub('Mapa · Apuração 2026 · 1º turno<small id="sub">1º turno · Presidente · dados públicos do TSE</small>', 'Mapa · Apuração 2026 · 2º turno<small id="sub">2º turno · Presidente · dados públicos do TSE</small>')
sub("'1º turno · Presidente · dados públicos do TSE':'1º turno · Governador · uma disputa por estado · dados públicos do TSE'", "'2º turno · Presidente · dados públicos do TSE':'2º turno · Governador · seis estados com 2º turno · dados públicos do TSE'")
# códigos de eleição: informados no Painel (ou ?fed=&est=), guardados no navegador
sub("const OFFS={pres:{e:6257,c:1,n:'Presidente'},gov:{e:6259,c:3,n:'Governador'}};",
"""const LSG=k=>{try{return localStorage.getItem(k)}catch(e){return null}};
(()=>{const q=new URLSearchParams(location.search);['fed','est','root'].forEach(k=>{const v=q.get(k);if(v){try{localStorage.setItem('ap26s.'+k,JSON.stringify(v.trim()))}catch(e){}}});if(q.get('limpar')!==null)['fed','est','root'].forEach(k=>{try{localStorage.removeItem('ap26s.'+k)}catch(e){}})})();
const codeOf=k=>{try{return +String(JSON.parse(LSG('ap26s.'+k))||'').replace(/\\D/g,'')||0}catch(e){return 0}};
const GOVUF=['rn','am','ac','es','to','df'];
const OFFS={pres:{get e(){return window.__demo?9001:codeOf('fed')},c:1,n:'Presidente'},gov:{get e(){return window.__demo?9002:codeOf('est')},c:3,n:'Governador'}};
const needCode=()=>{if(!OFFS[S.off].e)throw new Error('informe os códigos de eleição do 2º turno (card "Códigos de eleição" na aba Painel, ou ?fed=…&est=… no endereço)')};""")
sub("const TSE='https://resultados.tse.jus.br/oficial/ele2026/';", "const TSE=(()=>{try{const r=JSON.parse(localStorage.getItem('ap26s.root')||'null');if(r)return r.endsWith('/')?r:r+'/'}catch(e){}return 'https://resultados.tse.jus.br/oficial/ele2026/'})();")
# demo: leitura simulada só para os arquivos de UF
sub("async function getj(u){\n", "async function getj(u){\n  if(window.__demo&&u.indexOf(IBGE)!==0){return /\\/dados\\/([a-z]{2})\\/\\1-c\\d{4}-e\\d{6}-u\\.json$/.test(u)?window.__demo.get(u):null}\n")
sub("async function loadUFs(tok){\n  let d=0;const off=S.off;\n  const res=await pool(ALLUF.map(u=>async()=>{if(tok!==S.tok)return;UFTs[off][u]=parse(await getj(uUF(u,off)));d++;if(tok===S.tok)prog('Carregando estados',d,27)}),8);",
"async function loadUFs(tok){\n  needCode();let d=0;const off=S.off;\n  const VAZIO=()=>({c:{},vv:0,vb:0,vn:0,tv:0,ts:0,st:0,te:0,cp:0,ab:0});\n  const res=await pool(ALLUF.map(u=>async()=>{if(tok!==S.tok)return;if(off==='gov'&&!GOVUF.includes(u)){UFTs[off][u]=VAZIO();d++;return}UFTs[off][u]=parse(await getj(uUF(u,off)))||VAZIO();d++;if(tok===S.tok)prog('Carregando estados',d,off==='gov'?6:27)}),8);")
sub("<!--@x-->", "", 0) if '<!--@x-->' in src else None
sub('<script>\n/* Geometria aproximada', '<!--@DEMOLIB--><script>\n/* Geometria aproximada')
sub('--bg:#f3f4f6; --surface:#ffffff','--bg:#ffffff; --surface:#ffffff')
# nota sobre governador
sub('<div class="seg" id="segOff">', '<div class="seg" id="segOff" title="Governador: apenas os seis estados com 2º turno">')

# ---- v0.3: seletor "Dados" (2º turno ao vivo / 1º turno de referência) e códigos padrão 6258/6260 ----
sub("||0}catch(e){return 0}};", "||({fed:6258,est:6260}[k]||0)}catch(e){return {fed:6258,est:6260}[k]||0}};")
sub("const needCode=()=>{if(!OFFS[S.off].e)", "const OK=()=>S.off+(S.t1?'1':'');\nconst needCode=()=>{if(!OFFS[OK()].e)")
sub("gov:{get e(){return window.__demo?9002:codeOf('est')},c:3,n:'Governador'}};", "gov:{get e(){return window.__demo?9002:codeOf('est')},c:3,n:'Governador'},pres1:{e:6257,c:1,n:'Presidente (1º turno)'},gov1:{e:6259,c:3,n:'Governador (1º turno)'}};")
sub("const S={off:'pres',", "const S={t1:false,off:'pres',")
sub("const UFTs={pres:{},gov:{}};", "const UFTs={pres:{},gov:{},pres1:{},gov1:{}};")
sub("const UFT=new Proxy({},{get:(_,k)=>UFTs[S.off][k],set:(_,k,v)=>{UFTs[S.off][k]=v;return true}});", "const UFT=new Proxy({},{get:(_,k)=>UFTs[OK()][k],set:(_,k,v)=>{UFTs[OK()][k]=v;return true}});")
sub("_d:{pres:{},gov:{}},_z:{pres:{},gov:{}}", "_d:{pres:{},gov:{},pres1:{},gov1:{}},_z:{pres:{},gov:{},pres1:{},gov1:{}}")
sub("get(){return M._d[S.off]}", "get(){return M._d[OK()]}")
sub("get(){return M._z[S.off]}", "get(){return M._z[OK()]}")
sub("const off=S.off;", "const off=OK();", 0)
sub("$('sub').textContent=S.off==='pres'?'2º turno · Presidente · dados públicos do TSE':'2º turno · Governador · seis estados com 2º turno · dados públicos do TSE';",
    "$('sub').textContent=S.t1?(S.off==='pres'?'1º turno (referência) · Presidente · dados públicos do TSE':'1º turno (referência) · Governador · 27 UFs · dados públicos do TSE'):(S.off==='pres'?'2º turno · Presidente · dados públicos do TSE':'2º turno · Governador · seis estados com 2º turno · dados públicos do TSE');")
sub('<div class="seg" id="segMode">', '<label>Dados <select id="selDados" title="Resultado ao vivo do 2º turno ou resultado final do 1º turno (referência)"><option value="2">2º turno (ao vivo)</option><option value="1">1º turno (referência)</option></select></label>\n    <div class="seg" id="segMode">')
sub("$('segMode').onclick=", "$('selDados').onchange=e=>{S.t1=e.target.value==='1';S.cand='';S.zsel=null;if(S.off==='gov'&&S.grp==='reg')S.grp='uf';goArr([S.lv,S.lv==='reg'?S.reg:S.uf,S.mun],true)};\n$('segMode').onclick=")

open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pag_mapa.html'), 'w', encoding='utf8').write(src)
print('ok', len(src))
