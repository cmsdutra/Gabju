#!/usr/bin/env python3
"""Tabela SAC (Sistema de Amortização Constante): geração e verificação.

Rotina modular de contadoria judicial. Amortização constante; juros e
prestação decrescentes. Leia `references/rotinas/tabela-sac.md` antes de
interpretar o resultado da verificação.

Uso:
  tabela_sac.py gerar --principal 100000 --taxa-mensal-pct 1.0 --parcelas 12

  tabela_sac.py verificar --principal 100000 --taxa-mensal-pct 1.0 --parcelas 12 \
      --tabela caminho/tabela.csv [--tolerancia 0.05]
      O CSV deve ter cabeçalho exato:
      periodo,saldo_inicial,juros,amortizacao,prestacao,saldo_final
      (uma linha por parcela, valores com ponto decimal).
"""
import argparse
import csv
import sys
from decimal import Decimal, ROUND_HALF_UP, getcontext

getcontext().prec = 40


def q(valor: Decimal) -> Decimal:
    return valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def gerar_tabela(principal: Decimal, taxa: Decimal, parcelas: int):
    amortizacao = q(principal / Decimal(parcelas))
    saldo = principal
    linhas = []
    for periodo in range(1, parcelas + 1):
        juros = q(saldo * taxa)
        amort_periodo = saldo if periodo == parcelas else amortizacao
        prestacao = amort_periodo + juros
        saldo_final = q(saldo - amort_periodo)
        linhas.append((periodo, q(saldo), juros, amort_periodo, prestacao, saldo_final))
        saldo = saldo_final
    return amortizacao, linhas


def cmd_gerar(args):
    principal = Decimal(str(args.principal))
    taxa = Decimal(str(args.taxa_mensal_pct)) / Decimal("100")
    parcelas = args.parcelas

    amortizacao, linhas = gerar_tabela(principal, taxa, parcelas)

    print(f"Amortização constante: {amortizacao:,.2f}\n")
    print(f"{'Período':>7} | {'Saldo inicial':>14} | {'Juros':>12} | {'Amortização':>12} | {'Prestação':>12} | {'Saldo final':>14}")
    for periodo, saldo_ini, juros, amort, prest, saldo_fim in linhas:
        print(f"{periodo:>7} | {saldo_ini:>14,.2f} | {juros:>12,.2f} | {amort:>12,.2f} | {prest:>12,.2f} | {saldo_fim:>14,.2f}")


def ler_csv(caminho):
    with open(caminho, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def cmd_verificar(args):
    principal = Decimal(str(args.principal))
    taxa = Decimal(str(args.taxa_mensal_pct)) / Decimal("100")
    parcelas = args.parcelas
    tolerancia = Decimal(str(args.tolerancia))

    _, esperado = gerar_tabela(principal, taxa, parcelas)
    informado = ler_csv(args.tabela)

    if len(informado) != len(esperado):
        print(f"ATENÇÃO: a tabela informada tem {len(informado)} linha(s); o esperado para {parcelas} parcelas é {len(esperado)}.")

    divergencias = 0
    for (periodo, saldo_ini_e, juros_e, amort_e, prest_e, saldo_fim_e), linha in zip(esperado, informado):
        saldo_ini_i = Decimal(linha["saldo_inicial"])
        juros_i = Decimal(linha["juros"])
        amort_i = Decimal(linha["amortizacao"])
        prest_i = Decimal(linha["prestacao"])
        saldo_fim_i = Decimal(linha["saldo_final"])

        diffs = {
            "saldo_inicial": (saldo_ini_i - saldo_ini_e).copy_abs(),
            "juros": (juros_i - juros_e).copy_abs(),
            "amortizacao": (amort_i - amort_e).copy_abs(),
            "prestacao": (prest_i - prest_e).copy_abs(),
            "saldo_final": (saldo_fim_i - saldo_fim_e).copy_abs(),
        }
        problemas = [campo for campo, dif in diffs.items() if dif > tolerancia]
        if problemas:
            divergencias += 1
            print(f"Período {periodo}: divergência em {', '.join(problemas)}")
            for campo in problemas:
                esperado_valor = {"saldo_inicial": saldo_ini_e, "juros": juros_e, "amortizacao": amort_e, "prestacao": prest_e, "saldo_final": saldo_fim_e}[campo]
                informado_valor = {"saldo_inicial": saldo_ini_i, "juros": juros_i, "amortizacao": amort_i, "prestacao": prest_i, "saldo_final": saldo_fim_i}[campo]
                print(f"    {campo}: informado {informado_valor:,.2f} / esperado (SAC, i={args.taxa_mensal_pct}%) {esperado_valor:,.2f}")

    print()
    if divergencias == 0:
        print(f"Nenhuma divergência acima da tolerância ({tolerancia}) — tabela regular para SAC com principal, taxa e nº de parcelas informados.")
    else:
        print(f"{divergencias} período(s) com divergência acima da tolerância ({tolerancia}).")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="comando", required=True)

    p_ger = sub.add_parser("gerar", help="Gera a tabela SAC esperada")
    p_ger.add_argument("--principal", required=True, type=float)
    p_ger.add_argument("--taxa-mensal-pct", required=True, type=float)
    p_ger.add_argument("--parcelas", required=True, type=int)
    p_ger.set_defaults(func=cmd_gerar)

    p_ver = sub.add_parser("verificar", help="Compara uma tabela informada contra a tabela SAC esperada")
    p_ver.add_argument("--principal", required=True, type=float)
    p_ver.add_argument("--taxa-mensal-pct", required=True, type=float)
    p_ver.add_argument("--parcelas", required=True, type=int)
    p_ver.add_argument("--tabela", required=True, help="Caminho do CSV com a tabela a verificar")
    p_ver.add_argument("--tolerancia", type=float, default=0.05)
    p_ver.set_defaults(func=cmd_verificar)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
