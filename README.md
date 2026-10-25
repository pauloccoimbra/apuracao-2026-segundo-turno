# Apuração 2026 · 2º turno

Painel e análises do segundo turno das eleições gerais de 2026 (25 de outubro de 2026), feitos só com os arquivos públicos de divulgação de resultados do TSE. Site estático: o navegador de cada visitante lê os dados e calcula tudo localmente.

- **Site:** https://pauloccoimbra.github.io/apuracao-2026-segundo-turno/
- **Repositório:** https://github.com/pauloccoimbra/apuracao-2026-segundo-turno
- **Site irmão (1º turno, 4 de outubro):** https://pauloccoimbra.github.io/apuracao-2026-primeiro-turno/

## Avisos

- Projeto independente de Paulo C. Coimbra (UFJF), sem vínculo com o TSE, partidos ou candidaturas.
- Cenários e projeções são hipóteses de trabalho, não previsão nem pesquisa eleitoral. O resultado oficial é o do TSE (https://resultados.tse.jus.br/).
- **Versão preliminar (v0.1).** A leitura ao vivo não foi testada contra os arquivos reais do 2º turno; só contra dados simulados no formato do 1º turno.

## Abas

- **Resumo** (`index.html`): porta de entrada, números do 1º turno, calendário, conferências, glossário, limites, como citar, privacidade.
- **Painel** (`painel.html`): presidente (nacional, região, UF) e os seis governos (RN, AM, AC, ES, TO, DF); projeção aritmética rotulada como tal.
- **Mapa** (`mapa.html`): grade por UF, presidente e governador, 2º turno e 1º turno. Municípios e zonas: próxima versão.
- **Evolução** (`evolucao.html`): série registrada no navegador (seções, percentuais, diferença), com a caixa "Incluir o exterior no total nacional".
- **Resultado × cenários** (`cenarios.html`): régua aritmética (r, s, s*(r)) com o 1º turno; r e s observados quando a apuração chega a 99,9%.
- **Governadores** (`governadores.html`): seis segundos turnos, voto cruzado e os 21 governos definidos no 1º turno.

## Códigos de eleição do TSE

O 2º turno usa códigos de eleição próprios. Informe-os no cartão "Códigos de eleição" de qualquer página de apuração, ou use `?fed=<código>&est=<código>` no endereço (`?limpar` apaga). Ficam só no navegador. No 1º turno eram 6257 (presidente) e 6259 (governador).

## Convenções

Margem: **Flávio Bolsonaro − Lula** (positivo favorece Flávio). 27 UFs + Exterior (28 unidades). Vírgula decimal, ponto de milhar, sinal de menos tipográfico (−). Votos *sub judice* fora dos válidos.

## Estrutura

```
index.html ... governadores.html   páginas prontas (CSS, JS e dados do 1º turno embutidos)
404.html
fonts/                             IBM Plex (woff2, SIL OFL 1.1)
tools/fontes/                      modelos (pag_*.html), base.css, lib.js, dados26.js, montar.py
tools/aplicar_layout.py            barra, rodapé, fontes, transições, contador
tools/layout/                      abas.json, layout.css, rodape.html
```

Para alterar: edite os modelos em `tools/fontes/` e rode `python3 tools/fontes/montar.py` na pasta do site (gera as páginas e aplica o layout). O contador GoatCounter usa o código `apuracao-2026-segundo-turno` (`GC_CODE` em `tools/aplicar_layout.py`); o site precisa existir no GoatCounter com esse código.

## Licenças e citação

Código sob MIT (`LICENSE`); dados do TSE sob os termos do TSE; fontes IBM Plex sob SIL OFL 1.1.

> Coimbra, P. C. *Apuração 2026 · 2º turno: painel e análises*. Site estático, outubro de 2026. https://pauloccoimbra.github.io/apuracao-2026-segundo-turno/ (acesso em: data).
