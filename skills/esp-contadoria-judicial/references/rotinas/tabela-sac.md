# Tabela SAC — Critérios de Regularidade

## O que caracteriza a Tabela SAC

Sistema de Amortização Constante: a amortização é **constante** (= principal ÷ número de parcelas) ao longo de todo o financiamento; os juros incidem sobre o saldo devedor (por isso decrescem) e a prestação, sendo juros + amortização, também decresce.

## O que a rotina verifica

`scripts/rotinas/tabela_sac.py verificar` recalcula, a partir do principal, da taxa e do número de parcelas contratados, a tabela SAC esperada, e compara linha a linha contra uma tabela informada (CSV), apontando divergências em saldo inicial, juros, amortização, prestação ou saldo final acima da tolerância definida.

## Como interpretar divergências

- **Amortização não é constante** ao longo da tabela informada: indício de que o sistema aplicado não é, de fato, SAC.
- **Juros do período divergem de saldo_inicial × taxa contratada**: mesma leitura da Tabela Price — indício de taxa diferente da contratada ou de base de cálculo diferente do saldo devedor.
- **Prestação não decresce de forma consistente com juros decrescentes**: sinal de que a amortização pode não estar realmente constante, mesmo que o valor nominal pareça correto em algumas parcelas.

## Limitação importante

Este teste confere regularidade **aritmética** frente aos parâmetros contratados que foram informados a ele. Não avalia se a taxa ou os parâmetros contratuais em si são lícitos — isso depende do título/contrato e da legislação aplicável ao caso concreto.
