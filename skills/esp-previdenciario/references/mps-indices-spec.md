# Especificação da Tabela de Atualização Monetária do MPS (Art. 33 Decreto 3.048/99)

## 1. Origem e Finalidade
- **Fonte Oficial**: Ministério da Previdência Social (MPS).
- **Página de Publicação**: [Índice de atualização das contribuições para cálculo do salário-de-benefício](https://www.gov.br/previdencia/pt-br/assuntos/previdencia-social/legislacao/indice-de-atualizacao-das-contribuicoes-para-calculo-do-salario-de-beneficio)
- **Finalidade**: Atualizar monetariamente os salários de contribuição a partir de julho de 1994 para a apuração da Renda Mensal Inicial (RMI) e do Salário de Benefício do Regime Geral de Previdência Social (RGPS).

## 2. Estrutura dos arquivos oficiais
O portal disponibiliza arquivos mensais de fatores do art. 33.
- **Conteúdo**:
  - Cabeçalho institucional com indicação da Portaria ministerial e mês de referência.
  - Coluna 1: Competência (armazenada como data serial originada em 1899-12-30).
  - Coluna 2: Fator simplificado de multiplicação (precisão de 6 casas decimais).
- **Início da Série**: Julho de 1994 (Plano Real).
- **Término da Série**: Mês imediatamente anterior à competência de publicação da portaria.

## 3. Mecanismo de Cache e Extração Determinística
O módulo `mps_indices.py`:
1. Consulta a URL oficial para identificar a portaria e tabela mais recente.
2. Baixa o arquivo oficial apenas quando necessário.
3. Descompacta-o via `zipfile` e analisa `sheet1.xml` e `sharedStrings.xml` de forma nativa e determinística, sem biblioteca de terceiros.
4. Salva um espelho estruturado na pasta de cache do usuário (`<cache>/mps/fatores_mps_MM_AAAA.json`; `<cache>` = `%LOCALAPPDATA%\cnis-calculator` no Windows, `~/.cache/cnis-calculator` no Linux/macOS, ou `CNIS_CALCULATOR_CACHE_DIR`). A pasta da skill pode ser somente leitura/sobrescrita quando distribuída como plugin.
5. Permite execução offline a partir do cache pré-carregado da skill (`references/.cache/`, só leitura), consultado depois do cache do usuário. Sem portal, usa o JSON mais recente (por ano/mês) entre as duas pastas.
6. Registra na saída a competência, a referência e a URL da fonte. Os caches empacotados são identificados por competência e podem exigir atualização.
