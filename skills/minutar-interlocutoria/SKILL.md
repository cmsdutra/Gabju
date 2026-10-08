---
name: minutar-interlocutoria
description: Redige fundamentação de decisão interlocutória geral (exclui embargos, saneamento e tutela provisória — skills próprias). Usar só com invocação expressa de minutar-interlocutoria ou pedido expresso de minuta/análise/julgamento/redação de decisão interlocutória geral.
---

# /minutar-interlocutoria

## Personalização

Leia [personalização do gabinete](../../references/personalizacao.md) ao aplicar convenções ou preencher dados institucionais e fechamento: use a personalização do ChatGPT disponível no contexto; dados ausentes recebem placeholders padrão.

## Leitura dos anexos

Quando precisar consultar anexos, tente primeiro a leitura direta. Se houver dificuldade concreta que impeça acessar o conteúdo necessário, acione $indexar-pdf somente para os PDFs afetados, informando a dificuldade observada. Tamanho e quantidade de páginas isolados não justificam indexação. Reutilize os textos recuperados e os diagnósticos ao retomar esta skill, preservando seu escopo e checkpoints.

Esta skill conduz a elaboração da fundamentação de decisões interlocutórias gerais, de acordo com templates e regras de estilo especificadas.

Não utilize esta skill para:

- embargos de declaração;
- decisão de saneamento;
- tutela provisória, tutela de urgência, tutela de evidência, pedido liminar ou medida cautelar;
- relatório de decisão ou sentença;
- fundamentação de sentença.

Nesses casos, utilize a skill própria, quando houver.

## Fluxo de Execução

### FASE 00 - PREPARAÇÃO

Ao iniciar, certifique-se de que os documentos apresentados pelo usuário estão legíveis e íntegros.

Identifique:

- quais questões estão pendentes de decisão;
- quem formulou cada requerimento;
- quais Ids. são indispensáveis para compreender a controvérsia;
- se há decisão anterior sobre o mesmo tema;
- se a questão é realmente interlocutória geral ou se deve ser encaminhada a outra skill.

Se a questão envolver matéria urgente ou pedido liminar, interrompa o uso desta skill e utilize `minutar-tutela`, salvo orientação expressa em sentido diverso.

### Verificação inicial — orientações do usuário

Verifique se a conversa ou algum anexo contém orientação expressa do usuário sobre o encaminhamento de cada questão incidental pendente.

- **Orientação suficiente para todas as questões**: trate-a como a deliberação do usuário sobre a Etapa 1. Pule a Etapa 1 — não a apresente nem peça confirmação dela — e vá direto à Etapa 2, incorporando a orientação ao plano de argumentação. Ao final da Etapa 2, não aguarde validação do usuário: avance automaticamente para a Etapa 3.
- **Orientação ausente, ou insuficiente para alguma questão**: siga o fluxo integral, com checkpoint ao final da Etapa 1 e da Etapa 2. Se a orientação cobrir apenas parte das questões, execute a Etapa 1 normalmente para as não cobertas e trate as demais como já deliberadas.

### Etapa 1 — Análise

**Dispensada quando houver orientação prévia suficiente** (ver "Verificação inicial" acima).

**Objetivo**: compreender as questões incidentais pendentes, mapear os fundamentos jurídicos aplicáveis e apresentar encaminhamentos para escolha ou confirmação do usuário antes de qualquer redação.

Execute os seguintes passos:

1. Leia os documentos do processo fornecidos pelo usuário, priorizando petições relacionadas ao incidente, manifestações da parte contrária, decisões anteriores, certidões, atos ordinatórios, atas e documentos diretamente relevantes.
2. Identifique cada questão pendente de decisão e agrupe questões que compartilhem a mesma premissa fático-jurídica.
3. Separe questões processuais, probatórias, executivas, de cumprimento, organização procedimental, intimação, regularização, intervenção de terceiros, perícia, penhora, desbloqueio, expedição de ofícios, produção de prova e outras deliberações incidentais.
4. Mapeie os fundamentos jurídicos aplicáveis, sem aprofundar a redação final.
5. Apresente a análise de cada questão no formato abaixo.
6. Ao final, apresente a tabela-resumo e aguarde o checkpoint do usuário.

**Encaminhamentos por questão**:

- Sugira até três direcionamentos possíveis, cada um com título sintético, encaminhamento e justificativa em até três linhas. Os direcionamentos devem ser genuinamente distintos, não variações de tom.
- Indique, quando houver, qual direcionamento parece mais adequado ao caso e por quê.
- Quando a decisão exigir providência prática, identifique prazo, destinatário, forma de cumprimento, necessidade de intimação, expedição de ofício, regularização, nova manifestação ou conclusão posterior.
- Não redija dispositivo na Etapa 1.

**Formato da Etapa 1**:

```markdown
### ETAPA 1 — ANÁLISE

---

**[Questão N — Título sintético]**

[Síntese fática da questão, com referência aos Ids. relevantes.]
[Normas e institutos jurídicos aplicáveis — apenas mapeamento, sem aprofundamento.]

Direcionamentos possíveis:
  Opção A — [Título]: [encaminhamento + justificativa em até três linhas.]
  Opção B — [Título]: [encaminhamento + justificativa em até três linhas.]
  Opção C — [Título, se aplicável]: [encaminhamento + justificativa em até três linhas.]
[Indicação do direcionamento sugerido, se houver, com justificativa.]
--

[Pontos de atenção ou riscos relevantes, se houver.]

---

**RESUMO**

| Questão | Encaminhamento proposto | Fundamento principal |
|---|---|---|
| ... | ... | ... |

---
⚠️ Aguardo confirmação dos encaminhamentos ou instruções antes de prosseguir para o Plano de Argumentação.
```

**STOP**: Após apresentar a Etapa 1, aguarde o checkpoint do usuário. **Não avance para a Etapa 2 sem confirmação ou instrução explícita**.

#### Registro no chat (Auditabilidade)

Após a validação/deliberação do usuário sobre os encaminhamentos da Etapa 1 (ou quando houver orientação prévia já adotada), apresente no chat um registro conciso da análise e deliberação contendo:
- Questões incidentais mapeadas e Ids. pertinentes;
- Encaminhamentos propostos e deliberação adotada;
- Quadro-resumo das deliberações (questão, requerente, solução adotada, fundamento normativo);
- Estado da minuta (etapa realizada e fases subsequentes).

Mantenha esse registro separado da minuta e avance para a Etapa 2.

---

### Etapa 2 — Plano de Argumentação

**Objetivo**: estruturar, em tópicos sintéticos, o raciocínio que orientará a redação. Não é rascunho; é um esqueleto argumentativo.

> [!important] Execute após o checkpoint da Etapa 1 — ou, no fluxo abreviado por orientação prévia suficiente, diretamente após a leitura das peças.

1. Para cada questão com encaminhamento confirmado pelo usuário ou definido por orientação prévia suficiente, desenvolva um plano em tópicos com frases curtas e diretas.
2. Use, por padrão, a seguinte estrutura lógico-argumentativa:

```markdown
→ {Apresentação da questão pendente}
→ {Síntese do requerimento ou situação processual}
→ {Apresentação da norma, ônus processual, regra procedimental ou instituto aplicável}
→ {Aplicação ao caso concreto, com referência aos Ids. relevantes}
→ {Refutação de argumentos contrários, quando houver}
→ {Definição da providência prática necessária}
→ {Conclusão parcial}
```

3. Se houver mais de uma questão que admita análise conjunta, crie um único bloco argumentativo.
4. Se houver questões autônomas, organize cada uma em tópico próprio.
5. Cada tópico deve representar um bloco argumentativo na redação final e pode ser dividido em subtópicos, a depender da complexidade do argumento.
6. O plano deve ser enxuto, com frases de até duas linhas por tópico.

**Formato da Etapa 2**:

```markdown
### ETAPA 2 — PLANO DE ARGUMENTAÇÃO

**[Questão N — Título sintético]**

1. [Frase direta descrevendo o que o parágrafo fará.]
2. [Frase direta apresentando norma, instituto ou regra processual aplicável.]
    2.1. [Subtópico, se necessário.]
    2.2. [Subtópico, se necessário.]
3. [Frase direta aplicando o fundamento ao caso concreto.]
4. [Frase direta para refutar argumento contrário, se houver.]
5. [Frase direta sobre a providência prática decorrente.]
6. [Conclusão parcial.]

**[Questão N+1 — ...]**
...

**CONCLUSÃO GERAL**
- [Síntese do que será deliberado.]
```

**Autoreflexão**: Antes de apresentar o Plano, certifique-se de que está condizente com as deliberações do usuário na Etapa 1, com a natureza interlocutória da questão e com a estrutura lógico-argumentativa aplicável. Se estiver, apresente o plano; senão, faça os ajustes necessários e repita a autoreflexão, no máximo em 2 rodadas.

---

#### CHECKPOINT OBRIGATÓRIO — VALIDAÇÃO DO PLANO DE ARGUMENTAÇÃO

**Dispensado quando houver orientação prévia suficiente** (ver "Verificação inicial" acima) — nesse caso, avance direto para a Etapa 3, sem aguardar confirmação.

**STOP**: Após apresentar o Plano de Argumentação no formato da Etapa 2, **aguarde validação explícita do usuário antes de qualquer avanço para a Etapa 3**.

O usuário pode:

- aceitar o plano integralmente;
- solicitar edições no plano;
- rejeitar o plano e solicitar reconstrução total.

IMPORTANTE: **Você não avança para a Etapa 3 (Redação) sem autorização expressa do usuário**, salvo no fluxo abreviado por orientação prévia suficiente. Fora dessa exceção, este é um checkpoint obrigatório.

---

### Etapa 3 — Redação

**Objetivo**: redigir a fundamentação completa, observando o template aplicável, as regras de estilo e o plano de argumentação aprovado.

- Template: `assets/template-decisao-interlocutoria.md`
- Regras de estilo: `references/regras-de-estilo.md`

Orientações:

1. Antes de iniciar a redação, carregue e leia atentamente as regras de estilo definidas em `references/regras-de-estilo.md` e o template em `assets/template-decisao-interlocutoria.md`.
2. Siga a estrutura do template, preenchendo cada bloco conforme as instruções nele contidas, observando as regras de estilo e o plano de argumentação aprovado na Etapa 2, utilizando-o como guia para cada parágrafo, sem citá-lo como fonte.
3. Inicie a fundamentação com o resumo das questões pendentes, conforme o template; se houver uma única questão pendente e encaminhamento evidente, dispense o resumo inicial e comece diretamente pela premissa decisória.
4. Agrupe questões quando compartilharem a mesma premissa fático-jurídica e separe-as em tópicos quando forem autônomas.
5. Inclua, na fundamentação, a razão concreta da providência prática, sem fórmulas justificativas abstratas como "a solução visa...", "essa solução harmoniza..." ou equivalentes. Não redija comandos de dispositivo, salvo pedido expresso do usuário. Corte parágrafo conclusivo que só antecipa o dispositivo quando a premissa decisória já estiver demonstrada. Quando o usuário pedir dispositivo, acione `minutar-dispositivo`: `minutar-dispositivo/references/estrutura.md` para heading/numeração/caixa do verbo/regra de preliminares (inclusive a exceção para decisão que julga conjunto de teses, ex. impugnação ao cumprimento de sentença), `minutar-dispositivo/references/catalogo-especies.md` § Decisão Interlocutória Geral e `minutar-dispositivo/references/circunstancias.md` para honorários, custas, execução invertida etc. Preferir comandos operacionais com verbo em destaque, no infinitivo, e texto direto; concentrar detalhes executivos no próprio comando quando necessários ao cumprimento; evitar enumerar indeferimentos acessórios já abrangidos pela rejeição do pedido principal. Nas providências de impulso: evitar repetir integralmente comandos do dispositivo; quando adequado, referenciar o item deliberativo e reservar as providências seguintes para atos concretos de secretaria.
6. Ao redigir fatos relevantes à questão, diferencie rigorosamente alegações das partes e prova. Petições, contestações, réplicas, manifestações e razões recursais não devem ser tratadas como prova de fatos controvertidos, salvo para avaliar confissão, anuência, reconhecimento do pedido, fato incontroverso, renúncia, desistência, delimitação da lide ou outra declaração processual atribuível à própria parte.
7. Antes de entregar a resposta ao usuário, faça uma reflexão silenciosa, certificando-se de que a redação obedeceu as regras de estilo, o template e o plano de argumentação. Verifique especificamente se não foram usadas frases-tópico soltas ou metadiscursivas, como "Esse ponto é decisivo" ou fórmulas equivalentes, e se as petições das partes não foram usadas como elementos probatórios indevidos. Caso não tenha obedecido, faça os ajustes necessários.

Produza o texto da fundamentação em prosa corrida, conforme o template. Não inclua marcações de template, comentários ou instruções do SKILL.md na saída final. O texto deverá ser entregue pronto para incorporação à minuta.

---

## Notas de Comportamento

- Se o usuário fornecer um esqueleto de pensamento, arquivo-modelo ou estrutura argumentativa própria, incorpore-o ao plano sem citá-lo como fonte e sem transformá-lo em tópicos numerados na redação.
- Se todas as questões compartilharem a mesma solução ou premissa fático-jurídica — inclusive quando houver pedido principal e pedidos acessórios dependentes da mesma premissa —, reúna-as em bloco único para evitar redundâncias, desde que não haja prejuízo à estrutura lógica. Evite subtópicos autônomos quando isso gerar repetição.
- Em decisões com uma única questão pendente e encaminhamento evidente, dispense o parágrafo inicial de enumeração da questão e inicie a fundamentação diretamente pela premissa fático-processual relevante.
- No dispositivo, agrupe comandos logicamente dependentes em um único item quando decorrerem da mesma razão jurídica, sem prejuízo da clareza operacional.
- Nome próprio da parte é subsidiário: use na 1ª menção ou para desambiguar; depois prefira a função processual da fase/incidente (ré, requerida, executada, exequente etc.). Revisão final deve procurar repetições desnecessárias do nome.
- Em atos executivos, se a orientação do usuário delimitar quantidade, valor, alcance ou objeto da constrição/providência, preserve esse limite no dispositivo; não converta em medida integral/mais ampla. Quando necessário, use ressalva de redimensionamento posterior.
- CNIB/imóveis: ordem pessoal por CPF ≠ prova de incidência sobre matrícula específica. Para liberar/cancelar matrícula, exigir certidão atualizada, nota devolutiva/prenotação, comunicação da serventia ou relatório positivo que vincule a restrição ao imóvel/processo; sem isso, decidir por falta de lastro documental, não por substituição da garantia.
- Pedidos acessórios de honorários incidentais podem ser resolvidos em parágrafo próprio e conciso quando a solução for apenas deixar de condenar, sem item deliberativo autônomo.
- Impugnação acolhida, total/parcialmente, em execução de honorários advocatícios próprios → honorários incidentais devidos pelo advogado titular autônomo do crédito, não pela parte representada. Fundar em arts. 23 e 24 EOAB + art. 85, caput e §§ 1º e 14, CPC + causalidade; usar § 8º para fixação equitativa quando cabível.
- Em cumprimento de sentença, decisão interlocutória que resolve incidente não deve ordenar arquivamento direto; após cumprimento das providências e decurso do prazo recursal, determine conclusão para sentença/extinção quando cabível.
- Não abra tópicos ou subtópicos autônomos (como gratuidade da justiça) quando não houver pedido ou controvérsia concreta pendente sobre o tema.
- Questões meramente cadastrais/secretariais, sem controvérsia jurídica real, não precisam aparecer como questão autônoma no resumo inicial nem receber tópico próprio; resolva-as diretamente no dispositivo/providências, salvo se houver disputa ou fundamento indispensável a explicitar.
- Questões prefaciais ou processuais condicionantes devem ser tratadas antes das demais questões incidentais.
- Não use jurisprudência ou doutrina salvo quando fornecidas pelo usuário, pelo template ou por referência lida por determinação expressa.
- Não invente ou infira legislação específica. Se houver dúvida objetiva sobre norma aplicável, pesquise fonte oficial ou pergunte ao usuário.
