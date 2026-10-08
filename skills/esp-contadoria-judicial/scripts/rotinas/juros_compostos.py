#!/usr/bin/env python3
"""Juros compostos: cálculo de montante e verificação de regularidade.

Rotina modular de contadoria judicial. Antes de usar o subcomando
`verificar`, leia `references/rotinas/juros-compostos.md` para os
critérios de regularidade considerados.

Uso:
  juros_compostos.py calcular --principal 10000 --taxa-mensal-pct 1.5 --meses 12
      Montante por capitalização composta: M = P * (1 + i)^n.

  juros_compostos.py verificar --principal 10000 --taxa-mensal-pct 1.5 --meses 12 \
      --montante-informado 12000.00 [--tolerancia 0.01]
      Compara um montante informado (ex.: de um demonstrativo apresentado
      por uma das partes) contra o esperado por capitalização simples e
      por capitalização composta, apontando qual regime é compatível.
"""
import argparse
import sys
from decimal import Decimal, ROUND_HALF_UP, getcontext

getcontext().prec = 40


def q(valor: Decimal) -> Decimal:
    return valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def montante_composto(principal: Decimal, taxa: Decimal, meses: Decimal) -> Decimal:
    return principal * (Decimal("1") + taxa) ** meses


def montante_simples(principal: Decimal, taxa: Decimal, meses: Decimal) -> Decimal:
    return principal * (Decimal("1") + taxa * meses)


def cmd_calcular(args):
    principal = Decimal(str(args.principal))
    taxa = Decimal(str(args.taxa_mensal_pct)) / Decimal("100")
    meses = Decimal(str(args.meses))

    montante = q(montante_composto(principal, taxa, meses))
    juros = montante - principal

    print(f"Principal:            {principal:,.2f}")
    print(f"Taxa mensal:          {args.taxa_mensal_pct}%")
    print(f"Meses:                {meses}")
    print(f"Montante (composto):  {montante:,.2f}")
    print(f"Juros:                {juros:,.2f}")


def cmd_verificar(args):
    principal = Decimal(str(args.principal))
    taxa = Decimal(str(args.taxa_mensal_pct)) / Decimal("100")
    meses = Decimal(str(args.meses))
    informado = Decimal(str(args.montante_informado))
    tolerancia = Decimal(str(args.tolerancia))

    esperado_simples = q(montante_simples(principal, taxa, meses))
    esperado_composto = q(montante_composto(principal, taxa, meses))

    diff_simples = (informado - esperado_simples).copy_abs()
    diff_composto = (informado - esperado_composto).copy_abs()

    print(f"Principal:                  {principal:,.2f}")
    print(f"Taxa mensal:                {args.taxa_mensal_pct}%")
    print(f"Meses:                      {meses}")
    print(f"Montante informado:         {informado:,.2f}")
    print(f"Esperado (juros simples):   {esperado_simples:,.2f}  (dif.: {diff_simples:,.2f})")
    print(f"Esperado (juros compostos): {esperado_composto:,.2f}  (dif.: {diff_composto:,.2f})")
    print()

    compat_simples = diff_simples <= tolerancia
    compat_composto = diff_composto <= tolerancia

    if compat_simples and not compat_composto:
        print("Compatível apenas com capitalização SIMPLES.")
    elif compat_composto and not compat_simples:
        print("Compatível apenas com capitalização COMPOSTA.")
    elif compat_simples and compat_composto:
        print("Compatível com ambos os regimes dentro da tolerância informada (diferença pouco relevante para os parâmetros dados).")
    else:
        print(
            "INCOMPATÍVEL com ambos os regimes para os parâmetros informados. "
            "Isso não confirma, por si só, irregularidade — confira antes se a taxa, "
            "o número de períodos ou o próprio montante informado foram transcritos corretamente."
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="comando", required=True)

    p_calc = sub.add_parser("calcular", help="Calcula o montante por capitalização composta")
    p_calc.add_argument("--principal", required=True, type=float)
    p_calc.add_argument("--taxa-mensal-pct", required=True, type=float)
    p_calc.add_argument("--meses", required=True, type=float)
    p_calc.set_defaults(func=cmd_calcular)

    p_ver = sub.add_parser("verificar", help="Verifica se um montante informado é compatível com juros simples ou compostos")
    p_ver.add_argument("--principal", required=True, type=float)
    p_ver.add_argument("--taxa-mensal-pct", required=True, type=float)
    p_ver.add_argument("--meses", required=True, type=float)
    p_ver.add_argument("--montante-informado", required=True, type=float)
    p_ver.add_argument("--tolerancia", type=float, default=0.01)
    p_ver.set_defaults(func=cmd_verificar)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
