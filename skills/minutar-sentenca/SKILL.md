---
name: minutar-sentenca
description: Redige a fundamentação de sentenças judiciais. Use esta skill sempre que o usuário pedir para redigir, desenvolver ou elaborar a fundamentação de uma sentença judicial.
---

# /minutar-sentenca

## Personalização

Leia [personalização do gabinete](../../references/personalizacao.md) ao aplicar convenções ou preencher dados institucionais e fechamento: use a personalização do ChatGPT disponível no contexto; dados ausentes recebem placeholders padrão.

## Leitura dos anexos

Quando precisar consultar anexos, tente primeiro a leitura direta. Se houver dificuldade concreta que impeça acessar o conteúdo necessário, acione $indexar-pdf somente para os PDFs afetados, informando a dificuldade observada. Tamanho e quantidade de páginas isolados não justificam indexação. Reutilize os textos recuperados e os diagnósticos ao retomar esta skill, preservando seu escopo e checkpoints.

Esta skill conduz a elaboração da fundamentação de sentenças judiciais, de acordo com templates e regras de estilo especificadas.

## Fluxo de Execução

### FASE 00 - PREPARAÇÃO

Ao iniciar, certifique-se de que os documentos apresentados pelo usuário estão legíveis e íntegros.

Verifique as mensagens e os anexos de orientação: só conta como "orientação pré-estabelecida do usuário" a indicação expressa de resultado, tese, argumento central ou encaminhamento decisório. Tipo de ato, assunto, tema, prioridade, rito ou metadados equivalentes não dispensam checkpoint.

### Etapa 1 — Análise

**Objetivo**: compreender o caso, mapear as controvérsias e apresentar encaminhamentos para escolha ou confirmação do usuário antes da redação quando ainda não houver orientação pré-estabelecida.

Execute os seguintes passos:

1. Leia os documentos do processo fornecidos pelo usuário (petições, decisões, laudos, atas de audiência etc.).
2. Identifique as controvérsias relevantes para a fundamentação, separando-as por questão ou tópico.
3. Apresente a análise de cada controvérsia no formato abaixo.
4. Ao final, apresente a tabela-resumo. Se já houver orientação pré-estabelecida do usuário sobre o encaminhamento decisório ou a tese a adotar, registre que a análise seguirá essa orientação e avance para a Etapa 2 sem checkpoint. Se não houver orientação pré-estabelecida suficiente, aguarde o checkpoint do usuário.

**Encaminhamentos por tipo de controvérsia**:

- Sugira até três direcionamentos possíveis, cada um com título sintético, encaminhamento e justificativa em até três linhas. Os direcionamentos devem ser genuinamente distintos — não variações de tom, mas diferenças reais de encaminhamento ou fundamento (ex.: acolhimento total, acolhimento parcial, rejeição; ou fundamentos alternativos para o mesmo encaminhamento quando há mais de uma via jurídica plausível). Indique, quando houver, qual direcionamento parece mais adequado ao caso e por quê.

**Formato da Etapa 1**:

```
### ETAPA 1 — ANÁLISE

---

**[Controvérsia N — Título sintético]**

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

| Controvérsia | Encaminhamento proposto | Fundamento principal |
|---|---|---|
| ... | ... | ... |

---
⚠️ [Use apenas quando não houver orientação pré-estabelecida suficiente:] Aguardo confirmação dos encaminhamentos ou instruções antes de prosseguir para o Plano de Argumentação.
```

**Checkpoint condicional**: Após apresentar a Etapa 1, aguarde o usuário se não houver orientação pré-estabelecida suficiente para fixar o encaminhamento. Tipo de minuta, assunto ou tema não dispensam checkpoint. Quando o usuário já tiver definido previamente o resultado, a tese, o argumento central ou outro direcionamento decisório bastante, avance diretamente para a Etapa 2, observando essa orientação.

#### Registro no chat (Auditabilidade)

Havendo deliberação do usuário no checkpoint da Etapa 1 (ou após a análise inicial com base em orientação pré-estabelecida), apresente no chat, antes da Etapa 2, um registro conciso da análise e deliberação contendo:
- Controvérsias mapeadas e Ids. pertinentes;
- Encaminhamentos avaliados e deliberação adotada;
- Quadro-resumo das deliberações (controvérsia, solução adotada, fundamento principal);
- Estado da minuta (etapa realizada e fases subsequentes).

Mantenha esse registro separado do texto da minuta e avance para a Etapa 2.

---

### Etapa 2 — Plano de Argumentação

**Objetivo**: estruturar, em tópicos sintéticos, o raciocínio que orientará a redação. Não é rascunho; é um esqueleto argumentativo (skeleton-of-thought).

> [!important] Execute após o checkpoint da Etapa 1, quando ele for necessário, ou diretamente após a análise quando houver orientação pré-estabelecida suficiente do usuário.

1. Para cada controvérsia com encaminhamento confirmado pelo usuário ou previamente definido por orientação pré-estabelecida, desenvolva um plano em tópicos com frases curtas e diretas, seguindo, por padrão, a seguinte **estrutura lógico-argumentativa**:
```
→ {Apresentação das controvérsias}
→ [para cada controvérsia]:
    → {Apresentação das normas, precedentes e institutos jurídicos aplicáveis}
    → {Aplicação no caso concreto}
    → {Refutação de argumentos contrários}
    → {Conclusão parcial}
→ {Conclusão geral}
```
2. Cada tópico deve representar um bloco argumentativo na redação final e pode ser dividido em subtópicos, a depender da complexidade do argumento.
3. O plano deve ser enxuto — frases de até duas linhas por tópico.

**Formato da Etapa 2**:

```
### ETAPA 2 — PLANO DE ARGUMENTAÇÃO

**[Controvérsia N — Título sintético]**

1. [Frase direta descrevendo o que o parágrafo fará — ex.: "Apresentar o instituto X e a norma Y aplicável ao caso."]
2. [Frase direta — ex.: "Aplicar o requisito Z ao contexto fático do Id. XXXXX."]
    2.1. [Subtópico, se necessário]
    2.2. [Subtópico, se necessário]
    ...
3. [Frase direta — ex.: "Refutar a tese da parte RÉ de que [...], com base em [fundamento]."]
    3.1. [Subtópico, se necessário]
    3.2. [Subtópico, se necessário]
    ...
4. [Conclusão parcial — ex.: "Concluir pelo acolhimento/rejeição do pedido."]

**[Controvérsia N+1 — ...]**
...

**CONCLUSÃO GERAL**
- [Síntese do que será deliberado na conclusão.]
```

> [!attention] **Autoreflexão**: Antes de apresentar o Plano, certifique-se de que está condizente com as deliberações do usuário na etapa 1 e com a estrutura lógico-argumentativa padrão. Se estiver, apresente o plano; senão, faça os ajustes necessários e repita a autoreflexão (máx: 2 rodadas).

---

Após apresentar o Plano de Argumentação no formato da Etapa 2, avance diretamente para a Etapa 3. O plano funciona como etapa de organização e transparência, não como checkpoint obrigatório, salvo se o usuário pedir expressamente validação antes da redação.

---

### Etapa 3 — Redação

**Objetivo**: redigir a fundamentação completa, observando o template aplicável, as regras de estilo e o plano de argumentação.

- Template: `assets/template-sentenca.md`
- Regras de estilo: `references/regras-de-estilo.md`

Orientações:

1. Antes de iniciar a redação, carregue e leia atentamente as regras de estilo definidas em `references/regras-de-estilo.md` e o template em `assets/template-sentenca.md`.
2. Siga a estrutura do template, preenchendo cada bloco conforme as instruções nele contidas, observando as regras de estilo e o plano de argumentação da Etapa 2, utilizando-o como guia para cada parágrafo, sem citá-lo como fonte.
3. Ao redigir fatos relevantes ao mérito, diferencie rigorosamente alegações das partes e prova. Petições, contestações, réplicas, manifestações e razões recursais não devem ser tratadas como prova de fatos controvertidos, salvo para avaliar confissão, anuência, reconhecimento do pedido, fato incontroverso, renúncia, desistência, delimitação da lide ou outra declaração processual atribuível à própria parte.
4. Na abertura do tópico de mérito, redija um parágrafo de apresentação do objeto da ação, sucinto e objetivo, com a seguinte estrutura: iniciar por "Conforme relatado"; indicar a pretensão principal da parte autora; sintetizar o argumento central que sustenta o pedido; em seguida, apresentar o contraponto defensivo da parte ré. Não antecipar a conclusão do julgamento nesse parágrafo.
5. Na deliberação judicial, preliminar/prejudicial afastada fica só na fundamentação; suprima do dispositivo comandos do tipo "REJEITO a preliminar/prejudicial...". Só delibere expressamente no dispositivo a questão prefacial acolhida, quando decotar a cognição de mérito, extinguir parte do processo ou produzir providência dispositiva própria. Esta regra vale para sentença de mérito; para decisões interlocutórias cujo próprio objeto é julgar um conjunto de teses (ex. impugnação ao cumprimento de sentença), há exceção — ver `minutar-dispositivo/references/estrutura.md` § Preliminares e prejudiciais.
6. Ao redigir a **DELIBERAÇÃO JUDICIAL** e as **PROVIDÊNCIAS DE IMPULSO PROCESSUAL** (fechamento do template, após a fundamentação), acione `minutar-dispositivo`: use `minutar-dispositivo/references/estrutura.md` para heading/numeração/caixa do verbo/encerramento, `minutar-dispositivo/references/catalogo-especies.md` § Sentença A/B/C para o padrão do resultado e `minutar-dispositivo/references/circunstancias.md` para honorários, custas, AJG, remessa necessária, correção/juros e demais circunstâncias aplicáveis ao caso.
7. Calibre a extensão pela função de cada fundamento: diga só o necessário para resolver a controvérsia, sem repetir a mesma premissa em parágrafos diferentes, sem reforços retóricos e sem refutar argumentos laterais que não alterem o resultado.
8. Antes de entregar a resposta ao usuário, faça uma reflexão silenciosa, certificando-se de que a redação obedeceu as regras de estilo e o plano de argumentação, bem como as regras negativas e as restrições da skill. Verifique especificamente se não foram usadas frases-tópico soltas ou metadiscursivas, como "Esse ponto é decisivo" ou fórmulas equivalentes, se as petições das partes não foram usadas como elementos probatórios indevidos, e se a DELIBERAÇÃO JUDICIAL não contém comando de rejeição de preliminar/prejudicial já superada na fundamentação (regra do item 5 acima). Caso não tenha obedecido, faça os ajustes necessários.

Produza o texto da fundamentação em prosa corrida, conforme o template. Não inclua marcações de template, comentários ou instruções do SKILL.md na saída final. O texto deverá ser entregue  pronto para incorporação à minuta.

---

## Casos Particulares

### Juizado Especial Federal (JEF) com exclusão do ente federal

Em ações do JEF com exclusão do ente federal do polo passivo, fundamente a extinção pelo art. 1º da Lei 10.259/2001 c/c art. 51, inc. III, da Lei 9.099/1995 e Enunciado 24 do FONAJEF, evitando usar como base principal o art. 330 ou o art. 485 do CPC. Em sentenças extintivas do JEF, prefira fórmula sucumbencial sintética — "Sem custas ou honorários" —, com referência ao art. 55 da Lei 9.099/1995, quando aplicável.

### Tutela provisória anteriormente concedida

Quando houver decisão anterior concedendo tutela provisória, cautelar, antecipatória, liminar ou provimento urgente equivalente:

1. Identifique a decisão concessiva, com referência ao respectivo Id. ou evento.
2. Na Etapa 1, inclua a existência da tutela provisória entre os pontos relevantes da controvérsia e avalie se houve, depois dela, elementos novos capazes de infirmar, confirmar ou alterar seus fundamentos.
3. Na Etapa 2, preveja bloco argumentativo específico para:
   - mencionar a decisão anterior;
   - transcrever, em bloco de citação, toda a fundamentação de mérito utilizada na decisão concessiva;
   - examinar se a contestação, as provas ou manifestações posteriores afastam ou não as conclusões então adotadas;
   - complementar a análise com os argumentos defensivos e os elementos probatórios produzidos depois da tutela, quando houver.
4. Na Etapa 3, transcreva literalmente, *ipsis litteris*, toda a fundamentação de mérito da decisão concessiva em bloco de citação Markdown (`>`), sem seleção discricionária, resumo, reescrita, condensação, saneamento de notas, adaptação de estilo ou qualquer outra intervenção do agente. Preserve integralmente a redação original, inclusive erros materiais, referências jurisprudenciais, citações, destaques, figuras de linguagem, pontuação, grafia, notas de rodapé e eventuais inconsistências. Exclua apenas blocos estranhos à fundamentação de mérito, como relatório, deliberação judicial/dispositivo e providências de impulso.
   - Sempre que a decisão estiver disponível como `.txt`, use preferencialmente o script determinístico `scripts/extract_fundamentacao.py` para extrair o bloco entre `FUNDAMENTAÇÃO` e `DELIBERAÇÃO JUDICIAL`/`DISPOSITIVO`, já formatado como citação Markdown.
   - **Revisão pós-extração obrigatória antes de seguir**: confira o bloco citado contra o original para garantir fidedignidade; corrija apenas artefatos materiais de transcrição/OCR que deturpem o texto original, especialmente símbolos jurídicos (`§` ≠ `$`/`S`/`8`), números de artigos, incisos, datas e Ids.
   - Recomponha quebras artificiais de linha dentro do mesmo parágrafo citado; preserve quebras estruturais reais (parágrafos, itens numerados, títulos) e o teor textual. Faça busca final por ruídos comuns (`Este documento foi gerado`, linhas de ementa quebradas palavra-a-palavra, `Id.` isolado em linha) antes de entregar.
   - Execute o script empacotado em `scripts/extract_fundamentacao.py` com o arquivo de decisão como argumento; se o ambiente não expuser o script, aplique os mesmos limites objetivos descritos no item seguinte.
   - Se o script não localizar marcadores claros, não faça recorte por intuição. Leia a decisão, identifique limites objetivos por títulos/linhas, informe a incerteza se necessário e transcreva apenas quando o intervalo completo da fundamentação de mérito estiver determinado.
5. Após o bloco de citação, desenvolva a análise de mérito da sentença a partir da estabilidade, confirmação, superação ou necessidade de complementação daqueles fundamentos.

Modelo de redação:

```markdown
A decisão que concedeu a tutela provisória (Id. ...) o fez sob os seguintes fundamentos:

> Nos termos do art. ..., o uso reiterado ...
>
> ...
>
> Há, portanto, elementos que indicam a probabilidade do direito vindicado pela parte autora.

De fato, após proferida a decisão, não foram apresentados elementos capazes de infirmar suas conclusões.

Em contestação, a parte ré sustentou que [...]. O argumento, contudo, não procede, pois [...].
```

---

## Notas de Comportamento

- Se o usuário fornecer um "esqueleto de pensamento", arquivo-modelo ou estrutura argumentativa própria, incorpore-a ao plano (Etapa 2) sem citá-la como fonte e sem transformá-la em tópicos numerados na redação.
- Se todas as controvérsias compartilharem a mesma solução ou premissa fático-jurídica, reúna-as em bloco único para evitar redundâncias, desde que não haja prejuízo à estrutura lógica.
- Questões prefaciais (gratuidade da justiça, emenda à inicial etc.) devem ser tratadas antes do mérito ou do pedido de tutela, conforme previsto nos templates.
- Conselho profissional ≠ isento de custas na Justiça Federal: art. 4º, parágrafo único, da Lei nº 9.289/1996 exclui entidades fiscalizadoras do exercício profissional da isenção do art. 4º, inc. I; se vencido, condenar ao pagamento de custas e despesas processuais.
- Honorários em causa de valor irrisório (inferior a R$ 39.000,00): aplicar art. 85, §§ 8º e 8º-A, do CPC e tabela OAB vigente indicada pelo usuário/task/modelo; para OAB-TO Resolução nº 07/2025, Anexo I, item 10.21 - honorários de R$ 3.913,20.
