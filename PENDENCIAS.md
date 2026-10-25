# Pendências (v0.1)

Arquivo de trabalho; fora do repositório pelo `.gitignore`.

1. **Códigos de eleição do 2º turno** (federal e estadual): confirmar no aplicativo do TSE; informar na página ou por `?fed=&est=`. Ou fixar em `tools/fontes/lib.js` depois de confirmados.
2. Confirmar formato dos arquivos do 2º turno (mesmo padrão `…-c0001-e00XXXX-u.json` e `br-e00XXXX-ab.json`?); lista de UFs com governador em 2º turno (RN, AM, AC, ES, TO, DF) no TSE.
3. ~~GoatCounter~~: resolvido na v0.3 (código `apuracao-2026-segundo-turno`; criar o site com esse código no GoatCounter).
4. **Cenários A, B, C e régua 2002–2022**: enviar o simulador antigo ou autorizar refazer com fonte citada.
5. **Link "Pesquisas do 2º turno 2026"**: endereço exato (não incluído).
6. Evolução: horários de totalização por seção (para reconstituir a noite).
7. Municípios e zonas no Mapa (reaproveitar `mapa.html` do 1º turno); lista de municípios do TSE do 2º turno (`arquivo-urna/…/config`).
8. Transferência por UF (Duncan–Davis e Goodman, com ressalvas), Participação, comparação 1º → 2º por município.
9. Votos sub judice/recontagens: hoje só exibidos (`vansj`) e fora dos válidos.
10. ORCID e DOI: não preenchidos.

## Pendências após v0.2
- Códigos de eleição do 2º turno no TSE (informar no card "Códigos de eleição" ou ?fed=&est=).
- Caminho da configuração de municípios do Mapa (arquivo-urna/3220/config/…): confirmar se o 2º turno usa o mesmo.
- Mapa: níveis município e zona só foram testados com simulação no nível UF; geometria do IBGE e arquivos municipais dependem do navegador do usuário.
- Evolução: histórico só existe a partir da abertura da página; reconstituição com horários de totalização das seções fica para depois da apuração.
- Atemporal: ordem do 1º turno usada como referência até haver ordem observada no 2º turno.
- Transferência de votos por UF; cenários A, B e C e régua 2002–2022; link "Pesquisas do 2º turno".
- Prumo: faixa é propagação de hipótese (±X p.p. ajustável), não intervalo estatístico estimado.
- Verificação final por agente independente ainda não feita.

## Após v0.3
- Mapa por município/zona do 2º turno: padrão de endereço confirmado (6260 municipal: 200); falta ver com dados reais após o início da apuração.
- O alerta só funciona com a página aberta no navegador.
