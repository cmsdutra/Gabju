---
name: minutar-completa
description: Encadeia relatório, fundamentação e dispositivo numa minuta completa de sentença, saneamento, tutela provisória ou decisão interlocutória. Use por padrão quando o usuário pedir para minutar, redigir, elaborar ou preparar esses atos, mesmo sem pedir expressamente minuta completa. Partes isoladas somente mediante delimitação expressa do usuário.
---

# /minutar-completa

Esta skill só define a ordem e a montagem. Cada parte segue integralmente a skill própria, com seus checkpoints.

## Escopo padrão e exceções

"Minute uma sentença", "redija uma decisão de tutela", "elabore o saneamento" e pedidos equivalentes significam minuta completa. Não pergunte se o usuário também quer relatório ou dispositivo. A invocação pelo nome de uma skill do ato segue a mesma regra.

Se o usuário pedir expressamente uma ou mais partes, entregue somente essas partes, usando as skills correspondentes e sem completar as demais seções. Exemplos: "redija a fundamentação da sentença", "somente o dispositivo", "relatório e fundamentação, sem dispositivo". A invocação direta de $minutar-relatorio-geral ou $minutar-dispositivo já delimita a seção desejada. Pedidos exclusivos de análise não acionam a montagem de minuta.

Preserve os checkpoints das skills próprias. As chamadas internas devem devolver somente a etapa atribuída e não reiniciar esta coordenação. Use seções adequadas ao ato: a minuta completa de despacho segue sua estrutura própria.

## Roteiro

| Ato | Relatório | Fundamentação | Dispositivo |
|---|---|---|---|
| Sentença | $minutar-relatorio-geral | $minutar-sentenca | incluído na fundamentação |
| Saneamento | $minutar-relatorio-geral | $minutar-saneamento | incluído na fundamentação |
| Tutela provisória | $minutar-relatorio-geral | $minutar-tutela | $minutar-dispositivo |
| Interlocutória geral | $minutar-relatorio-geral | $minutar-interlocutoria | $minutar-dispositivo |

Embargos de declaração e despacho já são completos: delegue a $minutar-embargos ou $minutar-despacho. Ato não identificado → pergunte.

## Execução

1. **Relatório**: informe o tipo de minuta à skill de relatório. Mantenha o texto internamente para a montagem final e prossiga sem exibi-lo nem aguardar confirmação.
2. **Fundamentação**: use o relatório como mapa das peças, sem repetir a narrativa. Exiba os checkpoints de análise e plano exigidos pela skill própria, bem como seus registros de deliberação, separados da minuta. Mantenha a redação internamente até a montagem final.
3. **Dispositivo**: quando previsto no roteiro, passe à skill de dispositivo o resultado e as circunstâncias apurados na fundamentação. Reserve o bloco para a montagem final.
4. **Montagem**: relatório, fundamentação, deliberação judicial, providências de impulso e linha de local e data, nesta ordem e sem duplicar seções. Antes de entregar, confira se todo pedido do relatório foi enfrentado e se fundamentação e dispositivo são coerentes entre si.

Entregue a minuta integral uma única vez, em um único documento. Não crie artefatos separados para relatório, fundamentação ou dispositivo. Quando uma skill chamada determinar a entrega de uma parte, receba-a internamente para a montagem; os checkpoints de deliberação e de plano continuam sendo apresentados ao usuário. Se o usuário pedir expressamente uma prévia de seção, apresente-a e preserve a montagem única ao final.
