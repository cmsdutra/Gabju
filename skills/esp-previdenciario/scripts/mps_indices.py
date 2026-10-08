"""
mps_indices.py - Download, parsing e cache dos índices oficiais do Ministério da Previdência Social
(Tabela de atualização monetária dos salários-de-contribuição para apuração do salário-de-benefício - Art. 33 Decreto 3.048/99).
"""

import os
import re
import json
import urllib.request
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any

from parametros_externos import diretorio_cache

MPS_URL = "https://www.gov.br/previdencia/pt-br/assuntos/previdencia-social/legislacao/indice-de-atualizacao-das-contribuicoes-para-calculo-do-salario-de-beneficio"
# Cache pré-carregado que acompanha a skill (somente leitura: num plugin, a pasta da skill pode ser
# sobrescrita a cada atualização). Downloads novos vão para a pasta de cache do usuário.
BUNDLED_CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", ".cache")
DEFAULT_CACHE_DIR = os.path.join(diretorio_cache(), "mps")

def get_available_mps_tables() -> List[Dict[str, str]]:
    """
    Varre a página do Ministério da Previdência Social e retorna a lista de tabelas disponíveis ordenadas por competência (mais recente primeiro).
    """
    req = urllib.request.Request(MPS_URL, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return []

    # Busca links com padrão fatores_de_atualizacao_MM_AAAA_art_33.xlsx
    pattern = r'href=["\']([^"\']*fatores_de_atualizacao[_-](\d{2})_(\d{4})[^"\']*\.xlsx)["\']'
    matches = re.findall(pattern, html, re.IGNORECASE)
    results = []
    seen = set()
    for url, m, y in matches:
        comp = f"{int(m):02d}/{y}"
        if comp not in seen:
            seen.add(comp)
            results.append({
                "competencia": comp,
                "ano": int(y),
                "mes": int(m),
                "url": url
            })
    
    # Ordenar decrescente (ano desc, mes desc)
    results.sort(key=lambda x: (x["ano"], x["mes"]), reverse=True)
    return results

def parse_mps_xlsx(xlsx_path: str) -> Dict[str, Any]:
    """
    Analisa deterministicamente o arquivo .xlsx oficial do MPS usando zipfile e XML (sem dependências externas).
    Retorna metadados (referência, portaria) e dicionário { 'MM/AAAA': fator_float }.
    """
    with zipfile.ZipFile(xlsx_path, "r") as z:
        # 1. Carregar sharedStrings se existirem
        shared_strings = []
        if "xl/sharedStrings.xml" in z.namelist():
            tree_ss = ET.fromstring(z.read("xl/sharedStrings.xml"))
            ns = {"ns": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
            for si in tree_ss.findall("ns:si", ns):
                t = si.find("ns:t", ns)
                shared_strings.append(t.text if (t is not None and t.text is not None) else "")

        # 2. Carregar sheet1.xml
        sheet = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
        ns = {"ns": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

        rows = sheet.findall(".//ns:row", ns)
        portaria_info = ""
        ref_mes = ""
        fatores = {}

        for row in rows:
            cells = row.findall("ns:c", ns)
            row_vals = []
            for c in cells:
                t_attr = c.attrib.get("t")
                v = c.find("ns:v", ns)
                val = v.text if v is not None else ""
                if t_attr == "s" and val.isdigit():
                    idx = int(val)
                    val = shared_strings[idx] if idx < len(shared_strings) else ""
                row_vals.append(val)

            if not row_vals:
                continue

            # Captura cabeçalho de Portaria / Referência
            for val_str in row_vals:
                if "Portaria" in val_str or "Mês de Referência" in val_str:
                    portaria_info = val_str.strip()

            # Captura linhas de dados
            c0 = row_vals[0].strip() if len(row_vals) > 0 else ""
            c1 = row_vals[1].strip() if len(row_vals) > 1 else ""

            if c0.isdigit() and c1:
                try:
                    # Data serial do Excel (1899-12-30 + dias)
                    dt = datetime(1899, 12, 30) + timedelta(days=int(c0))
                    comp_key = dt.strftime("%m/%Y")
                    fator_val = float(c1.replace(",", "."))
                    fatores[comp_key] = fator_val
                except Exception:
                    pass

        return {
            "referencia_portaria": portaria_info,
            "total_competencias": len(fatores),
            "fatores": fatores
        }

def get_mps_indices(competencia_ref: Optional[str] = None, cache_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Obtém a tabela de índices MPS.
    Se competencia_ref for omitida, busca a mais recente disponível.
    Utiliza cache local (pasta do usuário + cache pré-carregado da skill) para execução rápida e offline.
    """
    if cache_dir is None:
        cache_dir = DEFAULT_CACHE_DIR
    leitura = [cache_dir] + ([BUNDLED_CACHE_DIR] if os.path.isdir(BUNDLED_CACHE_DIR) else [])
    try:
        os.makedirs(cache_dir, exist_ok=True)
    except OSError:
        pass

    def _ler_cache(nome: str) -> Optional[Dict[str, Any]]:
        for pasta in leitura:
            caminho = os.path.join(pasta, nome)
            if os.path.exists(caminho):
                with open(caminho, "r", encoding="utf-8") as f:
                    return json.load(f)
        return None

    # 1. Verificar se já existe em cache
    if competencia_ref:
        em_cache = _ler_cache(f"fatores_mps_{competencia_ref.replace('/', '_')}.json")
        if em_cache is not None:
            return em_cache

    # 2. Descobrir tabelas no portal ou usar mais recente
    tables = get_available_mps_tables()
    target_table = None

    if competencia_ref:
        for t in tables:
            if t["competencia"] == competencia_ref:
                target_table = t
                break
    elif tables:
        target_table = tables[0] # mais recente

    if target_table:
        comp_clean = target_table["competencia"].replace("/", "_")
        em_cache = _ler_cache(f"fatores_mps_{comp_clean}.json")
        if em_cache is not None:
            return em_cache

        cache_json = os.path.join(cache_dir, f"fatores_mps_{comp_clean}.json")
        cache_xlsx = os.path.join(cache_dir, f"fatores_mps_{comp_clean}.xlsx")
        try:
            req = urllib.request.Request(target_table["url"], headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                with open(cache_xlsx, "wb") as f_out:
                    f_out.write(resp.read())
            
            data = parse_mps_xlsx(cache_xlsx)
            data["competencia_ref"] = target_table["competencia"]
            data["url_fonte"] = target_table["url"]

            with open(cache_json, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return data
        except Exception as e:
            pass

    # 3. Fallback: cache JSON mais recente (por ano/mês, não pelo nome do arquivo) entre as pastas
    def _ano_mes(caminho: str) -> Tuple[int, int]:
        m = re.match(r"fatores_mps_(\d{2})_(\d{4})\.json$", os.path.basename(caminho))
        return (int(m.group(2)), int(m.group(1))) if m else (0, 0)

    cached_files = []
    for pasta in leitura:
        if os.path.isdir(pasta):
            cached_files += [os.path.join(pasta, f) for f in os.listdir(pasta)
                             if f.startswith("fatores_mps_") and f.endswith(".json")]
    if cached_files:
        cached_files.sort(key=_ano_mes, reverse=True)
        with open(cached_files[0], "r", encoding="utf-8") as f:
            return json.load(f)

    return {"competencia_ref": "08/2026", "fatores": {}, "referencia_portaria": ""}

if __name__ == "__main__":
    import sys
    print("Buscando índices MPS...")
    res = get_mps_indices()
    print(f"Competência Ref: {res.get('competencia_ref')}")
    print(f"Portaria: {res.get('referencia_portaria')}")
    print(f"Total de fatores carregados: {len(res.get('fatores', {}))}")
    sample_comps = ["07/1994", "12/1995", "01/2000", "11/2019", "07/2026"]
    for sc in sample_comps:
        print(f"   {sc} -> {res.get('fatores', {}).get(sc)}")
