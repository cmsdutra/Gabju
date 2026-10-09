---
name: minutar-dispositivo
description: Redige a seção de dispositivo da minuta — DELIBERAÇÃO JUDICIAL e PROVIDÊNCIAS DE IMPULSO PROCESSUAL — a partir do resultado já deliberado e das circunstâncias modificadoras do caso (gratuidade, remessa necessária, honorários, custas, correção/juros, prazo recursal, execução invertida, PIX/RPV etc.). Use sempre que outra skill minutar-* (sentença, saneamento, tutela, interlocutória, despacho, embargos) chegar à etapa de redigir dispositivo/providências de impulso, ou quando o usuário pedir para redigir/ajustar diretamente a deliberação judicial ou as providências de impulso processual de uma minuta.
---

# /minutar-dispositivo

## Personalização

Leia [personalização do gabinete](../../references/personalizacao.md) ao aplicar convenções ou preencher dados institucionais e fechamento: use a personalização do ChatGPT disponível no contexto; dados ausentes recebem placeholders padrão.

## Leitura dos anexos

Quando precisar consultar anexos, tente primeiro a leitura direta. Se houver dificuldade concreta que impeça acessar o conteúdo necessário, acione $indexar-pdf somente para os PDFs afetados, informando a dificuldade observada. Tamanho e quantidade de páginas isolados não justificam indexação. Reutilize os textos recuperados e os diagnósticos ao retomar esta skill, preservando seu escopo e checkpoints.

Catálogo autocontido de padrões da seção de dispositivo (DELIBERAÇÃO JUDICIAL + PROVIDÊNCIAS DE IMPULSO PROCESSUAL), consolidado a partir de amostra estratificada de minutas reais do gabinete. Esta skill **não delibera o mérito** — converte um resultado já decidido (pela skill material chamadora ou pelo usuário) na estrutura e linguagem fixas do dispositivo do gabinete, escolhendo as fórmulas certas por espécie de ato e por circunstância modificadora do caso.

## Fluxo obrigatório

1. **Obtenha o resultado deliberado**: espécie de ato final (sentença procedente/parcial/improcedente/extintiva — "Sentença A/B/C" na convenção do gabinete —, saneamento, tutela concessiva/denegatória, despacho, embargos acolhidos/rejeitados/não conhecidos, decisão interlocutória geral) + comando principal. Se chamada por outra skill `minutar-*`, receba esse dado dela; se invocada diretamente pelo usuário sem essa definição, **pergunte antes de redigir** — esta skill não escolhe o mérito.
2. **Levante as circunstâncias modificadoras** aplicáveis ao caso concreto a partir das orientações do usuário, das peças anexadas e da fundamentação já redigida: gratuidade da justiça, remessa necessária, honorários, custas, correção monetária/juros, prazo recursal/trânsito/arquivamento, execução invertida/multa, PIX/RPV, litisconsórcio com resultados distintos, prioridade de tramitação. Nunca presuma a aplicação de uma circunstância sem base nos autos ou na orientação do usuário.
3. **Leia sempre** `references/estrutura.md` — regras fixas de heading, numeração, caixa do verbo, encerramento (sem assinatura) e a regra de preliminares/prejudiciais no dispositivo.
4. **Selecione os catálogos aplicáveis**: em `references/catalogo-especies.md`, o sub-catálogo da espécie de ato do passo 1; em `references/circunstancias.md`, cada circunstância do passo 2. São bancos de padrões de linguagem, não fonte de dado — adapte aos fatos, valores, partes e Ids. do caso concreto; nunca copie nome, valor ou Id. de exemplo do catálogo para a minuta real.
5. **Redija**, nesta ordem: `## **DELIBERAÇÃO JUDICIAL**` (alíneas minúsculas entre parênteses) e `## **PROVIDÊNCIAS DE IMPULSO PROCESSUAL**` (numerais romanos minúsculos entre parênteses), encerrando com a fórmula de local/data.
6. **Revise antes de entregar**: sequência de alíneas/romanos sem letra/numeral repetido ou pulado; verbo de comando na caixa correta (MAIÚSCULA na deliberação, minúscula no impulso); nenhuma preliminar/prejudicial indevida no dispositivo (regra do passo 3).
7. **Entregue o bloco** para a skill/minuta chamadora inserir na seção correspondente. Não redija relatório nem fundamentação, e não repita conteúdo já resolvido em outra seção da minuta.

## Quando perguntar ao usuário

- Resultado/comando principal não definido por quem chama a skill.
- Circunstância modificadora relevante (AJG, remessa necessária, litisconsórcio com resultado distinto) sem informação suficiente nos autos para redigir com segurança.
- Espécie de ato não coberta por nenhum sub-catálogo de `references/catalogo-especies.md` e sem padrão análogo aplicável.

## Bundled Files

- [Estrutura e invariantes](references/estrutura.md) — heading, numeração alínea/romano, caixa do verbo, fórmula de encerramento (local/data, sem assinatura), referência a Id., regra de preliminares/prejudiciais. **Ler sempre.**
- [Catálogo por espécie de ato](references/catalogo-especies.md) — padrões de DELIBERAÇÃO JUDICIAL e PROVIDÊNCIAS DE IMPULSO por espécie (sentença procedente/improcedente/parcial/extintiva, saneamento, tutela, despacho, embargos, interlocutória geral). Ler o sub-catálogo aplicável ao caso.
- [Catálogo por circunstância modificadora](references/circunstancias.md) — padrões transversais (gratuidade, remessa necessária, honorários, custas, correção/juros, prazo recursal/trânsito, execução invertida, PIX/RPV, prioridade). Ler cada circunstância identificada no caso.

## Restrições

- Não invente valores, nomes, Ids., prazos ou fundamentos legais ausentes dos autos/orientação do usuário — as fórmulas dos catálogos são modelos de linguagem, não fonte de dado.
- Fonte única desta seção: a caixa do verbo e a numeração de alíneas/romanos são regidas só por `references/estrutura.md`. Ao alterar essa regra, edite apenas aqui — não a reproduza em outra skill.
- Não altere conteúdo já redigido de relatório ou fundamentação ao inserir o dispositivo.
