#!/usr/bin/env python3
"""Encadeia variações percentuais mensais em um coeficiente acumulado.

Rotina modular de contadoria judicial. Não embute valores de índice — as
variações devem vir do usuário, dos autos ou de consulta confirmada à fonte
oficial.

Uso:
  coeficiente.py 0.42 1.87 -0.15 ...
      Ex.: três competências com variação de 0,42%, 1,87% e -0,15%.
"""
import argparse
import sys
from decimal import Decimal, getcontext

getcontext().prec = 40


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("variacoes", nargs="+", type=float, help="Variações percentuais mensais, ex.: 0.42 1.87 -0.15")
    args = parser.parse_args()

    coef = Decimal("1")
    for pct in args.variacoes:
        coef *= (Decimal("1") + Decimal(str(pct)) / Decimal("100"))

    print(f"Coeficiente acumulado: {coef.quantize(Decimal('0.0000000001'))}")


if __name__ == "__main__":
    sys.exit(main())
