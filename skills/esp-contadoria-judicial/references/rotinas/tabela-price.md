# Tabela Price — Critérios de Regularidade

## O que caracteriza a Tabela Price

Sistema Francês de Amortização: a prestação é **constante** ao longo de todo o financiamento; dentro de cada prestação, os juros incidem sobre o saldo devedor (por isso decrescem) e a amortização é a diferença entre a prestação e os juros do período (por isso cresce). O saldo devedor deve zerar exatamente na última parcela.

PMT (prestação) = P × i / (1 − (1 + i)⁻ⁿ), em que P é o principal, i a taxa periódica e n o número de parcelas.

## O que a rotina verifica

`scripts/rotinas/tabela_price.py verificar` recalcula, a partir do principal, da taxa e do número de parcelas contratados, a tabela Price esperada, e compara linha a linha contra uma tabela informada (CSV), apontando divergências em saldo inicial, juros, amortização, prestação ou saldo final acima da tolerância definida.

## Como interpretar divergências

- **Prestação não é constante** ao longo da tabela informada: forte indício de que o sistema aplicado não é, de fato, Price — ou de que há capitalização adicional não contratada.
- **Juros do período divergem de saldo_inicial × taxa contratada**: indício de que a taxa efetivamente aplicada é diferente da contratada, ou de que os juros incidem sobre uma base diferente do saldo devedor informado.
- **Saldo final da última parcela não zera**: indício de erro de arredondamento acumulado (normalmente pequeno, poucos centavos) ou de erro estrutural na tabela (se a diferença for relevante).

Divergências pequenas e uniformes (poucos centavos, em todas as parcelas) geralmente decorrem de arredondamento, não de irregularidade. Divergências concentradas, crescentes ou que só aparecem a partir de determinado período costumam indicar um problema estrutural — reporte o padrão observado, não apenas a divergência isolada.

## Limitação importante

Este teste confere regularidade **aritmética** frente aos parâmetros contratados que foram informados a ele. Não avalia se a taxa ou os parâmetros contratuais em si são lícitos — isso depende do título/contrato e da legislação aplicável ao caso concreto.
