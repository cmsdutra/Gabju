"""
parametros_externos.py - Salário mínimo e teto do RGPS para competências posteriores à tabela
estática de salario_minimo.py, com validação, cache e avisos.

Fontes (ver references/parametros-rgps-spec.md):
- Salário mínimo: BCB/SGS série 1619 (oficial); reserva: página de contribuição mensal do INSS.
- Teto: página de contribuição mensal do INSS (oficial); reserva/conferência: tabelas do IEPREV e
  do Previdenciarista (não oficiais).

Regras:
- Valor confirmado fica em cache na pasta do usuário e não é consultado de novo (histórico não muda).
- Valor novo só é aceito se for maior que o anterior e com reajuste plausível (REAJUSTE_MAXIMO).
- Sem confirmação, usa o último valor conhecido e registra aviso — nunca em silêncio.
- CNIS_CALCULATOR_OFFLINE=1 desliga a rede; CNIS_CALCULATOR_CACHE_DIR troca a pasta do cache.
"""

import json
import os
import re
import time
import urllib.request
from datetime import date
from html import unescape
from typing import Dict, List, Optional, Tuple

URL_BCB_SM = ("https://api.bcb.gov.br/dados/serie/bcdata.sgs.1619/dados"
              "?formato=json&dataInicial={ini}&dataFinal={fim}")
URL_INSS_TABELA = ("https://www.gov.br/inss/pt-br/direitos-e-deveres/inscricao-e-contribuicao/"
                   "tabela-de-contribuicao-mensal")
FONTES_TETO_NAO_OFICIAIS = [
    ("IEPREV", "https://www.ieprev.com.br/ferramentas/tabela-dos-tetos-previdenciarios-do-inss"),
    ("Previdenciarista", "https://previdenciarista.com/tabela-historica-de-tetos-previdenciarios-da-previdencia-social-inss-a-partir-de-1994/"),
]
FONTE_BCB = "BCB/SGS 1619"
FONTE_INSS = "INSS (tabela de contribuição mensal)"

# Reajuste acima de 25% sobre o valor anterior é tratado como leitura errada da fonte.
REAJUSTE_MAXIMO = 1.25
ARQUIVO_CACHE = "parametros_rgps.json"

MESES = {
    "janeiro": 1, "fevereiro": 2, "março": 3, "marco": 3, "abril": 4, "maio": 5, "junho": 6,
    "julho": 7, "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12,
    "jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6,
    "jul": 7, "ago": 8, "set": 9, "out": 10, "nov": 11, "dez": 12,
}
_RE_VALOR = r"(\d{1,3}(?:\.\d{3})*,\d{2})"

# Estado da execução: consultas já tentadas e avisos gerados
_TENTATIVAS: set = set()
_AVISOS_COMP: Dict[str, List[str]] = {}
_AVISOS_GERAIS: List[str] = []
_PROVISORIOS: List[Tuple[str, str, float]] = []  # (parâmetro, competência, valor usado)
_CACHE: Optional[dict] = None


# --------------------------------------------------------------------------------------------
# Utilitários
# --------------------------------------------------------------------------------------------

def diretorio_cache() -> str:
    """Pasta de cache do usuário (fora da pasta da skill, que num plugin pode ser somente leitura)."""
    env = os.environ.get("CNIS_CALCULATOR_CACHE_DIR")
    if env:
        return env
    if os.name == "nt":
        return os.path.join(os.environ.get("LOCALAPPDATA") or os.path.expanduser("~"), "cnis-calculator")
    base = os.environ.get("XDG_CACHE_HOME") or os.path.join(os.path.expanduser("~"), ".cache")
    return os.path.join(base, "cnis-calculator")

def _offline() -> bool:
    return os.environ.get("CNIS_CALCULATOR_OFFLINE") == "1"

def _hoje() -> date:
    return date.today()

def _chave(comp: str) -> Tuple[int, int]:
    m, y = comp.split("/")
    return int(y), int(m)

def _comp(y: int, m: int) -> str:
    return f"{m:02d}/{y}"

def _comp_hoje() -> str:
    h = _hoje()
    return _comp(h.year, h.month)

def _proxima(comp: str) -> str:
    y, m = _chave(comp)
    return _comp(y + 1, 1) if m == 12 else _comp(y, m + 1)

def _anterior(comp: str) -> str:
    y, m = _chave(comp)
    return _comp(y - 1, 12) if m == 1 else _comp(y, m - 1)

def _num(txt: str) -> float:
    return float(txt.replace(".", "").replace(",", "."))

def _fmt(v: float) -> str:
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def _plausivel(anterior: float, novo: float, pode_repetir: bool) -> bool:
    if pode_repetir and abs(novo - anterior) < 0.005:
        return True
    return anterior < novo <= anterior * REAJUSTE_MAXIMO

def _baixar(url: str, timeout: int = 20, tentativas: int = 3) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for n in range(tentativas):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                dados = resp.read()
            break
        except Exception:
            # A API do BCB devolve 502 intermitente; nova tentativa antes de ir para a reserva
            if n == tentativas - 1:
                raise
            time.sleep(1.5 * (n + 1))
    # A página do INSS declara ISO-8859-1, mas é servida em UTF-8
    try:
        return dados.decode("utf-8")
    except UnicodeDecodeError:
        return dados.decode("latin-1")

def _texto(html: str) -> str:
    """HTML -> texto corrido, sem tags, com espaços normalizados."""
    t = re.sub(r"(?is)<(script|style|template)\b.*?</\1>", " ", html)
    t = re.sub(r"(?s)<!--.*?-->", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = unescape(t).replace("\xa0", " ")
    return re.sub(r"\s+", " ", t)


# --------------------------------------------------------------------------------------------
# Parsers (determinísticos, testados com cópias salvas das páginas em tests/fixtures)
# --------------------------------------------------------------------------------------------

def parse_bcb_sm(conteudo_json: str) -> Dict[str, float]:
    """Resposta da API SGS (lista de {"data": "01/MM/AAAA", "valor": "x"}) -> {MM/AAAA: valor}."""
    out = {}
    for item in json.loads(conteudo_json):
        _, m, y = item["data"].split("/")
        out[_comp(int(y), int(m))] = float(item["valor"])
    return out

def parse_inss_tabela(html: str) -> Optional[dict]:
    """
    Página de contribuição mensal do INSS -> {"inicio": MM/AAAA, "salario_minimo": x, "teto": y}.
    Usa o título "TABELAS VÁLIDAS A PARTIR DA COMPETÊNCIA <MÊS> DE <ANO>"; o salário mínimo é a
    primeira faixa ("Até R$ x") e o teto é o maior valor da seção. Exige que o par
    "R$ <S.M.> até R$ <teto>" da tabela do contribuinte individual confirme os dois.
    """
    t = _texto(html)
    m = re.search(r"A PARTIR DA COMPET\w*NCIA\s+(\w+)\s+DE\s+(\d{4})", t, re.I)
    if not m:
        return None
    mes = MESES.get(m.group(1).lower())
    if not mes:
        return None
    secao = t[m.end(): m.end() + 4000]
    fim = re.search(r"Os valores das tabelas", secao, re.I)
    if fim:
        secao = secao[:fim.start()]
    valores = [_num(v) for v in re.findall(r"R\$\s*" + _RE_VALOR, secao)]
    primeira = re.search(r"At\w\s*R\$\s*" + _RE_VALOR, secao, re.I)
    if not valores or not primeira:
        return None
    sm, teto = _num(primeira.group(1)), max(valores)
    pares = {(_num(a), _num(b)) for a, b in
             re.findall(r"R\$\s*" + _RE_VALOR + r"\s*at\w\s*R\$\s*" + _RE_VALOR, secao, re.I)}
    if (sm, teto) not in pares:
        return None
    return {"inicio": _comp(int(m.group(2)), mes), "salario_minimo": sm, "teto": teto}

def parse_tabela_tetos(html: str) -> List[Tuple[str, float]]:
    """
    Tabela histórica de tetos (IEPREV, Previdenciarista) -> [(MM/AAAA de início, valor)], em ordem.
    Reconhece "janeiro de 2026 R$ 8.475,55" e "jan/2026 R$ 8.475,55".
    """
    t = _texto(html)
    nomes = "|".join(sorted(MESES, key=len, reverse=True))
    padrao = r"\b(" + nomes + r")\s*(?:de|/)\s*(\d{4})\s+R\$\s*" + _RE_VALOR
    linhas = {}
    for mes_txt, ano, valor in re.findall(padrao, t, re.I):
        comp = _comp(int(ano), MESES[mes_txt.lower()])
        linhas.setdefault(comp, _num(valor))
    return sorted(linhas.items(), key=lambda kv: _chave(kv[0]))


# --------------------------------------------------------------------------------------------
# Cache
# --------------------------------------------------------------------------------------------

def _cache() -> dict:
    global _CACHE
    if _CACHE is None:
        _CACHE = {"salario_minimo": {}, "teto": []}
        try:
            with open(os.path.join(diretorio_cache(), ARQUIVO_CACHE), "r", encoding="utf-8") as f:
                dados = json.load(f)
            _CACHE["salario_minimo"] = dados.get("salario_minimo", {})
            _CACHE["teto"] = dados.get("teto", [])
        except (OSError, ValueError):
            pass
    return _CACHE

def _salvar_cache() -> None:
    try:
        pasta = diretorio_cache()
        os.makedirs(pasta, exist_ok=True)
        destino = os.path.join(pasta, ARQUIVO_CACHE)
        tmp = destino + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(_cache(), f, ensure_ascii=False, indent=2)
        os.replace(tmp, destino)
    except OSError as e:
        _aviso_geral(f"Não foi possível gravar o cache de parâmetros em {diretorio_cache()}: {e}")

def reiniciar_estado() -> None:
    """Esquece cache em memória, tentativas e avisos (usado pelos testes)."""
    global _CACHE
    _CACHE = None
    _TENTATIVAS.clear()
    _AVISOS_COMP.clear()
    _AVISOS_GERAIS.clear()
    _PROVISORIOS.clear()


# --------------------------------------------------------------------------------------------
# Avisos
# --------------------------------------------------------------------------------------------

def _aviso_geral(msg: str) -> None:
    if msg not in _AVISOS_GERAIS:
        _AVISOS_GERAIS.append(msg)

def _aviso_comp(parametro: str, comp: str, valor: float) -> None:
    futura = " (competência futura)" if _chave(comp) > _chave(_comp_hoje()) else ""
    msg = (f"{parametro} de {comp} não confirmado em fonte externa{futura}; "
           f"usado o último valor conhecido (R$ {_fmt(valor)})")
    lista = _AVISOS_COMP.setdefault(comp, [])
    if msg not in lista:
        lista.append(msg)
        _PROVISORIOS.append((parametro, comp, valor))

def avisos_competencia(comp: str) -> List[str]:
    return list(_AVISOS_COMP.get(comp, []))

def avisos_gerais() -> List[str]:
    """Avisos de fonte (divergências, valores rejeitados) + resumo dos valores provisórios."""
    out = list(_AVISOS_GERAIS)
    por_parametro: Dict[str, List[Tuple[str, float]]] = {}
    for parametro, comp, valor in _PROVISORIOS:
        por_parametro.setdefault(parametro, []).append((comp, valor))
    for parametro, itens in por_parametro.items():
        itens.sort(key=lambda x: _chave(x[0]))
        faixa = itens[0][0] if len(itens) == 1 else f"{itens[0][0]} a {itens[-1][0]}"
        valores = sorted({v for _, v in itens})
        out.append(f"{parametro} não confirmado em {len(itens)} competência(s) ({faixa}); "
                   f"usado o último valor conhecido (R$ {', R$ '.join(_fmt(v) for v in valores)}). "
                   "Confira antes de usar o cálculo.")
    return out


# --------------------------------------------------------------------------------------------
# Salário mínimo
# --------------------------------------------------------------------------------------------

def _ultimo_sm(comp: str, base_comp: str, base_valor: float) -> float:
    anteriores = [(k, r["valor"]) for k, r in _cache()["salario_minimo"].items()
                  if _chave(k) < _chave(comp)]
    if not anteriores:
        return base_valor
    return max(anteriores, key=lambda kv: _chave(kv[0]))[1]

def _registrar_sm(meses: Dict[str, float], fonte: str, base_comp: str, base_valor: float) -> None:
    """Grava meses em ordem, validando cada um contra o anterior (repetição é permitida)."""
    sm = _cache()["salario_minimo"]
    hoje_iso = _hoje().isoformat()
    for comp in sorted(meses, key=_chave):
        if _chave(comp) <= _chave(base_comp) or comp in sm:
            continue
        anterior = _ultimo_sm(comp, base_comp, base_valor)
        if not _plausivel(anterior, meses[comp], pode_repetir=True):
            _aviso_geral(f"Salário mínimo de {comp} lido em {fonte} (R$ {_fmt(meses[comp])}) "
                         f"rejeitado: implausível frente ao anterior (R$ {_fmt(anterior)})")
            break
        sm[comp] = {"valor": meses[comp], "fonte": fonte, "obtido_em": hoje_iso}

def _atualizar_sm(base_comp: str, base_valor: float) -> None:
    ini = _proxima(base_comp)
    fim = _comp_hoje()
    if _chave(ini) > _chave(fim):
        return
    y_i, m_i = _chave(ini)
    y_f, m_f = _chave(fim)
    try:
        url = URL_BCB_SM.format(ini=f"01/{m_i:02d}/{y_i}", fim=f"28/{m_f:02d}/{y_f}")
        _registrar_sm(parse_bcb_sm(_baixar(url)), FONTE_BCB, base_comp, base_valor)
    except Exception:
        pass
    if fim in _cache()["salario_minimo"]:
        return
    # Reserva: página do INSS cobre do início da vigência até o mês da consulta
    try:
        info = parse_inss_tabela(_baixar(URL_INSS_TABELA))
    except Exception:
        info = None
    if info and _chave(info["inicio"]) > _chave(base_comp):
        meses, c = {}, info["inicio"]
        while _chave(c) <= _chave(fim):
            meses[c] = info["salario_minimo"]
            c = _proxima(c)
        _registrar_sm(meses, FONTE_INSS, base_comp, base_valor)

def salario_minimo_externo(comp: str, base_comp: str, base_valor: float) -> float:
    """S.M. de competência posterior à tabela estática (base_comp/base_valor = última estática)."""
    reg = _cache()["salario_minimo"].get(comp)
    if reg is None and not _offline() and "sm" not in _TENTATIVAS:
        _TENTATIVAS.add("sm")
        _atualizar_sm(base_comp, base_valor)
        _salvar_cache()
        reg = _cache()["salario_minimo"].get(comp)
    if reg is not None:
        return reg["valor"]
    valor = _ultimo_sm(comp, base_comp, base_valor)
    _aviso_comp("Salário mínimo", comp, valor)
    return valor


# --------------------------------------------------------------------------------------------
# Teto do RGPS
# --------------------------------------------------------------------------------------------

def _vigencia_teto(comp: str) -> Optional[dict]:
    candidatas = [v for v in _cache()["teto"] if _chave(v["inicio"]) <= _chave(comp)]
    return max(candidatas, key=lambda v: _chave(v["inicio"])) if candidatas else None

def _teto_confirmado(comp: str) -> Optional[float]:
    """
    Confirmado se a vigência externa que cobre a competência começou no mesmo ano (o teto é
    reajustado todo janeiro desde 2010) e a fonte foi consultada com a competência já iniciada.
    """
    v = _vigencia_teto(comp)
    if v and _chave(v["inicio"])[0] == _chave(comp)[0] and _chave(v["confirmado_ate"]) >= _chave(comp):
        return v["valor"]
    return None

def _atualizar_teto(base_comp: str, base_valor: float) -> None:
    hoje = _comp_hoje()
    hoje_iso = _hoje().isoformat()
    novas: Dict[str, dict] = {}

    try:
        info = parse_inss_tabela(_baixar(URL_INSS_TABELA))
    except Exception:
        info = None
    if info and _chave(info["inicio"]) > _chave(base_comp):
        novas[info["inicio"]] = {"inicio": info["inicio"], "valor": info["teto"],
                                 "fonte": FONTE_INSS, "confirmado_ate": hoje, "obtido_em": hoje_iso}

    nao_oficiais: Dict[str, Dict[str, float]] = {}
    for nome, url in FONTES_TETO_NAO_OFICIAIS:
        try:
            linhas = parse_tabela_tetos(_baixar(url))
        except Exception:
            continue
        for i, (inicio, valor) in enumerate(linhas):
            if _chave(inicio) <= _chave(base_comp):
                continue
            fim = _anterior(linhas[i + 1][0]) if i + 1 < len(linhas) else hoje
            nao_oficiais.setdefault(inicio, {})[nome] = valor
            if inicio in novas:
                if abs(novas[inicio]["valor"] - valor) >= 0.005:
                    _aviso_geral(f"Teto de {inicio}: INSS informa R$ {_fmt(novas[inicio]['valor'])} e "
                                 f"{nome} informa R$ {_fmt(valor)}; usado o valor do INSS")
                continue
            novas[inicio] = {"inicio": inicio, "valor": valor, "fonte": f"{nome} (não oficial)",
                             "confirmado_ate": fim, "obtido_em": hoje_iso}

    for inicio, por_fonte in nao_oficiais.items():
        if len(set(round(v, 2) for v in por_fonte.values())) > 1 and not novas[inicio]["fonte"] == FONTE_INSS:
            detalhes = "; ".join(f"{n}: R$ {_fmt(v)}" for n, v in por_fonte.items())
            _aviso_geral(f"Teto de {inicio} diverge entre fontes não oficiais ({detalhes}); valor descartado")
            del novas[inicio]

    existentes = {v["inicio"]: v for v in _cache()["teto"]}
    anterior = base_valor
    for inicio in sorted(set(existentes) | set(novas), key=_chave):
        nova = novas.get(inicio)
        atual = existentes.get(inicio)
        if nova is None:
            anterior = atual["valor"]
            continue
        if atual is not None:
            if abs(atual["valor"] - nova["valor"]) < 0.005:
                if _chave(nova["confirmado_ate"]) > _chave(atual["confirmado_ate"]):
                    atual["confirmado_ate"] = nova["confirmado_ate"]
            else:
                _aviso_geral(f"Teto de {inicio}: fonte informa agora R$ {_fmt(nova['valor'])}, "
                             f"cache tem R$ {_fmt(atual['valor'])}; mantido o cache")
            anterior = atual["valor"]
            continue
        if not _plausivel(anterior, nova["valor"], pode_repetir=False):
            _aviso_geral(f"Teto de {inicio} lido em {nova['fonte']} (R$ {_fmt(nova['valor'])}) "
                         f"rejeitado: implausível frente ao anterior (R$ {_fmt(anterior)})")
            continue
        _cache()["teto"].append(nova)
        anterior = nova["valor"]
    _cache()["teto"].sort(key=lambda v: _chave(v["inicio"]))

def teto_externo(comp: str, base_comp: str, base_valor: float) -> float:
    """Teto de competência posterior à tabela estática (base_comp/base_valor = última estática)."""
    valor = _teto_confirmado(comp)
    if valor is None and not _offline() and "teto" not in _TENTATIVAS:
        _TENTATIVAS.add("teto")
        _atualizar_teto(base_comp, base_valor)
        _salvar_cache()
        valor = _teto_confirmado(comp)
    if valor is not None:
        return valor
    v = _vigencia_teto(comp)
    usado = v["valor"] if v else base_valor
    _aviso_comp("Teto do RGPS", comp, usado)
    return usado
