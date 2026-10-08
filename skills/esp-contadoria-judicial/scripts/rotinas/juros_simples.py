#!/usr/bin/env python3
"""Juros simples sobre um principal, dada taxa mensal e número de meses.

Rotina modular de contadoria judicial. Capitalização simples: J = P * i * n.

Uso:
  juros_simples.py --principal 20000.00 --taxa-mensal-pct 0.5 --meses 18
"""
import argparse
import sys
from decimal import Decimal, ROUND_HALF_UP, getcontext

getcontext().prec = 40


def q(valor: Decimal) -> Decimal:
    return valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--principal", required=True, type=float)
    parser.add_argument("--taxa-mensal-pct", required=True, type=float)
    parser.add_argument("--meses", required=True, type=float)
    args = parser.parse_args()

    principal = Decimal(str(args.principal))
    taxa = Decimal(str(args.taxa_mensal_pct)) / Decimal("100")
    meses = Decimal(str(args.meses))

    juros = q(principal * taxa * meses)
    total = principal + juros

    print(f"Principal:      {principal:,.2f}")
    print(f"Taxa mensal:    {args.taxa_mensal_pct}%")
    print(f"Meses:          {meses}")
    print(f"Juros simples:  {juros:,.2f}")
    print(f"TOTAL:          {total:,.2f}")


if __name__ == "__main__":
    sys.exit(main())
