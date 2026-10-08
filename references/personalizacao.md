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
| Nome do magistrado ou da magistrada | `[NOME DO(A) MAGISTRADO(A)]` |
| Cargo | `[CARGO DO(A) MAGISTRADO(A)]` |

Preencha apenas campos conhecidos, preservando placeholders dos demais. Exemplo de fechamento: `[LOCALIDADE/UF], data de assinatura do sistema.` Inclua assinatura apenas quando o fluxo ou usuário a exigir; se exigida, mantenha seus campos mesmo quando desconhecidos. Nome em caixa alta e cargo conforme o dado disponibilizado. Mantenha a data gerada pelo sistema de assinatura quando o modelo adotar essa fórmula.

Placeholders são campos pendentes explícitos, não dados reais. Indique-os em nota breve ao entregar o texto. Preserve nomes e localidades de partes, fatos e fontes documentais; a personalização trata da unidade prolatora, não substitui os dados do processo.

Convenções redacionais incluídas no plugin são padrões ajustáveis à personalização e às instruções expressas da tarefa. Em revisão de texto existente, alterações continuam sujeitas ao protocolo de aprovação da skill.
