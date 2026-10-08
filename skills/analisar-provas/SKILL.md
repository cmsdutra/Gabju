---
name: analisar-provas
description: Faz análise das provas.
disable-model-invocation: true
---

# /analisar-provas

## Leitura dos anexos

Quando precisar consultar anexos, tente primeiro a leitura direta. Se houver dificuldade concreta que impeça acessar o conteúdo necessário, acione $indexar-pdf somente para os PDFs afetados, informando a dificuldade observada. Tamanho e quantidade de páginas isolados não justificam indexação. Reutilize os textos recuperados e os diagnósticos ao retomar esta skill, preservando seu escopo e checkpoints.

Esta skill é **autocontida**: mapeia por conta própria as hipóteses fáticas controvertidas relevantes à prova, define o standard probatório de cada uma, inventaria os documentos instrutórios apresentados e analisa cada elemento de prova à luz das hipóteses mapeadas — sem depender de relatório produzido por outra skill. Ao final, entrega um relatório estruturado com apontamentos individuais e uma análise preliminar do conjunto probatório.

Não utilize esta skill para:

- mapear a controvérsia jurídica e argumentativa completa da causa (preliminares, prejudiciais, teses jurídicas, pedidos) — isso é objeto da skill `analisar-controversias`, independente desta e não é pré-requisito para a sua execução;
- redigir relatório processual, saneamento, decisão ou sentença;
- analisar ou resumir petição inicial, contestação, réplica, decisões, despachos ou acórdãos como se fossem prova.

## Escopo: documentos instrutórios × peças processuais

- **Documentos instrutórios** (objeto da análise): laudos, perícias, exames, contratos, comprovantes, extratos, notificações, prints, atas de audiência, depoimentos, certidões, registros administrativos, fotografias e demais elementos que veiculem prova de fato.
- **Peças processuais** (petição inicial, contestação, réplica, manifestações, decisões, despachos, acórdãos): usadas **apenas contextualmente**, na Etapa 1, para identificar as hipóteses fáticas controvertidas e o regime de ônus da prova. Nunca são objeto da análise probatória em si, nem citadas como fonte do que se considera provado — ressalvado o uso de peças para verificar confissão, anuência, reconhecimento do pedido ou fato incontroverso, quando estritamente necessário para delimitar a hipótese.
- Diante de dúvida sobre a natureza de um documento (instrutório ou peça principal), classifique pelo conteúdo, não pelo nome do arquivo ou pela posição nos autos.

## Fluxo de Execução

### FASE 00 — Preparação

1. Reúna as peças processuais disponíveis (petição inicial, contestação(ões), réplica(s), decisões anteriores) e os documentos instrutórios apresentados.
2. Separe, entre os documentos apresentados, os documentos instrutórios (objeto da análise) das peças processuais (uso apenas contextual na Etapa 1), conforme a seção "Escopo".
3. Se faltar peça processual essencial para identificar alguma hipótese fática controvertida (ex.: contestação mencionada mas não fornecida), avise o usuário em vez de presumir seu conteúdo.

### Etapa 1 — Mapeamento das Hipóteses Fáticas Controvertidas e Standard Probatório

1. A partir das peças processuais disponíveis, identifique as **hipóteses fáticas controvertidas** — fatos relevantes ao julgamento sobre os quais há divergência entre as partes (afirmado por uma, negado ou contraditado por outra) — distinguindo-as dos fatos incontroversos, que não dependem de prova (art. 374, III, CPC), e das questões exclusivamente jurídicas, que não são objeto desta skill.
2. Formule cada hipótese como enunciado objetivo e verificável (ex.: "existência de nexo causal entre o acidente e a lesão relatada").
3. Para cada hipótese, defina o **standard probatório** aplicável — o grau de convicção exigido para considerá-la demonstrada — considerando:
   - a regra geral de distribuição do ônus da prova (art. 373, incs. I e II, CPC): quem alega o fato constitutivo, impeditivo, modificativo ou extintivo correspondente;
   - eventual inversão do ônus da prova (ex.: art. 6º, inc. VIII, CDC) ou redistribuição dinâmica (art. 373, § 1º, CPC), **apenas se já fundamentada em decisão anterior** ou expressamente informada pelo usuário — não redistribua o ônus por conta própria nesta skill;
   - presunções legais aplicáveis à matéria (ex.: presunção de veracidade de documento público, presunção de boa-fé);
   - dificuldade de produção da prova pelo onerado (fato negativo, fato de difícil reconstituição), quando relevante para calibrar o rigor da análise na Etapa 4.
4. Se já houver decisão de saneamento ou outra decisão anterior fixando as controvérsias de fato e a distribuição do ônus da prova, utilize-a como referência preferencial para esta etapa, sem alterar o que já foi decidido.

**Formato da Etapa 1**:

```markdown
| Hipótese fática controvertida | Parte onerada | Regra de ônus aplicada | Standard probatório |
|---|---|---|---|
| [enunciado objetivo] | [autor/réu] | [art. 373, I/II CPC; inversão; redistribuição] | [grau de convicção exigido e por quê] |
```

Não avance para a Etapa 2 sem esse mapeamento — ele é o filtro que orienta toda a análise subsequente.

### Etapa 2 — Inventário Probatório

1. Relacione todos os documentos instrutórios apresentados, classificando cada um por tipo: documental, pericial (médica, contábil, ambiental, engenharia, grafotécnica etc.), oral (testemunhal, depoimento pessoal) ou outra (inspeção judicial, ata notarial, prova emprestada).
2. Relacione preliminarmente cada documento instrutório à(s) hipótese(s) fática(s) mapeada(s) na Etapa 1 a que se refere. Um documento pode tocar mais de uma hipótese. Documento sem relação direta com nenhuma hipótese deve ser sinalizado como tal — nunca descartado silenciosamente.

**Formato da Etapa 2**:

```markdown
| Documento/Id. | Tipo | Subtipo (se pericial) | Parte que produziu/requereu | Hipótese(s) relacionada(s) |
|---|---|---|---|---|
```

### Etapa 3 — Análise Individual por Elemento de Prova

Para cada documento instrutório listado no inventário, avalie:

- a **relação com a hipótese**: **direta** (o documento prova o próprio fato) ou **indireta/indiciária** (o documento permite inferência lógica em direção ao fato, sem prová-lo diretamente);
- o que o documento efetivamente demonstra, com precisão (data, autoria, conteúdo, alcance);
- o grau de aptidão comprobatória em relação a cada hipótese a que se relaciona (prova plena, indiciária, insuficiente ou irrelevante), à luz do standard probatório definido na Etapa 1;
- ressalvas formais relevantes: autenticidade, legibilidade, tempestividade, cadeia de custódia, ausência de assinatura ou de identificação, ambiguidade de datas ou de titularidade;
- lacunas: o que o documento não prova, mas que a hipótese exigiria.

**Antes de avaliar cada documento, consulte o arquivo de referência correspondente ao seu tipo e aplique os critérios específicos ali descritos**:

| Tipo de prova | Arquivo de referência |
|---|---|
| Documental | `references/prova-documental.md` |
| Pericial (médica, contábil, ambiental, engenharia etc.) | `references/prova-pericial.md` |
| Oral (testemunhal, depoimento pessoal) | `references/prova-oral.md` |
| Outra (inspeção judicial, ata notarial, presunções/indícios, prova digital atípica, prova emprestada) | `references/prova-outras.md` |

**Formato da Etapa 3** (repita por documento instrutório):

```markdown
**Documento [Id./identificação] — [natureza do documento]**

Hipótese(s) relacionada(s): [enunciado sintético da Etapa 1]

Relação com a hipótese: [direta | indireta/indiciária] — [justificativa]

O que demonstra: [síntese objetiva do conteúdo probatório]

Aptidão comprobatória: [plena | indiciária | insuficiente | irrelevante] — [justificativa à luz do standard probatório]

Ressalvas: [formais e específicas do tipo de prova, conforme arquivo de referência; caso contrário, "nenhuma ressalva relevante"]
```

### Etapa 4 — Análise Preliminar do Conjunto Probatório (Conclusão do Relatório)

Para cada hipótese fática mapeada na Etapa 1, releia o conjunto dos documentos instrutórios a ela relacionados e identifique:

- **convergências**: documentos que se reforçam mutuamente quanto ao mesmo fato;
- **contradições**: documentos que se conflitam, indicando qual tem maior força probatória e por quê (ex.: documento público sobre privado, perícia sobre alegação genérica, prova contemporânea ao fato sobre prova posterior);
- **lacunas do conjunto**: fato relevante para a hipótese que nenhum documento instrutório aborda, mesmo que isoladamente cada peça pareça consistente;
- **dependência entre provas**: quando a força de um documento depende da confirmação por outro ainda não produzido ou frágil;
- **avaliação preliminar quanto ao standard probatório**: se, à luz do conjunto, a hipótese está comprovada, não comprovada, ou parcialmente comprovada/dependente de prova adicional, sempre como leitura preliminar do acervo — não como julgamento antecipado do mérito.

**Formato da Etapa 4**:

```markdown
### Hipótese [n] — [enunciado sintético]

**Leitura de conjunto**: [convergências, contradições e lacunas identificadas]

**Avaliação preliminar quanto ao standard probatório**: [comprovada | não comprovada | parcialmente comprovada / dependente de prova adicional] — [justificativa]

[repita para cada hipótese]

### Leitura do Acervo Probatório como um Todo

[Achados transversais que não se restringem a uma única hipótese: documentos que sustentam ou fragilizam mais de uma hipótese simultaneamente, inconsistências gerais de instrução, padrões de insuficiência.]
```

## Formato do Relatório (entrega)

Consolide as Etapas 1 a 4 no seguinte formato:

```markdown
# Análise de Provas — Proc. [número]

## 1. Hipóteses Fáticas Controvertidas e Standard Probatório

[tabela da Etapa 1]

## 2. Inventário Probatório

[tabela da Etapa 2]

## 3. Análise Individual por Elemento de Prova

### Hipótese [n] — [descrição sintética]

[apontamentos individuais de cada documento instrutório relacionado, no formato da Etapa 3]

[repita a estrutura acima para cada hipótese]

## 4. Análise Preliminar do Conjunto Probatório

[estrutura da Etapa 4, por hipótese, seguida da leitura do acervo como um todo]

## 5. Quadro-Resumo

| Hipótese | Standard exigido | Avaliação preliminar | Elemento(s) de maior peso | Lacuna principal (se houver) |
|---|---|---|---|---|

## 6. Documentos Não Correlacionados a Hipóteses

[Liste, se houver, documentos instrutórios sem relação direta com as hipóteses mapeadas, sem descartá-los como irrelevantes sem justificativa.]
```

Entregue o relatório em Markdown no chat. Se o ambiente permitir criar arquivo para download, use `<13-primeiros-dígitos-do-processo-sem-pontuação> - Análise de Provas.md`; na falta do número, use `Análise de Provas.md`.

## Princípios de Execução

- **Autocontenção**: execute o mapeamento da Etapa 1 mesmo que o usuário não forneça relatório prévio de controvérsias. Se o usuário fornecer diretamente hipóteses fáticas já delimitadas (por mensagem ou por documento de apoio), use-as como ponto de partida, mas confirme e complemente com a leitura própria das peças antes de prosseguir à Etapa 2.
- **Eficiência**: execute a análise em fluxo único, sem checkpoints intermediários — não é minuta judicial, e a interrupção para validação de plano só é necessária se o volume de documentos ou hipóteses tornar recomendável confirmar o escopo antes de avançar. Não releia documentos já processados sem motivo concreto.
- **Objetividade**: baseie cada apontamento no conteúdo verificável do documento, não em inferência ou paráfrase da narrativa das partes. Evite frases-tópico metadiscursivas ("esse ponto é decisivo", "vale destacar que"); integre a relevância diretamente ao apontamento substantivo. Diferencie sempre alegação (peça processual) de prova (documento instrutório).
- **Unidade Factual**: ao colacionar as hipóteses fáticas, evite fragmentações excessivas, observando, no que couber, a unidade factual das causas de pedir remota (fática) e de eventual defesa indireta (fatos impeditivos, modificativos ou extintivos).
- **Transparência**: cite o Id. ou identificação de cada documento analisado. Quando a análise depender de informação ausente, ambígua ou de baixa qualidade (ilegibilidade, corte de imagem, ausência de metadados), declare a limitação expressamente em vez de presumir o conteúdo. Não atribua a um documento força probatória que ele não comporta.

## Notas de Comportamento

- Se um mesmo documento instrutório for relevante a mais de uma hipótese, repita sua análise individual em cada hipótese pertinente, ajustando o foco ao fato controvertido específico — não apenas faça referência cruzada.
- Se houver indício de prova ilícita, extemporânea ou produzida sem contraditório, sinalize a ressalva formal no apontamento individual, sem emitir juízo de admissibilidade — essa decisão cabe a fases posteriores (saneamento ou sentença).
- Não avalie a distribuição do ônus da prova além do que já estiver fixado em decisão anterior, nem proponha julgamento antecipado; isso é objeto de `minutar-saneamento` ou `minutar-sentenca`. Esta skill limita-se ao mapeamento de hipóteses, ao standard probatório correspondente e à análise do conteúdo e da correlação da prova em si.
- Se o volume de documentos instrutórios for muito grande, priorize profundidade nos documentos centrais de cada hipótese e trate documentos manifestamente periféricos de forma mais sintética, sem omiti-los do inventário.

## Arquivos de Referência

- `references/prova-documental.md` — critérios de análise de prova documental.
- `references/prova-pericial.md` — critérios gerais de prova pericial e critérios específicos por subtipo (médica, contábil, ambiental/engenharia).
- `references/prova-oral.md` — critérios de análise de prova testemunhal e depoimento pessoal.
- `references/prova-outras.md` — critérios de análise de inspeção judicial, ata notarial, presunções/indícios e prova digital atípica.
