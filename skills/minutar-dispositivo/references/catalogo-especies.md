---
created: 2026-10-08
updated: 2026-10-08
ai-agent: "Codex CLI"
---

# Catálogo por Espécie de Ato

Fórmulas verbatim (adaptar aos fatos do caso; nunca copiar nome/valor/Id. de exemplo). Taxonomia = convenção interna do próprio gabinete (`act-type` do frontmatter das minutas): Sentença A (mérito comum), Sentença B (especial — reconhecimento do pedido/homologação), Sentença C (extintiva sem mérito), Decisão Interlocutória, Decisão Tutela Provisória, Despacho, Embargos de Declaração, Saneamento.

Regras gerais de formatação (heading, alínea/romano, caixa do verbo, encerramento) → `estrutura.md`. Circunstâncias transversais (AJG, remessa necessária, honorários etc.) → `circunstancias.md`, combine com o padrão de espécie abaixo.

## Sentença A — procedente / parcialmente procedente

**Padrão-base**:
> **(a)** **ACOLHO** os pedidos formulados na petição inicial, nos termos do art. 487, inc. I, do Código de Processo Civil, para condenar [parte ré] ao pagamento, ao autor, de indenização por danos morais no valor de R$ 1.000,00 (mil reais).

**Procedência parcial** (variantes de verbo coexistem sem diferença semântica: "ACOLHO PARCIALMENTE" / "ACOLHO EM PARTE" / "JULGO PARCIALMENTE PROCEDENTES"):
> **(a) JULGO PARCIALMENTE PROCEDENTES os pedidos** formulados na petição inicial, nos termos do art. 487, inc. I, do CPC, para declarar [...] e, por conseguinte, condenar [ré] ao pagamento das diferenças [...]

**Fórmula fixa quase universal**: `nos termos do art. 487, inc. I, do Código de Processo Civil, para [verbo infinitivo: condenar/declarar/determinar]...` — citado em praticamente toda sentença de mérito (procedente, improcedente ou parcial), como "carimbo" processual logo após o verbo de julgamento.

**Confirmação/concessão de tutela na própria sentença** (inserir na prévia da deliberação principal):
> "**CONFIRMO** a tutela provisória concedida pela decisão de Id. [...], e, por conseguinte, **ACOLHO** os pedidos formulados..."

**Duas ou mais tutelas específicas no mesmo comando** — usar lista com quebra de linha:
```
**(a)** ... para:

**(a.1)** declarar nulo o contrato [...] celebrado entre as partes; e

**(a.2)** condenar o requerido ao pagamento ao autor de R$ 2.000,00 (dois mil reais) a título de indenização por danos morais.
```

### Litisconsórcio com resultados distintos

Sucumbência recíproca fracionada por réu:
> **(a)** **ACOLHO EM PARTE** os pedidos [...]; **(b)** **CONDENO** [réu 1] ao pagamento de 40% (quarenta por cento) das custas [...]; **(c)** **CONDENO** a autora ao pagamento de 60% (sessenta por cento) das custas [...]

Solidariedade entre entes públicos co-réus com direcionamento primário (saúde, Tema 793/STF):
> **(a)** **ACOLHO** os pedidos [...] para condenar solidariamente a UNIÃO e o ESTADO [UF] à continuidade do tratamento de saúde [...], com direcionamento primário da obrigação ao ESTADO [UF], por ser o ente com maior aptidão operacional [...], nos termos do Tema 793 do Supremo Tribunal Federal.

Custeio integral por um ente com ressarcimento pelo outro:
> **(a.1)** O custeio recairá integralmente sobre a UNIÃO [...] Na hipótese de impossibilidade de cumprimento pela UNIÃO, o ESTADO [UF] deverá providenciar o fornecimento, fazendo jus ao ressarcimento integral pela UNIÃO via repasse Fundo a Fundo (FNS ao FES).

Nota: em litisconsórcio de entes públicos, prefira "condenar solidariamente, com direcionamento primário a X" ou "custeio por X com ressarcimento por Y" — não "condenar apenas um". Em litisconsórcio passivo sem solidariedade, use uma alínea de mérito por réu com percentuais de sucumbência proporcionais.

**Providências de impulso — padrão-base de sentença de mérito (sem remessa necessária)**:
> **(i)** **intimar** as partes desta sentença e aguardar o prazo recursal;
> **(ii)** interposto recurso, **colher** contrarrazões e, por fim, **encaminhar** os autos à instância revisora para julgamento, independentemente de juízo de admissibilidade;
> **(iii)** não interposto recurso no prazo legal, **certificar** o trânsito em julgado e **arquivar** o feito com as formalidades de praxe.

Com remessa necessária ou pendência de novo requerimento → ver `circunstancias.md` § Remessa necessária / § Prazo recursal.

## Sentença A — improcedente

**Padrão-base**, estável e recorrente:
> **(a)** **REJEITO** os pedidos formulados na petição inicial, nos termos do art. 487, inc. I, do Código de Processo Civil.
>
> **(b)** **CONDENO** [a parte autora] ao pagamento de honorários advocatícios em favor [da Procuradoria Federal/do(a) patrono(a) da parte adversária], [fixados em/no importe de] R$ 3.721,20 (três mil, setecentos e vinte e um reais e vinte centavos) [ou] 10% sobre o valor da causa, nos termos do art. 85, §§ 2º, 8º, 8º-A e 19, do Código de Processo Civil, e do item 10.21 do Anexo I da Resolução OAB/TO nº 05/2024.

Variante: `**(a) JULGO IMPROCEDENTES** os pedidos formulados na petição inicial, nos termos do art. 487, inc. I, do Código de Processo Civil;`

Nota: o valor de R$ 3.721,20 no exemplo acima reflete a Resolução OAB/TO 05/2024, vigente no período coberto pela amostra — **superada**. Valor de piso atualizado (Resolução OAB/TO nº 07/2025, Anexo I, item 10.21): **R$ 3.913,20** (ver `minutar-sentenca/SKILL.md` § Notas de Comportamento, fonte única deste valor). O combo "art. 85, §§ 2º, 8º, 8º-A e 19, CPC" é o fundamento-padrão de honorários por equidade/mínimo em JEF.

Providências de impulso: mesmo padrão-base de sentença de mérito acima.

## Sentença C — extintiva sem resolução de mérito

Ilegitimidade passiva de ente federal em JEF (extinção antes da citação dos demais):
> Diante do exposto, **INDEFIRO a petição inicial**, nos termos do art. 51, inc. II, da Lei nº 9.099/1995, c/c art. 1º, da Lei nº 10.259/2001.
>
> Sem custas ou honorários.

Com reconhecimento explícito da ilegitimidade antes:
> **(a)** **RECONHEÇO** a ilegitimidade passiva de [ré]; **(b)** por consequência, **INDEFIRO** a petição inicial e **EXTINGO** o processo sem resolução do mérito, nos termos do art. 1º da Lei nº 10.259/2001 c/c art. 51, inc. III, da Lei nº 9.099/1995 e do Enunciado 24 do FONAJEF.
> Sem condenação em custas ou honorários (art. 55, Lei 9.099/1990).

Perda superveniente de objeto (óbito da parte):
> **(a)** **EXTINGO** o processo sem resolução do mérito, em razão da perda superveniente do objeto decorrente do óbito da parte autora, nos termos do art. 485, inc. IX, do Código de Processo Civil.
> **(b)** **CONDENO** o espólio da parte autora ao pagamento de honorários advocatícios [...], a serem rateados em partes iguais entre os réus, nos termos do art. 85, § 8º, do CPC, e do Tema-RR 1.313. Contudo, fica a exigibilidade das verbas sucumbenciais suspensa, em razão da gratuidade da justiça deferida à parte autora, nos termos do art. 98, § 3º, do Código de Processo Civil.

Falta de interesse de agir (matéria decidida em outra via):
> **(a)** **EXTINGO** o processo sem resolução do mérito, por ausência de interesse de agir, nos termos do art. 485, inc. VI, do Código de Processo Civil.

**Providências de impulso características (JEF — diferente do padrão de sentença de mérito: citação só ocorre se houver recurso)**:
> **(i)** **intimar** a parte autora;
> **(ii)** interposto recurso, **citar** os requeridos e **colher** suas contrarrazões, remetendo os autos, em seguida, à Turma Recursal;
> **(iii)** decorrido o prazo recursal *in albis*, **certificar** o trânsito em julgado e **arquivar** o feito com as formalidades de praxe.

## Saneamento

Ver também `minutar-saneamento/assets/template-saneamento.md` (template operacional completo, inclusive fluxos de perícia AJG/não-AJG). Abertura característica **diferente do resto do corpus**: `Ante o exposto, **DECIDO**:` (não "Diante do exposto"). Verbo-núcleo em **minúscula** mesmo em negrito — diferença sistemática de registro frente a sentença/tutela.

**Padrão-base, altamente estruturado e repetitivo (parece template fixo do gabinete)**:
> **(a)** **resolver** as questões processuais pendentes e declarar saneado o feito;
> **(b)** **fixar** as controvérsias de fato e de direito conforme disposto na fundamentação;
> **(c)** **manter** a distribuição do ônus da prova nos termos do art. 373, inc. I e II, do Código de Processo Civil, incumbindo à parte autora a demonstração dos fatos constitutivos de seu direito e à(s) parte(s) ré(s) a comprovação de eventuais fatos impeditivos, modificativos ou extintivos;
> **(d)** **deferir** a produção de **perícia [médica/contábil]**, para [objeto da perícia]; [detalhamento em (d.1), (d.2)... conforme AJG ou não — ver template-saneamento.md]
> **(e)** **indeferir** [demais provas requeridas], por [motivo].

**Providências de impulso típicas (perícia)**:
> **(i)** **intimar** as partes sobre esta decisão e para que, no prazo de 5 (cinco) dias, manifestem eventuais causas de impedimento ou suspeição do perito, indiquem assistentes técnicos e apresentem quesitos (art. 465, § 1º, CPC);
> **(ii)** com a manifestação das partes, não havendo impugnação quanto à nomeação, **intimar** o perito para, no prazo de 5 (cinco) dias, dizer se aceita o encargo e, se for o caso, apresentar proposta de honorários;
> **(iii)** aceito o encargo e apresentada a proposta de honorários, **intimar** as partes para manifestação no prazo de 5 (cinco) dias;
> **(iv)** por fim, **concluir** os autos para arbitramento dos honorários e determinar o início dos trabalhos periciais.

## Decisão de Tutela Provisória

Competência JEF/PJEC incidental à tutela: reconhecer competência do JEF adjunto pode entrar na deliberação; alteração de fluxo é providência operacional, não alínea autônoma, salvo orientação expressa.

### Concessiva
> **(b)** **DEFIRO** a tutela provisória de urgência, nos termos do art. 300 do Código de Processo Civil, para determinar [comando específico] [...]
> **(a.1)** [prazo de cumprimento], sob pena de multa diária [...] limitada, a princípio, em R$ [valor].

Confirmação em definitivo (ações de saúde):
> **(a)** **ACOLHO** os pedidos [...] confirmando em definitivo a tutela provisória de urgência concedida (Id. [...]).
> **(a.2)** Fica mantida a contracautela fixada na tutela provisória: o autor deverá apresentar, a cada 6 (seis) meses, receita e relatório médicos atualizados [...], sob pena de cessação da eficácia da ordem judicial, condicionada à deliberação deste Juízo.

Tutela de evidência (art. 311, IV):
> **(b)** **CONCEDO** a tutela provisória de evidência, na forma do art. 311, inc. IV, do Código de Processo Civil, determinando à [ré] que a providência indicada no item "a" seja realizada no prazo de 30 (trinta) dias, contados da intimação desta sentença, sob pena de multa a ser fixada por este juízo.

### Denegatória
> **(a)** **INDEFIRO** a tutela provisória pleiteada.

Com reserva de reanálise após contraditório:
> **(a)** **indeferir**, por ora, a tutela provisória de urgência, sem prejuízo de reanálise após o contraditório;

**Providências de impulso pós-tutela em fase de conhecimento (padrão muito estável, aparece tanto na concessão quanto na denegação)**:
> **(i)** **intimar** a parte autora desta decisão;
> **(ii)** **expedir** o necessário para intimar em tempo hábil a parte ré sobre a tutela provisória concedida; [só se concedida]
> **(iii)** **citar** a parte ré e **intimá-la** a oferecer contestação no prazo legal;
> **(iv)** havendo arguição de preliminares ou prejudiciais, defesa indireta ou juntada de documentos inéditos, **abrir vista** ao autor pelo prazo de 15 (quinze) dias;
> **(v)** por fim, **concluir** os autos para decisão ou, não havendo especificação de novas provas, para julgamento.

PJEC/JEF após tutela inicial:
> **(i)** **incluir** a tramitação dos autos em segredo de justiça; [se aplicável]
> **(ii)** **alterar** o fluxo processual para PJEC; [se competência JEF adjunto reconhecida]
> **(iii)** **intimar** a parte autora desta decisão;
> **(iv)** **citar** a UNIÃO e **intimá-la** para apresentar contestação no prazo de 30 (trinta) dias;
> **(v)** apresentada contestação com preliminares, prejudiciais, defesa indireta ou documentos inéditos, **abrir vista** à parte autora pelo prazo de 10 (dez) dias;
> **(vi)** por fim, **concluir** os autos para decisão ou, não havendo especificação de novas provas, para sentença.

Rito de Juizado Especial (CEJUC):
> **(ii)** **citar** os réus e, em seguida, encaminhar os autos ao CEJUC para tentativa de conciliação, observando-se, no caso de não haver autocomposição, o prazo de 15 (quinze) dias para oferecimento da contestação, contados da audiência.

Dispensa de audiência de conciliação (rito comum que não admite autocomposição, ex. contra a Fazenda Pública) → ver `circunstancias.md`.

## Despacho de mero expediente / instrução

Só PROVIDÊNCIAS DE IMPULSO PROCESSUAL, sem DELIBERAÇÃO JUDICIAL própria, quando não há juízo decisório:
> ## **PROVIDÊNCIAS DE IMPULSO PROCESSUAL**
> A Secretaria deverá:
> **(i)** **arquivar** os autos com as formalidades de praxe.
> [LOCALIDADE/UF], data de assinatura do sistema.

Emenda de inicial:
> **(i)** **intimar** a parte autora para que, no prazo de [N] dias, emende a petição inicial, [especificação dos documentos/esclarecimentos exigidos, numerados], sob pena de indeferimento da petição inicial, nos termos do art. 321, parágrafo único, do Código de Processo Civil.
> **(ii)** cumpridas as diligências, **concluir** novamente os autos para decisão.

Remessa à Contadoria/NUCOD/SECAJ (cumprimento de sentença):
> **(i)** **remeter** os autos à Contadoria Judicial para cálculo do valor devido conforme os parâmetros do título executivo [...] e, no que forem silentes, o Manual de Cálculos da Justiça Federal em vigor.
> **(ii)** concluída a conta, **abrir vista** às partes pelo prazo de 15 (quinze) dias;
> **(iii)** decorrido o prazo, com ou sem manifestação, **concluir** os autos para deliberação.

## Embargos de Declaração

Ver também `minutar-embargos/assets/template-fundamentacao.md` (Blocos 5-6, com regras específicas de caixa do verbo já alinhadas a esta skill).

Rejeição (padrão dominante):
> Diante do exposto, **REJEITO** os embargos de declaração opostos [pela autora/pelo réu] (Id. [nº]), nos termos da fundamentação.

Variante processual (dois verbos):
> Diante do exposto, **CONHEÇO** dos embargos de declaração de Id. [...], mas **NEGO-LHES PROVIMENTO**, nos termos da fundamentação.

Não conhecimento:
> Diante do exposto, **NÃO CONHEÇO** dos embargos declaratórios de Id. [...], porquanto intempestivos.

Acolhimento com modificação parcial:
> Diante do exposto, **ACOLHO** os embargos de declaração opostos pela [parte] (Id. [nº]), para corrigir erro material na sentença embargada, com modificação parcial do resultado, estabelecendo que [novo comando corrigido], mantidos os demais parâmetros fixados na sentença.

**Providências de impulso características**:
> **(i)** **intimar** as partes desta [decisão/sentença] [integrativa];
> **(ii)** **cumprir**, no que restar, o disposto na [sentença/decisão] de Id. [nº do ato embargado], observando o disposto no art. 1.026 do CPC.

Nota: "[decisão/sentença] integrativa" é o termo recorrente para designar o ato que resolve os embargos — as providências remetem ao cumprimento "no que restar" (não reabre cumprimento já realizado, só o suspenso pela interrupção do prazo).

## Decisão Interlocutória Geral

Alta heterogeneidade de objeto; forma idêntica às demais: `Diante do exposto, **DECIDO**:` + alíneas (a)(b)(c) + providências em romanos.

**Impugnação ao cumprimento de sentença — rejeitada/homologação**:
> **(a)** **ACOLHER** a impugnação ao cumprimento de sentença apresentada pelo [executado] (Id. [nº]), e **HOMOLOGAR** o valor de R$ [...], já depositado judicialmente [...], como suficiente para satisfação da verba honorária executada nestes autos.

**Impugnação — acolhida em parte**:
> **(a)** **ACOLHER PARCIALMENTE** as impugnações apresentadas pelos réus e pelo [órgão], apenas para arbitrar os honorários periciais em R$ [...];

Impugnação com múltiplas teses (aplica a exceção de preliminares/prejudiciais de `estrutura.md`):
> **(a)** **REJEITAR** a impugnação à gratuidade da justiça; **(b)** **REJEITAR** a preliminar de ilegitimidade ativa; **(c)** **REJEITAR** a prejudicial de prescrição; **(d)** ... [mérito remanescente]

Remessa de competência (ilegitimidade passiva de ente federal):
> **(a)** **DECLARO** a ilegitimidade passiva de [ré federal] e, por consequência, **DETERMINO** a restituição dos autos à [Vara/Comarca de origem], nos termos do art. 45, § 3º, do Código de Processo Civil, e do art. 109, inc. I, da Constituição da República.

Restituição de ação principal à Justiça Estadual após julgamento de oposição:
> **(f)** **DETERMINO** que, após o trânsito em julgado, seja a ação principal nº [...] restituída ao Juízo Estadual de origem, diante da improcedência da oposição deduzida pela autarquia federal e da inexistência de causa remanescente de competência da Justiça Federal, nos termos do art. 45, § 3º, do Código de Processo Civil, e da Súmula 224 do Superior Tribunal de Justiça.
