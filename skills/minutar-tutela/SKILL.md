---
name: minutar-tutela
description: Analisa e minuta decisões de tutela provisória, completas por padrão; partes isoladas somente quando expressamente solicitadas. Abrange tutela provisória (urgência, evidência, liminares em procedimentos especiais e questões processuais ligadas ao pedido urgente). Use para analisar/julgar/decidir/redigir minuta de tutela provisória, liminar, antecipação, tutela cautelar, de urgência ou evidência.
---

# /minutar-tutela

## Personalização

Leia [personalização do gabinete](../../references/personalizacao.md) ao aplicar convenções ou preencher dados institucionais e fechamento: use a personalização do ChatGPT disponível no contexto; dados ausentes recebem placeholders padrão.

## Leitura dos anexos

Quando precisar consultar anexos, tente primeiro a leitura direta. Se houver dificuldade concreta que impeça acessar o conteúdo necessário, acione $indexar-pdf somente para os PDFs afetados, informando a dificuldade observada. Tamanho e quantidade de páginas isolados não justificam indexação. Reutilize os textos recuperados e os diagnósticos ao retomar esta skill, preservando seu escopo e checkpoints.

## Escopo da entrega

Pedidos para minutar, redigir, elaborar ou preparar este ato produzem, por padrão, a minuta completa, mesmo sem as palavras "completa", "integral" ou "inteira". A invocação desta skill pelo nome também segue esse padrão. Conduza esses pedidos pelo $minutar-completa.

Entregue partes isoladas apenas quando o usuário delimitar expressamente o escopo, por exemplo, "redija a fundamentação", "somente o relatório", "apenas o dispositivo" ou "relatório e fundamentação, sem dispositivo". Pedidos exclusivos de análise ou julgamento não iniciam a redação de uma minuta sem solicitação. Preserve os checkpoints de deliberação e de plano de argumentação.

Quando chamada por $minutar-completa, execute apenas a etapa atribuída, devolva o texto à skill coordenadora e não a acione novamente. Na execução parcial, redija somente as seções solicitadas, ainda que o template contenha outras seções.


Esta skill conduz a elaboração da fundamentação de decisões sobre tutela provisória, de acordo com templates e regras de estilo especificadas.

## Fluxo de Execução

### FASE 00 - PREPARAÇÃO

Ao iniciar, certifique-se de que os documentos apresentados pelo usuário estão legíveis e íntegros.

Identifique a espécie de tutela requerida:

- tutela provisória de urgência antecipada;
- tutela provisória de urgência cautelar;
- tutela de evidência;
- liminar ou medida equivalente em procedimento especial;
- indisponibilidade de bens em ação de improbidade administrativa (regime próprio do art. 16 da Lei 8.429/1992 — não é tutela de urgência/evidência do CPC puro);
- questão processual diretamente condicionante do exame da tutela.

Quando houver procedimento especial, verifique se há regra legal específica para a liminar antes de aplicar o art. 300 ou o art. 311 do Código de Processo Civil.

### Verificação inicial — orientações do usuário

Verifique se a conversa ou algum anexo contém orientação expressa do usuário sobre o encaminhamento de cada questão ligada ao pedido urgente (por exemplo, conceder ou indeferir, e por quê).

- **Orientação suficiente para todas as questões**: trate-a como a deliberação do usuário sobre a Etapa 1. Pule a Etapa 1 — não a apresente nem peça confirmação dela — e vá direto à Etapa 2, incorporando a orientação ao plano de argumentação. Ao final da Etapa 2, não aguarde validação do usuário: avance automaticamente para a Etapa 3.
- **Orientação ausente, ou insuficiente para alguma questão**: siga o fluxo integral, com checkpoint ao final da Etapa 1 e da Etapa 2. Se a orientação cobrir apenas parte das questões, execute a Etapa 1 normalmente para as não cobertas e trate as demais como já deliberadas.

### Etapa 1 — Análise

**Dispensada quando houver orientação prévia suficiente** (ver "Verificação inicial" acima).

**Objetivo**: compreender o pedido urgente, mapear os requisitos jurídicos incidentes e apresentar encaminhamentos para escolha ou confirmação do usuário antes de qualquer redação.

Execute os seguintes passos:

1. Leia os documentos do processo fornecidos pelo usuário, priorizando petição inicial, documentos instrutórios ligados à urgência, manifestações sobre a tutela, decisões anteriores e atos processuais relevantes.
2. Identifique as questões pendentes de decisão, separando questões prefaciais e processuais do pedido de tutela quando necessário.
3. Classifique a tutela requerida e mapeie os requisitos jurídicos aplicáveis.
4. Em tutela de urgência, examine primeiro o perigo de dano ou risco ao resultado útil do processo. Só prossiga ao exame da probabilidade do direito se a urgência estiver presente, salvo orientação diversa do usuário ou necessidade lógica do caso.
5. Em tutela de evidência, não exija perigo de dano. Examine a hipótese do art. 311 do CPC ou fundamento legal específico indicado pelo usuário.
6. Apresente a análise de cada questão no formato abaixo.
7. Ao final, apresente a tabela-resumo e aguarde o checkpoint do usuário.

**Encaminhamentos por questão**:

- Sugira até três direcionamentos possíveis, cada um com título sintético, encaminhamento e justificativa em até três linhas. Os direcionamentos devem ser genuinamente distintos, não variações de tom. Indique, quando houver, qual direcionamento parece mais adequado ao caso e por quê.
- Ao propor concessão, delimite com precisão a obrigação, seus limites, prazo de cumprimento, eventual multa, caução, reversibilidade e providências de comunicação ou intimação.
- Ao propor indeferimento, explicite qual requisito não foi demonstrado e se algum exame fica prejudicado.

**Formato da Etapa 1**:

```markdown
### ETAPA 1 — ANÁLISE

---

**[Questão N — Título sintético]**

[Síntese fática da questão, com referência aos Ids. relevantes.]
[Espécie de tutela e requisitos jurídicos aplicáveis — apenas mapeamento, sem aprofundamento.]

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
- Questões/pedidos urgentes mapeados e Ids. pertinentes;
- Encaminhamentos propostos e deliberação adotada;
- Quadro-resumo das deliberações (pedido, parte, solução adotada, fundamento normativo);
- Estado da minuta (etapa realizada e fases subsequentes).

Mantenha esse registro separado da minuta e avance para a Etapa 2.

---

### Etapa 2 — Plano de Argumentação

**Objetivo**: estruturar, em tópicos sintéticos, o raciocínio que orientará a redação. Não é rascunho; é um esqueleto argumentativo.

> [!important] Execute após o checkpoint da Etapa 1 — ou, no fluxo abreviado por orientação prévia suficiente, diretamente após a leitura das peças.

1. Para cada questão com encaminhamento confirmado pelo usuário ou definido por orientação prévia suficiente, desenvolva um plano em tópicos com frases curtas e diretas.
2. Use, por padrão, a seguinte estrutura lógico-argumentativa para tutela de urgência:

```markdown
→ {Apresentação da questão pendente}
→ {Apresentação da norma aplicável}
→ {Exame do perigo de dano ou risco ao resultado útil do processo}
→ {Exame da probabilidade do direito, se não prejudicado}
→ {Exame da reversibilidade e da proporcionalidade da medida, se pertinente}
→ {Delimitação dos efeitos práticos da decisão}
→ {Conclusão parcial}
```

3. Use, por padrão, a seguinte estrutura lógico-argumentativa para tutela de evidência:

```markdown
→ {Apresentação da questão pendente}
→ {Apresentação da hipótese legal aplicável}
→ {Exame da suficiência documental ou do fundamento específico}
→ {Refutação de argumentos contrários, se houver}
→ {Delimitação dos efeitos práticos da decisão}
→ {Conclusão parcial}
```

4. Para liminares em procedimentos especiais, adapte a estrutura aos requisitos legais específicos do procedimento.
5. Cada tópico deve representar um bloco argumentativo na redação final e pode ser dividido em subtópicos, a depender da complexidade do argumento.
6. O plano deve ser enxuto, com frases de até duas linhas por tópico.

**Formato da Etapa 2**:

```markdown
### ETAPA 2 — PLANO DE ARGUMENTAÇÃO

**[Questão N — Título sintético]**

1. [Frase direta descrevendo o que o parágrafo fará.]
2. [Frase direta descrevendo o requisito ou ponto fático-jurídico.]
    2.1. [Subtópico, se necessário.]
    2.2. [Subtópico, se necessário.]
3. [Frase direta para refutar argumento contrário, se houver.]
4. [Frase direta sobre limites, prazo, multa, caução ou providência prática, se aplicável.]
5. [Conclusão parcial.]

**[Questão N+1 — ...]**
...

**CONCLUSÃO GERAL**
- [Síntese do que será deliberado.]
```

**Autoreflexão**: Antes de apresentar o Plano, certifique-se de que está condizente com as deliberações do usuário na Etapa 1, com a espécie de tutela identificada e com a estrutura lógico-argumentativa aplicável. Se estiver, apresente o plano; senão, faça os ajustes necessários e repita a autoreflexão, no máximo em 2 rodadas.

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

- Estrutura comum: `assets/estrutura-comum.md` (toda redação).
- Modalidade: `assets/urgencia.md`, `assets/evidencia.md`, `assets/indisponibilidade-improbidade.md` ou `assets/procedimento-especial.md` (somente as modalidades presentes no caso).
- Exemplos: `assets/exemplos.md` (consulta opcional para tutela de urgência).
- Regras de estilo: `references/regras-de-estilo.md` (toda redação).

Orientações:

1. Antes de iniciar a redação, leia `references/regras-de-estilo.md` e `assets/estrutura-comum.md`. Pela classificação da Etapa 1, leia apenas o arquivo de cada modalidade efetivamente presente na decisão. Consulte `assets/exemplos.md` somente se um exemplo de tutela de urgência ajudar na redação.
2. Siga a estrutura comum e o template da modalidade selecionada, observando as regras de estilo e o plano de argumentação aprovado na Etapa 2, utilizando-o como guia para cada parágrafo, sem citá-lo como fonte.
3. Em tutela de urgência, se ausente o perigo de dano ou risco ao resultado útil do processo, conclua que fica prejudicado o exame da probabilidade do direito, salvo orientação diversa do usuário.
4. Na etapa interna de fundamentação ou no pedido expresso dessa seção, inclua somente a fundamentação e a delimitação argumentativa da medida. Na minuta completa, inclua o dispositivo tanto na concessão quanto no indeferimento, pela coordenação de $minutar-completa. Para redigir o dispositivo solicitado ou integrar a minuta completa, acione `minutar-dispositivo` (`minutar-dispositivo/references/estrutura.md` + `minutar-dispositivo/references/catalogo-especies.md` § Decisão de Tutela Provisória + `minutar-dispositivo/references/circunstancias.md` para AJG, remessa necessária, execução invertida etc.) em vez de redigir a seção livremente.
5. Ao redigir fatos relevantes ao pedido de tutela, diferencie rigorosamente alegações das partes e prova. Petições, contestações, réplicas, manifestações e razões recursais não devem ser tratadas como prova de fatos controvertidos, salvo para avaliar confissão, anuência, reconhecimento do pedido, fato incontroverso, renúncia, desistência, delimitação da lide ou outra declaração processual atribuível à própria parte.
6. Antes de entregar a resposta ao usuário, faça uma reflexão silenciosa, certificando-se de que a redação obedeceu as regras de estilo, o template e o plano de argumentação. Verifique especificamente se não foram usadas frases-tópico soltas ou metadiscursivas, como "Esse ponto é decisivo" ou fórmulas equivalentes, e se as petições das partes não foram usadas como elementos probatórios indevidos. Caso não tenha obedecido, faça os ajustes necessários.

Produza o texto da fundamentação em prosa corrida, conforme o template. Não inclua marcações de template, comentários ou instruções do SKILL.md na saída final. O texto deverá ser entregue pronto para incorporação à minuta.

---

## Notas de Comportamento

- Se o usuário fornecer um esqueleto de pensamento, arquivo-modelo ou estrutura argumentativa própria, incorpore-o ao plano sem citá-lo como fonte e sem transformá-lo em tópicos numerados na redação.
- Se houver mais de um pedido urgente e todos compartilharem a mesma solução ou premissa fático-jurídica, reúna-os em bloco único para evitar redundâncias, desde que não haja prejuízo à estrutura lógica. Da mesma forma, quando houver uma única questão efetiva, redija a fundamentação em bloco único, sem criar subtópicos autônomos desnecessários.
- Não abra tópicos ou subtópicos autônomos (como gratuidade da justiça) quando não houver pedido ou controvérsia concreta pendente sobre o tema.
- Em decisões com tópicos próprios, dispense o parágrafo inicial de enumeração das questões pendentes quando ele apenas repetir os títulos que serão enfrentados em seguida.
- Competência JEF/PJEC: quando a tutela vier acompanhada de ajuste de fluxo p/ JEF adjunto, fundamente a competência absoluta com art. 3º, §§ 1º e 3º, Lei 10.259/2001; deixe a alteração de fluxo como providência operacional, salvo necessidade de comando decisório próprio.
- Indeferimento por requisitos cumulativos: se o usuário pedir ausência de urgência + ausência de probabilidade, analise ambos; após afastar urgência, use fórmula condicional ("ainda que fosse demonstrada a urgência...") antes de examinar probabilidade.
- Dados sensíveis de saúde: prefira "segredo de justiça" a "sigilo dos autos"; fundamente no art. 189, inc. III, CPC, c/c lei específica aplicável (ex.: Lei 14.289/2022).
- Quando a remessa ao CEJUC for providência processual simples e não controvertida, trate o tema apenas na deliberação judicial e nas providências de impulso, sem abrir tópico autônomo de fundamentação; nesses casos, prefira comando operacional para citar a parte ré e remeter os autos ao CEJUC, deixando a intimação para a audiência à rotina própria do centro de conciliação.
- Nas providências de impulso, formule comandos diretos com o verbo operacional em destaque, quando compatível com o padrão da minuta, e evite repetir deliberação já feita em decisão anterior — se a providência anterior ainda não tiver sido cumprida, referencie-a apenas na seção de providências de impulso.
- Questões prefaciais ou processuais que condicionem o exame da tutela devem ser tratadas antes do pedido urgente.
- Não use jurisprudência ou doutrina salvo quando fornecidas pelo usuário, pelo template ou por referência lida por determinação expressa.
- Não invente ou infira legislação específica. Se houver dúvida objetiva sobre norma aplicável, pesquise fonte oficial ou pergunte ao usuário.
