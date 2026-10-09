---
name: ajuda
description: Orienta o uso do plugin gabju — o que cada skill faz, qual usar, como pedir e como combiná-las. Use somente quando o usuário pedir ajuda expressamente ("ajuda", "o que você faz", "qual skill usar", "como começar", "como funciona o gabju").
---

# Ajuda do gabju

Responda a pedidos de orientação sobre o plugin. Esta skill **não executa** análise nem minuta: indica o caminho e devolve a decisão ao usuário.

## Como responder

1. **Pergunta genérica** ("o que você faz?", "como começar?") → apresente o [mapa de skills](#mapa-de-skills) de forma resumida, o [fluxo recomendado](#fluxo-recomendado) e as [dicas de uso](#dicas-de-uso). Ofereça detalhar qualquer item.
2. **Pergunta sobre uma tarefa** ("como faço um saneamento?") → indique a skill adequada, quando usar e quando não usar, e um exemplo de pedido adaptado ao que o usuário descreveu.
3. **Pergunta com anexos** ("o que faço com esses documentos?") → faça triagem: identifique o tipo e a fase do processo apenas pelo necessário para orientar (nomes dos arquivos, cabeçalhos, espécie das peças), recomende a sequência de skills e pergunte se o usuário quer iniciar. Não analise mérito, não resuma peças e não comece outra skill sem confirmação.
4. **Dúvida detalhada** (opções de scripts, personalização, desenvolvimento) → responda com base no [README do plugin](../../README.md), lendo apenas a seção pertinente.

Seja breve: responda à pergunta feita, sem despejar o catálogo inteiro quando não for pedido. Não invente skills, opções ou funcionalidades que não constem deste arquivo ou do README.

## Mapa de skills

### Leitura e segurança

| Quero... | Skill | Exemplo de pedido |
|---|---|---|
| Recuperar a leitura de um PDF ilegível, truncado ou inacessível | $indexar-pdf | "O PDF dos autos está ilegível nas páginas 40 a 85. Use $indexar-pdf." |
| Verificar se há instruções hostis a IA escondidas nos documentos | $auditar-prompt-injection | "Antes de analisar, use $auditar-prompt-injection nas peças." |

### Análise (insumo, não minuta)

Estas três só são acionadas quando o usuário pede expressamente o objetivo delas (análise de controvérsias, análise de provas, resumo dos documentos).

| Quero... | Skill | Exemplo de pedido |
|---|---|---|
| Visão estruturada e fiel de cada documento anexado | $sumarizar-processo | "Use $sumarizar-processo nos documentos anexados." |
| Mapear os pontos fáticos e jurídicos controvertidos nas peças | $analisar-controversias | "Use $analisar-controversias antes do saneamento." |
| Avaliar as provas frente às hipóteses fáticas | $analisar-provas | "Use $analisar-provas; o laudo pericial é o Id. 4455." |

### Minutas

| Quero... | Skill | Exemplo de pedido |
|---|---|---|
| Minuta completa (relatório + fundamentação + dispositivo) de sentença, saneamento, tutela ou interlocutória | $minutar-completa | "Redija uma decisão sobre o pedido de tutela." |
| Relatório de sentença, saneamento, tutela ou interlocutória | $minutar-relatorio-geral | "Use $minutar-relatorio-geral para o relatório de uma sentença." |
| Despacho de impulso processual | $minutar-despacho | "Use $minutar-despacho: intimar a autora para réplica em 15 dias." |
| Decisão interlocutória geral (gratuidade, competência, provas etc.) | $minutar-interlocutoria | "Use $minutar-interlocutoria para rejeitar a impugnação à gratuidade." |
| Saneamento e organização do processo (art. 357 do CPC) | $minutar-saneamento | "Use $minutar-saneamento; deferir perícia contábil." |
| Tutela provisória, liminar ou cautelar | $minutar-tutela | "Use $minutar-tutela. Indeferir: não há perigo de dano." |
| Sentença completa por padrão | $minutar-sentenca | "Use $minutar-sentenca. Procedente: o PPP comprova a exposição a ruído." |
| Decisão em embargos de declaração | $minutar-embargos | "Use $minutar-embargos. Rejeitar: não há a omissão alegada." |
| Deliberação judicial e providências de impulso | $minutar-dispositivo | "Use $minutar-dispositivo: procedência parcial, autor com AJG." |

### Revisão e validação

| Quero... | Skill | Exemplo de pedido |
|---|---|---|
| Revisar linguagem, técnica e estilo de um texto pronto | $revisar-texto | "Use $revisar-texto na minuta abaixo." |
| Conferir artigos, precedentes, transcrições e Ids. citados | $validar-citacoes | "Use $validar-citacoes na fundamentação anexada." |

### Especialistas

| Quero... | Skill | Exemplo de pedido |
|---|---|---|
| Correção monetária, juros, custas, honorários, Price/SAC, índices | $esp-contadoria-judicial | "Use $esp-contadoria-judicial para verificar a tabela de amortização." |
| Analisar CNIS, tempo especial, PPP/LTCAT, aposentadoria especial e RMI | $esp-previdenciario | "Use $esp-previdenciario para examinar o PPP, o tempo especial e os efeitos da ADI 6309." |
| Ações de saúde pública (SUS, medicamentos, ANVISA, NATJUS) | $esp-direito-sanitario | "Use $esp-direito-sanitario com $minutar-tutela." |

### Esta skill

| Quero... | Skill | Exemplo de pedido |
|---|---|---|
| Saber o que o plugin faz ou qual skill usar | $ajuda | "Use $ajuda: como faço uma decisão de saneamento?" |

## Fluxo recomendado

O caminho principal é pedir diretamente o ato desejado, sem conduzir cada seção à mão:

1. **Pedido** — anexe as peças e diga, por exemplo, "Minute uma sentença" ou "Redija uma decisão de tutela". Se já houver deliberação, informe o resultado e a razão central de cada questão.
2. **Preparação interna** — o modelo lê os anexos, verifica instruções hostis com $auditar-prompt-injection e recorre a $indexar-pdf somente diante de dificuldade concreta de leitura. As skills especialistas apoiam a minuta quando o tema exigir.
3. **Deliberação** — responda aos checkpoints de análise e plano quando faltarem orientações suficientes. O relatório e as demais partes são preparados internamente.
4. **Entrega** — receba a minuta completa em um único documento. $minutar-completa coordena sentença, tutela, saneamento e interlocutória; embargos e despachos seguem as skills próprias. Não é necessário pedir "minuta completa" nem chamar separadamente relatório e dispositivo.
5. **Revisão opcional** — peça $revisar-texto e/ou $validar-citacoes se desejar revisão ou conferência específica.

**Execução modular somente por pedido expresso:** para receber uma parte isolada, diga "redija somente a fundamentação", "apenas o relatório" ou "apenas o dispositivo". As skills $minutar-relatorio-geral e $minutar-dispositivo atendem às seções correspondentes. Relatórios analíticos de $sumarizar-processo, $analisar-controversias e $analisar-provas também dependem de pedido expresso; não são etapas obrigatórias da minuta.

## Dicas de uso

- **Escopo padrão.** "Minute uma sentença" já inclui relatório, fundamentação, dispositivo e providências. Para receber partes isoladas, delimite expressamente: "redija a fundamentação", "somente o relatório" ou "apenas o dispositivo". Chamar a skill do ato pelo nome também produz minuta completa por padrão.

- **Não é obrigatório usar `$`.** Na maioria das skills, basta pedir em linguagem natural. Chamar pelo nome garante a skill escolhida.
- **Checkpoints.** Sentença, tutela, saneamento e embargos param para o usuário escolher o encaminhamento. Para pular essas paradas, informe já no pedido o **resultado e a razão central** de cada questão. Informar só o tipo de ato ou o assunto não basta.
- **Dados do gabinete.** Localidade e unidade vêm das instruções personalizadas do ambiente de IA. Sem elas, a minuta sai com placeholders como `[LOCALIDADE/UF]`. A minuta termina na linha de local e data, sem assinatura: ela é aposta pelo sistema processual.
- **Revisão humana.** Toda minuta é rascunho: confira fatos, Ids., valores e fundamentos antes de assinar.
- **Mais detalhes.** O [README do plugin](../../README.md) traz descrição completa de cada skill, opções dos scripts e instruções de desenvolvimento.
