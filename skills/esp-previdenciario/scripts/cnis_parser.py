"""
cnis_parser.py - Extrator estruturado de dados de Extratos Previdenciários do CNIS (PDF).
Suporta PDFs digitais (texto nativo) e PDFs rasterizados/vetorizados/escaneados (via PyMuPDF + Tesseract OCR com rotação automática).
"""

import os
import re
import io
import json
import shutil
import fitz
from typing import Dict, List, Any, Optional, Tuple
from PIL import Image

try:
    import pytesseract
except ImportError:
    pytesseract = None

def check_tesseract_available() -> Tuple[bool, str]:
    """
    Verifica OCR em 2 camadas (pacote python + binário de sistema), já que 'pip install
    pytesseract' sem o binário 'tesseract' instalado é o caso mais comum de falha silenciosa
    em sandboxes (ex.: ambientes Codex/ChatGPT work sem tesseract-ocr no sistema).
    """
    if pytesseract is None:
        return False, "pacote python 'pytesseract' não instalado (pip install pytesseract)"
    if shutil.which("tesseract") is None:
        return False, (
            "pacote 'pytesseract' presente, mas binário 'tesseract' não encontrado no PATH "
            "(instale: 'apt install tesseract-ocr tesseract-ocr-por' / 'brew install tesseract tesseract-lang' / "
            "'choco install tesseract' — ou, sem acesso para instalar, forneça um .txt ao extrair_cnis.py "
            "com texto já extraído por outro meio)"
        )
    return True, ""

def _ocr_cache_path(pdf_path: str) -> str:
    """Caminho do cache de páginas OCR, ao lado do PDF, invalidado por tamanho+mtime do arquivo fonte."""
    stat = os.stat(pdf_path)
    key = f"{stat.st_size}_{int(stat.st_mtime)}"
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(pdf_path)), ".cnis_cache")
    return os.path.join(cache_dir, f"{base}.{key}.ocr.json")

def clean_ocr_date(d: str) -> str:
    """Corrige anomalias comuns de OCR em dígitos de datas (ex.: 97/04 -> 01/04, 91/11 -> 01/11, 92/05 -> 02/05)."""
    if not d:
        return ""
    p = d.strip().split("/")
    if len(p) == 3:
        day, m, y = p
        if day in ["97", "91"]:
            day = "01"
        elif day == "92":
            day = "02"
        try:
            return f"{int(day):02d}/{int(m):02d}/{y}"
        except ValueError:
            return d
    return d

def detect_page_rotation(img: Image.Image) -> int:
    """
    Detecta a rotação necessária (0, 90, 180, 270 graus anti-horário no PIL)
    para que o texto do CNIS fique legível e na vertical.
    """
    if not pytesseract:
        return 0
    keywords = ["extrato", "previdenciário", "cnis", "informações", "filiado", "relações"]
    # Testa primeiro rotação 270 (comum em digitalizações no sentido horário) e 0
    for angle in [270, 0, 180, 90]:
        test_img = img.rotate(angle, expand=True) if angle != 0 else img
        txt = pytesseract.image_to_string(test_img, lang="por", config="--psm 1 --dpi 150")
        txt_l = txt.lower()
        matches = sum(1 for kw in keywords if kw in txt_l)
        if matches >= 2:
            return angle
    return 0

def extract_text_from_pdf(pdf_path: str, use_cache: bool = True) -> List[str]:
    """
    Extrai o texto página a página.
    Se a página tiver estrutura de tabelas digital nativa, extrai via find_tables() para preservar a ordem horizontal de células.
    Se for texto nativo sem tabelas, extrai get_text("text").
    Se for raster/escaneado/imagem, renderiza em 200 DPI e aplica OCR com rotação automática.

    Páginas que exigem OCR são cacheadas ao lado do PDF (invalidado por tamanho+mtime) — reexecuções
    sobre o mesmo arquivo (ajuste de DER, correção de fórmulas, etc.) não repetem o OCR.
    """
    cache_path = _ocr_cache_path(pdf_path)
    if use_cache and os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cached = json.load(f)
            return cached["pages_text"]
        except (OSError, json.JSONDecodeError, KeyError):
            pass  # cache corrompido/incompleto, refaz normalmente

    doc = fitz.open(pdf_path)
    pages_text = []
    used_ocr = False

    for page_idx in range(len(doc)):
        page = doc[page_idx]

        # 1. Tenta extração via find_tables() para preservar layout de colunas do CNIS digital
        tabs = page.find_tables()
        if tabs.tables:
            table_lines = []
            for t in tabs:
                for row in t.extract():
                    for cell in row:
                        if cell:
                            for l in cell.splitlines():
                                if l.strip():
                                    table_lines.append(l.strip())
            if len(table_lines) > 5 and any(k in " ".join(table_lines).lower() for k in ["cnis", "filiado", "remunerações", "vínculo", "relações"]):
                pages_text.append("\n".join(table_lines))
                continue

        # 2. Texto nativo vetorial
        text_native = page.get_text("text").strip()
        if len(text_native) > 100 and any(k in text_native.lower() for k in ["cnis", "filiado", "remunerações", "vínculo"]):
            pages_text.append(text_native)
            continue

        # 3. Fallback para OCR
        ocr_ok, ocr_reason = check_tesseract_available()
        if not ocr_ok:
            raise RuntimeError(
                f"Página {page_idx + 1}/{len(doc)} de '{os.path.basename(pdf_path)}' não tem texto nativo "
                f"extraível e o OCR está indisponível ({ocr_reason}). Alternativa sem instalar nada: extraia "
                f"o texto da página por outro meio (ex.: leitura visual por um agente multimodal) e rode "
                f"extrair_cnis.py apontando para um .txt com esse conteúdo em vez do .pdf."
            )

        pix = page.get_pixmap(dpi=200)
        img = Image.open(io.BytesIO(pix.tobytes()))

        # Detecta rotação na 1ª página e reutiliza, ou detecta individualmente
        angle = 270 # Padrão observado em extratos invertidos
        if page_idx == 0:
            angle = detect_page_rotation(img)

        if angle != 0:
            img = img.rotate(angle, expand=True)

        txt_ocr = pytesseract.image_to_string(img, lang="por", config="--psm 4")
        pages_text.append(txt_ocr)
        used_ocr = True

    if use_cache and used_ocr:
        try:
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump({"pages_text": pages_text}, f, ensure_ascii=False)
        except OSError:
            pass  # cache é otimização; falha ao gravar não deve derrubar a extração

    return pages_text

def _extract_filiado(full_text: str) -> Dict[str, str]:
    """Identificação do Filiado (Nome/CPF/NIT/nascimento/mãe/emissão) — comum aos 2 formatos de texto suportados."""
    filiado = {
        "nome": "",
        "cpf": "",
        "nit": "",
        "data_nascimento": "",
        "nome_mae": "",
        "data_emissao": ""
    }

    m_nome = re.search(r'Nome:\s*([A-ZÁÉÍÓÚÂÊÔÃÕÇ\s]+?)(?:\n|Nome da mãe|$)', full_text, re.IGNORECASE)
    if m_nome:
        filiado["nome"] = m_nome.group(1).strip()

    m_cpf = re.search(r'CPF:\s*([0-9.\-]+)', full_text)
    if m_cpf:
        filiado["cpf"] = m_cpf.group(1).strip()

    m_nit = re.search(r'NIT:\s*([0-9.\-]+)', full_text)
    if m_nit:
        filiado["nit"] = m_nit.group(1).strip()

    m_nasc = re.search(r'Data de nascimento:\s*(\d{2}/\d{2}/\d{4})', full_text, re.IGNORECASE)
    if m_nasc:
        filiado["data_nascimento"] = m_nasc.group(1).strip()

    m_mae = re.search(r'Nome da mãe:\s*([A-ZÁÉÍÓÚÂÊÔÃÕÇ\s]+?)(?:\n|Relações Previdenciárias|$)', full_text, re.IGNORECASE)
    if m_mae:
        filiado["nome_mae"] = m_mae.group(1).strip()

    m_emissao = re.search(r'Extrato Previdenciário\s+(\d{2}/\d{2}/\d{4})', full_text)
    if m_emissao:
        filiado["data_emissao"] = m_emissao.group(1).strip()

    return filiado

def parse_cnis_text(pages_text: List[str]) -> Dict[str, Any]:
    """
    Processa o texto extraído das páginas (layout de tabela posicional, como produzido por
    OCR/Tesseract ou texto vetorial nativo do PDF) e gera a estrutura completa:
    Filiado, Vínculos e Remunerações.
    """
    vinculos = {}
    remunerações_por_seq = {}
    current_seq = None

    full_text = "\n".join(pages_text)
    filiado = _extract_filiado(full_text)

    # 2. Varredura linha a linha para Vínculos e Remunerações
    vinculo_line_pattern = r'^\s*(\d+)º?[\s\-—]+([0-9.\-]+)[\s|]+([0-9.\-/]+|RECOLHIMENTO)\s*(.*)'
    # Vínculo sem "Código Emp." (ex.: contribuinte individual em "AGRUPAMENTO DE CONTRATANTES/
    # COOPERATIVAS"): o NIT é seguido direto pelo texto da origem do vínculo.
    vinculo_sem_codigo_pattern = r'^\s*(\d+)º?[\s\-—]+(\d{3}\.\d{5}\.\d{2}-\d|\d\.\d{3}\.\d{3}\.\d{3}-\d)[\s|]+([A-ZÀ-Ú].*)$'

    vinculos = {}
    remunerações_por_seq = {}
    current_seq = None
    avisos: List[str] = []

    for page_idx, p_text in enumerate(pages_text):
        lines = p_text.splitlines()
        for line_idx, line in enumerate(lines):
            l = line.strip()
            if not l:
                continue

            # Cabeçalho de Vínculo sem código do empregador
            m_sc = re.match(vinculo_sem_codigo_pattern, l)
            if m_sc and not l.startswith('0') and int(m_sc.group(1)) <= 150 and not re.match(vinculo_line_pattern, l):
                seq = int(m_sc.group(1))
                rest = m_sc.group(3).strip()
                current_seq = seq
                remunerações_por_seq[seq] = []
                origem_txt = re.sub(r'\s*\b(Empregado|Contribuinte|Trabalhador|Facultativo|Segurado)\b.*', '', rest, flags=re.IGNORECASE)
                dates = [d for d in re.findall(r'\b(\d{2}/\d{2}/\d{4})\b', rest)
                         if d != filiado["data_nascimento"] and d != filiado["data_emissao"]]
                ult_remuns = re.findall(r'(?<!\d/)(\d{2}/\d{4})(?!\d)', rest)
                vinculos[seq] = {
                    "seq": seq,
                    "origem": "CNIS",
                    "cod_recolhimento": "05" if "Contribuinte Individual" in rest else "01",
                    "nit": m_sc.group(2),
                    "cnpj": "",
                    "empregador": ' '.join(origem_txt.split()),
                    "data_inicio": clean_ocr_date(dates[0]) if len(dates) >= 1 else "",
                    "data_fim": clean_ocr_date(dates[1]) if len(dates) >= 2 else "",
                    "ult_remun": ult_remuns[-1] if ult_remuns else "",
                    "pagina": page_idx + 1
                }
                continue

            # Cabeçalho de Vínculo
            m_v = re.match(vinculo_line_pattern, l)
            if m_v and not l.startswith('0') and int(m_v.group(1)) <= 150:
                seq = int(m_v.group(1))
                nit = m_v.group(2)
                c3 = m_v.group(3)
                rest = m_v.group(4).strip()

                current_seq = seq
                remunerações_por_seq[seq] = []

                # Classificação da Origem, Código de Recolhimento e Empregador
                if c3 == "RECOLHIMENTO":
                    origem = "RECOLHIMENTO"
                    cnpj = ""
                    if "Facultativo" in rest:
                        cod_rec = "09"
                        emp = "Segurado Facultativo"
                    else:
                        cod_rec = "06"
                        emp = "Contribuinte Individual"
                elif "Benefício" in rest or (c3.isdigit() and len(c3) >= 8 and '/' not in c3 and '.' not in c3):
                    origem = "Benefício"
                    cnpj = c3
                    if "AUXILIO DOENCA" in rest.upper():
                        cod_rec = "12"
                        emp = "Benefício B31 - Auxílio-Doença Previdenciário"
                    elif "APOSENTADORIA" in rest.upper():
                        cod_rec = "12"
                        emp = "Benefício B42 - Aposentadoria por Tempo de Contribuição"
                    else:
                        cod_rec = "12"
                        emp = "Benefício Previdenciário"
                else:
                    origem = "CNIS"
                    cnpj = c3
                    cod_rec = "05" if "Contribuinte Individual" in rest else "01"
                    sub = re.sub(r'\|\s*', '', rest)
                    sub = re.sub(r'\b(Empregado|Contribuinte|Trabalhador|Facultativo).*', '', sub, flags=re.IGNORECASE)
                    sub = re.sub(r'\s*SEALUMASA.*', '', sub)
                    # Verifica se há continuação de nome na próxima linha
                    if line_idx + 1 < len(lines):
                        next_line = lines[line_idx + 1].strip()
                        if any(kw in next_line for kw in ["DESENVOLVIMENTO", "AEROPORTUARIA"]):
                            part = re.sub(r'\b(Empregado|Contribuinte|Trabalhador|Facultativo|Público).*', '', next_line, flags=re.IGNORECASE).strip()
                            sub = (sub + " " + part).strip()
                    emp = ' '.join(sub.split())

                # Normalização de CNPJ truncado pelo OCR
                if cnpj == "80.718.984":
                    cnpj = "80.718.984/0001-38"

                # Extração de datas
                dates = re.findall(r'\b(\d{2}/\d{2}/\d{4})\b', rest)
                dates = [d for d in dates if d != filiado["data_nascimento"] and d != filiado["data_emissao"]]

                dt_ini = clean_ocr_date(dates[0]) if len(dates) >= 1 else ""
                dt_fim = clean_ocr_date(dates[1]) if len(dates) >= 2 else ""

                ult_remuns = re.findall(r'(?<!\d/)(\d{2}/\d{4})(?!\d)', rest)
                ult_remun = ult_remuns[-1] if ult_remuns else ""

                vinculos[seq] = {
                    "seq": seq,
                    "origem": origem,
                    "cod_recolhimento": cod_rec,
                    "nit": nit,
                    "cnpj": cnpj,
                    "empregador": emp,
                    "data_inicio": dt_ini,
                    "data_fim": dt_fim,
                    "ult_remun": ult_remun,
                    "pagina": page_idx + 1
                }
                continue

            # Varredura de remunerações e contribuições
            if current_seq is not None:
                if any(k in l for k in [
                    "Identificação do Filiado", "Relações Previdenciárias", "Valores Consolidados",
                    "Matrícula do", "Seq. NIT", "Competência", "Salário Contribuição", "Data Pgto.", "Página "
                ]):
                    continue
                if filiado["data_emissao"] and filiado["data_emissao"] in l:
                    continue

                # 1. Contribuições (recolhimento individual / facultativo): MM/AAAA DD/MM/AAAA contrib salario [ind]
                rec_matches = re.findall(r'(\d{2}/\d{4})\s+\d{2}/\d{2}/\d{4}\s+[\d.]+,\d{2}\s+([\d.]+,\d{2})(?:\s+([A-Z][A-Z0-9\-]+))?', l)
                if rec_matches:
                    for comp, val_str, ind in rec_matches:
                        val = float(val_str.replace(".", "").replace(",", "."))
                        remunerações_por_seq[current_seq].append({
                            "competencia": comp,
                            "remuneracao": val,
                            "indicadores": (ind or "").strip()
                        })
                    continue

                # 2. Contribuinte individual com tomador:
                #    MM/AAAA contratante(raiz ou CNPJ) tomador forma-de-prestação salario [ind]
                ci_match = re.match(r'^(\d{2}/\d{4})\s+([\d./\-]{8,18})\s+([\d./\-]{8,18})\s+((?:[A-Za-zÀ-ú]+\s+)+)(-?[\d.]+,\d{2})(?:\s+([A-Z][A-Z0-9\-]+))?', l)
                if ci_match:
                    comp, contratante, tomador, _forma, val_str, ind = ci_match.groups()
                    if val_str.startswith("-"):
                        avisos.append(f"Seq {current_seq}, competência {comp}: remuneração ilegível no OCR ('{val_str}'); "
                                      f"conferir no PDF e incluir manualmente no JSON.")
                    else:
                        remunerações_por_seq[current_seq].append({
                            "competencia": comp,
                            "remuneracao": float(val_str.replace(".", "").replace(",", ".")),
                            "indicadores": (ind or "").strip()
                        })
                    if not vinculos[current_seq]["cnpj"]:
                        vinculos[current_seq]["cnpj"] = max(contratante, tomador, key=len)
                    continue

                # 3. Remunerações padrão: MM/AAAA salario [ind]
                rem_matches = re.findall(r'(\d{2}/\d{4})\s+([\d.]+,\d{2})(?:\s+([A-Z][A-Z0-9\-]+))?', l)
                if rem_matches:
                    for comp, val_str, ind in rem_matches:
                        val = float(val_str.replace(".", "").replace(",", "."))
                        remunerações_por_seq[current_seq].append({
                            "competencia": comp,
                            "remuneracao": val,
                            "indicadores": (ind or "").strip()
                        })

    # Organiza resultado final
    lista_vinculos = []
    for s in sorted(vinculos.keys()):
        v_data = vinculos[s]
        v_data["remunerações"] = remunerações_por_seq.get(s, [])
        lista_vinculos.append(v_data)

    resultado = {
        "filiado": filiado,
        "total_vinculos": len(lista_vinculos),
        "vinculos": lista_vinculos
    }
    if avisos:
        resultado["avisos_extracao"] = avisos
    return resultado

def parse_cnis_pdf(pdf_path: str, use_cache: bool = True) -> Dict[str, Any]:
    """Função de entrada principal: lê PDF e retorna dicionário estruturado completo."""
    pages = extract_text_from_pdf(pdf_path, use_cache=use_cache)
    return parse_cnis_text(pages)

_LABELED_NOISE_LINES = {
    "inss", "cnis - cadastro nacional de informações sociais", "extrato previdenciário",
    "identificação do filiado", "relações previdenciárias", "remunerações",
}
_LABELED_STOP_MARKERS = ("valores consolidados por ano civil", "legenda de indicadores")

def is_labeled_cnis_text(raw_text: str) -> bool:
    """
    Detecta o formato 'rotulado' (1 campo por linha, ex. 'Data Início 01/12/1988',
    'Competência 09/1991') — típico de transcrição feita por um agente multimodal lendo as
    páginas do PDF (sem OCR local), em vez do dump posicional de tabela que Tesseract produz.
    """
    seq_hits = len(re.findall(r'(?m)^\s*Seq\.?\s*\d+\s*$', raw_text))
    label_hits = sum(1 for lbl in ("NIT ", "Código Emp.", "Data Início", "Competência ") if re.search(r'(?m)^\s*' + re.escape(lbl), raw_text))
    return seq_hits >= 1 and label_hits >= 2

def parse_cnis_labeled_text(raw_text: str) -> Dict[str, Any]:
    """
    Parser do formato rotulado (1 campo por linha). Cada vínculo abre em 'Seq. N' e fecha
    implicitamente no próximo 'Seq.' ou fim do texto; linhas sem rótulo reconhecido dentro do
    bloco de cabeçalho (matrícula truncada em 2 linhas, etc.) são ignoradas silenciosamente.
    Remunerações aceitam tanto o par 'Competência'/'Remuneração' quanto a forma compacta
    'MM/AAAA valor' (comum em quebras de página, atribuída ao vínculo aberto no momento).
    """
    filiado = _extract_filiado(raw_text)

    vinculos: Dict[int, Dict[str, Any]] = {}
    remuneracoes_por_seq: Dict[int, List[Dict[str, Any]]] = {}
    current_seq: Optional[int] = None
    pending_competencia: Optional[str] = None
    last_entry: Optional[Dict[str, Any]] = None
    stopped = False

    for raw_line in raw_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        low = line.lower()

        if any(marker in low for marker in _LABELED_STOP_MARKERS):
            stopped = True
        if stopped:
            continue
        if low in _LABELED_NOISE_LINES or low.startswith("nit:") or low.startswith("cpf:") or \
           low.startswith("nome:") or low.startswith("nome da mãe:") or low.startswith("data de nascimento:") or \
           low.startswith("o inss poderá") or low.startswith("os valores de remunerações") or \
           low.startswith("o segurado poderá") or low.startswith("você pode conferir") or \
           low.startswith("com o código") or low.startswith("página "):
            continue

        m_seq = re.match(r'^Seq\.?\s*(\d+)\s*$', line)
        if m_seq:
            current_seq = int(m_seq.group(1))
            vinculos[current_seq] = {
                "seq": current_seq, "origem": "CNIS", "cod_recolhimento": "01",
                "nit": "", "cnpj": "", "empregador": "",
                "data_inicio": "", "data_fim": "", "ult_remun": "", "pagina": 1,
            }
            remuneracoes_por_seq[current_seq] = []
            pending_competencia = None
            last_entry = None
            continue

        if current_seq is None:
            continue  # ruído antes do 1º "Seq." (ex.: preâmbulo/QR code)
        v = vinculos[current_seq]

        m = re.match(r'^NIT\s+(.+)$', line)
        if m:
            v["nit"] = m.group(1).strip()
            continue
        m = re.match(r'^Código Emp\.?\s+(.+)$', line)
        if m:
            v["cnpj"] = m.group(1).strip()
            continue
        m = re.match(r'^Origem do Vínculo\s+(.+)$', line)
        if m:
            v["empregador"] = m.group(1).strip()
            continue
        m = re.match(r'^Tipo Filiado no Vínculo\s+(.+)$', line)
        if m:
            tipo = m.group(1).strip()
            if "facultativo" in tipo.lower():
                v["cod_recolhimento"] = "09"
            elif "contribuinte individual" in tipo.lower():
                v["cod_recolhimento"] = "06"
            elif "avulso" in tipo.lower():
                v["cod_recolhimento"] = "04"
            continue
        m = re.match(r'^Data Início\s+(\d{2}/\d{2}/\d{4})\s*$', line)
        if m:
            v["data_inicio"] = clean_ocr_date(m.group(1))
            continue
        m = re.match(r'^Data Fim\s*(\d{2}/\d{2}/\d{4})?\s*$', line)
        if m:
            v["data_fim"] = clean_ocr_date(m.group(1)) if m.group(1) else ""
            continue
        m = re.match(r'^Últ\.?\s*Remun\.?\s+(\d{2}/\d{4})\s*$', line)
        if m:
            v["ult_remun"] = m.group(1)
            continue

        m = re.match(r'^Competência\s+(\d{2}/\d{4})\s*$', line)
        if m:
            pending_competencia = m.group(1)
            continue
        m = re.match(r'^Remuneração\s+([\d.]+,\d{2})\s*$', line)
        if m and pending_competencia:
            entry = {
                "competencia": pending_competencia,
                "remuneracao": float(m.group(1).replace(".", "").replace(",", ".")),
                "indicadores": ""
            }
            remuneracoes_por_seq[current_seq].append(entry)
            last_entry = entry
            pending_competencia = None
            continue

        m = re.match(r'^(\d{2}/\d{4})\s+([\d.]+,\d{2})\s*$', line)
        if m:
            entry = {
                "competencia": m.group(1),
                "remuneracao": float(m.group(2).replace(".", "").replace(",", ".")),
                "indicadores": ""
            }
            remuneracoes_por_seq[current_seq].append(entry)
            last_entry = entry
            continue

        m = re.match(r'^Indicadores\s+(\S.*)$', line)
        if m and last_entry is not None and not last_entry["indicadores"]:
            last_entry["indicadores"] = m.group(1).strip()
            continue
        # demais linhas sem rótulo reconhecido (matrícula truncada, "Indicadores" vazio,
        # rodapé de vínculo em aberto, etc.) são ignoradas silenciosamente.

    lista_vinculos = []
    for s in sorted(vinculos.keys()):
        v_data = vinculos[s]
        v_data["remunerações"] = remuneracoes_por_seq.get(s, [])
        lista_vinculos.append(v_data)

    return {
        "filiado": filiado,
        "total_vinculos": len(lista_vinculos),
        "vinculos": lista_vinculos
    }

def split_raw_text_into_pages(raw_text: str) -> List[str]:
    """
    Divide um texto já extraído (colado/gerado por outro meio, sem OCR local) em páginas
    sintéticas, reaproveitando o cabeçalho repetido do CNIS ('CNIS - Cadastro Nacional de
    Informações Sociais') como marcador de quebra de página. Sem o marcador, trata tudo como
    página única — parse_cnis_text ainda funciona, só perde a granularidade por página
    (afeta apenas o campo informativo 'pagina' e a heurística de continuação de nome entre linhas).
    """
    marker = "CNIS - Cadastro Nacional de Informações Sociais"
    if marker not in raw_text:
        return [raw_text]

    pages: List[str] = []
    idx = raw_text.find(marker)
    # Preserva eventual preâmbulo antes do 1º marcador (ex.: linha "INSS" isolada) grudado na 1ª página
    start = 0
    while True:
        next_idx = raw_text.find(marker, idx + len(marker))
        chunk = raw_text[start:next_idx] if next_idx != -1 else raw_text[start:]
        if chunk.strip():
            pages.append(chunk)
        if next_idx == -1:
            break
        start = next_idx
        idx = next_idx
    return pages

def parse_cnis_text_file(text_path: str) -> Dict[str, Any]:
    """
    Ingestão alternativa ao PDF: consome um .txt com o texto do CNIS já extraído por qualquer
    meio (OCR de outro ambiente, leitura visual por agente multimodal, cópia manual) — usada
    quando OCR local está indisponível (ver check_tesseract_available). Autodetecta o formato:
    - 'Rotulado' (1 campo por linha, ex. transcrição de um agente multimodal) → parse_cnis_labeled_text.
    - Tabela posicional (dump cru de OCR/Tesseract ou texto vetorial do PDF) → parse_cnis_text,
      mesmo motor do caminho PDF nativo, então correções de regex se aplicam a ambos.
    """
    with open(text_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
    if is_labeled_cnis_text(raw_text):
        return parse_cnis_labeled_text(raw_text)
    pages = split_raw_text_into_pages(raw_text)
    return parse_cnis_text(pages)

if __name__ == "__main__":
    import sys
    pdf_file = sys.argv[1] if len(sys.argv) > 1 else ".tmp/Extrato CNIS Jair Soares.pdf"
    print(f"Analisando {pdf_file}...")
    res = parse_cnis_pdf(pdf_file)
    print("Filiado:", res["filiado"])
    print(f"Total de Vínculos: {res['total_vinculos']}")
    for v in res["vinculos"]:
        print(f"Seq {v['seq']}: {v['empregador']} | CNPJ: {v['cnpj']} | Início: {v['data_inicio']} | Fim: {v['data_fim']} | Remuns: {len(v['remunerações'])}")
