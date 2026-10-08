#!/usr/bin/env python3
"""Verifica a regularidade interna de uma tabela de amortização, sem
presumir o sistema (Price, SAC ou outro).

Rotina modular de contadoria judicial. Útil quando não se quer (ou não se
pode) assumir de antemão qual sistema de amortização foi usado — checa
apenas se a própria tabela é aritmeticamente consistente. Leia
`references/rotinas/verificacao-de-tabela.md` antes de interpretar o
resultado.

Verificações feitas, linha a linha:
  1) saldo_inicial(t) == saldo_final(t-1)          [encadeamento entre parcelas]
  2) prestacao(t) == juros(t) + amortizacao(t)      [consistência da parcela]
  3) saldo_final(t) == saldo_inicial(t) - amortizacao(t)  [abatimento do saldo]
  4) se --taxa-mensal-pct for informada: juros(t) == saldo_inicial(t) * i
     [aponta se os juros do período não batem com a taxa contratada sobre
     o saldo devedor — divergência aqui é o principal indício de
     capitalização de juros (anatocismo) ou de aplicação de índice diverso
     do informado]

Ao final, também confere:
  5) soma das amortizações == principal informado (se --principal for dado)
  6) saldo final da última parcela ≈ 0

Uso:
  verificar_tabela.py --tabela caminho/tabela.csv [--principal 100000] \
      [--taxa-mensal-pct 1.0] [--tolerancia 0.05]
      O CSV deve ter cabeçalho exato:
      periodo,saldo_inicial,juros,amortizacao,prestacao,saldo_final
      (uma linha por parcela, em ordem, valores com ponto decimal).
"""
import argparse
import csv
import sys
from decimal import Decimal, getcontext

getcontext().prec = 40


def ler_csv(caminho):
    with open(caminho, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tabela", required=True, help="Caminho do CSV com a tabela a verificar")
    parser.add_argument("--principal", type=float, default=None, help="Principal contratado, para conferir a soma das amortizações")
    parser.add_argument("--taxa-mensal-pct", type=float, default=None, help="Taxa mensal contratada, para conferir juros(t) == saldo_inicial(t) * i")
    parser.add_argument("--tolerancia", type=float, default=0.05)
    args = parser.parse_args()

    tolerancia = Decimal(str(args.tolerancia))
    taxa = Decimal(str(args.taxa_mensal_pct)) / Decimal("100") if args.taxa_mensal_pct is not None else None

    linhas = ler_csv(args.tabela)
    if not linhas:
        print("Tabela vazia — nada a verificar.")
        return

    total_problemas = 0
    saldo_final_anterior = None
    soma_amortizacoes = Decimal("0")

    for linha in linhas:
        periodo = linha["periodo"]
        saldo_inicial = Decimal(linha["saldo_inicial"])
        juros = Decimal(linha["juros"])
        amortizacao = Decimal(linha["amortizacao"])
        prestacao = Decimal(linha["prestacao"])
        saldo_final = Decimal(linha["saldo_final"])
        soma_amortizacoes += amortizacao

        problemas = []

        if saldo_final_anterior is not None and (saldo_inicial - saldo_final_anterior).copy_abs() > tolerancia:
            problemas.append(f"saldo_inicial ({saldo_inicial:,.2f}) difere do saldo_final da parcela anterior ({saldo_final_anterior:,.2f})")

        if (prestacao - (juros + amortizacao)).copy_abs() > tolerancia:
            problemas.append(f"prestacao ({prestacao:,.2f}) != juros + amortizacao ({(juros + amortizacao):,.2f})")

        if (saldo_final - (saldo_inicial - amortizacao)).copy_abs() > tolerancia:
            problemas.append(f"saldo_final ({saldo_final:,.2f}) != saldo_inicial - amortizacao ({(saldo_inicial - amortizacao):,.2f})")

        if taxa is not None:
            juros_esperado = saldo_inicial * taxa
            if (juros - juros_esperado).copy_abs() > tolerancia:
                problemas.append(f"juros ({juros:,.2f}) != saldo_inicial * taxa contratada ({juros_esperado:,.2f}) — possível capitalização/índice divergente")

        if problemas:
            total_problemas += 1
            print(f"Período {periodo}:")
            for p in problemas:
                print(f"    - {p}")

        saldo_final_anterior = saldo_final

    print()
    if args.principal is not None:
        principal = Decimal(str(args.principal))
        if (soma_amortizacoes - principal).copy_abs() > tolerancia:
            total_problemas += 1
            print(f"Soma das amortizações ({soma_amortizacoes:,.2f}) != principal informado ({principal:,.2f})")
        else:
            print(f"Soma das amortizações confere com o principal informado ({principal:,.2f}).")

    if saldo_final_anterior is not None and saldo_final_anterior.copy_abs() > tolerancia:
        total_problemas += 1
        print(f"Saldo final da última parcela não zera: {saldo_final_anterior:,.2f}")
    else:
        print("Saldo final da última parcela zera corretamente.")

    print()
    if total_problemas == 0:
        print(f"Nenhuma irregularidade encontrada acima da tolerância ({tolerancia}).")
    else:
        print(f"{total_problemas} parcela(s)/verificação(ões) com irregularidade acima da tolerância ({tolerancia}).")


if __name__ == "__main__":
    sys.exit(main())
