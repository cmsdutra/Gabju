---
name: esp-contadoria-judicial
description: Consultas de contadoria judicial federal (correção monetária, juros, custas, honorários, precatórios/RPV); calcula/confere juros compostos e tabelas de amortização (Price, SAC); consulta índices (Selic, IPCA-E, INPC, TR) via Manual CJF. Também usar como etapa interna de outra skill/fluxo.
---

# /contadoria-judicial

## Leitura dos anexos

Quando precisar consultar anexos, tente primeiro a leitura direta. Se houver dificuldade concreta que impeça acessar o conteúdo necessário, acione $indexar-pdf somente para os PDFs afetados, informando a dificuldade observada. Tamanho e quantidade de páginas isolados não justificam indexação. Reutilize os textos recuperados e os diagnósticos ao retomar esta skill, preservando seu escopo e checkpoints.

Esta skill responde a consultas técnicas de contadoria judicial na Justiça Federal, combinando três fontes: a wiki normativa do manual de cálculos, a consulta a bases oficiais de índices econômicos e um conjunto de rotinas de cálculo/verificação, cada uma em seu próprio script e (quando necessário) sua própria referência — carregados sob demanda, apenas quando a rotina em questão é usada. Quando a consulta é direta do usuário, o produto é um **parecer estruturado**; quando a skill é acionada por outra skill/fluxo como etapa de verificação de cálculo, o produto é apenas o resultado técnico necessário, sem o formato de parecer (ver Passo 1).

## Fluxo de Execução

### Passo 1 — Classificar a consulta e o modo de resposta

Primeiro, identifique **quem está consultando e para quê**, pois isso determina o formato da entrega:

- **Consulta direta** — o usuário pergunta diretamente à contadoria (ex.: "qual índice incide nessa liquidação?", "elabore o cálculo desses juros", "quanto fica esse valor atualizado?"). A entrega é o **parecer estruturado** (Passo 5).
- **Uso interno por outra skill/fluxo** — esta skill foi acionada como etapa de uma tarefa maior, tipicamente para conferir ou apurar um cálculo dentro de uma minuta que outra skill está redigindo (ex.: uma futura skill de fundamentação e análise processual verificando se o valor de uma condenação/atualização citado nos autos está correto). Nesse caso **não produza um parecer formal** — entregue apenas o resultado técnico necessário (índice/valor usado, memória de cálculo, conclusão objetiva), no formato que a tarefa chamadora precisar incorporar. O template de parecer (`assets/templates/parecer.md`) não deve ser imposto nessa hipótese.

Em caso de dúvida sobre qual dos dois modos se aplica, verifique se a pergunta veio do usuário em linguagem natural (consulta direta) ou se veio de instruções/contexto de outra skill pedindo um insumo específico (uso interno).

Em seguida, identifique qual(is) elemento(s) a consulta exige, em qualquer um dos dois modos:

1. **Orientação normativa** — qual índice, taxa de juros, honorário ou procedimento incide em determinado tipo de ação/liquidação. Resolve-se consultando a wiki em `references/manual-de-calculos-2025/`.
2. **Dado de índice atualizado** — o valor numérico de um índice (Selic, IPCA-E, INPC, TR, poupança etc.) para um período específico, ainda não fornecido pelo usuário nem constante dos autos. Resolve-se consultando a fonte primária indicada em `references/indices-oficiais.md`; sem acesso à fonte, solicite o dado ao usuário.
3. **Cálculo aritmético ou verificação de regularidade** — aplicar coeficiente(s), juros ou honorários sobre um valor principal, ou conferir se um cálculo/tabela de amortização já apresentado é regular, a partir de parâmetros já validados. Resolve-se com a rotina correspondente em `scripts/rotinas/` (ver Passo 4).

A maioria das consultas combina os três. Não pule a classificação — ela determina quais dos passos seguintes são necessários.

### Passo 2 — Consultar a wiki normativa

Comece sempre por `references/manual-de-calculos-2025/index.md` para localizar o capítulo/item pertinente ao tipo de ação ou dívida em questão. Siga os links internos (`Veja também`) até encontrar a orientação específica sobre o indexador, a taxa de juros, os honorários ou o procedimento de cálculo (resumido/detalhado) aplicáveis.

Se o título judicial (sentença/acórdão) fornecido pelo usuário definir critério diferente do manual, **prevalece o título judicial** — o manual é orientação subsidiária, não vinculante (ver nota na página raiz da wiki).

Se a wiki não cobrir a hipótese ou houver ambiguidade relevante, informe o usuário em vez de decidir por conta própria.

### Passo 3 — Obter dados de índices oficiais (quando necessário)

Se a consulta exigir valor atual ou histórico não fornecido, identifique o índice, o período exato e se o cálculo exige variação por competência ou dados brutos para coeficiente acumulado. Consulte a fonte primária indicada em `references/indices-oficiais.md` quando o ambiente oferecer acesso à web.

Registre a fonte, a data da consulta, a série utilizada, a unidade e o período. Se não houver acesso à fonte oficial ou o dado não puder ser confirmado, peça ao usuário a tabela ou os valores e suspenda apenas a etapa numérica dependente deles.

**Nunca estime, arredonde de memória ou "complete" um valor de índice não confirmado.**

### Passo 4 — Executar a rotina de cálculo

Cada operação de cálculo/verificação é uma **rotina independente** em `scripts/rotinas/` — não há um script único acumulando tudo. Identifique apenas a rotina necessária para a consulta atual; não é preciso ler os scripts nem as referências das demais rotinas.

| Rotina | Uso | Script | Referência (ler apenas se for usar esta rotina) |
|---|---|---|---|
| Coeficiente de correção monetária | Encadear variações percentuais mensais em um coeficiente acumulado | `scripts/rotinas/coeficiente.py` | — (autoexplicativo via `--help`) |
| Atualização monetária | Aplicar coeficiente + juros + honorários sobre um principal, no padrão de tabela do manual | `scripts/rotinas/atualizacao_monetaria.py` | — (autoexplicativo via `--help`) |
| Juros simples | Juros simples dado taxa mensal e número de meses | `scripts/rotinas/juros_simples.py` | — (autoexplicativo via `--help`) |
| Juros compostos | Calcular montante composto, ou verificar se um montante informado é compatível com juros simples/compostos | `scripts/rotinas/juros_compostos.py` | `references/rotinas/juros-compostos.md` |
| Tabela Price | Gerar a tabela Price esperada, ou verificar uma tabela informada contra ela | `scripts/rotinas/tabela_price.py` | `references/rotinas/tabela-price.md` |
| Tabela SAC | Gerar a tabela SAC esperada, ou verificar uma tabela informada contra ela | `scripts/rotinas/tabela_sac.py` | `references/rotinas/tabela-sac.md` |
| Verificação genérica de tabela | Conferir a regularidade interna de uma tabela de amortização sem presumir o sistema (Price/SAC/outro) | `scripts/rotinas/verificar_tabela.py` | `references/rotinas/verificacao-de-tabela.md` |

Rode `python3 scripts/rotinas/<arquivo>.py --help` (ou `<subcomando> --help`) para confirmar os parâmetros exatos de qualquer rotina. As rotinas de verificação de tabela (`tabela_price.py`, `tabela_sac.py`, `verificar_tabela.py`) recebem a tabela a conferir como um CSV com cabeçalho `periodo,saldo_inicial,juros,amortizacao,prestacao,saldo_final` — monte esse CSV a partir dos dados fornecidos pelo usuário antes de rodar a rotina.

Para cálculos que envolvam múltiplos períodos com regras diferentes (ex.: método detalhado de precatório complementar, com 3 fases de atualização), execute a rotina pertinente uma vez por fase e monte a tabela final combinando os resultados, no mesmo padrão dos exemplos do manual.

Ao concluir que uma tabela ou cálculo apresenta irregularidade, não presuma automaticamente a causa jurídica (ex.: anatocismo) — reporte o achado aritmético e, se for redigir parecer (Passo 5), remeta à wiki normativa ou ao usuário a qualificação jurídica do achado.

### Passo 5 — Entregar o resultado

O formato da entrega depende do modo identificado no Passo 1:

- **Consulta direta:** leia `references/memory.md` e redija o parecer usando `assets/templates/parecer.md`, preenchendo apenas as seções pertinentes ao quesito concreto.
- **Uso interno por outra skill/fluxo:** leia `references/memory.md` e entregue apenas o resultado técnico pedido (índice/valor usado com fonte, memória de cálculo, conclusão objetiva), sem seções não solicitadas.

---

## Limitações Absolutas

- Não invente, estime ou aproxime valores de índices econômicos. Todo valor numérico usado em um cálculo deve vir do usuário, dos autos ou de uma consulta oficial feita no momento (Passo 3).
- Não decida qual índice/taxa é juridicamente aplicável em caso de conflito entre o manual e o título judicial — o título judicial prevalece; em caso de ambiguidade, pergunte.
- Não cite jurisprudência além da já referenciada na wiki do manual ou fornecida expressamente pelo usuário (número do processo, tribunal e ementa/texto completo).
- Não realize pesquisas externas de doutrina ou legislação além do necessário para localizar dados de índices oficiais (Passo 3) — a fundamentação normativa vem do manual.
- Não emita juízo sobre o mérito da causa. O parecer de contadoria é técnico (índices, cálculos e procedimento), não decisório.
- Sempre registre, no parecer, a fonte e a data de consulta de qualquer índice obtido externamente — nunca apresente um número sem rastreabilidade.

---

## Arquivos de referência

- `references/manual-de-calculos-2025/` — wiki normativa do Manual de Orientação de Procedimentos para os Cálculos na Justiça Federal (CJF, Resolução n. 963/2025). **Consulte antes de qualquer orientação sobre índice, juros ou procedimento aplicável.**
- `references/indices-oficiais.md` — mapa de fontes primárias por índice econômico, para orientar (e avaliar a plausibilidade d)o Passo 3.
- `references/memory.md` — regra consolidada sobre cumulação da Selic. **Leia antes de executar cálculo ou redigir parecer.**
- `assets/templates/parecer.md` — estrutura do parecer técnico, usada apenas no modo de consulta direta (Passo 1).
- `scripts/rotinas/` e `references/rotinas/` — rotinas modulares de cálculo e verificação (ver tabela do Passo 4). Cada rotina é independente; leia apenas o script/referência da rotina que a consulta atual exigir.
