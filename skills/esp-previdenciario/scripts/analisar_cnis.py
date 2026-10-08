#!/usr/bin/env python3
"""Analisa deterministicamente um JSON canônico de CNIS e emite JSON ou Markdown."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

from _cnis_engine import (
    analisar_transicoes_ec103,
    calcular_valores,
    calcular_vinculos,
    dias_para_amd,
    parse_date_br,
)
from mps_indices import get_mps_indices
from salario_minimo import avisos_parametros


def _json_default(value: Any) -> str:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    raise TypeError(f"Tipo não serializável: {type(value).__name__}")


def _validar_entrada(data: Any) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if not isinstance(data, dict):
        raise ValueError("o JSON canônico deve ser um objeto")
    filiado = data.get("filiado")
    vinculos = data.get("vinculos")
    if not isinstance(filiado, dict):
        raise ValueError("campo obrigatório 'filiado' ausente ou inválido")
    if not isinstance(vinculos, list):
        raise ValueError("campo obrigatório 'vinculos' ausente ou inválido")
    return filiado, vinculos


def _media_pbc(valores: list[dict[str, Any]], fatores: dict[str, Any]) -> tuple[float | None, list[str]]:
    aptas = [v for v in valores if v["conta_rmi"] == "Sim"]
    ausentes = sorted(v["competencia"] for v in aptas if v["competencia"] not in fatores)
    if ausentes:
        return None, [
            "RMI não calculada: faltam fatores MPS para " + ", ".join(ausentes) + "."
        ]
    if not aptas:
        return None, ["RMI não calculada: nenhuma competência integra o PBC desde 07/1994."]
    return sum(v["valor_atualizado_float"] for v in aptas) / len(aptas), []


def analisar(data: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    filiado, vinculos = _validar_entrada(data)
    vinculos_calc, total, pre, pos = calcular_vinculos(vinculos, args.der)
    avisos = list(data.get("avisos_extracao") or [])
    fontes: dict[str, Any] = {"parametros_rgps": "tabelas internas e fontes identificadas nos avisos"}

    tabela_mps: dict[str, Any] = {"fatores": {}}
    if args.sem_rmi:
        avisos.append("Cálculo de RMI desativado por --sem-rmi; competências exibidas sem média do PBC.")
    else:
        tabela_mps = get_mps_indices(args.competencia_mps)
        fontes["indices_mps"] = {
            "competencia": tabela_mps.get("competencia_ref"),
            "referencia": tabela_mps.get("referencia_portaria"),
            "url": tabela_mps.get("url_fonte"),
        }

    valores = calcular_valores(vinculos, tabela_mps)
    media = None
    if not args.sem_rmi:
        media, avisos_media = _media_pbc(valores, tabela_mps.get("fatores", {}))
        avisos.extend(avisos_media)
    avisos.extend(avisos_parametros())

    transicoes: list[dict[str, Any]] = []
    nascimento = parse_date_br(str(filiado.get("data_nascimento") or ""))
    der = parse_date_br(args.der) if args.der else None
    if args.sexo or args.expectativa_sobrevida is not None:
        faltantes = []
        if not der:
            faltantes.append("DER")
        if not nascimento:
            faltantes.append("data de nascimento no JSON")
        if not args.sexo:
            faltantes.append("sexo")
        if faltantes:
            avisos.append("Regras de transição não analisadas; faltam: " + ", ".join(faltantes) + ".")
        else:
            transicoes = analisar_transicoes_ec103(
                args.sexo,
                nascimento,
                der,
                total,
                pre,
                expectativa_sobrevida=args.expectativa_sobrevida,
                media_pbc=media,
            )
    elif der and nascimento:
        avisos.append("Regras de transição não analisadas sem --sexo M|F.")

    sobreposicoes = [
        {
            "seq": v["seq"],
            "empregador": v["empregador"],
            "dias_concomitantes": v["concomitancia"],
            "segmentos": [s for s in v["segmentos"] if s["concomitancia"] > 0],
        }
        for v in vinculos_calc
        if v["concomitancia"] > 0
    ]

    return {
        "identificacao": filiado,
        "parametros": {
            "der": args.der,
            "sexo": args.sexo,
            "expectativa_sobrevida": args.expectativa_sobrevida,
            "rmi_habilitada": not args.sem_rmi,
        },
        "tempo_contribuicao": {
            "dias_liquidos": total,
            "amd": dias_para_amd(total),
            "dias_pre_ec103": pre,
            "amd_pre_ec103": dias_para_amd(pre),
            "dias_pos_ec103": pos,
            "amd_pos_ec103": dias_para_amd(pos),
        },
        "vinculos": vinculos_calc,
        "sobreposicoes": sobreposicoes,
        "competencias_consolidadas": valores,
        "pbc": {
            "quantidade_competencias": sum(v["conta_rmi"] == "Sim" for v in valores),
            "media": media,
        },
        "regras_transicao": transicoes,
        "avisos": list(dict.fromkeys(str(a) for a in avisos if a)),
        "fontes": fontes,
    }


def _dinheiro(valor: float | None) -> str:
    if valor is None:
        return "não calculável"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def render_markdown(resultado: dict[str, Any]) -> str:
    ident = resultado["identificacao"]
    tempo = resultado["tempo_contribuicao"]
    params = resultado["parametros"]
    linhas = [
        "# Relatório técnico previdenciário",
        "",
        "## Objeto e documentação analisada",
        "",
        "Análise determinística do JSON canônico extraído do CNIS.",
        "",
        "## Identificação e parâmetros",
        "",
        f"- Segurado: {ident.get('nome') or '-'}",
        f"- CPF/NIT: {ident.get('cpf') or ident.get('nit') or '-'}",
        f"- DER: {params.get('der') or 'não informada'}",
        f"- Sexo informado: {params.get('sexo') or 'não informado'}",
        "",
        "## Metodologia",
        "",
        "Foram apurados dias por segmento, descontadas sobreposições, aplicada a regra de mês cheio pós-EC 103/2019 e consolidadas remunerações concomitantes por competência.",
        "",
        "## Resultado do tempo de contribuição",
        "",
        f"- Total: {tempo['dias_liquidos']} dias ({tempo['amd']})",
        f"- Até 12/11/2019: {tempo['dias_pre_ec103']} dias ({tempo['amd_pre_ec103']})",
        f"- Desde 13/11/2019: {tempo['dias_pos_ec103']} dias ({tempo['amd_pos_ec103']})",
        "",
        "## Concomitâncias e períodos desconsiderados",
        "",
    ]
    if resultado["sobreposicoes"]:
        for item in resultado["sobreposicoes"]:
            linhas.append(f"- Vínculo {item['seq']} ({item['empregador']}): {item['dias_concomitantes']} dias descontados.")
    else:
        linhas.append("Nenhuma sobreposição descontada.")
    linhas += [
        "",
        "## Salários de contribuição e RMI",
        "",
        f"- Competências consolidadas: {len(resultado['competencias_consolidadas'])}",
        f"- Competências no PBC: {resultado['pbc']['quantidade_competencias']}",
        f"- Média do PBC: {_dinheiro(resultado['pbc']['media'])}",
        "",
        "## Regras de transição",
        "",
    ]
    if resultado["regras_transicao"]:
        for regra in resultado["regras_transicao"]:
            linhas.append(f"- **{regra['regra']}**: {regra['situacao']}. {regra['detalhe']}")
    else:
        linhas.append("Não analisadas por insuficiência de parâmetros ou porque não foram solicitadas.")
    linhas += ["", "## Inconsistências e ressalvas", ""]
    if resultado["avisos"]:
        linhas.extend(f"- {aviso}" for aviso in resultado["avisos"])
    else:
        linhas.append("Nenhum aviso automático.")
    linhas += [
        "",
        "## Conclusão técnica",
        "",
        "Os resultados são aritméticos e dependem da conferência do JSON contra o CNIS e dos documentos comprobatórios. A conclusão jurídica sobre o benefício permanece sujeita à análise do caso.",
        "",
    ]
    return "\n".join(linhas)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", help="JSON canônico produzido por extrair_cnis.py")
    parser.add_argument("--der", help="DER/data de corte em DD/MM/AAAA")
    parser.add_argument("--competencia-mps", help="competência dos fatores MPS em MM/AAAA")
    parser.add_argument("--sexo", choices=["M", "F"], help="sexo explicitamente informado")
    parser.add_argument("--expectativa-sobrevida", type=float, help="expectativa IBGE em anos")
    parser.add_argument("--sem-rmi", action="store_true", help="apura apenas tempo e competências, sem RMI")
    parser.add_argument("--relatorio", action="store_true", help="emite relatório Markdown em vez de JSON")
    parser.add_argument("--out", help="arquivo de saída; se omitido, escreve em stdout")
    args = parser.parse_args()

    try:
        input_path = Path(args.input_path)
        if input_path.suffix.lower() != ".json":
            raise ValueError("a entrada obrigatória deve ser um arquivo .json canônico")
        data = json.loads(input_path.read_text(encoding="utf-8"))
        resultado = analisar(data, args)
        saida = render_markdown(resultado) if args.relatorio else json.dumps(
            resultado, ensure_ascii=False, indent=2, default=_json_default
        ) + "\n"
        if args.out:
            Path(args.out).write_text(saida, encoding="utf-8")
        else:
            sys.stdout.write(saida)
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
