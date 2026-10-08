---
created: 2026-10-08
updated: 2026-10-08
ai-agent: "Codex CLI"
---

# TEMPLATE - SANEAMENTO

> [!attention] ATENÇÃO:
> - Linhas iniciadas com "//" são instruções importantes. Leia-as atentamente.
> - Tags pseudo-XML, como <se/>, <loop/>, <exemplo-output>, devem ser interpretadas como meta-instruções específicas - delimitação contextual, iteração, execução condicional, entre outras. Não as interprete como texto final.

<template-saneamento>

## **CONSIDERAÇÕES INICIAIS**

// Parágrafo padrão. Deve ser transcrito de forma literal em todas as minutas de saneamento:

Nos termos do art. 357, do Código de Processo Civil, encerrada a fase postulatória e não estando o feito maduro para sentença, deverá o juízo, em decisão de saneamento e organização do feito: (i) resolver as questões processuais pendentes; (ii) delimitar as questões de fato sobre as quais recairá a atividade probatória; (iii) definir a distribuição do ônus da prova, observado o disposto no art. 373, do CPC; (iv) delimitar as questões de direito relevantes para a decisão de mérito; e (v) designar, se necessário, audiência de instrução e julgamento.

Passo doravante a apreciar cada um dos pontos.

## **QUESTÕES PROCESSUAIS PENDENTES**

[...]

[Superadas as questões acima/não havendo questões preliminares ou prejudiciais a serm apreciadas], **declaro** saneado o processo.

## **FIXAÇÃO DE CONTROVÉRSIAS**

### CONTROVÉRSIAS DE FATO

// Síntese das controvérsias de fato, extraídas do conjunto postulatório. Deve-se, inicialmente, trazer o contexto, com as narrativas de cada parte e, em seguida, destacando o que é controvertido e o que não o é.

<exemplo-output>

Conforme relatado, o autor afirma que trafegava em velocidade regular na Rodovia BR-153, no momento em que, surpreendido por um buraco na pista, não conseguiu desviar e capotou o carro, causando danos morais e materiais.

A autarquia ré, por sua vez, afirma que o autor deu causa ao acidente, pois, de acordo com registros da pista, trafegava em velocidade acima da permitida e com faróis de milha desligados.

Portanto, a controvérsia instaurada durante o conjunto postulatório cinge-se à regularidade, ou não, do veículo e da forma de sua condução no momento do acidente, o que, a princípio, pode caracterizar a culpa concorrente ou exclusiva da vítima, com ruptura do nexo causal.

Por outro lado, não há controvérsia sobre a ocorrência do acidente, o dano moral ou o prejuízo material narrado pelo autor. Trata-se de fatos incontroversos.

</exemplo-output>

// Se a lista dos pontos fáticos de cada narrativa for extensa (> 3), prefira adotar formato de lista, com números romandos minúsculos como marcadores. Ex: (i) ...; (ii) ...;

// ATENÇÃO: nesta seção, devem ser delimitadas apenas as **questões de fato**, ou seja, de narrativa factual, não sendo o espaço adequado para delimitação das controvérsias jurídicas.

### CONTROVÉRSIAS DE DIREITO

// Síntese das **questões jurídicas** levantadas a partir das controvérsias. Não é necessário contextualização, já que o juiz tem certa liberdade de fazer o enquadramento dos fatos na moldura jurídica que entender mais adequada (*iura novit curia*).

// Deve iniciar com o seguinte parágrafo-padrão:

As controvérsias de direito podem ser delimitadas, a partir do quadro fático, da seguinte forma: ...; 

// Ao listar as questões jurídicas, prefira fazê-lo em parágrafo corrido, sem lista com quebras de linha. Seja sucinto e objetivo, apenas levantando a questão, sem maiores explicações. Por exemplo:

<exemplo-output>

... da seguinte forma: aplicação, no caso, da responsabilidade objetiva estatal ou da responsabilidade subjetiva; se, diante dos fatos, há ou não ruptura do nexo causal suficiente para afastamento da responsabilidade; dosimetria de eventual indenização. 

</exemplo-output>

## **ATIVIDADE PROBATÓRIA**

### DISTRIBUIÇÃO DO ÔNUS DA PROVA


### DILAÇÃO PROBATÓRIA

// Em caso de deferimento de perícia, usar a seção apenas para fundamentar a utilidade/necessidade da prova e indeferir provas inadequadas. O detalhamento operacional da perícia deve ficar na DELIBERAÇÃO JUDICIAL e nas PROVIDÊNCIAS DE IMPULSO PROCESSUAL.

Para o esclarecimento das questões de fato, entendo útil e relevante a produção de [prova pericial], consistente na [descrição objetiva da perícia], bem como [objeto da perícia].

[Fundamente a pertinência da prova técnica, relacionando-a às controvérsias de fato e aos documentos já produzidos, sem antecipar juízo de mérito.]

[Indefira, se for o caso, prova testemunhal, depoimento pessoal ou outra prova inadequada à controvérsia técnica, explicando a inadequação.]

## **DELIBERAÇÃO JUDICIAL**

Ante o exposto, **DECIDO**:

**(a)** **RESOLVER** as questões processuais pendentes e declarar saneado o feito;

**(b)** **FIXAR** as controvérsias de fato e de direito conforme disposto na fundamentação;

**(c)** **MANTER** a distribuição do ônus da prova nos termos do art. 373, inc. I e II, do Código de Processo Civil, incumbindo à parte autora a demonstração dos fatos constitutivos de seu direito e à parte ré a comprovação de eventuais fatos impeditivos, modificativos ou extintivos;

// Em caso de deferimento de perícia, utilizar este padrão. Há dois fluxos possíveis a partir do item (d), mutuamente exclusivos, conforme a parte pleiteante da prova seja ou não beneficiária da gratuidade da justiça. Use apenas o bloco SE CONDICAO aplicável ao caso — não misture os dois.

**(d)** **DEFERIR** a produção de **perícia [tipo da perícia]**, para [objeto da perícia];

<SE CONDICAO="parte pleiteante da perícia NÃO é beneficiária da gratuidade da justiça — nomeação direta de perito">

**(d.1)** para tanto, **NOMEIO** como perito [NOME DO PERITO] ([registro profissional]), cuja qualificação é conhecida por esta Secretaria;

**(d.2)** esclareço que os honorários periciais deverão ser integralmente adiantados pela parte [autora/ré], que pugnou pela produção da prova;

**(d.3)** fica, desde já, autorizado o levantamento de 50% (cinquenta por cento) dos honorários arbitrados no início do trabalho; o restante será pago após a entrega do laudo e prestados os esclarecimentos pertinentes;

**(d.4)** o laudo deverá ser entregue no prazo de 10 (dez) dias, contados do início da perícia;

**(d.5)** apresento os seguintes quesitos do Juízo, que deverão ser respondidos pelo perito, sem prejuízo dos quesitos a serem apresentados pelas partes:

*(d.5.1) [Quesito judicial 1, formulado de modo a cobrir diagnóstico, fato ou circunstância técnica central.]* 

*(d.5.2) [Quesito judicial 2, formulado de modo a cobrir nexo, necessidade, suficiência ou adequação técnica.]* 

*(d.5.3) [Quesito judicial 3, formulado de modo a cobrir observações técnicas relevantes, urgência, duração, periodicidade, provisoriedade ou esclarecimentos complementares.]* 

</SE>

<SE CONDICAO="parte pleiteante da perícia é beneficiária da gratuidade da justiça — perícia custeada e designada via NUCOD, sem nomeação direta de perito pelo Juízo">

// Ver `assets/exemplos/ex-contrato-bancario-anatocismo-pericia-ajg.md` para calibrar este fluxo.

**(d.1)** considerando que a parte demandante é beneficiária da gratuidade processual, **FIXO** os honorários periciais no valor máximo da tabela editada pelo Conselho da Justiça Federal (Resolução nº 305/2014), devendo o pagamento ser efetuado nos termos da Lei nº 14.331 de 04/05/2022 e **MAJORO-OS** ante a complexidade da causa evidenciada pelos seguintes fatores: i) a ação não tramita no Juizado Especial, o que exige maior cuidado em razão do elevado valor envolvido; ii) as partes costumam formular quesitos específicos e não padronizados; iii) necessidade de o perito examinar vários aspectos sobre a doença, incapacidade, grau, permanência, data de início, data da cessação, necessidade de assistência de terceiros, anamnese da parte, cotejo de documentação laudos e exames médicos, resposta aos inúmeros quesitos das partes, elaboração de laudo, eventual resposta a impugnação, etc., nos termos do artigo 28, § 2º, I, III e IV, da Resolução 305/2014-CJF e Portaria NUCOD/TO nº 001, de 05/04/2024 para fixar o valor definitivo em **R$ 340,00 (trezentos e quarenta reais)**.

**(d.2)** **DETERMINO** a remessa dos autos ao NUCOD para designação da perícia;

**(d.3)** **FORMULO**, desde já, os seguintes quesitos do Juízo, que deverão ser respondidos pelo(a) perito(a), sem prejuízo dos quesitos a serem eventualmente apresentados pelas partes:

*(d.3.1) [Quesito judicial 1, formulado de modo a cobrir diagnóstico, fato ou circunstância técnica central.]* 

*(d.3.2) [Quesito judicial 2, formulado de modo a cobrir nexo, necessidade, suficiência ou adequação técnica.]* 

*(d.3.3) [Quesito judicial 3, formulado de modo a cobrir observações técnicas relevantes, urgência, duração, periodicidade, provisoriedade ou esclarecimentos complementares.]* 

</SE>

**(e)** **INDEFERIR** [prova indeferida], por [fundamento sintético de inadequação, inutilidade ou desnecessidade].

## **PROVIDÊNCIAS DE IMPULSO PROCESSUAL**

A Secretaria deverá:

<SE CONDICAO="nomeação direta de perito — fluxo não-AJG">

**(i)** **intimar** as partes sobre esta decisão e para que, no prazo de 5 (cinco) dias, manifestem eventuais causas de impedimento ou suspeição do perito, indiquem assistentes técnicos e apresentem quesitos;

**(ii)** com a manifestação das partes, não havendo impugnação quanto à nomeação, **intimar** o perito para, no prazo de 5 (cinco) dias, dizer se aceita o encargo e, se for o caso, apresentar proposta de honorários;

**(iii)** aceito o encargo e apresentada a proposta de honorários, **intimar** as partes para manifestação no prazo de 5 (cinco) dias;

**(iv)** por fim, **concluir** os autos para arbitramento dos honorários e determinar o início dos trabalhos periciais.

</SE>

<SE CONDICAO="perícia via NUCOD — fluxo AJG">

**(i)** **intimar** as partes desta decisão e para que, caso queiram, apresentem quesitos e indiquem assistentes técnicos no prazo de 5 (cinco) dias;

**(ii)** após, com ou sem quesitos, **encaminhar** os autos ao NUCOD para designação da perícia;

**(iii)** com a apresentação do laudo, **abrir vista** às partes pelo prazo comum de 15 (quinze) dias e, em seguida, **concluir** os autos para julgamento.

</SE>
