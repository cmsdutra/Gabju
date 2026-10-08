# Fontes Oficiais de Índices de Atualização

Referência rápida sobre onde cada índice usado em cálculos judiciais é publicado oficialmente. Use esta tabela para decidir **onde buscar**, não como fonte do valor em si — o valor numérico deve vir de consulta atual à fonte oficial ou ser fornecido pelo usuário, nunca de memória.

| Índice | Uso típico no manual | Fonte primária | Observação |
|---|---|---|---|
| Selic | Juros de mora em dívida ativa da Fazenda Nacional; juros/correção em condenações contra a Fazenda a partir de dez./2021 (EC n. 113/2021) | Banco Central do Brasil (SGS) | Existe a Selic diária e a Selic acumulada no mês — confirme qual delas o cálculo exige |
| IPCA-E | Correção monetária em precatórios/RPV no período constitucional de pagamento; diversas liquidações de sentença | IBGE (índice oficial), replicado pelo BCB (SGS) | Não confundir com o IPCA "cheio" (índice diferente, usado para outras finalidades) |
| INPC | Correção monetária padrão em diversas liquidações de sentença (benefícios previdenciários, ações condenatórias em geral, FGTS etc.) | IBGE, replicado pelo BCB (SGS) | |
| IGP-M / IGP-DI | Contratos e dívidas diversas (ex.: Caixa Econômica Federal, ECT) quando previstos no título | FGV/IBRE, replicado pelo BCB (SGS) | |
| TR | Poupança (remuneração básica); FGTS | Banco Central do Brasil (SGS) | |
| Poupança (regra antiga/nova) | Juros de mora equivalentes à remuneração da poupança em diversas liquidações | Banco Central do Brasil (SGS) | A regra de cálculo mudou com a Lei n. 12.703/2012 (Selic > 8,5% a.a. → TR + 0,5% a.m.; caso contrário → TR + 70% da Selic) — confirme sempre qual regra se aplica ao período |
| Ufir, BTN, OTN, ORTN | Indexadores nominais históricos (índices extintos) | Não há série "ao vivo" — valores estão consolidados em tabelas históricas do próprio manual ou de tribunais | Buscar preferencialmente na doutrina/tabelas já compiladas, não em API de série temporal |
| Tabelas de coeficiente de atualização para precatórios/RPV | Cálculo complementar/suplementar de precatório (capítulo 5 do manual) | Conselho da Justiça Federal (CJF) — resolução vigente sobre atualização de precatórios e RPV | Pode divergir do índice de mercado equivalente; sempre identificar a resolução do CJF em vigor no período pedido |

## Como esta wiki se relaciona com os índices

`references/manual-de-calculos-2025/` explica **qual** indexador incide em cada tipo de ação/liquidação (regra jurídica). Esta página explica **onde** encontrar o valor numérico atual (fonte do dado). As rotinas empacotadas em `scripts/rotinas/` executam apenas a aritmética sobre parâmetros já validados. Regra jurídica, fonte numérica e cálculo são etapas distintas e devem permanecer rastreáveis.
