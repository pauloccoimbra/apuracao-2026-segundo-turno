#!/usr/bin/env python3
"""Monta as páginas HTML a partir dos modelos em tools/fontes/ e aplica o layout comum.
Uso (a partir da pasta do site):  python3 tools/fontes/montar.py [--demo] [--saida PASTA]
Modelos: pag_*.html, base.css, lib2.js, dados26.js, demo.js. Não edite à mão os HTMLs gerados.
pag_mapa/perfil/participacao/governadores vêm de gerar_pag_mapa.py e gerar_pag_apoio.py (a partir do site do 1º turno)."""
import os, shutil, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
args = sys.argv[1:]
DEMO = '--demo' in args
SAIDA = RAIZ
if '--saida' in args:
    SAIDA = os.path.abspath(args[args.index('--saida') + 1])
ler = lambda n: open(os.path.join(AQUI, n), encoding='utf8').read()
css, dados, lib = ler('base.css'), ler('dados26.js'), ler('lib2.js')
if DEMO:
    lib = lib.replace('<option value="60000" selected>60 s</option>', '<option value="3000" selected>3 s (demo)</option><option value="60000">60 s</option>')
    lib = lib.replace('/*@DEMO*/', ler('demo.js'))
PAGINAS = ['index', 'painel', 'mapa', 'evolucao', 'atemporal', 'cenarios', 'perfil', 'participacao', 'governadores']
if SAIDA != RAIZ:
    if os.path.exists(SAIDA): shutil.rmtree(SAIDA)
    shutil.copytree(RAIZ, SAIDA, ignore=shutil.ignore_patterns('tools', '*.zip', '.git'))
    shutil.copytree(os.path.join(RAIZ, 'tools'), os.path.join(SAIDA, 'tools'))
for nome in PAGINAS:
    h = ler(f'pag_{nome}.html')
    if nome == 'mapa':
        h = h.replace('<!--@DEMOLIB-->', f'<script>{dados}</script><script>{lib}</script>' if DEMO else '')
    else:
        h = h.replace('/*@CSS*/', css).replace('/*@DATA*/', dados).replace('/*@LIB*/', lib)
    open(os.path.join(SAIDA, f'{nome}.html'), 'w', encoding='utf8').write(h)
    print('montado', nome)
subprocess.check_call([sys.executable, os.path.join(SAIDA, 'tools', 'aplicar_layout.py'), SAIDA])
