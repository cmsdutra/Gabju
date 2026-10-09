---
created: 2026-10-08
updated: 2026-10-08
ai-agent: "Codex CLI"
---

# Estrutura e Invariantes do Dispositivo

Fonte: leitura literal de amostra estratificada de minutas reais do gabinete por `act-type` e período. As regras abaixo são invariantes fortes na amostra, salvo onde indicado como variação estilística legítima.

## Headings

- `## **DELIBERAÇÃO JUDICIAL**` — nível 2, texto em maiúsculas, negrito duplo-asterisco. Nunca `###`/`#`, nunca "DISPOSITIVO" como heading real.
- `## **PROVIDÊNCIAS DE IMPULSO PROCESSUAL**` — mesmo padrão de formatação.
- Ordem sempre: DELIBERAÇÃO JUDICIAL primeiro, PROVIDÊNCIAS DE IMPULSO PROCESSUAL depois.
- Despacho de mero expediente sem comando decisório próprio (só movimentação cartorária) → só `PROVIDÊNCIAS DE IMPULSO PROCESSUAL`, sem heading de deliberação.

## Numeração dos itens

- **DELIBERAÇÃO JUDICIAL**: alíneas minúsculas entre parênteses em negrito — `**(a)**`, `**(b)**`, `**(c)**`. Subitens com numeração decimal da letra-mãe: `**(a.1)**`, `**(a.2)**`, até `**(d.5.2)**` em quesitos periciais numerados. Nunca numeral romano, nunca letra maiúscula.
- **PROVIDÊNCIAS DE IMPULSO PROCESSUAL**: sempre numeral romano minúsculo entre parênteses em negrito — `**(i)**`, `**(ii)**`, `**(iii)**`, com o mesmo padrão decimal em subitens. Invariante sem exceção na amostra — é o marcador mais confiável para diferenciar as duas seções.
- Antes de entregar, confira a sequência (sem letra/romano repetido ou pulado) — erro de digitação nesse ponto é o defeito de revisão mais comum observado no corpus.

## Verbo de comando

- **DELIBERAÇÃO JUDICIAL**: verbo-núcleo em negrito. Padrão de apresentação do plugin: **CAIXA ALTA** no verbo principal de sentenças e da maioria das decisões (ex.: `**REJEITO**`, `**ACOLHO**`, `**DEFERIR**`, `**DECLARO**`). Verbos de alíneas subordinadas/acessórias que apenas desdobram o item principal podem ficar em minúscula (ex.: `**(a.1)** **declarar** nulo o contrato...`). Não inverta nem misture os dois padrões dentro do mesmo item.
- **PROVIDÊNCIAS DE IMPULSO PROCESSUAL**: verbo em negrito sempre em **minúscula**, mesmo quando o verbo correspondente na deliberação estava em maiúscula (ex.: `**intimar**`, `**colher**`, `**certificar**`, `**arquivar**`, `**cumprir**`, `**concluir**`, `**oficiar**`).
- Nota de corpus: decisões interlocutórias mostram alguma oscilação real de caixa no verbo principal (maiúscula/minúscula convivendo). Trate isso como inconsistência legada a não reproduzir, não como padrão a seguir — aplique sempre CAIXA ALTA no verbo principal da deliberação.

## Fórmula de abertura da deliberação

- `Diante do exposto:` — mais comum em sentenças definitivas.
- `Diante do exposto, **DECIDO**:` — comum em decisões interlocutórias e tutelas.
- `Ante o exposto, **DECIDO**:` — convenção específica de **decisões de saneamento** (100% da amostra de saneamento usa "Ante o exposto", não "Diante do exposto").
- `Diante do exposto, **DETERMINO**:` — variante rara, decisão que só determina diligência sem comando de mérito propriamente dito.
- Sempre há fórmula de transição antes do primeiro item; nenhum arquivo da amostra abre direto em "(a)".

## Frase de abertura das providências

`A Secretaria deverá:`. Em Juizado Especial Federal, adapte para a secretaria/unidade do JEF quando aplicável.

## Partes no dispositivo

Nome próprio = subsidiário: use para identificar o destinatário do comando quando indispensável; depois prefira a função processual da fase/incidente (executada, exequente, ré, autora etc.). Providências de impulso podem referir a parte por função ou ao item deliberativo, evitando repetir nomes já individualizados.

## Fórmula de encerramento (local/data)

Última linha da minuta, fora de qualquer item, texto corrido sem negrito/lista: `[LOCALIDADE/UF], data de assinatura do sistema.` Nunca hardcode data real — a data é sempre gerada pelo sistema de assinatura.

Nada vem depois dessa linha: sem assinatura, nome ou cargo do(a) magistrado(a), "(assinado digitalmente)" ou marcação HTML. A assinatura é aposta pelo sistema processual.

## Referência a Id. no dispositivo

Padrão geral de citação de peças dos autos: `Id. <número>` (maiúscula em "Id", ponto, número sem separador de milhar). Usado tanto na deliberação (para identificar o objeto do julgamento: "a impugnação ao cumprimento de sentença (Id. 2218005274)") quanto nas providências (para referenciar decisão anterior a cumprir: "cumprir, no que restar, o disposto na sentença de Id. 2202144738"). Com página específica: `Id. 2213462831, p. 444`.

## Preliminares e prejudiciais no dispositivo

Regra-base (herdada de `minutar-sentenca`, confirmada pelo corpus para **sentenças de mérito**): preliminar/prejudicial **rejeitada/superada** fica só na fundamentação; só entra como alínea própria do dispositivo a questão prefacial **acolhida**, quando decota a cognição de mérito, extingue parte do processo ou produz providência dispositiva própria.

**Exceção observada e confirmada no corpus** — decisões cujo próprio objeto central é resolver um conjunto de teses/impugnações (típico de **decisão interlocutória sobre impugnação ao cumprimento de sentença**, mas aplicável a qualquer decisão estruturada como julgamento de teses autônomas): cada tese, **inclusive as rejeitadas**, recebe alínea própria, porque ali a rejeição da tese não é passagem lógica incidental a um pedido principal distinto — é o próprio mérito da decisão. Exemplo real:
> **(a)** **REJEITAR** a impugnação à gratuidade da justiça; **(b)** **REJEITAR** a preliminar de ilegitimidade ativa; **(c)** **REJEITAR** a prejudicial de prescrição; **(d)** ... [mérito remanescente]

Critério para diferenciar: pergunte se a questão prefacial é **incidental** a um pedido de mérito distinto (regra-base se aplica: só acolhida vai ao dispositivo) ou se **é ela própria, junto de outras, o objeto integral da decisão** (exceção se aplica: cada uma vira alínea, acolhida ou rejeitada).

## Padrões formais recorrentes a preservar

- Erros a nunca reproduzir: letra/numeral repetido (ex. dois itens "(b)" seguidos), verbo de comando mal grafado (ex. "DETERMO" por "DETERMINO") — defeitos humanos pontuais do corpus, não convenção do gabinete.
- Quadro de valores/apuração extenso: prefira tabela Markdown a texto corrido; evite depender de imagem colada quando o conteúdo puder ser expresso em texto/tabela.
