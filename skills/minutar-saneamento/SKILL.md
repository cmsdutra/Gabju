---
name: minutar-saneamento
description: "Redige decisão de saneamento e organização do processo: resolve questões pendentes, fixa controvérsias, distribui ônus da prova e delibera sobre provas. Use mediante invocação expressa ou pedido de saneamento."
---

# /minutar-saneamento

## Personalização

Leia [personalização do gabinete](../../references/personalizacao.md) ao aplicar convenções ou preencher dados institucionais e fechamento: use a personalização do ChatGPT disponível no contexto; dados ausentes recebem placeholders padrão.

## Leitura dos anexos

Quando precisar consultar anexos, tente primeiro a leitura direta. Se houver dificuldade concreta que impeça acessar o conteúdo necessário, acione $indexar-pdf somente para os PDFs afetados, informando a dificuldade observada. Tamanho e quantidade de páginas isolados não justificam indexação. Reutilize os textos recuperados e os diagnósticos ao retomar esta skill, preservando seu escopo e checkpoints.

Esta skill conduz a elaboração de minuta de decisão de saneamento e organização do processo, de acordo com o art. 357 do Código de Processo Civil, templates e regras de estilo especificadas.

Não utilize esta skill para:

- decisão interlocutória geral sem finalidade de saneamento;
- tutela provisória, pedido liminar ou medida cautelar;
- embargos de declaração;
- relatório isolado de decisão ou sentença;
- fundamentação de sentença.

Nesses casos, utilize a skill própria, quando houver.

## Fluxo de Execução

### FASE 00 - PREPARAÇÃO

Ao iniciar, certifique-se de que os documentos apresentados pelo usuário estão legíveis e íntegros.

Identifique:

- se a fase postulatória está encerrada;
- se houve réplica ou decurso de prazo;
- se há questões processuais pendentes;
- quais pedidos de prova foram formulados pelas partes;
- se há necessidade de perícia, prova oral, prova documental suplementar, expedição de ofícios ou outra diligência;
- em caso de perícia, se a parte pleiteante é beneficiária da gratuidade da justiça (define o fluxo de custeio e nomeação: NUCOD, sem nomeação direta de perito, versus nomeação direta com adiantamento pela parte);
- quais controvérsias de fato dependem de prova;
- quais controvérsias de direito são relevantes para o julgamento de mérito;
- se há orientação específica do usuário na conversa ou em arquivo anexo.

Se o processo estiver maduro para julgamento antecipado, alerte o usuário e indique que a hipótese pode exigir sentença, salvo se houver orientação expressa para sanear.

### Verificação inicial — orientações do usuário

Verifique se a conversa ou algum anexo contém orientação expressa do usuário sobre o encaminhamento de cada questão processual pendente, controvérsia, ônus da prova e atividade probatória.

- **Orientação suficiente para todos os blocos**: trate-a como a deliberação do usuário sobre a Etapa 1. Pule a Etapa 1 — não a apresente nem peça confirmação dela — e vá direto à Etapa 2, incorporando a orientação ao plano da minuta. Ao final da Etapa 2, não aguarde validação do usuário: avance automaticamente para a Etapa 3.
- **Orientação ausente, ou insuficiente para algum bloco**: siga o fluxo integral, com checkpoint ao final da Etapa 1 e da Etapa 2. Se a orientação cobrir apenas parte dos blocos, execute a Etapa 1 normalmente para os não cobertos e trate os demais como já deliberados.

### Etapa 1 — Análise

**Dispensada quando houver orientação prévia suficiente** (ver "Verificação inicial" acima).

**Objetivo**: compreender o estado processual, mapear questões pendentes e apresentar encaminhamentos para confirmação do usuário antes de qualquer redação.

Execute os seguintes passos:

1. Leia as peças principais, especialmente petição inicial, contestação, réplica, manifestações sobre provas, decisões anteriores, atas e documentos que impactem a instrução.
2. Identifique e sintetize as questões processuais pendentes, como preliminares, regularização de representação, impugnações, competência, ilegitimidade, prescrição, decadência, conexão, chamamento, intervenção de terceiros ou incidentes ainda não decididos.
3. Separe as controvérsias de fato que dependem de prova das controvérsias de direito relevantes para a sentença.
4. Verifique os pedidos de prova e avalie pertinência, necessidade, utilidade e adequação à controvérsia.
5. Defina a distribuição do ônus da prova, em regra conforme art. 373, incs. I e II, do CPC, salvo hipótese de redistribuição.
6. Identifique providências de impulso necessárias após o saneamento.
7. Apresente a análise no formato abaixo e aguarde o checkpoint do usuário.

**Encaminhamentos por bloco**:

- Sugira até três direcionamentos possíveis quando houver dúvida real de encaminhamento.
- Quando a solução for técnica e única, apresente diretamente a proposta e a justificativa.
- Ao tratar de provas, indique expressamente deferimento, indeferimento ou necessidade de especificação complementar.
- Ao propor redistribuição do ônus da prova, explicite fundamento, fato específico abrangido e parte onerada.
- Não redija minuta na Etapa 1.

**Formato da Etapa 1**:

```markdown
### ETAPA 1 — ANÁLISE

---

**Estado Processual**

[Síntese da fase processual e dos atos relevantes, com referência aos Ids. indispensáveis.]

---

**Questões Processuais Pendentes**

[Questão N — síntese, fundamento aplicável e encaminhamento proposto.]

---

**Controvérsias de Fato**

1. [Controvérsia fática que depende de prova.]
2. [...]

---

**Controvérsias de Direito**

1. [Questão jurídica relevante para a sentença.]
2. [...]

---

**Atividade Probatória**

| Prova requerida | Parte requerente | Encaminhamento | Justificativa |
|---|---|---|---|
| ... | ... | deferir/indeferir/postergar | ... |

---

**Ônus da Prova**

[Distribuição proposta e eventual necessidade de redistribuição.]

---

**RESUMO**

| Bloco | Encaminhamento proposto | Fundamento principal |
|---|---|---|
| Questões processuais | ... | ... |
| Controvérsias de fato | ... | ... |
| Controvérsias de direito | ... | ... |
| Provas | ... | ... |
| Ônus da prova | ... | ... |

---
⚠️ Aguardo confirmação dos encaminhamentos ou instruções antes de prosseguir para o Plano da Minuta.
```

**STOP**: Após apresentar a Etapa 1, aguarde o checkpoint do usuário. **Não avance para a Etapa 2 sem confirmação ou instrução explícita**.

#### Registro no chat (Auditabilidade)

Após a validação/deliberação do usuário sobre os encaminhamentos da Etapa 1 (ou quando houver orientação prévia já adotada), apresente no chat um registro conciso da análise e deliberação contendo:
- Questões processuais e controvérsias (fato e direito) mapeadas com Ids. pertinentes;
- Encaminhamentos propostos e deliberação adotada sobre preliminares, provas e ônus probatório;
- Quadro-resumo das deliberações;
- Estado da minuta (etapa realizada e fases subsequentes).

Mantenha esse registro separado da minuta e avance para a Etapa 2.

---

### Etapa 2 — Plano da Minuta

**Objetivo**: estruturar a decisão de saneamento em tópicos sintéticos, antes da redação final.

> [!important] Execute após o checkpoint da Etapa 1 — ou, no fluxo abreviado por orientação prévia suficiente, diretamente após a leitura das peças.

1. Para cada bloco confirmado pelo usuário ou definido por orientação prévia suficiente, desenvolva um plano com frases curtas e diretas.
2. Use, por padrão, a seguinte estrutura:

```markdown
→ {Relatório breve da fase processual}
→ {Considerações iniciais sobre o art. 357 do CPC}
→ {Resolução das questões processuais pendentes}
→ {Declaração de saneamento do processo}
→ {Fixação das controvérsias de fato}
→ {Fixação das controvérsias de direito}
→ {Distribuição do ônus da prova}
→ {Deliberação sobre atividade probatória}
→ {Deliberação judicial}
→ {Providências de impulso processual}
```

3. Adapte a estrutura quando algum bloco for desnecessário, mantendo a lógica do art. 357 do CPC.
4. O plano deve ser enxuto, com frases de até duas linhas por tópico.
5. Não antecipe a redação em prosa; apenas organize o que será escrito.

**Formato da Etapa 2**:

```markdown
### ETAPA 2 — PLANO DA MINUTA

1. **Relatório**
   - [Síntese do estado processual que será narrada.]

2. **Questões Processuais Pendentes**
   - [Questão e encaminhamento.]

3. **Controvérsias de Fato**
   - [Controvérsia fática a fixar.]

4. **Controvérsias de Direito**
   - [Controvérsia jurídica a fixar.]

5. **Ônus da Prova**
   - [Regra de distribuição ou redistribuição.]

6. **Atividade Probatória**
   - [Provas deferidas, indeferidas ou providências.]

7. **Deliberação e Providências**
   - [Comandos que serão levados à deliberação judicial e ao impulso.]
```

**Autoreflexão**: Antes de apresentar o Plano, certifique-se de que ele contempla todos os incisos relevantes do art. 357 do CPC e respeita as deliberações do usuário na Etapa 1. Se estiver, apresente o plano; senão, faça os ajustes necessários e repita a autoreflexão, no máximo em 2 rodadas.

---

#### CHECKPOINT OBRIGATÓRIO — VALIDAÇÃO DO PLANO DA MINUTA

**Dispensado quando houver orientação prévia suficiente** (ver "Verificação inicial" acima) — nesse caso, avance direto para a Etapa 3, sem aguardar confirmação.

**STOP**: Após apresentar o Plano da Minuta no formato da Etapa 2, **aguarde validação explícita do usuário antes de qualquer avanço para a Etapa 3**.

O usuário pode:

- aceitar o plano integralmente;
- solicitar edições no plano;
- rejeitar o plano e solicitar reconstrução total.

IMPORTANTE: **Você não avança para a Etapa 3 (Redação) sem autorização expressa do usuário**, salvo no fluxo abreviado por orientação prévia suficiente. Fora dessa exceção, este é um checkpoint obrigatório.

---

### Etapa 3 — Redação

**Objetivo**: redigir a minuta completa da decisão de saneamento, observando o template aplicável, as regras de estilo e o plano aprovado.

- Template: `assets/template-saneamento.md`
- Regras de estilo: `references/regras-de-estilo.md`

Orientações:

1. Antes de iniciar a redação, carregue e leia atentamente as regras de estilo definidas em `references/regras-de-estilo.md` e o template em `assets/template-saneamento.md`.
2. Consulte os exemplos em `assets/exemplos/`, se existentes e pertinentes ao tipo de controvérsia, para calibrar a estrutura da deliberação judicial e das providências de impulso.
3. Siga a estrutura do template, preenchendo cada bloco conforme as instruções nele contidas, observando as regras de estilo e o plano aprovado na Etapa 2, utilizando-o como guia sem citá-lo como fonte.
4. Redija relatório breve apenas na extensão necessária para contextualizar a decisão de saneamento.
5. Resolva as questões processuais pendentes antes de declarar saneado o processo.
6. Fixe controvérsias de fato e de direito de modo objetivo, evitando transformar a seção em fundamentação de mérito.
7. Delimite o ônus da prova por fatos ou grupos de fatos, quando necessário.
8. Delibere sobre provas de forma motivada, indicando pertinência, utilidade e necessidade.
9. Em caso de deferimento de perícia, siga o padrão do template: fundamentação breve na seção de dilação probatória; detalhamento em subitens da deliberação judicial e providências de impulso correspondentes ao fluxo aplicável — (i) parte pleiteante NÃO beneficiária da gratuidade da justiça: nomeação direta do perito, honorários adiantados pela parte, prazo de laudo e quesitos na deliberação judicial, providências de intimação das partes, aceite do perito, proposta de honorários, manifestação e conclusão para arbitramento; (ii) parte pleiteante beneficiária da gratuidade da justiça: sem nomeação direta de perito, fixação dos honorários no teto da Resolução CJF 305/2014, remessa ao NUCOD para designação da perícia e formulação dos quesitos do Juízo já na deliberação, providências de intimação das partes para quesitos/assistentes técnicos, encaminhamento ao NUCOD, abertura de vista após o laudo e conclusão para julgamento. Consulte `assets/exemplos/ex-contrato-bancario-anatocismo-pericia-ajg.md` para calibrar o fluxo (ii).
10. Inclua deliberação judicial e providências de impulso processual quando o usuário pedir minuta completa ou quando o template exigir esses blocos. Nas providências de impulso, formule comandos diretos com o verbo operacional em destaque, quando compatível com o padrão da minuta, e evite repetir deliberação já feita em decisão anterior — se a providência anterior ainda não tiver sido cumprida, referencie-a apenas na seção de providências de impulso. Para as fórmulas fora do fluxo de perícia (AJG geral, honorários, custas etc.), consulte `minutar-dispositivo/references/circunstancias.md`; regras de heading/numeração/caixa do verbo → `minutar-dispositivo/references/estrutura.md`.
11. Ao redigir fatos relevantes ao saneamento, diferencie rigorosamente alegações das partes e prova. Petições, contestações, réplicas, manifestações e razões recursais não devem ser tratadas como prova de fatos controvertidos, salvo para avaliar confissão, anuência, reconhecimento do pedido, fato incontroverso, renúncia, desistência, delimitação da lide, pedidos de prova ou outra declaração processual atribuível à própria parte.
12. Antes de entregar a resposta ao usuário, faça uma reflexão silenciosa, certificando-se de que a redação obedeceu as regras de estilo, o template e o plano. Verifique especificamente se não foram usadas frases-tópico soltas ou metadiscursivas, como "Esse ponto é decisivo" ou fórmulas equivalentes, e se as petições das partes não foram usadas como elementos probatórios indevidos. Caso não tenha obedecido, faça os ajustes necessários.

Produza o texto pronto para incorporação à minuta. Não inclua marcações de template, comentários ou instruções do SKILL.md na saída final.

---

## Notas de Comportamento

- Se o usuário fornecer um esqueleto de pensamento, arquivo-modelo ou estrutura própria, incorpore-o ao plano sem citá-lo como fonte e sem transformá-lo em tópicos numerados na redação.
- Se houver controvérsias repetidas ou sobrepostas, consolide-as em enunciados objetivos.
- Não abra tópicos ou subtópicos autônomos (como gratuidade da justiça) quando não houver pedido ou controvérsia concreta pendente sobre o tema.
- Evite resolver o mérito sob o rótulo de fixação de controvérsias. O saneamento organiza a instrução e delimita o julgamento futuro.
- Não use jurisprudência ou doutrina salvo quando fornecidas pelo usuário, pelo template ou por referência lida por determinação expressa.
- Não invente ou infira legislação específica. Se houver dúvida objetiva sobre norma aplicável, pesquise fonte oficial ou pergunte ao usuário.
