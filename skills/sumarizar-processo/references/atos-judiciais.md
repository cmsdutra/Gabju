# Atos Judiciais

São atos judiciais:
- Despacho
- Sentença
- Decisão
- Acórdão relativo ao processo
  - Inclusive o veiculado em ofício do Tribunal
  - Excluem-se os acórdãos juntados pelas partes como reforço argumentativo

# Saída

```markdown

# ATOS JUDICIAIS

<loop condição="cada ato judicial" ordem="crescente de id.">

## [TIPO] - [ID]

**Aspectos Gerais:**
- ID do ato: [ID atribuído ao ato judicial no processo]
- Tipo: [saneamento/tutela provisória/julgamento de embargos/sentença/decisão interlocutória geral]
- Data: [DD-MM-AAAA]
- Órgão Prolator: [Juízo de 1º Grau/Turma Recursal/Decisão Monocrática de Relator/Turma/Seção/Plenário/Corte Especial]
- Magistrado Prolator: [nome do magistrado]
- Petição(ões) de Origem: [Petições referenciadas no ato como base decisória - idetificar ID e tipo de petição]
- Carga Decisória: [efeitos da decisão no processo: extintiva (total ou parcial)/resolutiva (total ou parcial)/suspensiva/outro]
- Classificação: [mérito/processual/misto]
---
**Fundamentos:**
- Endeamento Argumentativo: 
    `detalhamento logicamente encadeado de **todos** os fundamentos jurídicos utilizados na decisão para a deliberação da(s) questão(ões). No caso de decisões complexas (decisões de múltiplas questões), como decisão de saneamento e organização do processo, sentença ou tutela provisória, divida em tópicos os argumentos de cada seção decisória.`
    - [argumento 1]
    - [argumento 2]
    - ... `7 a 15 blocos argumentativos completos, se TIPO for sentença, acórdão, tutela provisória ou decisão de saneamento; e de 3 a 7 blocos argumentativos completos, se TIPO for decisão interlocutória geral, despacho ou outro ato simples`
    - [argumento n] 
    `IMPORTANTE: se o ato judicial for uma decisão de saneamento e organização do feito: CRIE mais dois subtópicos dentro da seção "Fundamentos": - Controvérsias de Fato e de Direito: transcrever literal e integralmente os parágrafos da decisão que delimitam as controvérsias; e - Prova Deferida: transcrever literal e integralmente o trecho da decisão que trata da prova deferida.`
- Ratio decidendi: 
    `identifique o enunciado jurídico abstrato que serve de base à decisão, e que poderia ser aplicado como precedente para outros atos → a ratio decidendi. Se o ato não for decisório (como despacho ou ato ordinatório, apenas registre "não se aplica")`
- Conclusão decisória: 
    `descreva de forma sintética o desfecho prático atribuído ao caso. Exemplo: "deferiu a tutela provisória para..." ou "saneou o feito, afastando as preliminares de ..., delimitou as questões controvertidas..." ou "acolheu os pedidos formulados na petição inicial...`
- Precedentes jurisprudenciais citados:
    `lista dos precedentes jurisprudenciais citados no ato, se houver`
- Dispositivos legais citados:
    `lista dos dispositivos legais citados no ato, se houver`
---
**Conclusão:**
- Dispositivo:
    `transcrever, de forma literal, completa e detalhada, todas as deliberações contidas no dispositivo do ato (os provimentos jurisdicionais)`
    - [deliberação 1]
    - ...
    - [deliberação n]
---
**Síntese:**
- Síntese técnica:
    - `resumo técnico do ato de até 150 palavras`
- Palavras-chave: `listar, em um único parágrafo, separadas por vírgula e espaço, de 5 a 10 (em função da complexidade do ato) palavras-chave`
-----
</loop>

```

# ORIENTAÇÕES GERAIS
- Não apresente justificativas, apenas o conteúdo organizado.
- Se algum dado não for localizado, registrar "não localizado".
- Mantenha máximo rigor técnico e clareza textual.
- Atenção especial à fidelidade ao ato judicial original.
- Evitar qualquer narrativa de fatos ou histórico processual fora do encadeamento jurídico.
- [!ATENÇÃO]: Decisão de Saneamento exige tratamento especial! Verifique obrigatoriamente se as controvérsias e a prova deferida estão transcritas literalmente.