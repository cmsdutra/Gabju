# Template e Estilo — Relatório Judicial

## Tom e Estilo Geral

- Técnica de **storytelling jurídico**: ênfase no conflito e na controvérsia a ser apreciada.
- Linguagem técnica, sem dramatização ou adjetivação excessiva.
- Neutralidade descritiva rigorosa.
- Tom técnico-formal com uso preciso dos conceitos jurídicos pertinentes.
- Cada parágrafo deve conter uma unidade de ideia, com transição fluída em relação ao parágrafo anterior.
- Priorização da fidelidade factual aos documentos fornecidos.
- **Nome das partes**: uso subsidiário. Apresente o nome apenas na primeira menção ou para desambiguar partes com a mesma função; depois prefira a função processual adequada ao momento (autor/réu/requerida/executada/exequente etc.). Se a função muda pela fase processual, acompanhe a fase, não repita o nome.
- **Denominação de manifestações das partes**: prefira denominações processuais simples e neutras, como "petição", em vez de qualificações como "petição intercorrente", salvo quando a qualificação específica for relevante para compreender o ato processual.
- **UNIÃO**: prefira "UNIÃO" a "UNIÃO FEDERAL" ao designar o ente federal como parte.
- **Referência temporal a atos**: use "anterior/posterior" só se a ordem temporal importar à narrativa; em regra, identifique o ato pelo Id. ("a tutela foi indeferida pela decisão de Id. ..." / "foi indeferida (Id. ...)").

---

## Formato do output

O relatório é **texto corrido**, e não se subdivide em seções ou com separador visual. 
Ressalvado o título do relatório ('# **RELATÓRIO**'), o modelo **não deve** inserir nenhum elemento de estrutura (como `##`, `###`, `---`, negrito em subtítulos, etc.) no texto final entregue ao usuário. 
Antes de redigir, consulte o **texto de exemplo** relacionado ao tipo de minuta para calibrar o nível de detalhe e o estilo narrativo esperados.

### Textos de Exemplo

Os textos de exemplo fornecidos são os seguintes:

| Nível de Detalhe | Tipos Comuns de Minuta (rol exemplificativo) | Arquivo de Referência |
| --- | --- | --- |
| Detalhado | Sentença, Saneamento, Tutela Provisória | `/assets/exemplos/ex-rel-completo.md` |
| Conciso | Interlocutórias comuns, despachos, decisão sobre incidentes processuais | `/assets/exemplos/ex-rel-conciso.md` |

Identifique o texto de exemplo utilizado de acordo com o tipo de minuta pretendido. Se houver dúvida, pergunte ao usuário antes de escolher. 

---

## Regras de Formatação

Status: IMPORTANTE. Se sobrepõem aos exemplos.

| Elemento | Regra |
|---|---|
| Nomes das partes | MAIÚSCULAS, sem negrito |
| Negrito | Vedado, salvo os previstos nos templates |
| Itálico | Somente para palavras e expressões estrangeiras |
| Números e valores | Numeral seguido do extenso entre parênteses — Ex.: `12 (doze) anos`, `R$ 2,00 (dois reais)`, `15% (quinze por cento)` |
| **Exceção** ao extenso | A regra geral de escrever por extenso NÃO SE APLICA a datas — nunca as transcreva por extenso. Valores inseridos em estruturas complexas (tabelas) também dispensam o extenso |
| Citações | Somente indiretas, incorporadas ao argumento (*inline*), sem aspas. Citação direta é vedada. |
| Id. dos atos | Todo ato processual citado (exceto petição inicial) deve ter o número de Id. indicado, mesmo em citação indireta |

---

## Regras por Tipo de Minuta

- **Despacho**: o relatório deve primar pela concisão.
- **Decisão interlocutória**: resuma decisões anteriores apenas na parte necessária para contextualizar a controvérsia pendente, evitando repetir histórico processual lateral já narrado no próprio ato anterior.
- **Tutela provisória**: concentre a descrição do pedido urgente e de seus fundamentos em parágrafo próprio, evitando repetir os mesmos pedidos no resumo final de mérito.
- **Pedidos da petição inicial** ("Ao final, requereu..."): seja conciso; foque nas providências requeridas, sem necessidade de citação dos fundamentos utilizados.
- **Argumentos jurídicos da petição inicial**: evite parágrafos muito longos; se o número de argumentos ultrapassar três, prefira utilizar lista, conforme especificado nos templates.
- **Juizado Especial Federal (JEF)**: o meio de impugnação da sentença é "recurso" ou "recurso inominado", julgado pela Turma Recursal — nunca "apelação", que é julgada pelo TRF-1.

## Template Estrutural

Selecione o template na pasta `/assets/templates/` que melhor se relacione com o caso em questão, observando o seguinte:

| Tipo de Minuta | Template |
| --- | --- |
| Sentença ou Saneamento | `t_sentenca.md` |
| Tutela provisória | `t_tutProv.md` |
| Interlocutória Geral | `t_interlocutoria.md` |

Selecione o template com maior correspondência se o tipo de minuta no caso concreto não corresponder exatamente a nenhum dos tipos de minuta pré-definidos acima.

> [!info] Ao ler o template, assuma que:
> - O texto iniciado com "//" são blocos de instrução. Leia-os atentamente e não os reproduza na resposta. 
> - o template utiliza tags pseudo-xml para instruções estruturais específicas (como <loop/>) e delimitação de contexto (como <exemplo/>). Não as exiba no texto final.
