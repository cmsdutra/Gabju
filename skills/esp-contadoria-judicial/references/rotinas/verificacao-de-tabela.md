# Verificação Genérica de Tabela de Amortização — Critérios

## Quando usar esta rotina em vez de `tabela_price.py`/`tabela_sac.py`

Use `scripts/rotinas/verificar_tabela.py` quando **não** se souber (ou não se quiser presumir) qual sistema de amortização foi utilizado, ou quando o objetivo for apenas confirmar se a tabela apresentada é internamente consistente, independentemente do método. Se já se sabe que o sistema contratado é Price ou SAC, prefira a rotina específica — ela também confere se a tabela corresponde *a esse sistema*, não só se é internamente consistente.

## O que a rotina verifica

Linha a linha, sem presumir método:

1. `saldo_inicial(t) == saldo_final(t-1)` — encadeamento entre parcelas;
2. `prestacao(t) == juros(t) + amortizacao(t)` — consistência da própria parcela;
3. `saldo_final(t) == saldo_inicial(t) - amortizacao(t)` — abatimento correto do saldo;
4. (se a taxa contratada for informada) `juros(t) == saldo_inicial(t) * taxa` — os juros lançados batem com a taxa contratada aplicada sobre o saldo devedor.

Ao final: soma das amortizações confere com o principal informado, e o saldo final da última parcela zera.

## Como interpretar divergências

- Falhas nos itens 1–3 indicam **inconsistência aritmética da própria tabela**, independente de qualquer parâmetro externo — a tabela não fecha com ela mesma.
- Falha no item 4 é o indício mais direto de **capitalização de juros não evidenciada** (juros incidindo sobre uma base diferente do saldo devedor declarado) ou de aplicação de taxa diferente da contratada — mas confirme, antes de concluir por irregularidade, que a taxa informada à rotina é de fato a taxa contratada no título/contrato.
- Divergência apenas na soma final das amortizações, com todas as linhas individualmente consistentes, sugere erro de captura dos dados (ex.: parcela faltante na tabela) mais do que erro de cálculo.

## Limitação importante

Esta rotina não identifica **qual** sistema de amortização foi usado, nem se os parâmetros contratuais (taxa, prazo) são lícitos — apenas se a tabela informada é aritmeticamente consistente consigo mesma e, quando a taxa é informada, com essa taxa.
