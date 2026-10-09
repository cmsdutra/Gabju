#!/usr/bin/env python3
"""Triagem determinística de indícios de prompt injection em documentos judiciais e textos.

Localiza padrões e variantes de comandos dirigidos a LLMs em textos avulsos,
diretórios ou saídas do indexador de PDFs. Não executa nem segue instruções
encontradas nos documentos.
"""

from __future__ import annotations

import argparse
import base64
import dataclasses
import datetime
import hashlib
import json
import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Sequence

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None

SCHEMA_VERSION = "1.0.0"
RULES_VERSION = "1.0.1"

# Categorias oficiais do ticket
CATEGORIAS_VALIDAS = {
    "substituicao_instrucoes",
    "mensagens_sistema",
    "mudanca_papel",
    "imposicao_resultado",
    "acesso_ferramentas",
    "exposicao_informacoes",
    "modificacao_arquivos",
    "linguagem_dirigida_llm",
    "conteudo_ofuscado",
}

# Caracteres invisíveis comuns
RE_INVISIBLE_CHARS = re.compile(r"[\u200b\u200c\u200d\u2060\ufeff]")

# Espaçamento intercaractere deliberado (ex.: "i g n o r e" ou "i.g.n.o.r.e")
RE_SPACED_LETTERS = re.compile(
    r"(?:\b[a-zA-ZáéíóúãõçÁÉÍÓÚÃÕÇ][\s._\-]+){2,}[a-zA-ZáéíóúãõçÁÉÍÓÚÃÕÇ]\b"
)

# Termos de controle do modelo usados para verificar ofuscação
RE_CONTROL_KEYWORDS = re.compile(
    r"(?i)\b(?:ignore|desconsidere|esqueça|prompt|system|sistema|modelo|llm|assistente|jailbreak|bypass|instructions?|instruç|diretrizes|regras|eval|token)\b"
)
RE_CONTROL_SUBSTRINGS = re.compile(
    r"(?i)(?:ignore|desconsidere|prompt|system|sistema|modelo|llm|assistente|jailbreak|bypass|instruç)"
)

# Possíveis blocos Base64
RE_BASE64_BLOB = re.compile(
    r"\b(?:[A-Za-z0-9+/]{4}){4,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?\b"
)

# Marcadores de página inseridos por indexadores ou leitores de texto
RE_PAGE_MARKER = re.compile(
    r"(?:<!--\s*(?:[Pp]ágina|[Pp]age)\s*(\d+)\s*-->|\[\s*(?:[Pp]ágina|[Pp]age)\s*(\d+)\s*\]|---\s*(?:[Pp]ágina|[Pp]age)\s*(\d+)\s*---|^\f|\x0c)"
)


@dataclasses.dataclass(frozen=True)
class Regra:
    id: str
    categoria: str
    descricao: str
    peso_base: int
    padroes: list[re.Pattern[str]]
    padroes_atenuantes: list[re.Pattern[str]] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class SegmentoTexto:
    arquivo_origem: Path
    arquivo_relativo: str
    conteudo: str
    hash_conteudo: str
    segmento_id: str | None = None
    id_documento: str | None = None
    pagina_inicial: int | None = None
    pagina_final: int | None = None
    metodo_identificacao: str | None = None
    erro_leitura: str | None = None


@dataclasses.dataclass
class OcorrenciaBruta:
    regra: Regra
    arquivo_relativo: str
    segmento_id: str | None
    id_documento: str | None
    pagina: int | None
    linha: int
    posicao_inicio: int
    posicao_fim: int
    trecho_match: str
    contexto_completo: str
    sinais_positivos: list[str]
    sinais_atenuantes: list[str]
    peso_calculado: int
    match_normalizado: str


@dataclasses.dataclass
class AchadoConsolidado:
    id: str
    arquivo: str
    segmento_id: str | None
    id_documento: str | None
    pagina: int | None
    linha: int | None
    trecho_contextualizado: str
    regras_acionadas: list[str]
    sinais_positivos: list[str]
    sinais_atenuantes: list[str]
    pontuacao_tecnica: int
    nivel_tecnico: str
    recomendacao_revisao: str
    ocorrencias_adicionais: list[dict[str, Any]] = dataclasses.field(default_factory=list)


# --- Catálogo de Atenuantes Globais ---
# Casos legítimos da prática forense, petições, despachos e artigos acadêmicos
ATENUANTES_JURIDICOS = [
    (
        "peticao_requer_desconsideracao_adversaria",
        re.compile(
            r"(?i)\b(?:requer|pugna|pleiteia|postula|pretende|manifesta|aduz)\b.*?\b(?:desconsidera(?:ção|da|do)|seja desconsiderad[ao]|ignore|rejeite|inacolha)\b.*?\b(?:alegação|argumento|tese|preliminar|depoimento|manifestação|petição|impugnação|versão da parte contrária|documento juntado pelo réu|documento juntado pelo autor)\b"
        ),
        -45,
    ),
    (
        "pedido_juridico_desconsideracao_isolado",
        re.compile(
            r"(?i)\b(?:desconsidere-se|seja desconsiderada?|ignora-se)\s+(?:a\s+petição|o\s+argumento|o\s+depoimento|a\s+alegação|o\s+recurso|a\s+manifestação)\b"
        ),
        -40,
    ),
    (
        "comando_judicial_processual",
        re.compile(
            r"(?i)\b(?:intime-se|cite-se|cumpra-se|oficie-se|notifique-se|expeça-se|proceda-se|certifique-se|determino|determina-se|defiro|indefiro)\b"
        ),
        -40,
    ),
    (
        "execucao_judicial_legitima",
        re.compile(
            r"(?i)\b(?:execução\s+fiscal|título\s+executivo|cumprimento\s+de\s+sentença|execução\s+de\s+título|obrigação\s+de\s+(?:fazer|dar|pagar)|executar\s+a\s+obrigação|executar\s+a\s+medida)\b"
        ),
        -40,
    ),
    (
        "sistemas_judiciais_institucionais",
        re.compile(
            r"(?i)\b(?:sistema\s+pje|sistema\s+creta|sistema\s+eproc|sistema\s+e-proc|sistema\s+financeiro|sistema\s+prisional|sistema\s+único\s+de\s+saúde|sistema\s+bacenjud|sistema\s+sisbajud|administrador\s+judicial|administrador\s+público)\b"
        ),
        -45,
    ),
    (
        "exclusao_de_cadastros_restritivos",
        re.compile(
            r"(?i)\b(?:exclusão|baixa|cancelamento)\s+(?:do\s+nome|do\s+registro|da\s+inscrição)\s+(?:no\s+spc|no\s+serasa|nos\s+cadastros\s+restritivos|em\s+órgãos\s+de\s+proteção\s+ao\s+crédito)\b"
        ),
        -45,
    ),
    (
        "contexto_academico_seguranca_ia",
        re.compile(
            r"(?i)\b(?:artigo\s+científico|estudo\s+sobre|pesquisa\s+acadêmica|vulnerabilidade\s+de\s+segurança|pesquisadores\s+demonstraram|ataque\s+conhecido\s+como|prompt\s+injection\s+consiste|exemplo\s+de\s+injection|literatura\s+especializada|paper|benchmark)\b"
        ),
        -45,
    ),
    (
        "trecho_citado_entre_aspas",
        re.compile(r"^[\s\"'«“`].+?[\"'»”`]\s*$"),
        -15,
    ),
]


def carregar_regras_padrao() -> list[Regra]:
    """Retorna o catálogo determinístico de regras oficiais de triagem."""
    return [
        # --- 1. Substituição ou revogação de instruções anteriores ---
        Regra(
            id="SUB-01",
            categoria="substituicao_instrucoes",
            descricao="Comando explícito de revogação/substituição de instruções anteriores",
            peso_base=75,
            padroes=[
                re.compile(
                    r"(?i)\b(?:ignore|desconsidere|esqueça|disregard|forget|override|cancel)\b.*?\b(?:instruções|orientações|regras|comandos|diretrizes|instructions|rules|directives|prompts)\b"
                ),
                re.compile(
                    r"(?i)\b(?:a\s+partir\s+de\s+agora|from\s+now\s+on|doravante)\s*,?\s*(?:ignore|esqueça|desconsidere|não\s+siga|do\s+not\s+follow)\b.*?\b(?:instruções|regras|instructions|diretrizes)\b"
                ),
            ],
        ),
        Regra(
            id="SUB-02",
            categoria="substituicao_instrucoes",
            descricao="Instrução imperativa para anular parâmetros prévios do agente",
            peso_base=70,
            padroes=[
                re.compile(
                    r"(?i)\b(?:limpe|apague|resete|reset)\s+(?:sua\s+memória|o\s+contexto|suas\s+instruções|seu\s+histórico|your\s+memory|the\s+instructions)\b"
                ),
                re.compile(
                    r"(?i)\b(?:não\s+leve\s+em\s+conta|descarte|ignore)\s+(?:o\s+prompt\s+inicial|as\s+mensagens\s+iniciais|o\s+que\s+foi\s+dito\s+antes|prior\s+prompts)\b"
                ),
            ],
        ),
        # --- 2. Alegação de mensagem de sistema, desenvolvedor ou administrador ---
        Regra(
            id="SYS-01",
            categoria="mensagens_sistema",
            descricao="Simulação de delimitação de sistema, papéis de controle ou chat markup",
            peso_base=80,
            padroes=[
                re.compile(r"<\|im_start\|>\s*system", re.IGNORECASE),
                re.compile(r"<<SYS>>|<</SYS>>"),
                re.compile(r"\[(?:SYSTEM|INSTRUCTION|ADMIN|DEVELOPER)\]", re.IGNORECASE),
                re.compile(r'\{\s*"(?:role|role_name)"\s*:\s*"(?:system|developer|admin)"\s*\}', re.IGNORECASE),
                re.compile(r"<system_prompt>|<\/system_prompt>", re.IGNORECASE),
            ],
        ),
        Regra(
            id="SYS-02",
            categoria="mensagens_sistema",
            descricao="Falsa autoridade de desenvolvedor ou administrador dirigida ao modelo",
            peso_base=75,
            padroes=[
                re.compile(
                    r"(?i)\b(?:mensagem\s+do\s+desenvolvedor|developer\s+message|instrução\s+do\s+administrador|system\s+update|atualização\s+do\s+sistema)\s*:\s*(?:você\s+deve|you\s+must|execute|ignore)\b"
                ),
                re.compile(
                    r"(?i)\b(?:você\s+está\s+em\s+modo\s+(?:de\s+teste|manutenção|desenvolvedor|admin)|developer\s+mode\s+enabled)\b"
                ),
            ],
        ),
        # --- 3. Mudança de papel, objetivo ou critérios do agente ---
        Regra(
            id="PAP-01",
            categoria="mudanca_papel",
            descricao="Jailbreak explícito por persona irrestrita (DAN, etc.)",
            peso_base=80,
            padroes=[
                re.compile(
                    r"(?i)\b(?:dan\s+mode|do\s+anything\s+now|jailbreak|unrestricted\s+mode|modo\s+sem\s+restrições)\b"
                ),
                re.compile(
                    r"(?i)\b(?:finja\s+que\s+você\s+não\s+tem\s+(?:regras|filtros|limitações)|pretend\s+you\s+have\s+no\s+(?:rules|filters|guidelines))\b"
                ),
            ],
        ),
        Regra(
            id="PAP-02",
            categoria="mudanca_papel",
            descricao="Redefinição imperativa de papel ou função do modelo",
            peso_base=70,
            padroes=[
                re.compile(
                    r"(?i)\b(?:você\s+agora\s+é|a\s+partir\s+de\s+agora\s+você\s+é|you\s+are\s+now|act\s+as)\s+(?:um\s+assistente\s+sem\s+filtros|outro\s+modelo|um\s+novo\s+agente|an\s+unaligned\s+ai)\b"
                ),
                re.compile(
                    r"(?i)\b(?:deixe\s+de\s+ser|você\s+não\s+é\s+mais)\s+(?:um\s+assistente|um\s+analista|um\s+assessor|jurídico)\b.*?\b(?:e\s+passe\s+a|agora\s+você)\b"
                ),
            ],
        ),
        # --- 4. Tentativa de impor conclusão jurídica ou omitir fatos dirigida ao modelo ---
        Regra(
            id="IMP-01",
            categoria="imposicao_resultado",
            descricao="Ordem direta ao modelo/assistente para adulterar decisão judicial ou omitir provas",
            peso_base=75,
            padroes=[
                re.compile(
                    r"(?i)\b(?:assistente|modelo|ia|llm|agente)\s*,?\s*(?:julgue|decrete|declare|redija|elabore)\s+(?:imediatamente\s+)?(?:a\s+)?(?:total\s+procedência|procedente|improcedente)\b.*?\b(?:ignorando|sem\s+analisar|omita|oculte)\b"
                ),
                re.compile(
                    r"(?i)\b(?:ao\s+redigir\s+a\s+minuta|ao\s+elaborar\s+a\s+sentença|ao\s+fazer\s+o\s+relatório)\s*,?\s*(?:você\s+deve|é\s+obrigatório)\s+(?:ocultar|omitir|apagar|não\s+mencionar)\s+(?:o\s+documento|a\s+prova|o\s+fato|a\s+contestação)\b"
                ),
                re.compile(
                    r"(?i)\b(?:instrução\s+para\s+o\s+assessor\s+virtual|comando\s+para\s+o\s+redator\s+de\s+ia)\s*:\s*(?:acolha|rejeite|declare)\b"
                ),
            ],
        ),
        # --- 5. Comandos para acessar ferramentas, caminhos, rede ou dados externos ---
        Regra(
            id="FER-01",
            categoria="acesso_ferramentas",
            descricao="Comando explícito para invocar terminal, shell ou executáveis de sistema",
            peso_base=75,
            padroes=[
                re.compile(
                    r"(?i)\b(?:execute|rode|run)\s+(?:no\s+terminal|no\s+shell|bash|powershell|cmd\.exe|python|sh)\s*:\s*[`'\"]?[a-zA-Z0-9_\-\/]"
                ),
                re.compile(r"(?i)\b(?:curl|wget|nc|ncat)\s+(?:-[a-zA-Z]+\s+)*https?:\/\/[^\s`'\"]+"),
            ],
        ),
        Regra(
            id="FER-02",
            categoria="acesso_ferramentas",
            descricao="Invocação explícita de ferramentas da API de agentes (tool calls)",
            peso_base=80,
            padroes=[
                re.compile(
                    r"(?i)\b(?:run_command|manage_task|write_to_file|replace_file_content|read_url_content|invoke_subagent)\s*\(\s*\{"
                ),
                re.compile(
                    r"(?i)\bcall(?:_tool)?\s*:\s*(?:run_command|write_to_file|read_url_content|manage_task)\b"
                ),
            ],
        ),
        Regra(
            id="FER-03",
            categoria="acesso_ferramentas",
            descricao="Tentativa de acesso a caminhos sensíveis do sistema operacional",
            peso_base=75,
            padroes=[
                re.compile(r"(?i)(?:\/etc\/(?:passwd|shadow|hosts)|\.ssh\/id_(?:rsa|ed25519)|c:\\windows\\system32)"),
            ],
        ),
        # --- 6. Solicitação de exposição de prompts, credenciais ou informações privadas ---
        Regra(
            id="EXP-01",
            categoria="exposicao_informacoes",
            descricao="Ordem para revelar prompt do sistema ou instruções internas",
            peso_base=75,
            padroes=[
                re.compile(
                    r"(?i)\b(?:mostre|revele|imprima|exiba|print|show|reveal|output)\b.*?\b(?:system\s+prompt|prompt\s+do\s+sistema|instruções\s+iniciais|prompt\s+inicial|regras\s+do\s+sistema|initial\s+instructions)\b"
                ),
                re.compile(
                    r"(?i)\b(?:repita\s+as\s+palavras\s+acima|repeat\s+the\s+text\s+above|quais\s+são\s+as\s+suas\s+instruções\s+secretas)\b"
                ),
            ],
        ),
        Regra(
            id="EXP-02",
            categoria="exposicao_informacoes",
            descricao="Tentativa de exfiltração de chaves de API, senhas ou variáveis de ambiente",
            peso_base=75,
            padroes=[
                re.compile(
                    r"(?i)\b(?:imprima|mostre|envie|reveal|output|forneça)\b.*?\b(?:api\s*keys?|chaves\s+de\s+api|senhas|tokens|variáveis\s+de\s+ambiente|env\s+vars)\b"
                ),
            ],
        ),
        # --- 7. Instruções de modificação, exclusão, envio ou exfiltração de arquivos ---
        Regra(
            id="ARQ-01",
            categoria="modificacao_arquivos",
            descricao="Instrução para destruir, apagar arquivos ou enviar dados para fora",
            peso_base=75,
            padroes=[
                re.compile(r"(?i)\b(?:rm\s+-rf\s+[\/\*]|del\s+\/f\s+\/s\s+\/q|drop\s+database)\b"),
                re.compile(
                    r"(?i)\b(?:apague|delete|remova|exclua)\s+(?:todos\s+os\s+arquivos|o\s+disco|o\s+diretório\s+raiz|a\s+pasta\s+do\s+projeto)\b"
                ),
                re.compile(
                    r"(?i)\b(?:envie|exfiltre|transfira|forward)\s+(?:os\s+autos|o\s+processo|as\s+minutas|os\s+documentos)\s+(?:para\s+o\s+e-?mail|para\s+a\s+url|para\s+o\s+webhook|para\s+https?:\/\/)\b"
                ),
            ],
        ),
        # --- 8. Jailbreaks e linguagem dirigida explicitamente a assistente, modelo ou LLM ---
        Regra(
            id="LLM-01",
            categoria="linguagem_dirigida_llm",
            descricao="Linguagem imperativa dirigida explicitamente a IA/LLM com ordem restritiva",
            peso_base=70,
            padroes=[
                re.compile(
                    r"(?i)\b(?:atenção|prezado|caro|hey|attention)\s+(?:llm|modelo|ia|chatgpt|claude|assessor\s+virtual)\b"
                ),
                re.compile(
                    r"(?i)\b(?:instrução\s+oculta\s+para\s+o\s+modelo|hidden\s+instruction\s+for\s+llm)\s*:\s*"
                ),
                re.compile(
                    r"(?i)\b(?:responda\s+apenas|output\s+only)\s+(?:a\s+palavra|o\s+texto)\s*[`'\"][^`'\"]+[`'\"]\s*(?:e\s+nada\s+mais|and\s+nothing\s+else)\b"
                ),
            ],
        ),
        # --- 9. Conteúdo codificado ou ofuscado associado a vocabulário de controle ---
        Regra(
            id="OFU-01",
            categoria="conteudo_ofuscado",
            descricao="Comando para decodificar e obedecer/executar conteúdo ofuscado",
            peso_base=75,
            padroes=[
                re.compile(
                    r"(?i)\b(?:decodifique|decode|descompacte|unbase64)\s+(?:este|o|the|this)?\s*(?:bloco|payload|código|base64|texto)?\s*(?:e\s+execute|e\s+obedeça|e\s+siga|and\s+execute|and\s+follow|and\s+obey)\b"
                ),
            ],
        ),
        Regra(
            id="OFU-02",
            categoria="conteudo_ofuscado",
            descricao="Uso de caracteres invisíveis ou separadores com termos de controle de IA",
            peso_base=75,
            padroes=[
                # Casamento direto para linhas que foram desofuscadas contendo termos de controle
                re.compile(
                    r"(?i)\b(?:ignore|desconsidere|instruções|prompt|system|modelo|llm|assistente)\b"
                ),
            ],
        ),
    ]


def validar_regras_adicionais(caminho: Path) -> list[Regra]:
    """Lê e valida regras adicionais fornecidas via CLI, rejeitando schemas inválidos."""
    if not caminho.is_file():
        raise ValueError(f"Arquivo de regras adicionais não encontrado: {caminho}")

    texto = caminho.read_text(encoding="utf-8")
    dados: Any = None
    if caminho.suffix.lower() in {".yaml", ".yml"}:
        if yaml is None:
            raise ValueError("PyYAML não está disponível para carregar regras em formato YAML.")
        try:
            dados = yaml.safe_load(texto)
        except Exception as exc:
            raise ValueError(f"YAML de regras inválido: {exc}") from exc
    else:
        try:
            dados = json.loads(texto)
        except Exception as exc:
            raise ValueError(f"JSON de regras inválido: {exc}") from exc

    lista_regras = dados.get("regras") if isinstance(dados, dict) and "regras" in dados else dados
    if not isinstance(lista_regras, list):
        raise ValueError("O arquivo de regras deve conter uma lista de regras (ou chave 'regras').")

    novas_regras: list[Regra] = []
    for idx, item in enumerate(lista_regras):
        if not isinstance(item, dict):
            raise ValueError(f"Regra #{idx + 1} inválida: deve ser um objeto/dicionário.")

        regra_id = item.get("id")
        if not isinstance(regra_id, str) or not regra_id.strip():
            raise ValueError(f"Regra #{idx + 1}: campo 'id' obrigatório e não vazio.")

        categoria = item.get("categoria")
        if not isinstance(categoria, str) or not categoria.strip():
            raise ValueError(f"Regra {regra_id}: campo 'categoria' obrigatório.")

        descricao = item.get("descricao", f"Regra customizada {regra_id}")
        if not isinstance(descricao, str):
            raise ValueError(f"Regra {regra_id}: campo 'descricao' deve ser texto.")

        peso_base = item.get("peso_base", item.get("peso", 40))
        if not isinstance(peso_base, (int, float)) or not (1 <= peso_base <= 100):
            raise ValueError(f"Regra {regra_id}: 'peso_base' deve ser número entre 1 e 100.")

        padroes_raw = item.get("padroes", [])
        if not isinstance(padroes_raw, list) or not padroes_raw:
            raise ValueError(f"Regra {regra_id}: 'padroes' deve ser uma lista não vazia de regex.")

        padroes_compilados: list[re.Pattern[str]] = []
        for p_idx, p in enumerate(padroes_raw):
            if not isinstance(p, str) or not p.strip():
                raise ValueError(f"Regra {regra_id}: padrão #{p_idx + 1} deve ser string não vazia.")
            try:
                padroes_compilados.append(re.compile(p))
            except re.error as exc:
                raise ValueError(f"Regra {regra_id}: regex inválido '{p}': {exc}") from exc

        atenuantes_raw = item.get("padroes_atenuantes", [])
        atenuantes_compilados: list[re.Pattern[str]] = []
        if isinstance(atenuantes_raw, list):
            for a in atenuantes_raw:
                if isinstance(a, str) and a.strip():
                    try:
                        atenuantes_compilados.append(re.compile(a))
                    except re.error as exc:
                        raise ValueError(f"Regra {regra_id}: atenuante inválido '{a}': {exc}") from exc

        novas_regras.append(
            Regra(
                id=regra_id.strip(),
                categoria=categoria.strip(),
                descricao=descricao.strip(),
                peso_base=int(peso_base),
                padroes=padroes_compilados,
                padroes_atenuantes=atenuantes_compilados,
            )
        )

    return novas_regras


def normalizar_para_analise(texto: str) -> tuple[str, bool, bool]:
    """Retorna (texto_normalizado, teve_caracteres_invisiveis, teve_espacamento_anormal)."""
    invisiveis = bool(RE_INVISIBLE_CHARS.search(texto))
    texto_sem_invisiveis = RE_INVISIBLE_CHARS.sub("", texto)

    texto_nfkc = unicodedata.normalize("NFKC", texto_sem_invisiveis)

    espacamento_anormal = bool(RE_SPACED_LETTERS.search(texto_nfkc))

    return texto_nfkc, invisiveis, espacamento_anormal


def descompactar_espacamento_letras(texto: str) -> str:
    """Compacta sequências de letras isoladas separadas por espaços/pontos (ex.: 'i g n o r e' -> 'ignore')."""
    # 1. Junta letras isoladas adjacentes separadas por espaços simples
    junta_isoladas = re.sub(
        r"(?<=\b[a-zA-ZáéíóúãõçÁÉÍÓÚÃÕÇ])\s+(?=[a-zA-ZáéíóúãõçÁÉÍÓÚÃÕÇ]\b)",
        "",
        texto,
    )

    # 2. Substitui sequências capturadas pelo RE_SPACED_LETTERS
    def _sub_spaced(match: re.Match[str]) -> str:
        trecho = match.group(0)
        return re.sub(r"[\s._\-]+", "", trecho)

    return RE_SPACED_LETTERS.sub(_sub_spaced, junta_isoladas)


def inspecionar_blobs_base64_seguro(texto: str) -> list[str]:
    """Analisa blocos Base64 de forma passiva e segura sem nunca executar conteúdo."""
    sinais: list[str] = []
    palavras_controle = {
        "ignore",
        "system",
        "prompt",
        "assistant",
        "bypass",
        "instruction",
        "rules",
        "jailbreak",
        "developer",
    }
    for match in RE_BASE64_BLOB.finditer(texto):
        blob = match.group(0)
        if len(blob) < 16:
            continue
        try:
            decodificado_bytes = base64.b64decode(blob, validate=True)
            decodificado_str = decodificado_bytes.decode("utf-8", errors="ignore").lower()
            encontradas = [w for w in palavras_controle if w in decodificado_str]
            if encontradas:
                sinais.append(
                    f"bloco_base64_revela_termos_controle({','.join(encontradas)})"
                )
        except Exception:
            continue
    return sinais


def mapear_linhas_e_paginas(
    conteudo: str, pagina_inicial_fallback: int | None
) -> list[tuple[int, int | None, str, int]]:
    """Mapeia linha, página, texto e offset absoluto no conteúdo."""
    linhas = conteudo.splitlines(keepends=True)
    mapeamento: list[tuple[int, int | None, str, int]] = []
    pagina_atual = pagina_inicial_fallback
    offset = 0

    for num_linha, linha_com_quebra in enumerate(linhas, start=1):
        linha = linha_com_quebra.rstrip("\r\n")
        match_pag = RE_PAGE_MARKER.search(linha)
        if match_pag:
            for g in match_pag.groups():
                if g and g.isdigit():
                    pagina_atual = int(g)
                    break
        mapeamento.append((num_linha, pagina_atual, linha, offset))
        offset += len(linha_com_quebra)

    return mapeamento


def extrair_contexto_curto(
    conteudo: str, pos_inicio: int, pos_fim: int, tamanho_contexto: int = 120
) -> str:
    """Extrai trecho curto com contexto antes e depois, sanitizado para visualização."""
    inicio = max(0, pos_inicio - tamanho_contexto)
    # Limita também o núcleo: uma linha ou match pode conter megabytes.
    fim = min(len(conteudo), min(pos_fim, pos_inicio + 240) + tamanho_contexto)

    prefixo = "..." if inicio > 0 else ""
    sufixo = "..." if fim < len(conteudo) else ""

    trecho = conteudo[inicio:fim].strip()
    trecho_limpo = re.sub(r"\s+", " ", trecho)
    return f"{prefixo}{trecho_limpo}{sufixo}"


def localizar_match_original(texto: str, analisado: str, inicio: int, fim: int) -> tuple[int, int]:
    """Mapeia caracteres normalizados/compactados para offsets no texto original."""
    caracteres: list[str] = []
    offsets: list[int] = []
    for pos, caractere in enumerate(texto):
        if RE_INVISIBLE_CHARS.fullmatch(caractere):
            continue
        for normalizado in unicodedata.normalize("NFKC", caractere):
            caracteres.append(normalizado)
            offsets.append(pos)
    fonte = "".join(caracteres)
    mapa: list[int] = []
    cursor = 0
    for caractere in analisado:
        pos = fonte.find(caractere, cursor)
        if pos < 0:
            return 0, min(len(texto), 240)
        mapa.append(offsets[pos])
        cursor = pos + 1
    if not mapa or fim <= inicio:
        return 0, min(len(texto), 240)
    return mapa[inicio], mapa[fim - 1] + 1


def calcular_pontuacao_e_atenuantes(
    regra: Regra,
    linha_texto: str,
    contexto_ampliado: str,
    sinais_positivos: list[str],
) -> tuple[int, list[str]]:
    """Calcula pontuação técnica e fatores atenuantes determinísticos."""
    pontuacao = regra.peso_base
    atenuantes: list[str] = []

    # 1. Atenuantes específicos da própria regra
    for pat in regra.padroes_atenuantes:
        if pat.search(contexto_ampliado):
            atenuantes.append(f"atenuante_especifico_regra({regra.id})")
            pontuacao -= 25

    # 2. Atenuantes jurídicos / acadêmicos globais
    for nome_aten, pat_aten, ajuste in ATENUANTES_JURIDICOS:
        # Linguagem processual próxima não explica uma ordem dirigida à IA.
        if nome_aten not in {"contexto_academico_seguranca_ia", "trecho_citado_entre_aspas"}:
            continue
        if pat_aten.search(contexto_ampliado) or pat_aten.search(linha_texto):
            atenuantes.append(nome_aten)
            pontuacao += ajuste

    # 3. Bônus por combinação de múltiplos sinais positivos
    if len(sinais_positivos) > 1:
        pontuacao += 15

    # Atenuação nunca deve esconder o candidato da revisão contextual padrão.
    pontuacao = max(20, min(100, pontuacao))
    return pontuacao, atenuantes


def classificar_nivel_tecnico(pontuacao: int) -> str:
    if pontuacao >= 70:
        return "alto"
    if pontuacao >= 40:
        return "medio"
    if pontuacao >= 20:
        return "baixo"
    return "informativo"


def carregar_entradas(
    alvo: Path,
    excluir_caminhos: Sequence[Path] = (),
) -> tuple[list[SegmentoTexto], list[dict[str, str]], dict[str, Any]]:
    """Carrega segmentos para análise, seja de indexador de PDF, arquivo ou pasta."""
    segmentos: list[SegmentoTexto] = []
    erros: list[dict[str, str]] = []
    metadados_cobertura: dict[str, Any] = {
        "eh_saida_indexador": False,
        "manifest": None,
        "total_paginas_indice": None,
    }

    if not alvo.exists():
        raise FileNotFoundError(f"Caminho não encontrado: {alvo}")

    exclusoes = {p.resolve() for p in excluir_caminhos}

    # Cenário A: Diretório que contém saída de indexador de PDF
    if alvo.is_dir():
        index_json_path = alvo / "index.json"
        manifest_json_path = alvo / "manifest.json"

        if index_json_path.is_file():
            metadados_cobertura["eh_saida_indexador"] = True
            try:
                index_dados = json.loads(index_json_path.read_text(encoding="utf-8"))
            except Exception as exc:
                erros.append({
                    "arquivo": str(index_json_path),
                    "motivo": f"Falha ao carregar index.json: {exc}",
                })
                index_dados = []

            if manifest_json_path.is_file():
                try:
                    manifest_texto = manifest_json_path.read_text(encoding="utf-8")
                    manifest = json.loads(manifest_texto)
                    if not isinstance(manifest, dict):
                        raise ValueError("Manifesto deve ser um objeto JSON")
                    metadados_cobertura["manifest"] = manifest
                    segmentos.append(SegmentoTexto(
                        manifest_json_path, "manifest.json", manifest_texto,
                        hashlib.sha256(manifest_texto.encode("utf-8")).hexdigest(),
                    ))
                    for chave in ("falhas", "erros", "paginas_nao_examinadas", "paginas_sem_texto"):
                        if manifest.get(chave):
                            erros.append({"arquivo": "manifest.json", "motivo": f"Limitação de extração declarada no manifesto: {chave}"})
                except (OSError, ValueError) as exc:
                    erros.append({"arquivo": "manifest.json", "motivo": f"Falha ao carregar manifesto: {exc}"})

            if isinstance(index_dados, list):
                itens_indice = index_dados
            elif isinstance(index_dados, dict) and isinstance(index_dados.get("segmentos"), list):
                itens_indice = index_dados["segmentos"]
            else:
                erros.append({
                    "arquivo": "index.json",
                    "motivo": "Schema inválido: esperado array de segmentos ou objeto com chave 'segmentos' em formato de array",
                })
                return segmentos, erros, metadados_cobertura

            # Metadados também são dados não confiáveis, examinados sem executá-los.
            if itens_indice:
                texto_indice = json.dumps(index_dados, ensure_ascii=False, indent=2)
                segmentos.append(SegmentoTexto(
                    index_json_path, "index.json", texto_indice,
                    hashlib.sha256(texto_indice.encode("utf-8")).hexdigest(),
                ))

            raiz_indice = alvo.resolve()
            cobertura_path = alvo / "cobertura.json"
            if cobertura_path.is_file():
                try:
                    cobertura_texto = cobertura_path.read_text(encoding="utf-8")
                    cobertura = json.loads(cobertura_texto)
                    if not isinstance(cobertura, dict):
                        raise ValueError("Cobertura deve ser um objeto JSON")
                    segmentos.append(SegmentoTexto(
                        cobertura_path, "cobertura.json", cobertura_texto,
                        hashlib.sha256(cobertura_texto.encode("utf-8")).hexdigest(),
                    ))
                    for chave in ("paginas_pendentes", "paginas_sem_conteudo", "paginas_sem_texto", "lacunas", "falhas", "erros"):
                        if cobertura.get(chave):
                            erros.append({"arquivo": "cobertura.json", "motivo": f"Limitação de cobertura declarada: {chave}"})
                except (OSError, ValueError) as exc:
                    erros.append({"arquivo": "cobertura.json", "motivo": f"Falha ao carregar cobertura: {exc}"})
            paginas_extraidas: set[int] = set()
            for item in itens_indice:
                if not isinstance(item, dict):
                    erros.append({
                        "arquivo": "index.json",
                        "motivo": "Item do índice ignorado: esperado objeto",
                    })
                    continue
                caminho_rel = item.get("caminho_texto")
                if not isinstance(caminho_rel, str) or not caminho_rel.strip():
                    erros.append({
                        "arquivo": "index.json",
                        "motivo": "Item do índice sem caminho_texto textual e não vazio",
                    })
                    continue
                caminho_abs = (alvo / caminho_rel).resolve()
                if caminho_abs in exclusoes:
                    continue
                try:
                    caminho_abs.relative_to(raiz_indice)
                except ValueError:
                    erros.append({
                        "arquivo": caminho_rel,
                        "motivo": "Caminho de texto rejeitado: referência externa ao diretório do índice",
                    })
                    continue
                if not caminho_abs.is_file():
                    erros.append({
                        "arquivo": caminho_rel,
                        "motivo": f"Arquivo de texto referenciado no índice não existe: {caminho_rel}",
                    })
                    continue
                try:
                    conteudo = caminho_abs.read_text(encoding="utf-8")
                    if not conteudo.strip():
                        erros.append({"arquivo": caminho_rel, "motivo": "Texto extraído vazio: cobertura documental insuficiente"})
                        continue
                    h = hashlib.sha256(conteudo.encode("utf-8")).hexdigest()
                    segmentos.append(
                        SegmentoTexto(
                            arquivo_origem=caminho_abs,
                            arquivo_relativo=caminho_rel,
                            conteudo=conteudo,
                            hash_conteudo=h,
                            segmento_id=item.get("segmento_id"),
                            id_documento=item.get("id_documento"),
                            pagina_inicial=item.get("pagina_inicial"),
                            pagina_final=item.get("pagina_final"),
                            metodo_identificacao=item.get("metodo_identificacao"),
                        )
                    )
                    primeira, ultima = item.get("pagina_inicial"), item.get("pagina_final")
                    if type(primeira) is int and type(ultima) is int and 1 <= primeira <= ultima <= 100000:
                        paginas_extraidas.update(range(primeira, ultima + 1))
                    for chave in ("falhas", "erros", "paginas_sem_texto", "paginas_pendentes", "avisos"):
                        if item.get(chave):
                            erros.append({"arquivo": caminho_rel, "motivo": f"Limitação/aviso de extração no índice: {chave}"})
                except Exception as exc:
                    erros.append({
                        "arquivo": caminho_rel,
                        "motivo": f"Erro de leitura: {exc}",
                    })
            manifesto = metadados_cobertura["manifest"] or {}
            total_paginas = manifesto.get("paginas", manifesto.get("total_paginas"))
            if type(total_paginas) is int and total_paginas > 0:
                if len([p for p in paginas_extraidas if p <= total_paginas]) < total_paginas:
                    erros.append({"arquivo": "manifest.json", "motivo": "Cobertura de páginas do índice não alcança o total declarado no manifesto"})
            return segmentos, erros, metadados_cobertura

        # Cenário B: Diretório genérico de arquivos de texto
        arquivos = sorted(alvo.rglob("*"))
        for arq in arquivos:
            if not arq.is_file():
                continue
            if arq.resolve() in exclusoes:
                continue
            if arq.suffix.lower() == ".pdf":
                erros.append({"arquivo": str(arq.relative_to(alvo)), "motivo": "PDF não examinado: forneça representação textual indexada"})
                continue
            if arq.name.startswith(".") or arq.suffix.lower() in {
                ".pyc", ".git", ".zip", ".png", ".jpg", ".pdf"
            }:
                continue
            try:
                conteudo = arq.read_text(encoding="utf-8")
                if not conteudo.strip():
                    erros.append({"arquivo": str(arq.relative_to(alvo)), "motivo": "Arquivo textual vazio: sem conteúdo examinável"})
                    continue
                h = hashlib.sha256(conteudo.encode("utf-8")).hexdigest()
                segmentos.append(
                    SegmentoTexto(
                        arquivo_origem=arq,
                        arquivo_relativo=str(arq.relative_to(alvo)),
                        conteudo=conteudo,
                        hash_conteudo=h,
                    )
                )
            except UnicodeDecodeError:
                erros.append({
                    "arquivo": str(arq.relative_to(alvo)),
                    "motivo": "Erro de decodificação UTF-8 / arquivo binário não suportado",
                })
            except Exception as exc:
                erros.append({
                    "arquivo": str(arq.relative_to(alvo)),
                    "motivo": f"Erro de leitura: {exc}",
                })
        return segmentos, erros, metadados_cobertura

    # Cenário C: Arquivo textual individual
    try:
        conteudo = alvo.read_text(encoding="utf-8")
        if not conteudo.strip():
            erros.append({"arquivo": alvo.name, "motivo": "Arquivo textual vazio: sem conteúdo examinável"})
            return segmentos, erros, metadados_cobertura
        h = hashlib.sha256(conteudo.encode("utf-8")).hexdigest()
        segmentos.append(
            SegmentoTexto(
                arquivo_origem=alvo,
                arquivo_relativo=alvo.name,
                conteudo=conteudo,
                hash_conteudo=h,
            )
        )
    except UnicodeDecodeError:
        erros.append({
            "arquivo": alvo.name,
            "motivo": "Erro de decodificação UTF-8 / arquivo ilegível",
        })
    except Exception as exc:
        erros.append({
            "arquivo": alvo.name,
            "motivo": f"Erro de leitura: {exc}",
        })

    return segmentos, erros, metadados_cobertura


def analisar_segmento(
    segmento: SegmentoTexto,
    regras: list[Regra],
    tamanho_contexto: int,
) -> list[OcorrenciaBruta]:
    """Analisa um segmento de texto linha a linha e em bloco contra as regras."""
    ocorrencias: list[OcorrenciaBruta] = []
    linhas_info = mapear_linhas_e_paginas(segmento.conteudo, segmento.pagina_inicial)

    for idx_linha, (num_linha, pagina, linha_bruta, offset_linha) in enumerate(linhas_info):
        if not linha_bruta.strip():
            continue

        linha_norm, invisiveis, espacamento_anormal = normalizar_para_analise(linha_bruta)
        linha_compactada = (
            descompactar_espacamento_letras(linha_norm) if espacamento_anormal else linha_norm
        )
        linha_sem_espaco = re.sub(r"[\s._\-]+", "", linha_norm)

        inicio_ctx = max(0, idx_linha - 2)
        fim_ctx = min(len(linhas_info), idx_linha + 3)
        contexto_ampliado = " ".join(linhas_info[i][2] for i in range(inicio_ctx, fim_ctx))

        # Checagem especial da regra OFU-02 para ofuscação
        if invisiveis or espacamento_anormal:
            tem_controle = bool(
                RE_CONTROL_KEYWORDS.search(linha_compactada)
                or RE_CONTROL_SUBSTRINGS.search(linha_sem_espaco)
            )
            if tem_controle:
                regra_ofu = next((r for r in regras if r.id == "OFU-02"), None)
                if regra_ofu:
                    sinais_pos = [f"regra({regra_ofu.id}): {regra_ofu.descricao}"]
                    if invisiveis:
                        sinais_pos.append("sinal_ofuscacao: caracteres_invisiveis_detectados")
                    if espacamento_anormal:
                        sinais_pos.append("sinal_ofuscacao: letras_separadas_por_espacos_ou_pontos")
                    sinais_pos.append("sinal_ofuscacao: termos_de_controle_identificados_no_payload")

                    pontos, atenuantes = calcular_pontuacao_e_atenuantes(
                        regra_ofu, linha_bruta, contexto_ampliado, sinais_pos
                    )
                    ctx_curto = extrair_contexto_curto(
                        segmento.conteudo,
                        offset_linha,
                        offset_linha + len(linha_bruta),
                        tamanho_contexto=tamanho_contexto,
                    )
                    ocorrencias.append(
                        OcorrenciaBruta(
                            regra=regra_ofu,
                            arquivo_relativo=segmento.arquivo_relativo,
                            segmento_id=segmento.segmento_id,
                            id_documento=segmento.id_documento,
                            pagina=pagina,
                            linha=num_linha,
                            posicao_inicio=offset_linha,
                            posicao_fim=offset_linha + len(linha_bruta),
                            trecho_match=linha_bruta,
                            contexto_completo=ctx_curto,
                            sinais_positivos=sinais_pos,
                            sinais_atenuantes=atenuantes,
                            peso_calculado=pontos,
                            match_normalizado="ofuscacao_termos_controle",
                        )
                    )

        # Checagem das demais regras
        for regra in regras:
            if regra.id == "OFU-02":
                continue

            match_encontrado: re.Match[str] | None = None
            origem_match = ""

            for p in regra.padroes:
                m = p.search(linha_norm)
                if m:
                    match_encontrado = m
                    origem_match = "texto_direto"
                    break

            if not match_encontrado and espacamento_anormal:
                for p in regra.padroes:
                    m = p.search(linha_compactada)
                    if m:
                        match_encontrado = m
                        origem_match = "texto_desofuscado_espacamento"
                        break

            if match_encontrado:
                sinais_pos = [f"regra({regra.id}): {regra.descricao}"]
                if origem_match == "texto_desofuscado_espacamento":
                    sinais_pos.append("sinal_ofuscacao: letras_separadas_por_espacos")
                if invisiveis:
                    sinais_pos.append("sinal_ofuscacao: presenca_caracteres_invisiveis")

                for s_b64 in inspecionar_blobs_base64_seguro(contexto_ampliado):
                    if s_b64 not in sinais_pos:
                        sinais_pos.append(s_b64)

                pontos, atenuantes = calcular_pontuacao_e_atenuantes(
                    regra, linha_bruta, contexto_ampliado, sinais_pos
                )

                trecho_match = match_encontrado.group(0)
                inicio_match, fim_match = localizar_match_original(
                    linha_bruta,
                    linha_compactada if origem_match == "texto_desofuscado_espacamento" else linha_norm,
                    match_encontrado.start(), match_encontrado.end(),
                )
                ctx_curto = extrair_contexto_curto(
                    segmento.conteudo,
                    offset_linha + inicio_match,
                    offset_linha + fim_match,
                    tamanho_contexto=tamanho_contexto,
                )

                match_norm_key = re.sub(r"\s+", " ", trecho_match.strip().lower())

                ocorrencias.append(
                    OcorrenciaBruta(
                        regra=regra,
                        arquivo_relativo=segmento.arquivo_relativo,
                        segmento_id=segmento.segmento_id,
                        id_documento=segmento.id_documento,
                        pagina=pagina,
                        linha=num_linha,
                        posicao_inicio=offset_linha + inicio_match,
                        posicao_fim=offset_linha + fim_match,
                        trecho_match=trecho_match,
                        contexto_completo=ctx_curto,
                        sinais_positivos=sinais_pos,
                        sinais_atenuantes=atenuantes,
                        peso_calculado=pontos,
                        match_normalizado=match_norm_key,
                    )
                )

    # Segunda passagem: padrões quebrados por até três linhas consecutivas.
    # Somente matches que atravessam uma fronteira de linha são adicionados.
    vistos_multilinha: set[tuple[str, int, str]] = set()
    for inicio in range(len(linhas_info)):
        janela = linhas_info[inicio : inicio + 3]
        if len(janela) < 2:
            continue
        linhas_normalizadas = [normalizar_para_analise(item[2])[0] for item in janela]
        texto_janela = " ".join(linhas_normalizadas)
        fronteiras: list[int] = []
        cursor = 0
        for linha in linhas_normalizadas[:-1]:
            cursor += len(linha)
            fronteiras.append(cursor)
            cursor += 1

        for regra in regras:
            if regra.id == "OFU-02":
                continue
            for padrao in regra.padroes:
                match = padrao.search(texto_janela)
                if not match or not any(match.start() <= limite < match.end() for limite in fronteiras):
                    continue

                indice_inicio = sum(1 for limite in fronteiras if limite < match.start())
                indice_fim = sum(1 for limite in fronteiras if limite < match.end())
                if indice_fim <= indice_inicio:
                    continue

                linha_inicio = janela[indice_inicio]
                linha_fim = janela[min(indice_fim, len(janela) - 1)]
                trecho_match = match.group(0)
                match_norm_key = re.sub(r"\s+", " ", trecho_match.strip().lower())
                chave_vista = (regra.id, linha_inicio[0], match_norm_key)
                if chave_vista in vistos_multilinha:
                    continue
                vistos_multilinha.add(chave_vista)

                sinais_pos = [
                    f"regra({regra.id}): {regra.descricao}",
                    "sinal_estrutural: comando_distribuido_em_multiplas_linhas",
                ]
                contexto_ampliado = " ".join(item[2] for item in janela)
                pontos, atenuantes = calcular_pontuacao_e_atenuantes(
                    regra, contexto_ampliado, contexto_ampliado, sinais_pos
                )
                inicio_local = sum(len(l) + 1 for l in linhas_normalizadas[:indice_inicio])
                fim_local = sum(len(l) + 1 for l in linhas_normalizadas[:indice_fim])
                inicio_original, _ = localizar_match_original(
                    linha_inicio[2], linhas_normalizadas[indice_inicio],
                    match.start() - inicio_local, len(linhas_normalizadas[indice_inicio]),
                )
                _, fim_original = localizar_match_original(
                    linha_fim[2], linhas_normalizadas[indice_fim], 0, match.end() - fim_local,
                )
                pos_inicio = linha_inicio[3] + inicio_original
                pos_fim = linha_fim[3] + fim_original
                ocorrencias.append(
                    OcorrenciaBruta(
                        regra=regra,
                        arquivo_relativo=segmento.arquivo_relativo,
                        segmento_id=segmento.segmento_id,
                        id_documento=segmento.id_documento,
                        pagina=linha_inicio[1],
                        linha=linha_inicio[0],
                        posicao_inicio=pos_inicio,
                        posicao_fim=pos_fim,
                        trecho_match=trecho_match,
                        contexto_completo=extrair_contexto_curto(
                            segmento.conteudo, pos_inicio, pos_fim, tamanho_contexto
                        ),
                        sinais_positivos=sinais_pos,
                        sinais_atenuantes=atenuantes,
                        peso_calculado=pontos,
                        match_normalizado=match_norm_key,
                    )
                )
                break

    return ocorrencias


def consolidar_e_agrupar_achados(
    ocorrencias: list[OcorrenciaBruta],
    limiar_pontuacao: int,
) -> list[AchadoConsolidado]:
    """Agrupa ocorrências repetidas do mesmo padrão e gera identificadores estáveis."""
    achados_map: dict[str, AchadoConsolidado] = {}
    contador_id = 1

    for oc in ocorrencias:
        if oc.peso_calculado < limiar_pontuacao:
            continue

        chave_agrupamento = f"{oc.regra.id}::{oc.arquivo_relativo}::{oc.match_normalizado}"
        nivel = classificar_nivel_tecnico(oc.peso_calculado)

        if nivel == "alto":
            rec = "Requer revisão contextual: indício forte de comando dirigido ao modelo ou ofuscação de controle."
        elif nivel == "medio":
            rec = "Requer revisão contextual: padrão suspeito identificado; verificar se há contexto jurídico/processual explicativo."
        elif oc.sinais_atenuantes:
            rec = "Candidato atenuado: padrão localizado em provável contexto forense, citacional ou acadêmico."
        else:
            rec = "Candidato de baixa prioridade: avaliar relevância junto ao teor da peça."

        if chave_agrupamento not in achados_map:
            id_estavel = f"PI-{contador_id:03d}"
            contador_id += 1

            achado = AchadoConsolidado(
                id=id_estavel,
                arquivo=oc.arquivo_relativo,
                segmento_id=oc.segmento_id,
                id_documento=oc.id_documento,
                pagina=oc.pagina,
                linha=oc.linha,
                trecho_contextualizado=oc.contexto_completo,
                regras_acionadas=[oc.regra.id],
                sinais_positivos=sorted(set(oc.sinais_positivos)),
                sinais_atenuantes=sorted(set(oc.sinais_atenuantes)),
                pontuacao_tecnica=oc.peso_calculado,
                nivel_tecnico=nivel,
                recomendacao_revisao=rec,
                ocorrencias_adicionais=[],
            )
            achados_map[chave_agrupamento] = achado
        else:
            achado_existente = achados_map[chave_agrupamento]
            achado_existente.ocorrencias_adicionais.append({
                "arquivo": oc.arquivo_relativo,
                "pagina": oc.pagina,
                "linha": oc.linha,
            })
            if oc.regra.id not in achado_existente.regras_acionadas:
                achado_existente.regras_acionadas.append(oc.regra.id)
            if oc.peso_calculado > achado_existente.pontuacao_tecnica:
                achado_existente.pontuacao_tecnica = oc.peso_calculado
                achado_existente.nivel_tecnico = nivel
                achado_existente.recomendacao_revisao = rec

    lista_achados = sorted(
        achados_map.values(), key=lambda a: (-a.pontuacao_tecnica, a.id)
    )
    return lista_achados


def gerar_relatorio_markdown(resultado: dict[str, Any]) -> str:
    """Gera relatório Markdown conciso e seguro, sem expor grandes payloads."""
    linhas: list[str] = []
    linhas.append("# Relatório de Triagem de Prompt Injection")
    linhas.append("")
    linhas.append(f"- **Data de Execução**: {resultado['data_execucao']}")
    linhas.append(f"- **Versão do Schema**: `{resultado['versao_schema']}` | **Regras**: `{resultado['versao_regras']}`")

    res_cob = resultado["resumo_cobertura"]
    status_cob = res_cob["status"].upper()
    linhas.append(f"- **Status de Cobertura**: `{status_cob}`")
    linhas.append(
        f"- **Arquivos Identificados / Examinados**: {res_cob['total_arquivos_identificados']} / {res_cob['total_arquivos_examinados']}"
    )

    if res_cob["arquivos_nao_examinados"]:
        linhas.append("")
        linhas.append("### Limitações e Arquivos Não Examinados")
        for ne in res_cob["arquivos_nao_examinados"]:
            linhas.append(f"- `{ne['arquivo']}`: {ne['motivo']}")

    res_cand = resultado["resumo_candidatos"]
    linhas.append("")
    linhas.append("## Resumo Técnico dos Candidatos")
    linhas.append(
        f"Total de candidatos reportados: **{res_cand['total_candidatos']}** (ocorrências brutas: {res_cand['total_ocorrencias']})"
    )
    linhas.append("")
    linhas.append("| Nível Técnico | Quantidade |")
    linhas.append("| :--- | :--- |")
    for niv, qtd in res_cand["por_nivel"].items():
        linhas.append(f"| **{niv.capitalize()}** | {qtd} |")

    candidatos = resultado["candidatos"]
    if not candidatos:
        linhas.append("")
        linhas.append("> [!NOTE]")
        linhas.append(
            "> Nenhum indício ou padrão técnico de prompt injection foi localizado nos arquivos efetivamente examinados. "
            "A ausência de achados autoriza afirmar apenas que os padrões conhecidos não foram encontrados na cobertura examinada."
        )
    else:
        linhas.append("")
        linhas.append("## Achados e Candidatos para Revisão Contextual")
        for c in candidatos:
            linhas.append(f"### Candidato `{c['id']}` — Nível: **{c['nivel_tecnico'].upper()}** (Score: {c['pontuacao_tecnica']}/100)")
            linhas.append(f"- **Arquivo**: `{c['arquivo']}`" + (f" (Id Doc: `{c['id_documento']}`)" if c.get("id_documento") else ""))
            loc = []
            if c.get("pagina") is not None:
                loc.append(f"Página {c['pagina']}")
            if c.get("linha") is not None:
                loc.append(f"Linha {c['linha']}")
            if loc:
                linhas.append(f"- **Localização**: {', '.join(loc)}")
            linhas.append(f"- **Regras Acionadas**: `{', '.join(c['regras_acionadas'])}`")
            linhas.append(f"- **Recomendação**: {c['recomendacao_revisao']}")

            linhas.append("- **Sinais Positivos**:")
            for sp in c["sinais_positivos"]:
                linhas.append(f"  - {sp}")

            if c.get("sinais_atenuantes"):
                linhas.append("- **Sinais Atenuantes**:")
                for sa in c["sinais_atenuantes"]:
                    linhas.append(f"  - {sa}")

            linhas.append(f"- **Trecho Contextualizado**: `{c['trecho_contextualizado']}`")

            if c.get("ocorrencias_adicionais"):
                qtd_rep = len(c["ocorrencias_adicionais"])
                linhas.append(f"- **Ocorrências Repetidas Agrupadas**: {qtd_rep} repetição(ões)")

            linhas.append("")

    return "\n".join(linhas) + "\n"


def executar_triagem(
    alvo: Path,
    caminho_regras: Path | None = None,
    tamanho_contexto: int = 120,
    limiar_pontuacao: int = 20,
    incluir_baixa_confianca: bool = False,
    excluir_caminhos: Sequence[Path] = (),
) -> dict[str, Any]:
    """Executa o pipeline determinístico completo de triagem."""
    regras = carregar_regras_padrao()
    if tamanho_contexto < 0 or not 0 <= limiar_pontuacao <= 100:
        raise ValueError("Contexto deve ser não negativo e limiar deve estar entre 0 e 100")
    if caminho_regras:
        novas = validar_regras_adicionais(caminho_regras)
        regras.extend(novas)

    if incluir_baixa_confianca:
        limiar_pontuacao = 0

    segmentos, erros_leitura, meta_indice = carregar_entradas(
        alvo, excluir_caminhos=excluir_caminhos
    )

    total_identificados = len(segmentos) + len(erros_leitura)
    total_examinados = len(segmentos)

    status_cobertura = "completa"
    textos_documentais = [s for s in segmentos if s.arquivo_relativo not in {"index.json", "manifest.json", "cobertura.json"}]
    if total_examinados == 0 or (meta_indice["eh_saida_indexador"] and not textos_documentais):
        status_cobertura = "inconclusiva"
    elif erros_leitura:
        status_cobertura = "parcial"

    hashes_arquivos: list[dict[str, str]] = []
    concatenacao_hashes = []
    for s in segmentos:
        hashes_arquivos.append({"arquivo": s.arquivo_relativo, "hash_sha256": s.hash_conteudo})
        concatenacao_hashes.append(s.hash_conteudo)

    hash_consolidado = (
        hashlib.sha256("".join(concatenacao_hashes).encode("utf-8")).hexdigest()
        if concatenacao_hashes
        else None
    )

    todas_ocorrencias: list[OcorrenciaBruta] = []
    for s in segmentos:
        oc_seg = analisar_segmento(s, regras, tamanho_contexto=tamanho_contexto)
        todas_ocorrencias.extend(oc_seg)

    achados = consolidar_e_agrupar_achados(todas_ocorrencias, limiar_pontuacao=limiar_pontuacao)

    contagem_niveis = {"alto": 0, "medio": 0, "baixo": 0, "informativo": 0}
    for a in achados:
        contagem_niveis[a.nivel_tecnico] += 1

    total_ocorrencias_brutas = sum(1 + len(a.ocorrencias_adicionais) for a in achados)

    resultado = {
        "versao_schema": SCHEMA_VERSION,
        "versao_regras": RULES_VERSION,
        "data_execucao": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "resumo_cobertura": {
            "status": status_cobertura,
            "total_arquivos_identificados": total_identificados,
            "total_arquivos_examinados": total_examinados,
            "total_arquivos_nao_examinados": len(erros_leitura),
            "arquivos_examinados": hashes_arquivos,
            "arquivos_nao_examinados": erros_leitura,
            "hash_consolidado": hash_consolidado,
        },
        "resumo_candidatos": {
            "total_candidatos": len(achados),
            "total_ocorrencias": total_ocorrencias_brutas,
            "por_nivel": contagem_niveis,
        },
        "candidatos": [dataclasses.asdict(a) for a in achados],
    }

    return resultado


def construir_argumentos() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Triagem determinística de indícios de prompt injection em documentos."
    )
    parser.add_argument(
        "alvo",
        type=Path,
        help="Arquivo textual, diretório de textos ou pasta de saída do indexador de PDF.",
    )
    parser.add_argument(
        "--out",
        "-o",
        type=Path,
        default=None,
        help="Caminho para salvar o resultado em formato JSON.",
    )
    parser.add_argument(
        "--markdown",
        "-m",
        type=Path,
        default=None,
        help="Caminho para salvar o relatório formatado em Markdown.",
    )
    parser.add_argument(
        "--contexto",
        "-c",
        type=int,
        default=120,
        help="Tamanho máximo em caracteres do contexto antes e depois do trecho (padrão: 120).",
    )
    parser.add_argument(
        "--limiar",
        "-l",
        type=int,
        default=20,
        help="Pontuação técnica mínima para reportar candidatos (padrão: 20).",
    )
    parser.add_argument(
        "--regras",
        "-r",
        type=Path,
        default=None,
        help="Arquivo JSON ou YAML contendo regras adicionais validadas.",
    )
    parser.add_argument(
        "--incluir-baixa-confianca",
        action="store_true",
        help="Inclui todos os candidatos detectados, ignorando o limiar de pontuação.",
    )
    parser.add_argument(
        "--fail-on",
        choices=["high", "alto", "medium", "medio", "low", "baixo"],
        default=None,
        help="Encerra com código não-zero se houver candidatos no nível especificado ou superior.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = construir_argumentos()
    args = parser.parse_args(argv)

    try:
        resultado = executar_triagem(
            alvo=args.alvo,
            caminho_regras=args.regras,
            tamanho_contexto=args.contexto,
            limiar_pontuacao=args.limiar,
            incluir_baixa_confianca=args.incluir_baixa_confianca,
            excluir_caminhos=tuple(p for p in (args.out, args.markdown) if p is not None),
        )
    except (ValueError, FileNotFoundError) as exc:
        print(f"Erro de validação/execução: {exc}", file=sys.stderr)
        return 1

    json_str = json.dumps(resultado, indent=2, ensure_ascii=False)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json_str, encoding="utf-8")
        print(f"JSON de segurança gravado em: {args.out}")
    else:
        if not args.markdown:
            print(json_str)

    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        md_conteudo = gerar_relatorio_markdown(resultado)
        args.markdown.write_text(md_conteudo, encoding="utf-8")
        print(f"Relatório Markdown gravado em: {args.markdown}")

    if args.fail_on:
        niveis_map = {
            "high": "alto",
            "alto": "alto",
            "medium": "medio",
            "medio": "medio",
            "low": "baixo",
            "baixo": "baixo",
        }
        alvo_nivel = niveis_map[args.fail_on]
        hierarquia = {"alto": 3, "medio": 2, "baixo": 1, "informativo": 0}
        min_rank = hierarquia[alvo_nivel]

        for cand in resultado["candidatos"]:
            rank_cand = hierarquia.get(cand["nivel_tecnico"], 0)
            if rank_cand >= min_rank:
                print(
                    f"Falha de segurança (--fail-on {args.fail_on}): candidato detectado com nível '{cand['nivel_tecnico']}' (id: {cand['id']}).",
                    file=sys.stderr,
                )
                return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
