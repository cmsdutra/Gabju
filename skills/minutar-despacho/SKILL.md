---
name: minutar-despacho
description: Redige minutas de despacho judicial com providências de impulso processual e eventual fundamentação breve. Use para redigir/elaborar/preparar/minutar despacho, inclusive quando for preciso obter direcionamentos antes da redação.
---

# /despacho

## Personalização

Leia [personalização do gabinete](../../references/personalizacao.md) ao aplicar convenções ou preencher dados institucionais e fechamento: use a personalização do ChatGPT disponível no contexto; dados ausentes recebem placeholders padrão.

## Leitura dos anexos

Quando precisar consultar anexos, tente primeiro a leitura direta. Se houver dificuldade concreta que impeça acessar o conteúdo necessário, acione $indexar-pdf somente para os PDFs afetados, informando a dificuldade observada. Tamanho e quantidade de páginas isolados não justificam indexação. Reutilize os textos recuperados e os diagnósticos ao retomar esta skill, preservando seu escopo e checkpoints.

Redigir minuta de despacho judicial a partir das peças processuais anexadas e das orientações fornecidas pelo usuário na conversa ou em arquivo anexo.

## Fluxo obrigatório

1. Identificar o processo e o conjunto de documentos anexados.
   - Se houver documentos de mais de um processo, pedir ao usuário que indique qual deve ser trabalhado.

2. Ler as orientações fornecidas na conversa ou em arquivo anexo antes das peças.
   - Tratar as orientações expressas do usuário como prioritárias sobre as regras gerais da skill, salvo incompatibilidade com limite legal, factual ou de segurança.
   - Se não houver orientação suficiente, interromper a redação e perguntar objetivamente qual providência judicial se pretende determinar.

3. Ler o estilo.
   - Ler sempre `references/style.md` antes de redigir.

4. Consultar os recursos da skill.
   - Usar `assets/template.md` como estrutura-base obrigatória da minuta.
   - Ler os exemplos em `references/examples/` antes de redigir:
     - `simples.md`, para despachos de mero impulso, com contextualização breve e sem fundamentação autônoma.
     - `detalhado.md`, para despachos que exigem contexto processual mais robusto, análise preliminar ou explicação das razões da providência.
   - Adaptar a extensão da minuta ao caso concreto e às orientações do usuário; não copiar fatos, nomes, IDs ou providências dos exemplos.

5. Examinar as peças processuais necessárias.
   - Quando os anexos incluírem `index.json` e arquivos segmentados em `textos/`, usar o índice para selecionar as peças relevantes.
   - Priorizar peças principais e atos recentes que expliquem a providência de impulso: petições pendentes, decisões anteriores, certidões, manifestações, atas e documentos indispensáveis à providência.
   - Ignorar documentos meramente instrutórios quando não forem necessários para entender a providência.
   - Referência a `Id.`: petição inicial não recebe Id. no texto; demais peças/atos recebem Id. só na 1ª referência da minuta. Depois, referir por função processual ("a decisão", "a manifestação", "o documento"), salvo necessidade de desambiguação ou comando operacional dirigido ao documento.

6. Redigir a minuta.
   - Usar o título `# **DESPACHO**`.
   - Incluir `## **SITUAÇÃO ATUAL DO PROCESSO**` com resumo conciso do objeto relevante e do estado atual dos autos.
   - Incluir `## **FUNDAMENTOS**` somente quando a providência exigir justificativa, análise preliminar, exposição de motivo, ou quando o usuário pedir expressamente.
   - Incluir `## **PROVIDÊNCIAS DE IMPULSO PROCESSUAL**` com comandos claros à Secretaria da Vara. Consulte `minutar-dispositivo/references/catalogo-especies.md` § Despacho de mero expediente/instrução para os padrões recorrentes (arquivamento, emenda de inicial, remessa à Contadoria/NUCOD) e `minutar-dispositivo/references/estrutura.md` para a regra de numeração/caixa do verbo.
   - Formular providências em lista com numerais romanos minúsculos entre parênteses, com o verbo operacional em negrito e caixa baixa no início de cada item. Evite repetir deliberação já feita em decisão anterior; se a providência anterior ainda não tiver sido cumprida, referencie-a apenas nesta seção.
   - Encerrar com `[LOCALIDADE/UF], data do sistema.` salvo orientação diversa do usuário ou template específico.

7. Entregar a minuta.
   - Entregar o texto completo em Markdown no chat, pronto para copiar.
   - Se o ambiente permitir arquivo para download, usar `<13-primeiros-digitos-do-processo>.md`; na falta do número, usar `Despacho.md`.
   - Se o usuário anexar minuta preexistente e pedir integração, preservar o conteúdo não abrangido e inserir ou substituir apenas o despacho.

## Critérios de redação

- Priorizar concisão. Despacho não é sentença nem decisão interlocutória extensa.
- Explicitar apenas o contexto necessário para justificar o impulso processual.
- Não resolver mérito, tutela provisória, saneamento ou embargos de declaração se o ato pedido for mero despacho; se a providência exigir decisão, avisar o usuário e usar a skill adequada quando aplicável.
- Não inventar fatos, IDs, datas, valores, providências já cumpridas ou fundamentos legais.
- Não citar jurisprudência ou doutrina, salvo se o usuário fornecer expressamente ou se constar do template aplicável.
- Quando faltar dado essencial para determinar uma providência, perguntar ao usuário ou registrar a providência como diligência para obtenção do dado.
- Nunca fazer referência, no texto do despacho, a instruções da conversa, notas de orientação ou modelos consultados; incorporar a orientação como fundamento ou providência autônoma.

## Quando perguntar ao usuário

Perguntar antes de redigir quando:

- não houver orientação suficiente na conversa ou nos anexos;
- não for possível identificar a providência pretendida;
- houver conflito entre a orientação do usuário e as peças processuais;
- a providência pretendida exigir escolha jurídica relevante não indicada pelo usuário.

Havendo consulta prévia sobre a providência judicial, apresente antes da minuta um registro auditável conciso com a questão consultada e a deliberação adotada. Não incorpore esse registro ao texto do ato.

A pergunta deve ser curta e prática. Exemplo: `Qual providência o despacho deve determinar e há algum fundamento específico que deseja adotar?`
