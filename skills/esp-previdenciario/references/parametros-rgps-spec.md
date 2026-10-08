# Salário Mínimo e Teto do RGPS — Fontes, Validação e Ressalvas

Implementação: `scripts/salario_minimo.py` (tabela estática + API `get_salario_minimo`/`get_teto_rgps`) e `scripts/parametros_externos.py` (busca externa).

## 1. Camadas

| Competência | Origem | Status |
|---|---|---|
| ≤ `ULTIMA_COMPETENCIA_ESTATICA` (hoje `12/2026`) | tabela estática conferida | definitiva |
| posterior, confirmada | cache do usuário (`parametros_rgps.json`) ou fonte externa | definitiva (não reconsulta) |
| posterior, sem confirmação | último valor conhecido | **provisória** → aviso na saída em `avisos` |

S.M. antes de 01/1988 → `0.0` (fora da tabela; razão "x S.M." sai "-"). Teto antes de 07/1994 → `N/A`.

## 2. Fontes externas

| Parâmetro | Principal | Reserva |
|---|---|---|
| S.M. | [BCB/SGS 1619](https://api.bcb.gov.br/dados/serie/bcdata.sgs.1619/dados?formato=json) (mensal, JSON; 502 intermitente → 3 tentativas) | [página de contribuição mensal do INSS](https://www.gov.br/inss/pt-br/direitos-e-deveres/inscricao-e-contribuicao/tabela-de-contribuicao-mensal) (vigência do título até o mês da consulta) |
| Teto | página do INSS: título "TABELAS VÁLIDAS A PARTIR DA COMPETÊNCIA <MÊS> DE <ANO>"; teto = maior valor da seção; S.M. = 1ª faixa; exige o par "R$ S.M. até R$ teto" | [IEPREV](https://www.ieprev.com.br/ferramentas/tabela-dos-tetos-previdenciarios-do-inss) e [Previdenciarista](https://previdenciarista.com/tabela-historica-de-tetos-previdenciarios-da-previdencia-social-inss-a-partir-de-1994/) (não oficiais) |

- Página do INSS declara ISO-8859-1 mas é servida em UTF-8 (`_baixar` tenta UTF-8 primeiro).
- BCB **não** serve p/ histórico: soma os abonos de 1991 e registra 03–06/1994 em CR$.
- Nenhuma API pública traz o teto (IPEADATA recusou conexões em 09/2026; GitHub só tem constantes por ano).

## 3. Regras de aceitação

- Valor novo: maior que o anterior e ≤ anterior × `REAJUSTE_MAXIMO` (1,25); S.M. pode repetir mês a mês. Fora disso → rejeitado + aviso.
- Teto confirmado só se a vigência externa começou **no mesmo ano** da competência (reajuste todo janeiro desde 2010) e a fonte foi consultada com a competência já iniciada. Página do INSS ainda com a tabela do ano anterior não confirma o ano novo.
- INSS × não oficial divergentes → vale o INSS + aviso. Não oficiais divergentes entre si (sem INSS) → vigência descartada + aviso.
- Uma consulta por parâmetro por execução; falha → provisório, nova tentativa na próxima execução.

## 4. Cache e variáveis de ambiente

- `<cache>/parametros_rgps.json`; `<cache>` = `%LOCALAPPDATA%\cnis-calculator` (Windows), `$XDG_CACHE_HOME`/`~/.cache/cnis-calculator` (Linux/macOS). Fora da pasta da skill (plugin pode ser somente leitura).
- `CNIS_CALCULATOR_CACHE_DIR` → troca a pasta. `CNIS_CALCULATOR_OFFLINE=1` → sem rede (só estática + cache).
- Valor errado gravado no cache → apagar a entrada em `parametros_rgps.json`; a próxima execução reconsulta.

## 5. Ressalvas legais da tabela estática

Conferência de 24/09/2026: IBGE ("Evolução do salário mínimo", com decreto/portaria de cada valor), PDF do INSS "Valor do salário mínimo e respectivo fundamento legal", BCB/SGS 1619, atos normativos do teto e tabelas IEPREV/Previdenciarista.

- **1988–06/1989**: Piso Nacional de Salários (DL 2.351/87), o mínimo efetivamente pago. O Salário Mínimo de Referência da época (série do PDF do INSS) é outra série. 01/1989 = Cz$ 54.374,00 (decretado antes do NCz$).
- **1991**: valores legais sem abonos.
- **03–06/1994**: 64,79 URV (legal). O CNIS registra essas remunerações em CR$ → razão "x S.M." desses meses não é comparável (aptidão de mês cheio só importa ≥ 11/2019, sem efeito prático).
- **Teto**: 06/1997 e 06/1998 (reajuste passou a junho); 06–11/1998 = 1.081,50 (Port. MPAS 4.479/98); 12/1998 = 1.200,00 (EC 20, vigente desde 16/12/1998); 01–04/2004 = 2.400,00 (EC 41); 05/2004 = 2.508,72 (Port. MPS 479/04); 01/2011 = 3.691,74 (Port. Interm. 407/11, art. 2º, retroativo — contribuições de 01–06/2011 foram recolhidas sobre 3.689,66); 2026 = 8.475,55 (Port. Interm. MPS/MF 13/2026).

## 6. Estender a tabela estática

Opcional (a busca externa dispensa): acrescentar a vigência em `VIGENCIAS_REAL`/`VIGENCIAS_TETO_REAL` com o ato normativo em comentário, avançar `ULTIMA_COMPETENCIA_ESTATICA` e incluir o caso na suíte de testes.
