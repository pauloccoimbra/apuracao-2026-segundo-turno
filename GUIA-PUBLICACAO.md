# Guia de publicação (2º turno)

1. No repositório `apuracao-2026-segundo-turno`, substitua o conteúdo (incluindo a página "em construção") pelo da pasta `apuracao-2026-segundo-turno`. Mantenha `.nojekyll`. Não faça upload de `MUDANCAS.md` e `PENDENCIAS.md` (o `.gitignore` os exclui).
2. Settings → Pages: branch `main`, pasta `/ (root)`. Confira `https://pauloccoimbra.github.io/apuracao-2026-segundo-turno/` e o botão "1º turno ↗".
3. Antes das 17h de 25/10, abra o painel com `?fed=<código>&est=<código>` e confira com o TSE. Se não ler, use o cartão "Códigos de eleição".
4. Os links entre os sites já existem nos dois lados (1º turno tem "2º turno ↗").
5. Depois do resultado final e das conferências: release `v1.0.0` no GitHub para o Zenodo (DOI), como no `GUIA-GITHUB-ZENODO.md` do 1º turno. Só então descomente `doi` em `CITATION.cff` e o selo no README. Não use DOI nem ORCID inventados.
