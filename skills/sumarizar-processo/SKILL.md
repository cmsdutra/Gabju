---
name: sumarizar-processo
description: Classifica cada documento anexado (petição, ato judicial, documento auxiliar) e extrai dados estruturados fiéis ao original, sem inferências. Use somente quando o usuário pedir expressamente resumo, sumário ou extração estruturada dos documentos do processo; não use como etapa de minuta, relatório ou outra tarefa.
---

# /sumarizar-processo

## Leitura dos anexos

Quando precisar consultar anexos, tente primeiro a leitura direta. Se houver dificuldade concreta que impeça acessar o conteúdo necessário, acione $indexar-pdf somente para os PDFs afetados, informando a dificuldade observada. Tamanho e quantidade de páginas isolados não justificam indexação. Reutilize os textos recuperados e os diagnósticos ao retomar esta skill, preservando seu escopo e checkpoints.

O objetivo da skill é identificar o tipo de documento submetido e aplicar, com rigor absoluto, o modelo de análise correspondente, conforme os templates de referência em `references`.

---

# LEITURA

## CLASSIFICAÇÃO DO DOCUMENTO
Antes de iniciar a análise, classifique os documentos anexados em uma das três categorias abaixo, com base em seus elementos internos, linguagem e estrutura:
    1. **Petições** (ex: iniciais, contestações, réplicas, embargos, alegações finais etc.)
    2. **Atos Judiciais** (ex: decisões interlocutórias, sentenças, despachos, acórdãos, decisões monocráticas)
    3. **Documentos Auxiliares** (ex: laudos, certidões, pareceres, relatórios, requerimentos administrativos)

---

# EXTRAÇÃO E ANÁLISE

Faça a extração dos dados processuais, **passo a passo**, na seguinte ordem: petições → atos judiciais → documentos auxiliares.

## PARÂMETROS DE GERAÇÃO

Ao fazer a extração dos dados, use (simule) os seguintes parâmetros de geração:
    1. `temperature` = 0.1 → gere de forma quase determinística, com mínima variação.
    2. `top_p` = 0.2 → limite o vocabulário às expressões mais prováveis e precisas.
    3. `frequency_penalty` = 0.0 → não penalize repetições formais, se exigidas pela estrutura.
    4. `presence_penalty` = 0.0 → não incentive inclusão de novas ideias, apenas reflita o conteúdo.

Esses valores buscam garantir estabilidade e precisão para tarefas de extração de dados estruturados. 

### EXCEÇÕES OPERACIONAIS

| Situação | Ajuste |
| ----- | ----- |
| Documento com pouca legibilidade ou mal formatado | `top_p` = 0.5 |
| Geração de resumos ou sínteses | `temperature` = 0.3, `top_p` = 0.8 e `frequency_penalty` = 0.2 |

---

| Classe | Arquivo de referência |
| --- | --- |
| Atos Judiciais | `references/atos-judiciais.md` |
| Petições | `references/peticoes.md` |
| Documentos Auxiliares | `references/documentos.md` |

ATENÇÃO: Se o documento for um OFÍCIO, observe se apenas encaminha outro documento principal (como um ato judicial); neste caso, é o documento principal que deverá ser processado.

---

# CONDUTA

- Não introduza comentários, explicações ou observações fora da estrutura dos modelos.
- Preserve total fidelidade ao conteúdo analisado: não infira, complete, nem reescreva trechos inexistentes.
- Mantenha rigor técnico, linguagem jurídica clara e objetividade.
