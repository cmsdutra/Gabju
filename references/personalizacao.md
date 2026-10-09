---
created: 2026-10-08
updated: 2026-10-08
ai-agent: "Codex CLI"
---

# Personalização do gabinete

Para dados institucionais e fechamento, use as instruções de personalização do ChatGPT efetivamente disponíveis no contexto. Orientação expressa para a tarefa prevalece sobre os padrões pessoais. Não presuma acesso a configurações que não foram disponibilizadas ao modelo.

Campo ausente → use o placeholder padrão correspondente, sem interromper a redação para solicitá-lo:

| Campo | Placeholder |
|---|---|
| Localidade e UF | `[LOCALIDADE/UF]` |
| Unidade judiciária | `[UNIDADE JUDICIÁRIA]` |

Preencha apenas campos conhecidos, preservando placeholders dos demais.

## Fechamento

A minuta termina na linha de local e data, sempre no formato `[LOCALIDADE/UF], data de assinatura do sistema.` (com a localidade preenchida quando conhecida). Nunca escreva data real: ela é gerada pelo sistema de assinatura.

Nada vem depois dessa linha. Não inclua assinatura, nome ou cargo do(a) magistrado(a), "(assinado digitalmente)" nem marcação HTML, ainda que a personalização do ChatGPT informe esses dados ou traga modelo de assinatura: a assinatura é aposta pelo sistema processual. Em revisão de texto existente que contenha bloco de assinatura, aponte sua supressão como correção direta.

Placeholders são campos pendentes explícitos, não dados reais. Indique-os em nota breve ao entregar o texto. Preserve nomes e localidades de partes, fatos e fontes documentais; a personalização trata da unidade prolatora, não substitui os dados do processo.

Convenções redacionais incluídas no plugin são padrões ajustáveis à personalização e às instruções expressas da tarefa, exceto a regra de fechamento acima. Em revisão de texto existente, alterações continuam sujeitas ao protocolo de aprovação da skill.
