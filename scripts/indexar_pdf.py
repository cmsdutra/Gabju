#!/usr/bin/env python3
"""Indexador navegável de PDFs processuais longos.

Extrai e indexa páginas de documentos em formato PDF, preservando a
correspondência física de páginas, identificando IDs processuais em
cabeçalhos e conteúdos, aplicando OCR seletivamente quando necessário,
e produzindo um índice navegável e fragmentos textuais menores.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Sequence

# Metadados de versão
SCHEMA_VERSION = "1.0.0"
SCRIPT_VERSION = "1.0.0"

# Detecção opcional de bibliotecas
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    import pypdf
except ImportError:
    pypdf = None

try:
    from PIL import Image
except ImportError:
    Image = None

try:
    import pytesseract
except ImportError:
    pytesseract = None


class IndexadorPdfError(Exception):
    """Erro base para falhas do indexador de PDF."""


class PdfNaoEncontradoError(IndexadorPdfError):
    """Arquivo PDF não foi localizado."""


class PdfInvalidoError(IndexadorPdfError):
    """Arquivo PDF inválido ou corrompido."""


class PdfProtegidoError(IndexadorPdfError):
    """Arquivo PDF protegido por senha ou criptografia."""


class DependenciaAusenteError(IndexadorPdfError):
    """Dependência necessária para a operação não está instalada."""


# Expressões regulares para detecção de IDs processuais
RE_DOCUMENTO_ID = re.compile(r"(?i)\bDocumento\s+id[:.]?\s*(\d{4,})\b")
RE_NUM_ID = re.compile(r"(?i)\bNum\.\s*(\d{4,})(?:\s*-\s*P[aá]g\.\s*\d+)?\b")
RE_NUMERO_DOC = re.compile(r"(?i)\bN[uú]mero\s+do\s+[Dd]ocumento[:.]?\s*(\d{4,})\b")
RE_ID_HEADER = re.compile(r"(?i)\bId[:.]?\s*(\d{5,})\b")
RE_SUMARIO_LINE = re.compile(
    r"(?i)(?:^|\n)[ \t]*(?:[0-9]+[.\-)]|[•\-\*])?[ \t]*([^\n\r]+?)\s*[-–—:]\s*(?:Documento\s+id|Num\.|Id)?\s*(\d{4,})"
)

# Marcadores típicos de início e fim de peça processual
RE_INICIO_PECA = re.compile(
    r"(?i)\b(?:EXCELENT[ÍI]SSIMO|PODER JUDICI[ÁA]RIO|JUSTI[ÇC]A FEDERAL|TRIBUNAL REGIONAL|"
    r"PETI[ÇC][ÃA]O|CONTESTA[ÇC][ÃA]O|PROCURA[ÇC][ÃA]O|SUBSTABELECIMENTO|CERTID[ÃA]O DE JUNTADA|"
    r"TERMO DE AUDI[ÊE]NCIA|DECIS[ÃA]O|DESPACHO|SENTEN[ÇC]A|RELAT[ÓO]RIO|DECLARA[ÇC][ÃA]O|"
    r"COMPROVANTE DE|GUIA DE CUSTAS)\b"
)
RE_FIM_PECA = re.compile(
    r"(?i)\b(?:Nestes termos|Termos em que|Pede deferimento|P\. Deferimento|"
    r"Publique-se|Intimem-se|Cumpra-se|Assinado eletronicamente por|Assinatura do Juiz)\b"
)

# Substituição de caracteres ilegíveis ou especiais
RE_CARACTERES_CID = re.compile(r"\(cid:\d+\)")


@dataclasses.dataclass
class PaginaExtraida:
    """Dados extraídos de uma página física do PDF."""

    numero_pagina: int  # 1-based
    texto: str
    fonte: str  # 'nativo', 'ocr', 'vazio', 'pendente', 'erro'
    qualidade: str  # 'ok', 'insuficiente', 'vazio', 'ilegivel', 'pendente'
    motivo_qualidade: str
    avisos: list[str] = dataclasses.field(default_factory=list)
    id_principal: str | None = None
    metodo_id: str | None = None
    confianca_id: str | None = None
    eh_sumario: bool = False
    sumario_ids: list[str] = dataclasses.field(default_factory=list)
    eh_inicio_peca: bool = False
    eh_fim_peca: bool = False


@dataclasses.dataclass
class Segmento:
    """Segmento ou peça documental identificado no PDF."""

    segmento_id: str
    id_documento: str | None
    pagina_inicial: int  # 1-based inclusivo
    pagina_final: int  # 1-based inclusivo
    numero_paginas: int
    metodo_identificacao: str
    confianca_identificacao: str
    paginas: list[PaginaExtraida]
    caminho_texto: str | None = None
    hash_conteudo: str | None = None
    avisos: list[str] = dataclasses.field(default_factory=list)
    fonte_por_pagina: dict[str, str] = dataclasses.field(default_factory=dict)


def localizar_executavel_tesseract() -> str | None:
    """Tenta localizar o executável do Tesseract no ambiente atual."""
    # 1. Variável de ambiente direta
    env_cmd = os.environ.get("TESSERACT_CMD")
    if env_cmd and os.path.isfile(env_cmd):
        return env_cmd

    # 2. PATH padrão do sistema
    which_cmd = shutil.which("tesseract")
    if which_cmd:
        return which_cmd

    # 3. Caminhos padrão no Windows
    candidatos_windows = [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Tesseract-OCR" / "tesseract.exe",
        Path(os.environ.get("ProgramFiles", "C:\\Program Files")) / "Tesseract-OCR" / "tesseract.exe",
        Path(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")) / "Tesseract-OCR" / "tesseract.exe",
        Path(os.environ.get("ProgramFiles", "C:\\Program Files")) / "PDF24" / "tesseract" / "tesseract.exe",
    ]
    for cand in candidatos_windows:
        try:
            if cand.is_file():
                return str(cand)
        except OSError:
            continue

    # 4. Caminhos padrão no Linux / POSIX
    candidatos_posix = [
        Path("/usr/bin/tesseract"),
        Path("/usr/local/bin/tesseract"),
        Path("/opt/homebrew/bin/tesseract"),
    ]
    for cand in candidatos_posix:
        try:
            if cand.is_file():
                return str(cand)
        except OSError:
            continue

    return None


def obter_dependencias() -> dict[str, Any]:
    """Coleta informações das dependências disponíveis."""
    tesseract_exe = localizar_executavel_tesseract()
    tesseract_versao = None
    if tesseract_exe:
        if pytesseract is not None:
            pytesseract.pytesseract.tesseract_cmd = tesseract_exe
        try:
            import subprocess

            res = subprocess.run(
                [tesseract_exe, "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
                timeout=5,
            )
            primeira_linha = res.stdout.strip().splitlines()[0] if res.stdout else ""
            match = re.search(r"tesseract\s+([0-9.]+)", primeira_linha, re.IGNORECASE)
            tesseract_versao = match.group(1) if match else primeira_linha
        except Exception:
            tesseract_versao = "disponível"

    motor_pdf = "pymupdf" if fitz is not None else ("pypdf" if pypdf is not None else "nenhum")

    return {
        "python": sys.version.split()[0],
        "motor_pdf": motor_pdf,
        "pymupdf_versao": getattr(fitz, "__version__", None) if fitz else None,
        "pypdf_versao": getattr(pypdf, "__version__", None) if pypdf else None,
        "pytesseract_versao": getattr(pytesseract, "__version__", None) if pytesseract else None,
        "tesseract_disponivel": tesseract_exe is not None,
        "tesseract_caminho": tesseract_exe,
        "tesseract_versao": tesseract_versao,
    }


def calcular_sha256(caminho_arquivo: Path) -> str:
    """Calcula o hash SHA-256 de um arquivo em disco."""
    hasher = hashlib.sha256()
    with caminho_arquivo.open("rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def sanitizar_nome(nome: str) -> str:
    """Sanitiza strings para uso seguro como parte de nome de arquivo."""
    return re.sub(r"[^\w\-.]", "_", nome).strip("._-")


def avaliar_suficiencia_texto(texto: str) -> tuple[bool, str]:
    """Avalia transparentemente se o texto nativo extraído da página é suficiente.

    Critérios de reprovação:
    - Texto vazio ou composto apenas de espaços.
    - Menos de 30 caracteres sem presença mínima de palavras legíveis.
    - Alta proporção de caracteres CID ou corrompidos (>15%).
    - Baixa densidade alfanumérica (<25% de caracteres alfanuméricos).
    - Presença excessiva de caracteres binários / de controle não imprimíveis.
    """
    limpo = texto.strip()
    if not limpo:
        return False, "texto_vazio"

    total_chars = len(limpo)

    # 1. Caracteres de controle binários
    controles = sum(1 for c in limpo if ord(c) < 32 and c not in "\n\r\t\f")
    if controles / total_chars > 0.10:
        return False, "caracteres_de_controle_ou_binarios"

    # 2. Caracteres corrompidos ou CID
    cids = len(RE_CARACTERES_CID.findall(limpo))
    substituicoes = limpo.count("\ufffd")
    if (cids * 5 + substituicoes) / total_chars > 0.15:
        return False, "caracteres_corrompidos_ou_cid"

    # 3. Densidade alfanumérica
    alfanumericos = sum(1 for c in limpo if c.isalnum())
    if total_chars > 15 and (alfanumericos / total_chars) < 0.25:
        return False, "baixa_densidade_alfanumerica"

    # 4. Volume mínimo e palavras reconhecíveis
    palavras = re.findall(r"\b[A-Za-zÀ-ÿ]{2,}\b", limpo)
    if total_chars < 30 and len(palavras) < 2:
        return False, "poucos_caracteres_e_palavras"

    return True, "texto_suficiente"


def detectar_identificadores_pagina(
    texto: str,
    numero_pagina: int,
) -> dict[str, Any]:
    """Extrai IDs processuais, indicadores de sumário e limites documentais da página."""
    linhas = [line.strip() for line in texto.splitlines() if line.strip()]
    cabecalho_area = "\n".join(linhas[:5]) if linhas else ""

    id_principal = None
    metodo_id = None
    confianca_id = None
    eh_sumario = False
    sumario_ids: list[str] = []

    # 1. Verifica se a página é um sumário / índice com múltiplos IDs listados
    todas_linhas_sumario = RE_SUMARIO_LINE.findall(texto)
    todos_documento_ids = RE_DOCUMENTO_ID.findall(texto)
    tem_titulo_sumario = bool(
        re.search(
            r"(?i)\b(?:Sum[áa]rio|Índice|Tabela de Pe[çc]as|Rela[çc][ãa]o de Pe[çc]as|Tabela de Documentos)\b",
            cabecalho_area or texto[:300],
        )
    )

    if tem_titulo_sumario or len(todas_linhas_sumario) >= 2 or len(set(todos_documento_ids)) >= 2:
        eh_sumario = True
        sumario_ids = sorted(
            list({match[1] for match in todas_linhas_sumario} | set(todos_documento_ids))
        )
        metodo_id = "sumario_multiplos_ids"
        confianca_id = "baixa"
        id_principal = None

    if not eh_sumario:
        # 2. Procura ID no cabeçalho (prioridade e alta confiança)
        match_cabecalho = (
            RE_DOCUMENTO_ID.search(cabecalho_area)
            or RE_NUM_ID.search(cabecalho_area)
            or RE_NUMERO_DOC.search(cabecalho_area)
            or RE_ID_HEADER.search(cabecalho_area)
        )
        if match_cabecalho:
            id_principal = match_cabecalho.group(1)
            metodo_id = "cabecalho_id"
            confianca_id = "alta"
        else:
            # 3. Procura ID no conteúdo do corpo
            ids_corpo = set(todos_documento_ids)
            if len(ids_corpo) == 1:
                id_principal = list(ids_corpo)[0]
                metodo_id = "conteudo_id"
                confianca_id = "media"
            elif len(ids_corpo) > 1:
                id_principal = list(ids_corpo)[0]
                metodo_id = "conteudo_primeiro_id"
                confianca_id = "baixa"

    # 4. Marcadores de início e fim de peça
    eh_inicio = tem_titulo_sumario or bool(RE_INICIO_PECA.search(cabecalho_area or texto[:400]))
    eh_fim = bool(RE_FIM_PECA.search(texto[-400:] if len(texto) > 400 else texto))

    return {
        "id_principal": id_principal,
        "metodo_id": metodo_id,
        "confianca_id": confianca_id,
        "eh_sumario": eh_sumario,
        "sumario_ids": sumario_ids,
        "eh_inicio_peca": eh_inicio,
        "eh_fim_peca": eh_fim,
    }


def executar_ocr_pagina(
    doc_fitz: Any,
    page_num_0based: int,
    idioma: str = "por",
    dpi: int = 200,
    tesseract_exe: str | None = None,
) -> tuple[str, bool, str]:
    """Executa OCR em uma página individual via PyMuPDF e Tesseract.

    Retorna: (texto_extraido, sucesso, motivo_ou_erro)
    """
    if pytesseract is None:
        return "", False, "pytesseract_nao_instalado"

    if not tesseract_exe:
        return "", False, "tesseract_executavel_nao_encontrado"

    pytesseract.pytesseract.tesseract_cmd = tesseract_exe

    try:
        page = doc_fitz[page_num_0based]
        pix = page.get_pixmap(dpi=dpi)
        if Image is None:
            return "", False, "pillow_nao_instalado"

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Trata fallback gracioso de idioma se o especificado não constar
        try:
            texto = pytesseract.image_to_string(img, lang=idioma)
        except pytesseract.TesseractError as terr:
            if "data" in str(terr).lower() or "lang" in str(terr).lower():
                texto = pytesseract.image_to_string(img, lang="eng")
            else:
                raise terr

        return texto, True, "ocr_concluido"
    except Exception as exc:
        return "", False, f"falha_ocr: {exc}"


def extrair_pagina_individual(
    doc_fitz: Any,
    doc_pypdf: Any,
    numero_pagina_1based: int,
    ocr_mode: str = "auto",
    idioma: str = "por",
    dpi: int = 200,
    tesseract_exe: str | None = None,
) -> PaginaExtraida:
    """Extrai texto e analisa qualidade de uma página individual do PDF."""
    p_idx = numero_pagina_1based - 1
    texto_nativo = ""

    # 1. Extração nativa de texto
    if doc_fitz is not None:
        try:
            texto_nativo = doc_fitz[p_idx].get_text("text") or ""
        except Exception:
            texto_nativo = ""
    elif doc_pypdf is not None:
        try:
            texto_nativo = doc_pypdf.pages[p_idx].extract_text() or ""
        except Exception:
            texto_nativo = ""

    texto_nativo = texto_nativo.replace("\r\n", "\n").replace("\r", "\n")
    suficiente, motivo_nativo = avaliar_suficiencia_texto(texto_nativo)

    avisos: list[str] = []
    texto_final = texto_nativo
    fonte = "nativo"
    qualidade = "ok" if suficiente else "insuficiente"
    motivo_qualidade = motivo_nativo

    precisa_ocr = (ocr_mode == "sempre") or (ocr_mode == "auto" and not suficiente)

    if precisa_ocr:
        if ocr_mode == "nunca":
            avisos.append("ocr_desativado")
        else:
            if not tesseract_exe or pytesseract is None:
                fonte = "pendente"
                qualidade = "pendente"
                motivo_qualidade = "ocr_indisponivel"
                avisos.append("ocr_indisponivel: Tesseract OCR não instalado ou não configurado")
            elif doc_fitz is None:
                fonte = "pendente"
                qualidade = "pendente"
                motivo_qualidade = "motor_renderizacao_indisponivel"
                avisos.append("ocr_indisponivel: PyMuPDF necessário para renderizar imagem da página")
            else:
                # Executa OCR
                texto_ocr, ocr_ok, ocr_info = executar_ocr_pagina(
                    doc_fitz=doc_fitz,
                    page_num_0based=p_idx,
                    idioma=idioma,
                    dpi=dpi,
                    tesseract_exe=tesseract_exe,
                )
                if ocr_ok:
                    texto_ocr = texto_ocr.replace("\r\n", "\n").replace("\r", "\n")
                    ocr_suficiente, motivo_ocr = avaliar_suficiencia_texto(texto_ocr)
                    if texto_ocr.strip():
                        texto_final = texto_ocr
                        fonte = "ocr"
                        qualidade = "ok" if ocr_suficiente else "insuficiente"
                        motivo_qualidade = motivo_ocr
                    else:
                        # Página sem nenhum texto após OCR
                        fonte = "vazio"
                        qualidade = "vazio"
                        motivo_qualidade = "pagina_em_branco"
                        avisos.append("pagina_em_branco")
                else:
                    fonte = "pendente"
                    qualidade = "ilegivel"
                    motivo_qualidade = ocr_info
                    avisos.append(f"falha_ocr: {ocr_info}")

    elif not suficiente and ocr_mode == "nunca":
        if not texto_nativo.strip():
            fonte = "vazio"
            qualidade = "vazio"
            avisos.append("pagina_em_branco")
        elif motivo_nativo in (
            "caracteres_corrompidos_ou_cid",
            "caracteres_de_controle_ou_binarios",
            "baixa_densidade_alfanumerica",
        ):
            fonte = "ilegivel"
            qualidade = "ilegivel"
            avisos.append("pagina_ilegivel")
        else:
            fonte = "nativo"
            qualidade = "insuficiente"
            avisos.append("texto_nativo_insuficiente")

    # Identificação de IDs e limites
    info_ids = detectar_identificadores_pagina(texto_final, numero_pagina_1based)

    return PaginaExtraida(
        numero_pagina=numero_pagina_1based,
        texto=texto_final,
        fonte=fonte,
        qualidade=qualidade,
        motivo_qualidade=motivo_qualidade,
        avisos=avisos,
        id_principal=info_ids["id_principal"],
        metodo_id=info_ids["metodo_id"],
        confianca_id=info_ids["confianca_id"],
        eh_sumario=info_ids["eh_sumario"],
        sumario_ids=info_ids["sumario_ids"],
        eh_inicio_peca=info_ids["eh_inicio_peca"],
        eh_fim_peca=info_ids["eh_fim_peca"],
    )


def segmentar_paginas(
    paginas: list[PaginaExtraida],
    max_paginas_por_segmento: int = 20,
) -> list[Segmento]:
    """Agrupa páginas em segmentos contíguos de documentos ou sintéticos."""
    if not paginas:
        return []

    segmentos: list[Segmento] = []
    seg_idx = 1

    def criar_novo_segmento(
        p_inicial: PaginaExtraida,
        id_doc: str | None,
        metodo: str,
        confianca: str,
    ) -> Segmento:
        nonlocal seg_idx
        sid = f"{seg_idx:04d}"
        seg_idx += 1
        return Segmento(
            segmento_id=sid,
            id_documento=id_doc,
            pagina_inicial=p_inicial.numero_pagina,
            pagina_final=p_inicial.numero_pagina,
            numero_paginas=1,
            metodo_identificacao=metodo,
            confianca_identificacao=confianca,
            paginas=[p_inicial],
            avisos=list(p_inicial.avisos),
            fonte_por_pagina={str(p_inicial.numero_pagina): p_inicial.fonte},
        )

    atual: Segmento | None = None

    for p in paginas:
        if atual is None:
            # Primeiro segmento do documento
            id_doc = p.id_principal
            metodo = p.metodo_id or "sintetico_sem_id"
            confianca = p.confianca_id or "baixa"
            atual = criar_novo_segmento(p, id_doc, metodo, confianca)
            continue

        id_pagina = p.id_principal

        # Cenário 1: Página traz um ID explicitamente detectado
        if id_pagina is not None:
            if atual.id_documento == id_pagina:
                # Mesmo ID do segmento atual -> continuidade
                atual.paginas.append(p)
                atual.pagina_final = p.numero_pagina
                atual.numero_paginas += 1
                atual.fonte_por_pagina[str(p.numero_pagina)] = p.fonte
                atual.avisos.extend(av for av in p.avisos if av not in atual.avisos)
            else:
                # Novo ID detectado -> fecha segmento anterior e abre novo
                segmentos.append(atual)
                atual = criar_novo_segmento(p, id_pagina, p.metodo_id or "conteudo_id", p.confianca_id or "alta")

        # Cenário 2: Página NÃO traz ID detectado (id_pagina is None)
        else:
            if atual.id_documento is not None:
                # Segmento anterior possuía um ID específico
                # Se a peça anterior terminou, ou a página atual inicia uma nova peça:
                if atual.paginas[-1].eh_fim_peca or p.eh_inicio_peca:
                    segmentos.append(atual)
                    atual = criar_novo_segmento(p, None, "sintetico_sem_id", "baixa")
                else:
                    # Continuação da peça do segmento anterior
                    atual.paginas.append(p)
                    atual.pagina_final = p.numero_pagina
                    atual.numero_paginas += 1
                    atual.fonte_por_pagina[str(p.numero_pagina)] = p.fonte
                    atual.avisos.extend(av for av in p.avisos if av not in atual.avisos)
            else:
                # Segmento anterior já era sintético (sem ID)
                if atual.numero_paginas >= max_paginas_por_segmento or p.eh_inicio_peca:
                    segmentos.append(atual)
                    metodo_sintetico = (
                        "sintetico_limite_paginas"
                        if atual.numero_paginas >= max_paginas_por_segmento
                        else "sintetico_sem_id"
                    )
                    atual = criar_novo_segmento(p, None, metodo_sintetico, "baixa")
                else:
                    atual.paginas.append(p)
                    atual.pagina_final = p.numero_pagina
                    atual.numero_paginas += 1
                    atual.fonte_por_pagina[str(p.numero_pagina)] = p.fonte
                    atual.avisos.extend(av for av in p.avisos if av not in atual.avisos)

    if atual is not None:
        segmentos.append(atual)

    return segmentos


def validar_cobertura_e_conflitos(
    total_paginas: int,
    paginas: list[PaginaExtraida],
    segmentos: list[Segmento],
) -> dict[str, Any]:
    """Consolida métricas de cobertura, lacunas, sobreposições e conflitos de ID."""
    paginas_nativo = [p.numero_pagina for p in paginas if p.fonte == "nativo"]
    paginas_ocr = [p.numero_pagina for p in paginas if p.fonte == "ocr"]
    paginas_pendentes = [p.numero_pagina for p in paginas if p.fonte == "pendente"]
    paginas_sem_conteudo = [
        p.numero_pagina for p in paginas if p.fonte == "vazio" or p.qualidade in ("vazio", "ilegivel")
    ]

    intervalos: list[dict[str, Any]] = []
    paginas_cobertas: set[int] = set()
    sobreposicoes: list[dict[str, Any]] = []

    for seg in segmentos:
        intervalo_set = set(range(seg.pagina_inicial, seg.pagina_final + 1))
        intersec = paginas_cobertas & intervalo_set
        if intersec:
            sobreposicoes.append({
                "segmento_id": seg.segmento_id,
                "paginas_sobrepostas": sorted(list(intersec)),
            })
        paginas_cobertas.update(intervalo_set)
        intervalos.append({
            "segmento_id": seg.segmento_id,
            "id_documento": seg.id_documento,
            "pagina_inicial": seg.pagina_inicial,
            "pagina_final": seg.pagina_final,
            "numero_paginas": seg.numero_paginas,
        })

    paginas_esperadas = set(range(1, total_paginas + 1))
    lacunas = sorted(list(paginas_esperadas - paginas_cobertas))

    # Diagnóstico de IDs repetidos em intervalos não contíguos
    ocorrencias_id: dict[str, list[Segmento]] = {}
    for seg in segmentos:
        if seg.id_documento is not None:
            ocorrencias_id.setdefault(seg.id_documento, []).append(seg)

    ids_repetidos_nao_contiguos: list[str] = []
    ids_conflitantes: list[dict[str, Any]] = []

    for doc_id, segs in ocorrencias_id.items():
        if len(segs) > 1:
            ids_repetidos_nao_contiguos.append(doc_id)
            ids_conflitantes.append({
                "id": doc_id,
                "motivo": "Id repetido em intervalos não contíguos",
                "segmentos": [s.segmento_id for s in segs],
                "intervalos": [[s.pagina_inicial, s.pagina_final] for s in segs],
            })
            for s in segs:
                if "id_repetido_nao_contiguo" not in s.avisos:
                    s.avisos.append("id_repetido_nao_contiguo")

    # Diagnóstico de divergências entre sumário e cabeçalho
    for p in paginas:
        if p.eh_sumario and p.sumario_ids:
            # Verifica se os IDs do sumário entram em conflito com cabeçalhos encontrados
            for seg in segmentos:
                if (
                    seg.id_documento
                    and seg.pagina_inicial > p.numero_pagina
                    and seg.id_documento not in p.sumario_ids
                    and seg.confianca_identificacao == "alta"
                ):
                    ids_conflitantes.append({
                        "pagina": seg.pagina_inicial,
                        "id_cabecalho": seg.id_documento,
                        "ids_sumario": p.sumario_ids,
                        "motivo": "Id divergente entre sumário e cabeçalho",
                    })
                    if "conflito_id_sumario_cabecalho" not in seg.avisos:
                        seg.avisos.append("conflito_id_sumario_cabecalho")

    cobertura_pct = round((len(paginas_cobertas) / total_paginas * 100), 2) if total_paginas > 0 else 0.0

    return {
        "schema_version": SCHEMA_VERSION,
        "total_paginas": total_paginas,
        "paginas_nativo": sorted(paginas_nativo),
        "paginas_ocr": sorted(paginas_ocr),
        "paginas_pendentes": sorted(paginas_pendentes),
        "paginas_sem_conteudo": sorted(paginas_sem_conteudo),
        "intervalos_segmentos": intervalos,
        "lacunas": lacunas,
        "sobreposicoes": sobreposicoes,
        "ids_conflitantes": ids_conflitantes,
        "ids_repetidos_nao_contiguos": ids_repetidos_nao_contiguos,
        "resumo": {
            "total_paginas": total_paginas,
            "total_segmentos": len(segmentos),
            "cobertura_percentual": cobertura_pct,
        },
    }


def gerar_artefatos(
    saida_dir: Path,
    pdf_info: dict[str, Any],
    config: dict[str, Any],
    dependencias: dict[str, Any],
    segmentos: list[Segmento],
    cobertura: dict[str, Any],
    formato: str = "ambos",
) -> dict[str, Any]:
    """Persiste arquivos de saída (manifest.json, index.json, cobertura.json, textos/*.md)."""
    saida_dir.mkdir(parents=True, exist_ok=True)
    textos_dir = saida_dir / "textos"
    if formato in ("ambos", "markdown"):
        textos_dir.mkdir(parents=True, exist_ok=True)

    caminhos_textos: list[str] = []

    # 1. Geração dos arquivos de texto por segmento
    for seg in segmentos:
        if seg.id_documento:
            clean_id = sanitizar_nome(seg.id_documento)
            nome_arquivo = f"{seg.segmento_id}-id-{clean_id}.md"
            titulo_cabecalho = f"Documento ID {seg.id_documento}"
        else:
            nome_arquivo = f"{seg.segmento_id}-sem-id.md"
            titulo_cabecalho = "Sem ID"

        rel_path = f"textos/{nome_arquivo}"
        caminhos_textos.append(rel_path)
        seg.caminho_texto = rel_path

        # Montagem do conteúdo Markdown com marcadores explícitos de página
        partes_md: list[str] = [
            f"# Segmento {seg.segmento_id} — {titulo_cabecalho} (Páginas {seg.pagina_inicial} a {seg.pagina_final})\n"
        ]

        for p in seg.paginas:
            partes_md.append(f"<!-- Página {p.numero_pagina} -->\n")
            if p.fonte == "vazio":
                partes_md.append("[Página em branco ou sem conteúdo detectável]\n")
            elif p.fonte == "pendente":
                partes_md.append("[OCR indisponível: texto pendente de extração]\n")
            elif p.qualidade == "ilegivel":
                partes_md.append("[Página ilegível ou pendente de revisão]\n")
            else:
                conteudo_p = p.texto.strip()
                if conteudo_p:
                    partes_md.append(conteudo_p + "\n")
                else:
                    partes_md.append("[Página sem conteúdo textual detectado]\n")

        texto_completo = "\n".join(partes_md).strip() + "\n"
        seg.hash_conteudo = hashlib.sha256(texto_completo.encode("utf-8")).hexdigest()

        if formato in ("ambos", "markdown"):
            arquivo_md = saida_dir / rel_path
            arquivo_md.write_text(texto_completo, encoding="utf-8")

    # 2. Montagem de index.json
    itens_indice: list[dict[str, Any]] = []
    for seg in segmentos:
        itens_indice.append({
            "segmento_id": seg.segmento_id,
            "id_documento": seg.id_documento,
            "pagina_inicial": seg.pagina_inicial,
            "pagina_final": seg.pagina_final,
            "numero_paginas": seg.numero_paginas,
            "metodo_identificacao": seg.metodo_identificacao,
            "confianca_identificacao": seg.confianca_identificacao,
            "caminho_texto": seg.caminho_texto,
            "fonte_por_pagina": seg.fonte_por_pagina,
            "avisos": seg.avisos,
            "hash_conteudo": seg.hash_conteudo,
        })

    index_dados = {
        "schema_version": SCHEMA_VERSION,
        "total_segmentos": len(segmentos),
        "segmentos": itens_indice,
    }

    # 3. Montagem de manifest.json
    data_agora = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
    manifest_dados = {
        "schema_version": SCHEMA_VERSION,
        "script_version": SCRIPT_VERSION,
        "data_execucao": data_agora,
        "pdf": pdf_info,
        "total_paginas": pdf_info["total_paginas"],
        "configuracao": config,
        "dependencias": dependencias,
        "artefatos": {
            "manifest": "manifest.json",
            "index": "index.json",
            "cobertura": "cobertura.json",
            "textos": caminhos_textos if formato in ("ambos", "markdown") else [],
        },
        "resumo": {
            "total_segmentos": len(segmentos),
            "paginas_nativo": len(cobertura["paginas_nativo"]),
            "paginas_ocr": len(cobertura["paginas_ocr"]),
            "paginas_vazias": len(cobertura["paginas_sem_conteudo"]),
            "paginas_pendentes": len(cobertura["paginas_pendentes"]),
        },
        "falhas": [],
        "erros": [],
        "paginas_nao_examinadas": cobertura["paginas_pendentes"],
        "paginas_sem_texto": cobertura["paginas_sem_conteudo"],
    }

    if formato in ("ambos", "json"):
        (saida_dir / "manifest.json").write_text(
            json.dumps(manifest_dados, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (saida_dir / "index.json").write_text(
            json.dumps(index_dados, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (saida_dir / "cobertura.json").write_text(
            json.dumps(cobertura, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    return {
        "manifest": manifest_dados,
        "index": index_dados,
        "cobertura": cobertura,
    }


def verificar_cache_valido(
    saida_dir: Path,
    pdf_sha256: str,
    config: dict[str, Any],
) -> dict[str, Any] | None:
    """Verifica se a pasta de saída contém uma indexação válida e reaproveitável."""
    manifest_path = saida_dir / "manifest.json"
    index_path = saida_dir / "index.json"
    cobertura_path = saida_dir / "cobertura.json"

    if not (manifest_path.is_file() and index_path.is_file() and cobertura_path.is_file()):
        return None

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        index = json.loads(index_path.read_text(encoding="utf-8"))
        cobertura = json.loads(cobertura_path.read_text(encoding="utf-8"))

        # Confere hash do PDF
        if manifest.get("pdf", {}).get("sha256") != pdf_sha256:
            return None

        # Confere parâmetros essenciais de configuração
        conf_antiga = manifest.get("configuracao", {})
        for k in ("ocr", "idioma", "dpi", "max_paginas_por_segmento"):
            if conf_antiga.get(k) != config.get(k):
                return None

        # Confere se os arquivos de texto apontados existem
        itens = index if isinstance(index, list) else index.get("segmentos", [])
        for item in itens:
            caminho_rel = item.get("caminho_texto")
            if caminho_rel and not (saida_dir / caminho_rel).is_file():
                return None

        return {
            "manifest": manifest,
            "index": index,
            "cobertura": cobertura,
            "cache_hit": True,
        }
    except Exception:
        return None


def indexar_pdf(
    pdf_path: str | Path,
    out_dir: str | Path | None = None,
    ocr: str = "auto",
    idioma: str = "por",
    dpi: int = 200,
    force: bool = False,
    formato: str = "ambos",
    max_paginas_por_segmento: int = 20,
) -> dict[str, Any]:
    """Função central e programática para indexação de PDFs."""
    pdf_caminho = Path(pdf_path).resolve()
    if not pdf_caminho.exists():
        raise PdfNaoEncontradoError(f"Arquivo PDF não encontrado: {pdf_caminho}")
    if not pdf_caminho.is_file():
        raise PdfInvalidoError(f"O caminho especificado não é um arquivo: {pdf_caminho}")

    if out_dir is None:
        saida_dir = pdf_caminho.parent / f"{pdf_caminho.stem}_indexado"
    else:
        saida_dir = Path(out_dir).resolve()

    # Validação e coleta do arquivo PDF
    tamanho_bytes = pdf_caminho.stat().st_size
    if tamanho_bytes == 0:
        raise PdfInvalidoError("Arquivo PDF vazio (0 bytes)")

    pdf_sha256 = calcular_sha256(pdf_caminho)

    config_execucao = {
        "ocr": ocr,
        "idioma": idioma,
        "dpi": dpi,
        "force": force,
        "formato": formato,
        "max_paginas_por_segmento": max_paginas_por_segmento,
    }

    # Verificação de cache/reaproveitamento se force for False
    if not force:
        cache = verificar_cache_valido(saida_dir, pdf_sha256, config_execucao)
        if cache:
            return cache

    dependencias = obter_dependencias()
    if dependencias["motor_pdf"] == "nenhum":
        raise DependenciaAusenteError(
            "Nenhuma biblioteca de leitura de PDF disponível. Instale 'pymupdf' ou 'pypdf'."
        )

    # Abertura do PDF com tratamento rigoroso de criptografia e corrupção
    doc_fitz = None
    doc_pypdf = None
    total_paginas = 0

    if fitz is not None:
        try:
            doc_fitz = fitz.open(str(pdf_caminho))
            if doc_fitz.is_encrypted:
                doc_fitz.close()
                raise PdfProtegidoError(f"PDF protegido por senha ou criptografia: {pdf_caminho.name}")
            total_paginas = len(doc_fitz)
        except fitz.FileDataError as fde:
            raise PdfInvalidoError(f"Arquivo PDF corrompido ou formato inválido: {fde}") from fde
        except Exception as exc:
            if isinstance(exc, (PdfProtegidoError, PdfInvalidoError)):
                raise
            raise PdfInvalidoError(f"Falha ao abrir PDF com PyMuPDF: {exc}") from exc
    elif pypdf is not None:
        try:
            f = pdf_caminho.open("rb")
            doc_pypdf = pypdf.PdfReader(f)
            if doc_pypdf.is_encrypted:
                f.close()
                raise PdfProtegidoError(f"PDF protegido por senha ou criptografia: {pdf_caminho.name}")
            total_paginas = len(doc_pypdf.pages)
        except Exception as exc:
            if isinstance(exc, (PdfProtegidoError, PdfInvalidoError)):
                raise
            raise PdfInvalidoError(f"Falha ao abrir PDF com pypdf: {exc}") from exc

    if total_paginas == 0:
        if doc_fitz:
            doc_fitz.close()
        raise PdfInvalidoError("PDF não possui páginas legíveis (total_paginas = 0)")

    pdf_info = {
        "nome": pdf_caminho.name,
        "caminho": str(pdf_caminho),
        "tamanho_bytes": tamanho_bytes,
        "sha256": pdf_sha256,
        "total_paginas": total_paginas,
    }

    tesseract_exe = dependencias.get("tesseract_caminho")

    try:
        # Extração de cada página
        paginas_extraidas: list[PaginaExtraida] = []
        for num_p in range(1, total_paginas + 1):
            p_ext = extrair_pagina_individual(
                doc_fitz=doc_fitz,
                doc_pypdf=doc_pypdf,
                numero_pagina_1based=num_p,
                ocr_mode=ocr,
                idioma=idioma,
                dpi=dpi,
                tesseract_exe=tesseract_exe,
            )
            paginas_extraidas.append(p_ext)

        # Segmentação das páginas em documentos/peças
        segmentos = segmentar_paginas(
            paginas=paginas_extraidas,
            max_paginas_por_segmento=max_paginas_por_segmento,
        )

        # Validação de cobertura e diagnósticos
        cobertura = validar_cobertura_e_conflitos(
            total_paginas=total_paginas,
            paginas=paginas_extraidas,
            segmentos=segmentos,
        )

        # Geração e persistência dos artefatos
        resultado = gerar_artefatos(
            saida_dir=saida_dir,
            pdf_info=pdf_info,
            config=config_execucao,
            dependencias=dependencias,
            segmentos=segmentos,
            cobertura=cobertura,
            formato=formato,
        )
        resultado["cache_hit"] = False
        return resultado

    finally:
        if doc_fitz is not None:
            doc_fitz.close()


def criar_argument_parser() -> argparse.ArgumentParser:
    """Configura e retorna o parser de argumentos de linha de comando."""
    parser = argparse.ArgumentParser(
        description="Indexador navegável de PDFs processuais longos.",
        prog="indexar_pdf.py",
    )
    parser.add_argument(
        "pdf",
        help="Caminho do arquivo PDF a ser processado.",
    )
    parser.add_argument(
        "--out",
        "-o",
        dest="out",
        default=None,
        help="Diretório de saída para os artefatos gerados (padrão: <nome_do_pdf>_indexado).",
    )
    parser.add_argument(
        "--ocr",
        choices=["auto", "sempre", "nunca"],
        default="auto",
        help="Modo de aplicação de OCR: auto (padrão), sempre ou nunca.",
    )
    parser.add_argument(
        "--idioma",
        default="por",
        help="Idioma(s) para o OCR do Tesseract (ex.: por, eng, por+eng). Padrão: por.",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=200,
        help="Resolução DPI para renderização no OCR. Padrão: 200.",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Invalida cache existente e força novo processamento completo.",
    )
    parser.add_argument(
        "--formato",
        choices=["ambos", "json", "markdown"],
        default="ambos",
        help="Formato dos artefatos: ambos (padrão), json ou markdown.",
    )
    parser.add_argument(
        "--max-paginas-por-segmento",
        type=int,
        default=20,
        help="Limite máximo de páginas por segmento sintético sem ID. Padrão: 20.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Ponto de entrada de linha de comando."""
    parser = criar_argument_parser()
    args = parser.parse_args(argv)

    try:
        resultado = indexar_pdf(
            pdf_path=args.pdf,
            out_dir=args.out,
            ocr=args.ocr,
            idioma=args.idioma,
            dpi=args.dpi,
            force=args.force,
            formato=args.formato,
            max_paginas_por_segmento=args.max_paginas_por_segmento,
        )

        manifest = resultado.get("manifest", {})
        total_p = manifest.get("total_paginas", 0)
        total_seg = len(resultado.get("index", {}).get("segmentos", []))
        cache_status = " (reaproveitado do cache)" if resultado.get("cache_hit") else ""

        print(
            f"Indexação concluída com sucesso{cache_status}: {total_p} página(s) processada(s) em {total_seg} segmento(s)."
        )
        return 0

    except IndexadorPdfError as err:
        sys.stderr.write(f"Erro no indexador de PDF: {err}\n")
        return 1
    except Exception as exc:
        sys.stderr.write(f"Erro inesperado durante a indexação: {exc}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
