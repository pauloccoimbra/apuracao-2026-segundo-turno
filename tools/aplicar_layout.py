#!/usr/bin/env python3
"""Aplica o layout comum (barra de navegação, "Para que serve", "Veja também",
anterior/próxima, rodapé, fontes locais, transição entre páginas, contador de visitas)
a todas as páginas HTML do site. Idempotente: pode ser rodado quantas vezes quiser.

Uso:   python3 tools/aplicar_layout.py            (a partir da pasta do site)
       python3 tools/aplicar_layout.py /caminho/do/site

O gabarito fica em tools/layout/ (abas.json, layout.css, rodape.html).
Cada bloco inserido fica entre marcadores <!-- LAYOUT:XXX:INICIO --> ... <!-- LAYOUT:XXX:FIM -->.
"""
import json, os, re, sys, html

RAIZ = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'layout')
GC_CODE = 'apuracao-2026-segundo-turno'  # código do site no GoatCounter (parte antes de .goatcounter.com)

cfg = json.load(open(os.path.join(GAB, 'abas.json'), encoding='utf8'))
abas = cfg['abas']
grupos = {g['id']: g for g in cfg['grupos']}
por_arquivo = {a['arquivo']: a for a in abas}
css_layout = open(os.path.join(GAB, 'layout.css'), encoding='utf8').read()
rodape_tpl = open(os.path.join(GAB, 'rodape.html'), encoding='utf8').read()
fonts_css_path = os.path.join(RAIZ, 'fonts', 'fonts.css')
fonts_css = open(fonts_css_path, encoding='utf8').read() if os.path.exists(fonts_css_path) else ''
esc = html.escape


def marca(chave, conteudo):
    return f'<!-- LAYOUT:{chave}:INICIO -->{conteudo}<!-- LAYOUT:{chave}:FIM -->'


def remove(h, chave):
    return re.sub(rf'\s*<!-- LAYOUT:{chave}:INICIO -->.*?<!-- LAYOUT:{chave}:FIM -->', '', h, flags=re.S)


PRIM = 'https://pauloccoimbra.github.io/apuracao-2026-primeiro-turno/'


def nav_html(atual):
    partes = [f'<a class="mk" href="index.html">{esc(cfg["marca"])}</a>']
    partes.append('<a class="seg" href="'+PRIM+'" rel="noopener" title="Site do 1º turno (4 de outubro)">1º turno ↗</a>')
    gid = None
    for a in abas:
        if a['grupo'] != gid:
            if gid is not None:
                partes.append('</div>')
            gid = a['grupo']
            partes.append(f'<div class="g" role="group" aria-label="{esc(grupos[gid]["nome"])}"><span class="gl">{esc(grupos[gid]["nome"])}</span>')
        cur = ' aria-current="page"' if a['arquivo'] == atual else ''
        partes.append(f'<a href="{a["arquivo"]}"{cur}>{esc(a["nome"])}</a>')
    partes.append('</div>')
    return ('<a class="skip" href="#main">Pular para o conteúdo</a>'
            '<nav id="sitenav" aria-label="Páginas do site"><div class="in">' + ''.join(partes) + '</div></nav>'
            '<script>(function(){var n=document.querySelector("#sitenav .in"),a=n&&n.querySelector("[aria-current]");'
            'if(a)n.scrollLeft=a.offsetLeft-(n.clientWidth-a.offsetWidth)/2})()</script>')


def head_html(i, a):
    pre = ''
    if i > 0:
        pre += f'<link rel="prefetch" href="{abas[i-1]["arquivo"]}">'
    if i < len(abas) - 1:
        pre += f'<link rel="prefetch" href="{abas[i+1]["arquivo"]}">'
    return f'<style>{fonts_css}\n{css_layout}</style>{pre}'


def serve_html(a):
    if not a['serve']:
        return ''
    return f'<div class="serve wrap"><p><b>Para que serve:</b> {esc(a["serve"])}</p></div>'


def rodape_pagina(i, a):
    s = ''
    if a['veja']:
        links = ' '.join(f'<a href="{v}">{esc(por_arquivo[v]["nome"])}</a>' for v in a['veja'])
        s += f'<aside class="veja wrap" aria-label="Veja também"><b>Veja também:</b> {links}</aside>'
    ant = f'<a rel="prev" href="{abas[i-1]["arquivo"]}">← {esc(abas[i-1]["nome"])}</a>' if i > 0 else '<span></span>'
    prox = f'<a rel="next" href="{abas[i+1]["arquivo"]}">{esc(abas[i+1]["nome"])} →</a>' if i < len(abas) - 1 else '<span></span>'
    meio = '<a class="vz" href="index.html">Voltar ao Resumo</a>' if a['arquivo'] != 'index.html' else '<span></span>'
    s += f'<nav class="pager wrap" aria-label="Navegação entre abas">{ant}{meio}{prox}</nav>'
    s += rodape_tpl
    s += ('<script>(function(){var c=' + json.dumps(GC_CODE) + ';if(!c)return;'
          'var b="https://"+c+".goatcounter.com/",s=document.createElement("script");s.async=true;s.src="https://gc.zgo.at/count.js";'
          's.setAttribute("data-goatcounter",b+"count");document.head.appendChild(s);'
          'fetch(b+"counter/TOTAL.json").then(function(r){return r.ok?r.json():Promise.reject()}).then(function(j){'
          'var v=parseInt(String(j.count).replace(/\\D/g,""),10),e=document.getElementById("visitas");'
          'if(isFinite(v)&&v>0&&e)e.textContent="Visualizações do site: "+v.toLocaleString("pt-BR")}).catch(function(){})})();'
          '(function(){var m=document.getElementById("main");if(!m)return;m.setAttribute("tabindex","-1");'
          'if(!location.hash){window.scrollTo(0,0)}m.focus({preventScroll:true})})();</script>')
    return s


for i, a in enumerate(abas):
    caminho = os.path.join(RAIZ, a['arquivo'])
    if not os.path.exists(caminho):
        print('AVISO: não existe', a['arquivo']); continue
    h = open(caminho, encoding='utf8').read()
    for ch in ('HEAD', 'NAV', 'SERVE', 'RODAPE'):
        h = remove(h, ch)
    # título padronizado
    titulo = f'{a["nome"]} · Apuração 2026 · 2º turno'
    h = re.sub(r'<title>.*?</title>', f'<title>{esc(titulo)}</title>', h, count=1, flags=re.S)
    # cabeça
    h = h.replace('</head>', marca('HEAD', head_html(i, a)) + '</head>', 1)
    # <main> com id e tabindex
    def fix_main(m):
        t = m.group(0)
        if 'id=' not in t:
            t = t[:-1] + ' id="main">'
        return t
    h = re.sub(r'<main\b[^>]*>', fix_main, h, count=1)
    # barra logo após <body>
    h = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + marca('NAV', nav_html(a['arquivo'])), h, count=1)
    # "Para que serve" antes do <main>
    s = serve_html(a)
    if s:
        h = re.sub(r'(<main\b)', lambda m: marca('SERVE', s) + m.group(1), h, count=1)
    # veja também, anterior/próxima e rodapé depois de </main>
    h = h.replace('</main>', '</main>' + marca('RODAPE', rodape_pagina(i, a)), 1)
    open(caminho, 'w', encoding='utf8').write(h)
    print('ok', a['arquivo'])
