---
name: analisar-controversias
description: Analisa argumentos das partes e destaca controvérsias a resolver na tarefa.
disable-model-invocation: true
---

# /analisar-controversias

## Leitura dos anexos

Quando precisar consultar anexos, tente primeiro a leitura direta. Se houver dificuldade concreta que impeça acessar o conteúdo necessário, acione $indexar-pdf somente para os PDFs afetados, informando a dificuldade observada. Tamanho e quantidade de páginas isolados não justificam indexação. Reutilize os textos recuperados e os diagnósticos ao retomar esta skill, preservando seu escopo e checkpoints.

Esta skill analisa minuciosamente as **peças processuais** do caso (petição inicial, contestação(ões), réplica(s) e decisões anteriores), classificando sistematicamente os pontos fáticos e jurídicos controvertidos para subsidiar a deliberação judicial. Ao final, entrega um relatório estruturado com o mapeamento completo das controvérsias remanescentes.

Não utilize esta skill para:

- analisar documentos instrutórios (laudos, perícias, contratos, comprovantes e demais provas) — isso é objeto da skill `analisar-provas`, independente desta e não sucessora obrigatória;
- redigir relatório de minuta, saneamento, decisão ou sentença;
- fixar controvérsias como ato decisório — esta skill produz insumo analítico, não minuta.

## Escopo: peças processuais × documentos instrutórios

- **Peças processuais** (objeto da análise): petição inicial, contestação(ões), reconvenção, réplica(s), manifestações sobre preliminares/provas, decisões anteriores.
- **Documentos instrutórios** (fora do escopo): laudos, perícias, exames, contratos, comprovantes, extratos, atas de audiência, depoimentos e demais elementos de prova. Se apresentados junto às peças, ignore-os nesta análise — eles são objeto de `analisar-provas`, skill autocontida e independente, que faz seu próprio mapeamento de hipóteses fáticas a partir das peças.
- Diante de dúvida sobre a natureza de um documento, classifique pelo conteúdo, não pelo nome do arquivo ou pela posição nos autos.

## TOM E LINGUAGEM

- Técnico, formal, impessoal, preciso no vocabulário jurídico.
- Descrição de fatos/fundamentos: detalhada, completa, objetiva, sem juízo de valor.
- **Cite sempre o Id. do documento** referenciado direta ou indiretamente (ex.: "fato X (Id. ...)", "réu contesta (Id. ...)").
- Evite estrangeirismos (latim, alemão, inglês etc.), salvo termo jurídico consagrado sem equivalente em português.

## Fluxo de Execução

### FASE 00 — Preparação

1. Localize, entre os arquivos anexados à conversa, as peças processuais: petição inicial, contestação(ões), réplica(s) e decisões anteriores.
2. Separe, entre os documentos apresentados, as peças processuais (objeto da análise) dos documentos instrutórios (fora do escopo), conforme a seção "Escopo".
3. Se faltar peça essencial para a análise (ex.: contestação mencionada mas não fornecida), avise o usuário em vez de presumir seu conteúdo.
4. Verifique se há decisão(ões) anterior(es) que já tenham resolvido total ou parcialmente questões processuais, prejudiciais ou controvérsias — elas serão usadas para filtragem na Etapa 5.

### Etapa 1 — Petição Inicial (Id. ...)

1.1. **Partes**: autor(es), réu(s).
1.2. **Fatos**: listar detalhadamente (bullet points) todos os fatos narrados.
1.3. **Fundamentos jurídicos**: listar detalhadamente (bullet points) todas as teses (legais, jurisprudenciais etc.) invocadas.
1.4. **Pedidos**: listar (numerado) todos os pedidos (principais, subsidiários etc.).
1.5. **Especificação de provas**: informar se houve especificação concreta (ex.: "perícia para comprovar a incapacidade alegada"), não apenas protesto genérico.

### Etapa 2 — Contestação(ões)

Repita a estrutura abaixo para cada contestação apresentada.

**2.N. Contestação — [nome do réu] (Id. ...)**

- **Fatos (versão do réu)**: listar (bullet points), destacando concordâncias/divergências com a versão da inicial.
- **Preliminares processuais**: listar (bullet points), resumindo o argumento de cada uma.
- **Prejudiciais de mérito**: listar (bullet points) — prescrição, decadência etc. — resumindo o argumento.
- **Fundamentos de mérito (defesa direta)**: listar (bullet points) os argumentos contra os pedidos do autor.
- **Fatos impeditivos/modificativos/extintivos (defesa indireta)**: listar (bullet points), se houver, fatos novos trazidos na contestação que, em tese, impedem, modificam ou extinguem a pretensão do autor (art. 350 do CPC).
- **Impugnação documental**: houve? quais documentos? qual motivo? (indicar o Id. dos documentos impugnados, se houver essa informação).
- **Reconvenção**: houve? em caso positivo, resumir fatos, fundamentos e pedidos seguindo a estrutura da Etapa 1 (Id. ...).
- **Pedidos do réu**: listar (numerado).
- **Especificação de provas**: houve especificação concreta de provas? quais?

### Etapa 3 — Réplica(s)

Se não houver réplica, registre a ausência e siga para a Etapa 4. Caso contrário, repita a estrutura abaixo para cada réplica.

**3.N. Réplica — [nome do autor] (Id. ...)**

- **Resposta às preliminares**: listar (bullet points).
- **Resposta às prejudiciais**: listar (bullet points).
- **Resposta ao mérito/fatos da defesa**: listar (bullet points).
- **Resposta à impugnação documental**: se houver.
- **Contestação à reconvenção**: se houver, seguir a estrutura da Etapa 2.
- **Reiteração/aditamento de pedidos ou provas**: houve? quais?

### Etapa 4 — Confrontação Direta

4.1. **Pontos fáticos** — organize em formato comparativo:
   - **Incontroversos**: afirmado por uma parte e admitido ou não impugnado pela outra.
   - **Controversos**: afirmado por uma parte e negado/contraditado pela outra; descreva as duas versões.
   - **Novos fatos relevantes**: introduzidos na defesa ou na réplica.

4.2. **Pontos jurídicos**: liste as teses jurídicas conflitantes, em formato comparativo.

### Etapa 5 — Filtragem por Decisões Anteriores

Se não houver decisão anterior, registre a ausência e siga para a Etapa 6. Caso contrário, liste (bullet points) o que **já foi decidido**, para que não seja reapresentado como pendente na Etapa 6:

- questões processuais (preliminares etc.) — resumir a decisão;
- prejudiciais de mérito (prescrição etc.) — resumir a decisão;
- impacto de decisões sobre tutela provisória;
- decisões sobre ônus da prova ou admissão de provas;
- pontos controvertidos já fixados anteriormente.

### Etapa 6 — Resumo Estruturado das Controvérsias Remanescentes

Com base nas Etapas 4 e 5, liste apenas os pontos **pendentes** de análise/decisão:

6.1. **Questões processuais pendentes**: preliminares/outras não decididas (ex.: "análise de ilegitimidade passiva (réu X, Id. ...)").
6.2. **Questões incidentais pendentes**: (ex.: "incidente de falsidade documental (Id. ...)"; "necessidade de perícia (Ids. ..., ...)").
6.3. **Prejudiciais de mérito pendentes**: não decididas (ex.: "análise de prescrição (réu, Id. ...)").
6.4. **Controvérsias de mérito**: pontos fáticos e jurídicos centrais em disputa, essenciais ao julgamento, com a posição de cada parte e os respectivos Ids.
   - Ex. fático: "existência/extensão do dano material (autor, Id. ...) vs. contestação do nexo causal (réu, Id. ...)".
   - Ex. jurídico: "responsabilidade objetiva (autor, Id. ...) vs. subjetiva/prova de culpa (réu, Id. ...)".
   - Ex. fático/jurídico: "validade da cláusula 5 (Id. ...) — abusividade (réu, Id. ...) vs. defesa contratual (autor, Id. ...)".
6.5. **Correlação probatória**: para cada controvérsia fática, indicar os documentos e demais provas (com o respectivo Id.) a ela relacionados, quando essa informação constar das peças analisadas.

### Etapa 7 — Pesquisa complementar (somente sob pedido expresso)

Não execute esta etapa por iniciativa própria. Só a realize se o usuário pedir expressamente pesquisa de normas, precedentes ou doutrina aplicáveis ao caso.

Quando solicitado, ative a ferramenta de pesquisa na web e levante:

- todas as normas (constitucionais, legais, infralegais e tratados internacionais) aplicáveis ao caso, confirmando que cada norma **ainda está em vigor**;
- todos os precedentes vinculantes (RE com Repercussão Geral, REsp Repetitivo, IAC, IRDR, ADI, ADC, ADO, ADPF, Súmulas) aplicáveis ao caso, ainda que de forma indireta — explicando a relação com o caso;
- outros acórdãos de tribunais hierarquicamente superiores ao juízo que analisa o caso (ex.: causa perante uma vara federal — TRF da região, TNU, STJ, STF);
- trechos de artigos doutrinários sobre a matéria, preferindo artigos recentes de repositórios acadêmicos de alta relevância.

Apresente sempre a referência completa do precedente ou artigo citado e o link para verificação. Não invente informações nem faça inferências sem certeza de que a fonte apontada se relaciona com o caso analisado.

## Formato do Relatório (entrega)

Consolide as Etapas 1 a 6 (e a Etapa 7, se executada) no seguinte formato:

```markdown
# Análise de Controvérsias — Proc. [número]

## 1. Petição Inicial (Id. ...)

**Partes**: [autor(es) x réu(s)]

**Fatos**:
- ...

**Fundamentos jurídicos**:
- ...

**Pedidos**:
1. ...

**Especificação de provas**: [...]

## 2. Contestação(ões)

### 2.N. Contestação — [nome do réu] (Id. ...)
[estrutura da Etapa 2]

## 3. Réplica(s)

### 3.N. Réplica — [nome do autor] (Id. ...)
[estrutura da Etapa 3, ou "Não houve réplica."]

## 4. Confrontação Direta

**Pontos fáticos incontroversos**:
- ...

**Pontos fáticos controversos**:
- ...

**Novos fatos relevantes**:
- ...

**Pontos jurídicos conflitantes**:
- ...

## 5. Filtragem por Decisões Anteriores (Ids. ...)
[itens decididos, ou "Não há decisão anterior sobre questões pendentes."]

## 6. Resumo Estruturado das Controvérsias Remanescentes

**Questões processuais pendentes**:
- ...

**Questões incidentais pendentes**:
- ...

**Prejudiciais de mérito pendentes**:
- ...

**Controvérsias de mérito**:
1. ...

**Correlação probatória**:
| Controvérsia | Documento(s)/Id(s). relacionado(s) |
|---|---|

## 7. Pesquisa Complementar (se solicitada)

**Normas aplicáveis**: [...]

**Precedentes vinculantes**: [...]

**Acórdãos de tribunais superiores**: [...]

**Doutrina**: [...]
```

## Entrega

Entregue o relatório em Markdown no chat. Se o ambiente permitir criar arquivo para download, use `<13-primeiros-dígitos-do-processo-sem-pontuação> - Análise de Controvérsias.md`; na falta do número, use `Análise de Controvérsias.md`.

## Guardrails

- Limite-se ao conteúdo das peças fornecidas.
- Não crie, extrapole ou invente informações.
- Não faça pesquisa de jurisprudência, doutrina ou legislação, salvo pedido expresso do usuário (Etapa 7).
- Seja analítico, sem fazer pré-julgamentos ou emitir juízo de valor sobre o mérito da controvérsia.
- Não avalie provas nem se pronuncie sobre a suficiência do acervo probatório — isso é objeto de `analisar-provas`.
- Não distribua ônus da prova nem delibere sobre pedidos de prova — isso é objeto de `minutar-saneamento`.

## Notas de Comportamento

- Se houver mais de uma contestação ou réplica, mantenha a numeração sequencial (2.1, 2.2, ... / 3.1, 3.2, ...) na ordem em que as peças foram apresentadas.
- Se uma controvérsia de mérito envolver simultaneamente aspecto fático e jurídico, registre-a uma única vez na Etapa 6.4, indicando ambas as dimensões, em vez de duplicá-la entre fato e direito.
- Se o volume de peças for muito grande, priorize profundidade nos fatos e fundamentos centrais de cada controvérsia, tratando alegações manifestamente periféricas ou repetitivas de forma mais sintética, sem omiti-las do mapeamento.
- Não abra tópicos ou subtópicos (como reconvenção ou impugnação documental) quando a peça analisada não os contiver.
