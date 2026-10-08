"""
salario_minimo.py - Salário mínimo nacional e teto do RGPS por competência (MM/AAAA).

Duas camadas:
- Tabela estática conferida com a legislação até ULTIMA_COMPETENCIA_ESTATICA (histórico não muda).
- Depois dela, busca externa com validação e cache (parametros_externos.py). Valor não confirmado
  nunca é usado em silêncio: fica registrado em avisos_competencia().
"""

from typing import List, Optional, Tuple

import parametros_externos

# Última competência coberta pela tabela estática. Depois dela, os valores vêm de fonte externa.
ULTIMA_COMPETENCIA_ESTATICA = "12/2026"

# Tabela nominal por competência (MM/AAAA) -> (valor, moeda), 1988 a 06/1994.
# Fonte: IBGE, "Evolução do salário mínimo" (decreto/portaria de cada valor), conferida com o PDF
# do INSS "Valor do salário mínimo e respectivo fundamento legal" e com a série 1619 do BCB.
# - 1988 a 06/1989: Piso Nacional de Salários (DL 2.351/87), o mínimo efetivamente pago; a Lei
#   7.789/89 o extinguiu e restabeleceu o nome "salário mínimo". O Salário Mínimo de Referência
#   da mesma época (listado pelo INSS) é outra série e não é usado aqui.
# - 1991: valores legais sem os abonos (nota do IBGE). A série do BCB soma os abonos e diverge
#   em 04 a 08/1991 e 12/1991, por isso não serve para este período.
# - 03 a 06/1994: valor legal em URV. O CNIS registra essas remunerações em CR$, então a razão
#   remuneração/S.M. desses quatro meses não é comparável.
HISTORICO_SM = {
    # 1988 (Cz$) - Piso Nacional de Salários
    "01/1988": (4500.00, "Cz$"), "02/1988": (5280.00, "Cz$"), "03/1988": (6240.00, "Cz$"),
    "04/1988": (7260.00, "Cz$"), "05/1988": (8712.00, "Cz$"), "06/1988": (10368.00, "Cz$"),
    "07/1988": (12444.00, "Cz$"), "08/1988": (15552.00, "Cz$"), "09/1988": (18960.00, "Cz$"),
    "10/1988": (23700.00, "Cz$"), "11/1988": (30800.00, "Cz$"), "12/1988": (40425.00, "Cz$"),

    # 1989 (Cz$ em 01/1989, decretado antes da troca de moeda; NCz$ a partir de 02/1989)
    "01/1989": (54374.00, "Cz$"), "02/1989": (63.90, "NCz$"), "03/1989": (63.90, "NCz$"),
    "04/1989": (63.90, "NCz$"), "05/1989": (81.40, "NCz$"), "06/1989": (120.00, "NCz$"),
    "07/1989": (149.80, "NCz$"), "08/1989": (192.88, "NCz$"), "09/1989": (249.48, "NCz$"),
    "10/1989": (381.73, "NCz$"), "11/1989": (557.33, "NCz$"), "12/1989": (788.18, "NCz$"),

    # 1990 (NCz$ até 03/1990, Cr$ a partir de 04/1990)
    "01/1990": (1283.95, "NCz$"), "02/1990": (2004.37, "NCz$"), "03/1990": (3674.06, "NCz$"),
    "04/1990": (3674.06, "Cr$"), "05/1990": (3674.06, "Cr$"), "06/1990": (3857.76, "Cr$"),
    "07/1990": (4904.76, "Cr$"), "08/1990": (5203.46, "Cr$"), "09/1990": (6056.31, "Cr$"),
    "10/1990": (6425.14, "Cr$"), "11/1990": (8329.55, "Cr$"), "12/1990": (8836.82, "Cr$"),

    # 1991 (Cr$) - sem abonos
    "01/1991": (12325.60, "Cr$"), "02/1991": (15895.46, "Cr$"), "03/1991": (17000.00, "Cr$"),
    "04/1991": (17000.00, "Cr$"), "05/1991": (17000.00, "Cr$"), "06/1991": (17000.00, "Cr$"),
    "07/1991": (17000.00, "Cr$"), "08/1991": (17000.00, "Cr$"), "09/1991": (42000.00, "Cr$"),
    "10/1991": (42000.00, "Cr$"), "11/1991": (42000.00, "Cr$"), "12/1991": (42000.00, "Cr$"),

    # 1992 (Cr$)
    "01/1992": (96037.33, "Cr$"), "02/1992": (96037.33, "Cr$"), "03/1992": (96037.33, "Cr$"),
    "04/1992": (96037.33, "Cr$"), "05/1992": (230000.00, "Cr$"), "06/1992": (230000.00, "Cr$"),
    "07/1992": (230000.00, "Cr$"), "08/1992": (230000.00, "Cr$"), "09/1992": (522186.94, "Cr$"),
    "10/1992": (522186.94, "Cr$"), "11/1992": (522186.94, "Cr$"), "12/1992": (522186.94, "Cr$"),

    # 1993 (Cr$ até 07/1993, Cruzeiro Real CR$ a partir de 08/1993)
    "01/1993": (1250700.00, "Cr$"), "02/1993": (1250700.00, "Cr$"), "03/1993": (1709400.00, "Cr$"),
    "04/1993": (1709400.00, "Cr$"), "05/1993": (3303300.00, "Cr$"), "06/1993": (3303300.00, "Cr$"),
    "07/1993": (4639800.00, "Cr$"), "08/1993": (5534.00, "CR$"), "09/1993": (9606.00, "CR$"),
    "10/1993": (12024.00, "CR$"), "11/1993": (15021.00, "CR$"), "12/1993": (18760.00, "CR$"),

    # 1994 (CR$ até 02/1994, URV 03-06/1994, Real R$ a partir de 07/1994)
    "01/1994": (32882.00, "CR$"), "02/1994": (42829.00, "CR$"),
    "03/1994": (64.79, "URV"), "04/1994": (64.79, "URV"), "05/1994": (64.79, "URV"), "06/1994": (64.79, "URV"),
    "07/1994": (64.79, "R$"), "08/1994": (64.79, "R$"), "09/1994": (70.00, "R$"), "10/1994": (70.00, "R$"),
    "11/1994": (70.00, "R$"), "12/1994": (70.00, "R$"),
}

# Vigências do salário mínimo em R$ a partir de 1995 (conferidas mês a mês com a série 1619 do BCB)
VIGENCIAS_REAL = [
    ("01/1995", "04/1995", 70.00),
    ("05/1995", "04/1996", 100.00),
    ("05/1996", "04/1997", 112.00),
    ("05/1997", "04/1998", 120.00),
    ("05/1998", "04/1999", 130.00),
    ("05/1999", "03/2000", 136.00),
    ("04/2000", "03/2001", 151.00),
    ("04/2001", "03/2002", 180.00),
    ("04/2002", "03/2003", 200.00),
    ("04/2003", "04/2004", 240.00),
    ("05/2004", "04/2005", 260.00),
    ("05/2005", "03/2006", 300.00),
    ("04/2006", "03/2007", 350.00),
    ("04/2007", "02/2008", 380.00),
    ("03/2008", "01/2009", 415.00),
    ("02/2009", "12/2009", 465.00),
    ("01/2010", "12/2010", 510.00),
    ("01/2011", "02/2011", 540.00),
    ("03/2011", "12/2011", 545.00),
    ("01/2012", "12/2012", 622.00),
    ("01/2013", "12/2013", 678.00),
    ("01/2014", "12/2014", 724.00),
    ("01/2015", "12/2015", 788.00),
    ("01/2016", "12/2016", 880.00),
    ("01/2017", "12/2017", 937.00),
    ("01/2018", "12/2018", 954.00),
    ("01/2019", "12/2019", 998.00),
    ("01/2020", "01/2020", 1039.00),
    ("02/2020", "12/2020", 1045.00),
    ("01/2021", "12/2021", 1100.00),
    ("01/2022", "12/2022", 1212.00),
    ("01/2023", "04/2023", 1302.00),
    ("05/2023", "12/2023", 1320.00),
    ("01/2024", "12/2024", 1412.00),
    ("01/2025", "12/2025", 1518.00),
    ("01/2026", "12/2026", 1621.00),
]

def _parse_mm_yyyy(comp: str) -> Tuple[int, int]:
    p = comp.strip().split('/')
    return int(p[0]), int(p[1])

def _expandir_vigencias(vigencias, destino: dict) -> None:
    for ini_str, fim_str, val in vigencias:
        m_i, y_i = _parse_mm_yyyy(ini_str)
        m_f, y_f = _parse_mm_yyyy(fim_str)
        cur_y, cur_m = y_i, m_i
        while True:
            k = f"{cur_m:02d}/{cur_y}"
            if k not in destino:
                destino[k] = (val, "R$")
            if cur_y == y_f and cur_m == m_f:
                break
            cur_m += 1
            if cur_m > 12:
                cur_m = 1
                cur_y += 1

_expandir_vigencias(VIGENCIAS_REAL, HISTORICO_SM)

_M_ULT, _Y_ULT = _parse_mm_yyyy(ULTIMA_COMPETENCIA_ESTATICA)

def _apos_tabela_estatica(m: int, y: int) -> bool:
    return (y, m) > (_Y_ULT, _M_ULT)

def get_salario_minimo(competencia: str) -> Tuple[float, str]:
    """
    Retorna (valor, moeda) do salário mínimo vigente na competência (formato MM/AAAA).
    Exemplo: get_salario_minimo('11/2019') -> (998.00, 'R$')
    Após ULTIMA_COMPETENCIA_ESTATICA, consulta fonte externa (ver avisos_competencia).
    """
    comp = competencia.strip()
    if comp in HISTORICO_SM:
        return HISTORICO_SM[comp]
    try:
        m, y = _parse_mm_yyyy(comp)
    except Exception:
        return (0.0, "R$")
    if _apos_tabela_estatica(m, y):
        valor = parametros_externos.salario_minimo_externo(
            f"{m:02d}/{y}", ULTIMA_COMPETENCIA_ESTATICA, HISTORICO_SM[ULTIMA_COMPETENCIA_ESTATICA][0])
        return (valor, "R$")
    # Antes de 1988: fora da tabela (sem valor, em vez de um valor errado)
    return (0.0, "R$")

def format_currency_br(val: Optional[float], decimals: int = 2) -> str:
    """Formata valor float no padrão brasileiro: 1.234,56"""
    if val is None:
        return ""
    s = f"{val:,.{decimals}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


# Vigências do teto do RGPS (limite máximo do salário de contribuição) em R$ a partir de 07/1994.
# Conferidas com os atos normativos e com as tabelas do IEPREV e do Previdenciarista.
VIGENCIAS_TETO_REAL = [
    ("07/1994", "04/1995", 582.86),
    ("05/1995", "04/1996", 832.66),
    ("05/1996", "05/1997", 957.56),
    ("06/1997", "05/1998", 1031.87),   # reajuste passou a ser em junho (MP 1.572/97)
    ("06/1998", "11/1998", 1081.50),   # Portaria MPAS 4.479/98
    ("12/1998", "05/1999", 1200.00),   # EC 20/98 (vigência 16/12/1998)
    ("06/1999", "05/2000", 1255.32),
    ("06/2000", "05/2001", 1328.25),
    ("06/2001", "05/2002", 1430.00),
    ("06/2002", "05/2003", 1561.56),
    ("06/2003", "12/2003", 1869.34),
    ("01/2004", "04/2004", 2400.00),   # EC 41/2003
    ("05/2004", "04/2005", 2508.72),   # Portaria MPS 479/2004
    ("05/2005", "03/2006", 2668.15),
    ("04/2006", "03/2007", 2801.56),
    ("04/2007", "02/2008", 2894.28),
    ("03/2008", "01/2009", 3038.99),
    ("02/2009", "12/2009", 3218.90),
    ("01/2010", "12/2010", 3467.40),
    ("01/2011", "12/2011", 3691.74),   # Portaria Interm. 407/2011, art. 2º (retroativo a 01/2011)
    ("01/2012", "12/2012", 3916.20),
    ("01/2013", "12/2013", 4159.00),
    ("01/2014", "12/2014", 4390.24),
    ("01/2015", "12/2015", 4663.75),
    ("01/2016", "12/2016", 5189.82),
    ("01/2017", "12/2017", 5531.31),
    ("01/2018", "12/2018", 5645.80),
    ("01/2019", "12/2019", 5839.45),
    ("01/2020", "12/2020", 6101.06),
    ("01/2021", "12/2021", 6433.57),
    ("01/2022", "12/2022", 7087.22),
    ("01/2023", "12/2023", 7507.49),
    ("01/2024", "12/2024", 7786.02),
    ("01/2025", "12/2025", 8157.41),
    ("01/2026", "12/2026", 8475.55),   # Portaria Interm. MPS/MF 13/2026
]

HISTORICO_TETO = {}
_expandir_vigencias(VIGENCIAS_TETO_REAL, HISTORICO_TETO)

def get_teto_rgps(competencia: str) -> Tuple[float, str]:
    """
    Retorna (valor, moeda) do Teto do RGPS vigente na competência (formato MM/AAAA).
    Exemplo: get_teto_rgps('05/2023') -> (7507.49, 'R$')
    Após ULTIMA_COMPETENCIA_ESTATICA, consulta fonte externa (ver avisos_competencia).
    """
    comp = competencia.strip()
    if comp in HISTORICO_TETO:
        return HISTORICO_TETO[comp]
    try:
        m, y = _parse_mm_yyyy(comp)
    except Exception:
        return (0.0, "R$")
    if y < 1994 or (y == 1994 and m < 7):
        return (0.0, "N/A")
    if _apos_tabela_estatica(m, y):
        valor = parametros_externos.teto_externo(
            f"{m:02d}/{y}", ULTIMA_COMPETENCIA_ESTATICA, HISTORICO_TETO[ULTIMA_COMPETENCIA_ESTATICA][0])
        return (valor, "R$")
    return (0.0, "R$")

def avisos_competencia(competencia: str) -> List[str]:
    """Avisos sobre S.M./teto da competência que não puderam ser confirmados em fonte externa."""
    return parametros_externos.avisos_competencia(competencia.strip())

def avisos_parametros() -> List[str]:
    """Todos os avisos de S.M./teto gerados nesta execução, sem repetição."""
    return parametros_externos.avisos_gerais()
