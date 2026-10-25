# v0.1 preliminar (24/10/2026)

Arquivo de trabalho; fora do repositório pelo `.gitignore`.

- Site novo, substitui a página "em construção". Seis páginas: Resumo, Painel, Mapa (grade por UF), Evolução, Resultado × cenários, Governadores.
- Reaproveitado do 1º turno: mecanismo de layout (`aplicar_layout.py`, marca trocada para "Apuração 2026 · 2º turno", botão "1º turno ↗"), fontes IBM Plex, formato de leitura dos JSON do TSE (`carg[0].agr[].par[].cand[]`, `-ab.json`), dados do 1º turno por UF (`window.D26`, sem os dados de Congresso).
- Fundo branco; tipografia 14/13,5/13 px; margem Flávio Bolsonaro − Lula; "27 UFs + Exterior".
- Novo: cartão "Códigos de eleição" (ou `?fed=&est=`), porque o código do 2º turno no TSE não foi confirmado.
- Contador GoatCounter desligado (`GC_CODE` vazio).
- Números do 1º turno recalculados dos dados embutidos e conferidos: 119.300.788 válidos; Lula 53.879.538; Flávio 56.104.503; diferença 2.224.965; eliminados 9.316.747; brancos + nulos 5.969.801; abstenção 33.469.667 de 158.745.502 (21,08%); M/(2E) = 0,119407.

## Testes feitos
Chromium (Playwright), 1400 px claro e 390 px escuro, TSE simulado no formato do 1º turno (presidente em 28 unidades e seis governos, duas fases de apuração) e sem códigos: sem erro de console, sem NaN/undefined/Infinity, sem rolagem horizontal, tipografia 13/13,5 px em `main`.

## Não feito
- Nenhum teste contra os arquivos reais do 2º turno (TSE bloqueado no ambiente de construção).
- Verificação final por outro agente (fatos, aritmética, textos).
- Páginas: Transferência por UF, Participação, mapa de municípios/zonas, comparação 1º → 2º por município.
- Cenários A, B e C e régua histórica 2002–2022 (não estavam no zip do 1º turno).

## v0.2 (preliminar)
- Painel reescrito no padrão do 1º turno: card do líder, card de votação (nominais, válidos, anulados, anulados sub judice, brancos, nulos, eleitorado apto, apto das seções totalizadas, comparecimento, abstenção), resultado nacional com Flávio Bolsonaro (PL 22) primeiro, projeção aritmética com Prumo (faixa de incerteza ajustável) e a explicação mantida, mapa "Estados: líder por UF", evolução do % de válidos, tabela por região e "Presidente por estado".
- Novas abas: Mapa (código do 1º turno, códigos do 2º turno configuráveis, governador restrito a 6 UFs), Atemporal, Perfil do voto, Participação.
- Evolução refeita (Evolução, Por estado, Velocidade, Trocas, Método e fontes) com deslizador de tempo, a partir das leituras registradas no navegador.
- Resultado × cenários: atalhos, cenários salvos, matriz r × s, r e s observados/projetados e por UF.
- Governadores: bloco ao vivo dos seis segundos turnos acima do conteúdo do 1º turno.

## v0.3 (25/10/2026, verificação pré-apuração)
- Códigos do TSE confirmados na configuração oficial (ele-c.json): 2º turno presidente **6258**, governadores **6260** (pleito 3221). Agora são o padrão do site (continua possível alterar em "Códigos de eleição").
- Arquivos do 2º turno já publicados (zerados) e lidos no formato real; governadores casados pelo número de urna (RN 44×13, AM 55×22, AC 11×10, ES 10×15, TO 44×45, DF 11×13) e com nomes curtos do site.
- Novo: alerta de interrupção. Se nenhuma seção nova for totalizada no país por 10 minutos, aparece faixa de aviso, o título da aba muda para "⚠ Totalização parada" e, com "Avisar-me" ligado, toca um bipe e dispara notificação do navegador; avisa também quando retoma e lista as interrupções registradas. DEMO: link "simular interrupção".
- Painel (card "Estados · líder por UF") e Mapa: seletor **Dados** com "2º turno (ao vivo)" e "1º turno (referência)". No Painel o 1º turno usa o resultado final já embutido (cor e % do mais votado). No Mapa carrega os arquivos do 1º turno (6257 presidente, 6259 governador, 27 UFs, até município e zona).
- Corrigido: o Mapa só lia 6258/6260 se estivessem salvos no navegador; agora são o padrão.
- Rodapé: GoatCounter ativado com o código `apuracao-2026-segundo-turno` (contador próprio do 2º turno). Texto do rodapé alinhado ao do 1º turno (malhas do IBGE, sem "quando ativada").
- Aviso sonoro de interrupção: botão "Ligar aviso sonoro" + "Testar som"; alarme de 4 tons repetido a cada 30 s enquanto a totalização estiver parada (10 min sem seção nova), 3 tons ascendentes na retomada; instruções no item "Como usar o aviso sonoro de interrupção" (todas as abas ao vivo) e no Resumo. Exige clique para liberar o som e a aba aberta.
