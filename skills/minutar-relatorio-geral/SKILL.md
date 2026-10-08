---
name: minutar-relatorio-geral
description: Redige relatórios de minutas de decisões e sentenças no padrão da Justiça Federal, a partir das peças fornecidas. Use para redigir/elaborar/produzir relatório de minuta de decisão, despacho ou sentença. NÃO usar para embargos de declaração nem despacho (skills próprias).
---

# /minutar-relatorio-geral

## Personalização

Leia [personalização do gabinete](../../references/personalizacao.md) ao aplicar convenções ou preencher dados institucionais e fechamento: use a personalização do ChatGPT disponível no contexto; dados ausentes recebem placeholders padrão.

## Leitura dos anexos

Quando precisar consultar anexos, tente primeiro a leitura direta. Se houver dificuldade concreta que impeça acessar o conteúdo necessário, acione $indexar-pdf somente para os PDFs afetados, informando a dificuldade observada. Tamanho e quantidade de páginas isolados não justificam indexação. Reutilize os textos recuperados e os diagnósticos ao retomar esta skill, preservando seu escopo e checkpoints.

Esta skill permite a redação de relatórios de minutas de despachos, decisões e sentenças judiciais, no padrão adotado na unidade judiciária.

---

## Fluxo de Execução

### Passo 1 — Identificar o tipo de minuta

Antes de redigir qualquer conteúdo, identifique para qual tipo de minuta será o relatório: 

1. Sentença ou Saneamento
2. Tutela provisória (urgência ou evidência)
3. Decisão interlocutória

Essa classificação segue um agrupamento por nível de detalhamento factual (ex: relatorio de sentença é mais detalhado que o de decisão interlocutória comum) e foco da abordagem (decisões de tutela provisória de urgência têm foco na descrição da urgência e da tutela provisória pretendida, em detrimento da tutela de mérito final).

Preferencialmente, o tipo de minuta estará identificado em um arquivo de metadados da tarefa (campo `task` do frontmatter). Se não houver a informação em um arquivo de metadados da tarefa (método preferencial), faça a pergunta diretamente ao usuário.

> [!warning] **Não inicie a redação sem a identificação adequada do tipo de minuta.**

### Passo 2 — Coletar o material processual

Confirme quais peças foram fornecidas (petição inicial, contestação, réplica, decisões anteriores, acórdão de recurso etc.). Se faltar material essencial para descrever algum ato processual relevante, avise o usuário em vez de especular.

> [!attention] As peças a serem utilizadas no relatório são as principais, que marcam a condução do fluxo processual (petições, decisões, atas de audiência, informação da juntada de laudo etc.). Os documentos de mera instrução (como os anexos das petições, conteúdo do laudo e dos depoimentos) devem ser ignorados para o relatório.

### Passo 3 — Redigir o relatório

Siga rigorosamente as regras de estilo descritas em `references/estilo.md` e o template selecionado em `assets/templates/`. O relatório é entregue como texto corrido, sem headers, títulos de seção, separadores ou qualquer outra marcação estrutural visível (salvo o título "# RELATÓRIO"). As divisões do template são fases narrativas internas, para orientar a redação, não seções do documento final.

### Passo 4 - Revisar

Após a entrega do relatório, faça uma revisão do texto, observando os seguintes parâmetros:
- [ ] O texto obedece as regras estruturais do template?
- [ ] O texto obedece as regras de estilo (`estilo.md`)?
- [ ] O texto contém algum erro gramatical?
- [ ] O texto obedece as limitações absolutas desta skill?

Evite ser verboso na revisão; faça análise direta e concisa.

---

## Limitações Absolutas

- Não crie, extrapole, parafraseie ou invente informações além do que foi fornecido.
- Não realize pesquisas externas de jurisprudência, doutrina ou legislação.
- Não cite jurisprudência (precedentes, súmulas, decisões) a menos que o usuário tenha fornecido o texto completo ou a identificação exata (número do processo, tribunal e ementa).
- Não informe a data de protocolo de petições ou atos judiciais, salvo se for relevante para a solução da controvérsia.
- Nunca questione o usuário se deseja que redija a fundamentação ou o dispositivo. *A função desta skill é exclusivamente o relatório*.
- Nunca faça referência, no texto do relatório, a instruções da conversa, notas de orientação ou modelos consultados; incorpore a orientação como narrativa processual adequada.

---

## Arquivos de referências

- `references/estilo.md` — Regras de estilo e formatação. **Leia antes de redigir qualquer conteúdo.**
- `assets/exemplos/*.md` — Exemplos reais de relatórios por tipo de minuta. Consulte para calibrar o nível de detalhe, o estilo narrativo e a formatação esperados, de acordo com a dinâmica definida em `references/estilo.md`.
- `assets/templates/*.md` - Templates
