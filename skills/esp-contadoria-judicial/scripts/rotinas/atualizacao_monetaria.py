#!/usr/bin/env python3
"""Aplica coeficiente de correção monetária, juros e honorários sobre um principal.

Rotina modular de contadoria judicial. Replica a estrutura de tabela do
manual de cálculos (principal, coeficiente, principal corrigido, juros,
honorários, total). Não embute valores de índice.

Uso:
  atualizacao_monetaria.py --principal 20000.00 --coeficiente 1.1883716656 \
      [--juros-pct 14.15] [--honorarios-pct 10]
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
    parser.add_argument("--coeficiente", required=True, type=float)
    parser.add_argument("--juros-pct", type=float, default=None, help="Percentual de juros sobre o principal corrigido")
    parser.add_argument("--honorarios-pct", type=float, default=None, help="Percentual de honorários sobre o total (principal corrigido + juros)")
    args = parser.parse_args()

    principal = Decimal(str(args.principal))
    coeficiente = Decimal(str(args.coeficiente))
    principal_corrigido = q(principal * coeficiente)

    juros = Decimal("0")
    if args.juros_pct is not None:
        juros = q(principal_corrigido * Decimal(str(args.juros_pct)) / Decimal("100"))

    total = principal_corrigido + juros

    honorarios = Decimal("0")
    if args.honorarios_pct is not None:
        honorarios = q(total * Decimal(str(args.honorarios_pct)) / Decimal("100"))

    print(f"Principal:              {principal:,.2f}")
    print(f"Coeficiente aplicado:   {coeficiente}")
    print(f"Principal corrigido:    {principal_corrigido:,.2f}")
    if args.juros_pct is not None:
        print(f"Juros ({args.juros_pct}%):          {juros:,.2f}")
    print(f"TOTAL (sem honorários): {total:,.2f}")
    if args.honorarios_pct is not None:
        print(f"Honorários ({args.honorarios_pct}%):        {honorarios:,.2f}")
        print(f"TOTAL GERAL:            {(total + honorarios):,.2f}")


if __name__ == "__main__":
    sys.exit(main())
