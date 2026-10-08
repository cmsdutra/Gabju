"""
extrair_cnis.py - Módulo 1 (Extração) da skill cnis-calculator.
Ingestão de Extratos CNIS em qualquer formato de entrada (.pdf nativo/escaneado com OCR local,
.txt já extraído por outro meio, ou .json já estruturado) e geração do JSON canônico
(filiado + vínculos + remunerações, com "especialidade" opcional por vínculo) — a única saída
deste módulo. O módulo 2 (analisar_cnis.py) consome exclusivamente esse JSON.

Absorve toda a carga cognitiva de reconhecimento de padrão (OCR, tabela posicional, texto
rotulado 1-campo-por-linha); o módulo 2 é determinístico e não faz ingestão.
"""

import os
import sys
import json
import argparse

from cnis_parser import parse_cnis_pdf, parse_cnis_text_file


def main():
    parser = argparse.ArgumentParser(
        description="Módulo 1 (Extração) da skill cnis-calculator: ingere um Extrato CNIS "
                     "(.pdf nativo/escaneado, .txt já extraído, ou .json já estruturado) e grava "
                     "o JSON canônico usado como entrada do módulo 2 (analisar_cnis.py)."
    )
    parser.add_argument("input_path", help="Caminho do Extrato CNIS: .pdf, .txt (texto já extraído por outro meio, ex. transcrição multimodal) ou .json (já estruturado, usado como pass-through/validação).")
    parser.add_argument("--out", default=None, help="Caminho do JSON canônico de saída. Padrão: <nome_do_arquivo>_cnis.json no mesmo diretório do arquivo de entrada.")
    parser.add_argument("--no-cache", action="store_true", help="Ignora e sobrescreve o cache de OCR (.cnis_cache ao lado do PDF) — força reextração completa.")

    args = parser.parse_args()

    input_path = os.path.abspath(args.input_path)
    if not os.path.exists(input_path):
        print(f"Erro: Arquivo não encontrado: {input_path}", file=sys.stderr)
        sys.exit(1)

    ext = os.path.splitext(input_path)[1].lower()
    print(f"[1/2] Extraindo dados do CNIS: {input_path}...")
    if ext == ".pdf":
        cnis_data = parse_cnis_pdf(input_path, use_cache=not args.no_cache)
    elif ext == ".txt":
        cnis_data = parse_cnis_text_file(input_path)
    elif ext == ".json":
        with open(input_path, "r", encoding="utf-8") as f:
            cnis_data = json.load(f)
    else:
        print(f"Erro: extensão '{ext}' não suportada. Use .pdf, .txt (texto já extraído) ou .json (estrutura já normalizada).", file=sys.stderr)
        sys.exit(1)

    filiado = cnis_data.get("filiado", {})
    vinculos = cnis_data.get("vinculos", [])
    print(f"      Identificado: {filiado.get('nome', '-')} (CPF: {filiado.get('cpf', '-')}) | Total de vínculos: {len(vinculos)}")

    if args.out:
        out_path = os.path.abspath(args.out)
    else:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        out_path = os.path.join(os.path.dirname(input_path), f"{base_name}_cnis.json")
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    print("[2/2] Gravando JSON canônico...")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cnis_data, f, ensure_ascii=False, indent=2)

    print(f"\nSucesso! JSON canônico gerado: {out_path}")
    for aviso in cnis_data.get("avisos_extracao", []):
        print(f"AVISO: {aviso}")
    print("Para anotar fator de especialidade (1.4/1.2 etc.), edite manualmente o campo \"especialidade\" do(s) vínculo(s) relevante(s) neste JSON antes de rodar o módulo 2.")
    print("Módulo 2 (cálculo): python3 analisar_cnis.py \"" + out_path + "\" [--der DD/MM/AAAA] [--sexo M|F] [--expectativa-sobrevida <anos>] [--sem-rmi] [--relatorio]")


if __name__ == "__main__":
    main()
