---
name: esp-direito-sanitario
description: Analisa e minuta atos de direito sanitário sobre SUS, medicamentos, tratamentos, ANVISA, CONITEC e NATJUS. Use em decisões, sentenças, tutelas e despachos sobre prestações de saúde pública.
---

# Direito Sanitário

## Leitura dos anexos

Quando precisar consultar anexos, tente primeiro a leitura direta. Se houver dificuldade concreta que impeça acessar o conteúdo necessário, acione $indexar-pdf somente para os PDFs afetados, informando a dificuldade observada. Tamanho e quantidade de páginas isolados não justificam indexação. Reutilize os textos recuperados e os diagnósticos ao retomar esta skill, preservando seu escopo e checkpoints.

## Uso Obrigatório

Use esta skill sempre que a tarefa envolver fornecimento judicial de medicamento, tratamento, procedimento, cirurgia, insumo, produto de saúde, home care ou tecnologia em saúde pelo SUS.

Antes de minutar, leia os arquivos de referência necessários:

- `references/teses-stf.md`: sempre em demandas de saúde pública.
- `references/consultas-oficiais.md`: quando houver medicamento, tecnologia, PCDT, registro sanitário, preço ou incorporação ao SUS.
- `references/linhas-argumentativas.md`: sempre que houver minuta judicial de mérito ou tutela, para aplicar as linhas argumentativas de referência incluídas no pacote, sujeitas à adequação ao caso.
- `references/boilerplates.md`: quando precisar redigir fundamentação ou dispositivo.

## Fluxo de Análise

1. Identifique o objeto: medicamento, tratamento/procedimento, insumo, home care ou tecnologia não medicamentosa.
2. Classifique a tecnologia:
   - incorporada ao SUS;
   - não incorporada, mas registrada na ANVISA;
   - sem registro na ANVISA;
   - sem registro, mas com importação excepcional autorizada;
   - tratamento/procedimento médico sem recorte de medicamento.
3. Verifique competência, legitimidade e direcionamento:
   - medicamentos não incorporados com registro na ANVISA: aplicar Tema 1234/STF e custo anual do tratamento;
   - tratamentos, cirurgias e serviços de saúde em geral: aplicar Tema 793/STF, salvo regra específica de medicamento;
   - medicamento incorporado: observar repartição administrativa do SUS, CEAF/Grupo, PCDT e atuação operacional local.
4. Exija base técnica antes de decidir tutela ou mérito, salvo urgência documentada e prova suficiente:
   - consultar NATJUS quando disponível;
   - usar perícia quando a controvérsia depender de estágio clínico, falha terapêutica, imprescindibilidade ou adequação ao PCDT;
   - dispensar perícia quando a questão central for controle de legalidade de ato da CONITEC já instruído e a prova médica não alterar o resultado.
5. Leia `references/linhas-argumentativas.md` e avalie a linha argumentativa mais próxima por medicamento, doença, tema e providência. Se o usuário anexar precedentes mais recentes, confronte-os com a referência empacotada e priorize a orientação atual validada.

## Pontos de Prova

Em medicamentos não incorporados, conferir cumulativamente:

- negativa administrativa;
- registro na ANVISA ou hipótese excepcional do Tema 1161/500;
- ato de não incorporação da CONITEC, ausência de pedido ou mora de apreciação;
- ilegalidade controlável no ato administrativo, quando houver negativa de incorporação;
- inexistência ou inadequação concreta de substituto no SUS/PCDT;
- evidência científica de alto nível;
- laudo médico fundamentado com diagnóstico, CID, histórico terapêutico, tratamentos já tentados, falhas/intolerâncias, posologia e urgência;
- incapacidade financeira;
- custo anual pelo PMVG/CMED ou parâmetro público mais econômico.

Em tratamentos/procedimentos, conferir:

- inserção no SISREG ou fluxo público equivalente;
- classificação de risco e tempo de espera;
- prova de mora administrativa injustificada;
- risco concreto por atraso;
- possibilidade de direcionar cumprimento ao ente com maior aptidão operacional.

## Estilo da Minuta

- Trate organização interna do SUS como parâmetro de direcionamento e execução, não como exclusão automática de responsabilidade.
- Em decisões contra ato da CONITEC, limite a análise ao controle de legalidade; não substitua avaliação técnico-econômica por preferência judicial.
- Em medicamentos incorporados mas ainda não disponibilizados, diferencie incorporação formal de oferta efetiva.
- Em procedência, fixe contracautelas proporcionais: prescrição atualizada, relatório periódico, dispensação parcelada, unidade pública, conservação adequada, devolução de doses não utilizadas e aquisição pelo menor preço público verificável.
- Em tutela, quando a prova técnica ainda for insuficiente, prefira despacho para NATJUS/perícia urgente em vez de deferimento automático.

## Atualidade das fontes

As linhas argumentativas em `references/linhas-argumentativas.md` são material de apoio, não precedente judicial citável por si. Antes de aplicar norma, tese vinculante, registro sanitário, incorporação ou preço, confira a fonte oficial indicada nas referências quando o ambiente oferecer acesso à web. Sem acesso, explicite qual dado atual precisa ser confirmado ou peça ao usuário o documento correspondente.
