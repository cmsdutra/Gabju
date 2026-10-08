"""Núcleo determinístico de cálculo previdenciário a partir do JSON canônico do CNIS.

A interface pública é ``analisar_cnis.py``. Este módulo não faz ingestão, não gera
documentos e não oferece saída tabular: concentra apenas as funções de cálculo.
"""

import os
import sys
import json
import math
import argparse
from datetime import datetime, date, timedelta
from calendar import monthrange
from typing import Dict, List, Any, Optional, Tuple

from salario_minimo import get_salario_minimo, get_teto_rgps, format_currency_br, avisos_competencia, avisos_parametros
from mps_indices import get_mps_indices

DATA_REFORMA = date(2019, 11, 13)
CODES_MES_CHEIO_PRE = {"05", "06", "07", "08", "09", "10"}

TABELA_PARAMETROS_CODIGOS = [
    (1, "Empregado Urbano / Rural (CLT)", "Empregado", "Empregador (Empresa)", "Progressiva (7,5-14%)", "Sim (Absoluta)", "Sim", "Sim", "Vínculo comprovado gera tempo integral; salário ausente adota 1 S.M. (Art. 35, II)"),
    (2, "Empregado Doméstico (Pós-06/2015)", "Doméstico", "Empregador via eSocial", "DAE unificado", "Sim", "Sim", "Sim", "Equiparado a CLT; salário ausente adota 1 S.M."),
    (3, "Empregado Doméstico (Pré-06/2015)", "Doméstico", "Empregador Doméstico", "8% a 11% (GPS)", "Mitigada", "Sim", "Sim", "Exige CTPS idônea; na dúvida INSS exige guias quitadas"),
    (4, "Trabalhador Avulso", "Avulso", "Tomador / OGMO / Sindicato", "Folha de pagamento", "Sim", "Sim", "Sim", "Suprida por declaração oficial do OGMO/Sindicato"),
    (5, "Contribuinte Individual - Tomador PJ", "C.I.", "Empresa Tomadora (Lei 10.666)", "11% retido", "Sim", "Sim", "Sim", "Comprovada prestação de serviços (RPA/NF), gera tempo mesmo sem repasse"),
    (6, "Contribuinte Individual - Conta Própria", "C.I. / Autônomo", "Próprio Segurado", "20% (código 1007)", "Não", "Condicionada", "Sim", "0 dias líquidos. Ausência só é suprida com indenização (Art. 45-A)"),
    (7, "Contribuinte Individual - Simplificado", "C.I.", "Próprio Segurado", "11% sobre SM (cód 1163)", "Não", "Condicionada", "Não (Apenas Idade)", "0 dias p/ Tempo de Contribuição. Exige complementação de 9% + juros"),
    (8, "Microempreendedor Individual (MEI)", "C.I. Especial", "Próprio Segurado", "5% sobre SM (DAS-MEI)", "Não", "Condicionada", "Não (Apenas Idade)", "Se DAS não pago: 0 dias. Para tempo, exige complementação de 15%"),
    (9, "Segurado Facultativo - Normal", "Facultativo", "Próprio Segurado", "20% (código 1406)", "Não", "Condicionada", "Sim", "Proibido recolhimento retroativo sem inscrição prévia e tempestividade"),
    (10, "Facultativo - Baixa Renda", "Facultativo", "Próprio Segurado", "5% sobre SM (cód 1929)", "Não", "Condicionada", "Não (Apenas Idade)", "Se CadÚnico desatualizado, tempo é glosado até complementar para 11%/20%"),
    (11, "Segurado Especial (Produtor Rural)", "Segurado Especial", "Sub-rogação comercialização", "% sobre produção", "Sim (p/ tempo)", "Sim", "Sim (até 12/11/19)", "Tempo rural pré-2019 não tem salário no CNIS; gera tempo, RMI = 1 S.M."),
    (12, "Benefício Incapacidade Comum (B31)", "Beneficiário", "INSS", "Isento (SB entra no PBC)", "N/A", "Se intercalado", "Se intercalado", "Exige retorno imediato a atividade/recolhimento. Se não intercalar: 0 dias"),
    (13, "Benefício Acidentário (B91)", "Beneficiário", "INSS", "Isento", "N/A", "Sim", "Sim", "Suprido por processo de benefício acidentário/CAT"),
    (14, "Serviço Militar Obrigatório", "Militar", "Forças Armadas", "Não contributivo", "N/A", "Não", "Sim", "Suprido por Certificado de Reservista. Salário no PBC = 0"),
    (15, "Serviço Público / RPPS (via CTC)", "Servidor Efetivo", "Ente Federativo", "Regime Próprio", "N/A", "Conforme CTC", "Sim (recíproca)", "Requer certidão CTC original homologada com discriminação desde 07/1994"),
    (16, "Ajuste / Complementação EC 103", "Ajuste de Piso", "Próprio Segurado", "Diferença p/ SM (DARF 1872)", "Não", "Sim", "Sim", "Sem o recolhimento DARF: competência é descartada de tempo e RMI")
]

def parse_date_br(d_str: str) -> Optional[date]:
    """Converte 'DD/MM/AAAA' para objeto date."""
    if not d_str:
        return None
    try:
        parts = d_str.strip().split('/')
        return date(int(parts[2]), int(parts[1]), int(parts[0]))
    except Exception:
        return None

def format_date_br(d: Optional[date]) -> str:
    """Converte date para 'DD/MM/AAAA'."""
    if not d:
        return ""
    return d.strftime("%d/%m/%Y")

def dias_para_amd(dias_liquidos: int) -> str:
    """
    Critério padrão previdenciário do INSS:
    Ano = 365 dias, Mês = 30 dias.
    """
    if dias_liquidos <= 0:
        return "0A 0M 0D"
    anos = dias_liquidos // 365
    resto_ano = dias_liquidos % 365
    meses = resto_ano // 30
    dias = resto_ano % 30
    return f"{anos}A {meses}M {dias}D"

def _construir_segmentos_vinculo(dt_ini: date, dt_fim: date, especialidade_periodos: List[Dict[str, Any]]) -> List[Tuple[date, date, float]]:
    """
    Quebra [dt_ini, dt_fim] em segmentos cronológicos contíguos nos pontos de corte da
    Reforma da Previdência (13/11/2019) e dos períodos de fator de especialidade informados
    (campo opcional "especialidade" do vínculo, anotado manualmente pelo usuário — PPP/LTCAT).
    Cada segmento tem fase (pré/pós-reforma) e fator homogêneos, para que o fator seja
    aplicado diretamente sobre os dias líquidos exatos do próprio segmento (sem estimativa
    proporcional). Retorna lista de (segmento_inicio, segmento_fim, fator), em ordem cronológica.
    """
    breakpoints = {dt_ini, dt_fim + timedelta(days=1)}
    if dt_ini < DATA_REFORMA <= dt_fim:
        breakpoints.add(DATA_REFORMA)
    periodos_validos = []
    for p in especialidade_periodos:
        p_ini = parse_date_br(p.get("inicio"))
        p_fim = parse_date_br(p.get("fim"))
        fator = p.get("fator")
        if not p_ini or not p_fim or not fator:
            continue
        p_ini_c = max(p_ini, dt_ini)
        p_fim_c = min(p_fim, dt_fim)
        if p_ini_c > p_fim_c:
            continue
        periodos_validos.append((p_ini_c, p_fim_c, fator))
        breakpoints.add(p_ini_c)
        breakpoints.add(p_fim_c + timedelta(days=1))
    pontos = sorted(b for b in breakpoints if dt_ini <= b <= dt_fim + timedelta(days=1))
    segmentos = []
    for a, b in zip(pontos, pontos[1:]):
        seg_ini, seg_fim = a, b - timedelta(days=1)
        fator_seg = 1.0
        for p_ini, p_fim, fator in periodos_validos:
            if p_ini <= seg_ini and seg_fim <= p_fim:
                fator_seg = fator
                break
        segmentos.append((seg_ini, seg_fim, fator_seg))
    return segmentos

def _inicio_mes(d: date) -> date:
    return date(d.year, d.month, 1)

def _fim_mes(d: date) -> date:
    return date(d.year, d.month, monthrange(d.year, d.month)[1])

def _arredondar(x: float) -> int:
    """Arredondamento meio-para-cima, idêntico ao ROUND(x;0) da planilha para x >= 0."""
    return int(math.floor(x + 0.5))

def calcular_vinculos(vinculos: List[Dict[str, Any]], der_str: Optional[str] = None) -> Tuple[List[Dict[str, Any]], int, int, int]:
    """
    Apura o tempo de contribuição linha a linha, espelhando exatamente as fórmulas vivas da aba
    "Tempo de Contribuição" (a planilha recalcula sozinha; este cálculo só a reproduz para o
    terminal e para a análise das regras de transição).

    Cada vínculo vira uma ou mais linhas (segmentos cortados na Reforma e nos períodos de fator
    de especialidade), sempre a partir da data de início original, na ordem dos vínculos:
    - Mês cheio: linha com início após 12/11/2019 (qualquer categoria) ou categoria 05-10.
      Dias Brutos = 30 x competências; após a Reforma só contam competências com remuneração
      consolidada (soma dos vínculos, Tema 1070 STJ) >= salário mínimo.
    - Dias corridos (demais linhas pré-Reforma): Dias Brutos = Fim - Início + 1.
    - Cobertura da linha: o mês inteiro (dia 1 ao último dia) em mês cheio; Início a Fim em dias
      corridos.
    - Concomit.: em dias corridos, dias do período já cobertos por linhas anteriores; em mês cheio,
      para cada competência computada, a fração do mês já coberta por linhas anteriores x 30 (cada
      dia do mês vale 30/dias-do-mês). Assim uma competência nunca gera mais que 30 dias no total,
      inclusive no mês da Reforma e entre vínculos de categorias diferentes.
    - Dias Líquidos = arredondamento de (Dias Brutos - Concomit.) x Fator.
    """
    der = parse_date_br(der_str) if der_str else None
    vinculos_calculados = []

    total_remun_global: Dict[str, float] = {}
    for v in vinculos:
        for r in v.get("remunerações", []):
            c_k = r["competencia"]
            total_remun_global[c_k] = total_remun_global.get(c_k, 0.0) + r["remuneracao"]

    def competencia_apta(d: date) -> bool:
        c_key = f"{d.month:02d}/{d.year}"
        if c_key not in total_remun_global:
            return False
        sm_val, _ = get_salario_minimo(c_key)
        return total_remun_global[c_key] >= sm_val

    dias_cobertos = set()
    total_dias_liquidos_geral = 0
    total_dias_pre_reforma = 0
    total_dias_pos_reforma = 0

    for v in vinculos:
        seq = v["seq"]
        emp = v["empregador"]
        cnpj = v["cnpj"]
        cod_rec = v.get("cod_recolhimento", "01")
        origem = v.get("origem", "CNIS")
        dt_ini_orig = parse_date_br(v.get("data_inicio"))
        dt_fim_orig = parse_date_br(v.get("data_fim"))
        ult_remun = v.get("ult_remun", "")
        obs_list = []

        # 1. Vínculo em aberto: a última remuneração do próprio CNIS prevalece sobre a DER, que é
        # só um corte operacional e não prova que ESTE vínculo seguiu ativo até ela.
        dt_fim = dt_fim_orig
        if not dt_fim_orig:
            if ult_remun:
                try:
                    m_u, y_u = [int(x) for x in ult_remun.split('/')]
                    dt_fim = date(y_u, m_u, monthrange(y_u, m_u)[1])
                    obs_list.append(f"Vínculo em aberto no CNIS; data fim fixada na última competência ({format_date_br(dt_fim)}).")
                except ValueError:
                    dt_fim = None
            if dt_fim is None and der:
                dt_fim = der
                obs_list.append(f"Vínculo em aberto no CNIS; data fim fixada na DER ({format_date_br(der)}).")
            if dt_fim is None:
                obs_list.append("Vínculo em aberto sem data fim, sem última remuneração e sem DER.")

        if not dt_ini_orig or not dt_fim or dt_fim < dt_ini_orig:
            vinculos_calculados.append({
                "seq": seq,
                "origem": origem,
                "empregador": emp,
                "cnpj": cnpj,
                "cod_recolhimento": cod_rec,
                "inicio": format_date_br(dt_ini_orig),
                "fim": format_date_br(dt_fim),
                "mes_cheio": "Não",
                "status": "Incompleto",
                "dias_brutos": 0,
                "concomitancia": 0,
                "dias_liquidos": 0,
                "segmentos": [],
                "amd": "0A 0M 0D",
                "carencia": "Não",
                "observacoes": "; ".join(obs_list) or "Período inválido ou incompleto."
            })
            continue

        dias_brutos = (dt_fim - dt_ini_orig).days + 1

        # 2. Linhas (segmentos) a partir do início original; a concomitância é descontada por linha.
        especialidade_periodos = v.get("especialidade") or []
        segmentos_datas = _construir_segmentos_vinculo(dt_ini_orig, dt_fim, especialidade_periodos)

        dias_liquidos_vinculo = 0
        dias_pre_vinculo = 0
        dias_pos_vinculo = 0
        concomit_vinculo = 0.0
        segmentos_out = []

        for seg_ini, seg_fim, fator_seg in segmentos_datas:
            tipo_seg = "pre" if seg_fim < DATA_REFORMA else "pos"
            mes_cheio = seg_ini >= DATA_REFORMA or cod_rec in CODES_MES_CHEIO_PRE
            if mes_cheio:
                cob_ini, cob_fim = _inicio_mes(seg_ini), _fim_mes(seg_fim)
                meses = []
                d = cob_ini
                while d <= seg_fim:
                    meses.append(d)
                    d = _fim_mes(d) + timedelta(days=1)
                if seg_ini >= DATA_REFORMA:
                    computados = [m for m in meses if competencia_apta(m)]
                    descartados = len(meses) - len(computados)
                else:
                    computados, descartados = meses, 0
                bruto = 30 * len(computados)
                concomit = 0.0
                for m in computados:
                    dim = monthrange(m.year, m.month)[1]
                    cobertos = sum(1 for k in range(dim) if (m + timedelta(days=k)) in dias_cobertos)
                    concomit += cobertos * 30 / dim
                if tipo_seg == "pre":
                    obs_seg = f"Mês cheio pré-reforma ({len(computados)} competências a 30d) para categoria {cod_rec}."
                else:
                    obs_seg = f"{len(computados)} competência(s) a 30d pós-reforma."
                if descartados:
                    obs_seg += f" {descartados} competência(s) descartada(s) por remuneração total < Salário Mínimo."
            else:
                cob_ini, cob_fim = seg_ini, seg_fim
                bruto = (seg_fim - seg_ini).days + 1
                concomit = float(sum(1 for k in range(bruto) if (seg_ini + timedelta(days=k)) in dias_cobertos))
                obs_seg = "Dias corridos (categoria não sujeita a mês cheio pré-reforma)."

            if bruto > 0 and concomit >= bruto:
                obs_seg += " Período integralmente abrangido por vínculo(s) anterior(es)."
            elif concomit > 0:
                obs_seg += " Concomitância com vínculo(s) anterior(es) descontada."
            if fator_seg != 1.0:
                obs_seg += f" Fator de especialidade {fator_seg} aplicado."

            liquido = _arredondar((bruto - concomit) * fator_seg)
            for k in range((cob_fim - cob_ini).days + 1):
                dias_cobertos.add(cob_ini + timedelta(days=k))

            dias_liquidos_vinculo += liquido
            concomit_vinculo += concomit
            if tipo_seg == "pre":
                dias_pre_vinculo += liquido
            else:
                dias_pos_vinculo += liquido

            segmentos_out.append({
                "inicio": format_date_br(seg_ini),
                "fim": format_date_br(seg_fim),
                "tipo": tipo_seg,
                "mes_cheio": "Sim" if mes_cheio else "Não",
                "fator": fator_seg,
                "dias_brutos_segmento": bruto,
                "concomitancia": concomit,
                "dias_liquidos": liquido,
                "observacoes": obs_seg,
            })

        if dias_pre_vinculo > 0 and dias_pos_vinculo > 0:
            mes_cheio_status = "Parcial"
        elif dias_pos_vinculo > 0:
            mes_cheio_status = "Sim"
        else:
            mes_cheio_status = "Sim" if cod_rec in CODES_MES_CHEIO_PRE else "Não"

        total_dias_liquidos_geral += dias_liquidos_vinculo
        total_dias_pre_reforma += dias_pre_vinculo
        total_dias_pos_reforma += dias_pos_vinculo

        if any(s["fator"] != 1.0 for s in segmentos_out):
            obs_list.append("Fator de especialidade aplicado em ao menos um segmento — ver detalhamento por segmento na aba Tempo de Contribuição.")

        vinculos_calculados.append({
            "seq": seq,
            "origem": origem,
            "empregador": emp,
            "cnpj": cnpj,
            "cod_recolhimento": cod_rec,
            "inicio": format_date_br(dt_ini_orig),
            "fim": format_date_br(dt_fim),
            "mes_cheio": mes_cheio_status,
            "status": "Encerrado" if dt_fim_orig else "Ativo",
            "dias_brutos": dias_brutos,
            "concomitancia": _arredondar(concomit_vinculo),
            "dias_liquidos": dias_liquidos_vinculo,
            "segmentos": segmentos_out,
            "amd": dias_para_amd(dias_liquidos_vinculo),
            "carencia": "Sim",
            "observacoes": "; ".join(obs_list)
        })

    return vinculos_calculados, total_dias_liquidos_geral, total_dias_pre_reforma, total_dias_pos_reforma

def _pontos_minimos_ec103(ano_der: int, sexo: str) -> int:
    """Tabela progressiva de pontos (art. 15, EC 103/2019). Mulher: 86 (2019) -> 100 (2033+). Homem: 96 (2019) -> 105 (2028+)."""
    if sexo == "F":
        return min(100, 86 + max(0, ano_der - 2019))
    return min(105, 96 + max(0, ano_der - 2019))

def _idade_minima_progressiva_ec103(ano_der: int, sexo: str) -> float:
    """Idade mínima progressiva da regra de transição por idade (+6 meses/ano). Mulher: 56 (2019) -> 62. Homem: 61 (2019) -> 65."""
    if sexo == "F":
        return min(62.0, 56.0 + max(0, ano_der - 2019) * 0.5)
    return min(65.0, 61.0 + max(0, ano_der - 2019) * 0.5)

def calcular_fator_previdenciario(tempo_contrib_anos: float, idade_anos: float, expectativa_sobrevida_anos: float, aliquota: float = 0.31) -> float:
    """Fator previdenciário (Lei 9.876/1999, art. 7º), usado no Pedágio de 50% da EC 103/2019."""
    tc_a = tempo_contrib_anos * aliquota
    return (tc_a / expectativa_sobrevida_anos) * (1 + ((idade_anos + tc_a) / 100))

def _add_months(d: date, months: int) -> date:
    """Soma meses corridos a uma data, ajustando o dia ao último dia do mês de destino se necessário."""
    m = d.month - 1 + months
    y = d.year + m // 12
    m = m % 12 + 1
    day = min(d.day, monthrange(y, m)[1])
    return date(y, m, day)

def _projetar_data_por_tempo(der: date, tempo_atual_anos: float, tempo_necessario_anos: float) -> Tuple[date, bool]:
    """
    Projeta a data em que o tempo de contribuição necessário será atingido, assumindo
    contribuição ordinária continuada a partir da DER (mês cheio pós-EC103, 30 dias/mês
    por competência) — premissa confirmada com o usuário; ajustável manualmente depois.
    Retorna (data_projetada, ja_cumprido_na_der).
    """
    if tempo_atual_anos >= tempo_necessario_anos:
        return der, True
    dias_faltantes = (tempo_necessario_anos - tempo_atual_anos) * 365.0
    meses_faltantes = math.ceil(dias_faltantes / 30.0)
    return _add_months(der, meses_faltantes), False

def _data_idade_minima(data_nascimento: date, idade_min_anos: float) -> date:
    """Data de calendário em que o segurado atinge a idade mínima informada (em anos, com frações de 0,5 = 6 meses)."""
    total_meses = round(idade_min_anos * 12)
    return _add_months(data_nascimento, total_meses)

def _data_cumprimento_regra(der: date, data_nascimento: date, tempo_atual_anos: float, tempo_necessario_anos: float,
                              idade_min_anos: Optional[float] = None) -> date:
    """Data de cumprimento da regra = a mais tardia entre a projeção de tempo e a data de idade mínima (se houver)."""
    data_tempo, _ = _projetar_data_por_tempo(der, tempo_atual_anos, tempo_necessario_anos)
    if idade_min_anos is not None:
        data_idade = _data_idade_minima(data_nascimento, idade_min_anos)
        return max(data_tempo, data_idade)
    return data_tempo

def analisar_transicoes_ec103(sexo: str, data_nascimento: date, der: date, total_dias_geral: int,
                                total_dias_pre_reforma: int, expectativa_sobrevida: Optional[float] = None,
                                media_pbc: Optional[float] = None) -> List[Dict[str, Any]]:
    """
    Avalia elegibilidade e coeficiente estimado nas 4 regras de transição da EC 103/2019
    (Regra de Pontos, Pedágio 50%, Pedágio 100%, Idade Mínima Progressiva) e também na
    Regra Permanente/Ordinária pós-EC103 (que não é regra de transição, mas concorre com
    elas — aplicável se os requisitos definitivos forem cumpridos independentemente).

    ATENÇÃO — uso jurídico: os números de artigo citados seguem a sistematização doutrinária
    usual da EC 103/2019, mas devem ser conferidos pelo profissional contra o texto oficial
    antes de constar em peça formal. Tabelas de pontos/idade e percentuais de coeficiente são
    parâmetros normativos estáveis e goza de alta confiabilidade.
    """
    idade_der_anos = (der - data_nascimento).days / 365.25
    tempo_total_anos = total_dias_geral / 365.0
    tempo_ate_reforma_anos = total_dias_pre_reforma / 365.0
    ano_der = der.year

    resultados = []

    # 1. Regra de Pontos
    tempo_min = 30.0 if sexo == "F" else 35.0
    pontos_min = _pontos_minimos_ec103(ano_der, sexo)
    pontos_apurados = idade_der_anos + tempo_total_anos
    elegivel = tempo_total_anos >= tempo_min and pontos_apurados >= pontos_min
    if elegivel:
        data_cumprimento_pontos = der
    else:
        pontos_faltantes = max(0.0, pontos_min - pontos_apurados)
        tempo_faltante_min = max(0.0, tempo_min - tempo_total_anos)
        # Idade e tempo avançam juntos 1:1 com o tempo real decorrido, então os pontos
        # sobem 2 por ano (1 de idade + 1 de tempo) enquanto a contribuição continuar.
        t_necessario = max(pontos_faltantes / 2.0, tempo_faltante_min)
        meses_falt = math.ceil(t_necessario * 12)
        data_cumprimento_pontos = _add_months(der, meses_falt)
    rmi_pontos = media_pbc if media_pbc is not None else None
    resultados.append({
        "regra": "Regra de Pontos",
        "requisitos": f"Tempo mín. {tempo_min:.0f} anos + {pontos_min} pontos (idade + tempo) na DER + carência 180.",
        "situacao": "Elegível" if elegivel else "Não elegível",
        "detalhe": f"Tempo apurado: {tempo_total_anos:.2f}a | Pontos apurados: {pontos_apurados:.2f} (mín. {pontos_min})",
        "coeficiente": "100% da média aritmética simples (integral).",
        "implementado": True,
        "observacao": "Carência (180 contribuições) deve ser conferida no KPI 'Total de Carência Reconhecida'." + ("" if elegivel else " Projeção de data usa a tabela de pontos vigente no ano da DER; se a data projetada cruzar virada de ano, revisar manualmente."),
        "data_cumprimento": data_cumprimento_pontos,
        "ja_cumprido": elegivel,
        "rmi_estimada": rmi_pontos,
    })

    # 2. Pedágio de 50%
    faltante_reforma = max(0.0, tempo_min - tempo_ate_reforma_anos)
    aplicavel_pedagio50 = 0.0 < faltante_reforma <= 2.0
    tempo_necessario_50 = tempo_ate_reforma_anos + faltante_reforma * 1.5
    if not aplicavel_pedagio50:
        situacao_50 = "Não aplicável (em 13/11/2019 já tinha o tempo mínimo ou faltavam mais de 2 anos)"
    elif tempo_total_anos >= tempo_necessario_50:
        situacao_50 = "Elegível"
    else:
        situacao_50 = "Regra aplicável, tempo ainda não atingido"
    if not aplicavel_pedagio50:
        coef_50 = "Não aplicável — a regra não incide sobre este segurado (ver Situação)."
        implementado_50 = True
        rmi_50 = None
    elif expectativa_sobrevida:
        fp = calcular_fator_previdenciario(tempo_total_anos, idade_der_anos, expectativa_sobrevida)
        coef_50 = f"Fator previdenciário calculado: {fp:.4f} (Es={expectativa_sobrevida}a). RMI = maior valor entre (média x fator) e 100% da média."
        implementado_50 = True
        rmi_50 = max(media_pbc * fp, media_pbc) if media_pbc is not None else None
    else:
        coef_50 = "RMI pendente — depende do fator previdenciário (expectativa de sobrevida IBGE do ano/idade da DER). Informe via --expectativa-sobrevida <anos>."
        implementado_50 = False
        rmi_50 = None
    if aplicavel_pedagio50:
        data_cumprimento_50, ja_50 = _projetar_data_por_tempo(der, tempo_total_anos, tempo_necessario_50)
    else:
        data_cumprimento_50, ja_50 = None, False
    resultados.append({
        "regra": "Pedágio de 50%",
        "requisitos": f"Só se aplica a quem, em 13/11/2019, tinha até 2 anos faltantes p/ completar {tempo_min:.0f}a. Tempo exigido = tempo cumprido + 1,5x tempo faltante nessa data. Carência 180.",
        "situacao": situacao_50,
        "detalhe": f"Tempo até 12/11/2019: {tempo_ate_reforma_anos:.2f}a | Faltante nessa data: {faltante_reforma:.2f}a | Tempo exigido: {tempo_necessario_50:.2f}a | Tempo apurado: {tempo_total_anos:.2f}a",
        "coeficiente": coef_50,
        "implementado": implementado_50,
        "observacao": "Enquadramento (faltante <= 2 anos em 13/11/2019) exige revisão humana antes de uso formal.",
        "data_cumprimento": data_cumprimento_50,
        "ja_cumprido": ja_50,
        "rmi_estimada": rmi_50,
    })

    # 3. Pedágio de 100%
    idade_min_100 = 57.0 if sexo == "F" else 60.0
    tempo_necessario_100 = tempo_ate_reforma_anos + 2 * faltante_reforma
    elegivel_100 = idade_der_anos >= idade_min_100 and tempo_total_anos >= tempo_necessario_100
    data_cumprimento_100 = _data_cumprimento_regra(der, data_nascimento, tempo_total_anos, tempo_necessario_100, idade_min_100)
    rmi_100 = media_pbc if media_pbc is not None else None
    resultados.append({
        "regra": "Pedágio de 100%",
        "requisitos": f"Idade mín. {idade_min_100:.0f}a + pedágio de 100% sobre o tempo faltante em 13/11/2019 p/ completar {tempo_min:.0f}a + carência 180.",
        "situacao": "Elegível" if elegivel_100 else "Não elegível",
        "detalhe": f"Idade na DER: {idade_der_anos:.2f}a (mín. {idade_min_100:.0f}a) | Tempo exigido: {tempo_necessario_100:.2f}a | Tempo apurado: {tempo_total_anos:.2f}a",
        "coeficiente": "100% da média aritmética simples (integral), sem fator previdenciário.",
        "implementado": True,
        "observacao": "",
        "data_cumprimento": data_cumprimento_100,
        "ja_cumprido": elegivel_100,
        "rmi_estimada": rmi_100,
    })

    # 4. Idade Mínima Progressiva
    idade_min_prog = _idade_minima_progressiva_ec103(ano_der, sexo)
    elegivel_prog = idade_der_anos >= idade_min_prog and tempo_total_anos >= tempo_min
    coef_prog = 0.6 + max(0.0, (tempo_total_anos - 20.0) * 0.02)
    data_cumprimento_prog = _data_cumprimento_regra(der, data_nascimento, tempo_total_anos, tempo_min, idade_min_prog)
    rmi_prog = media_pbc * coef_prog if media_pbc is not None else None
    resultados.append({
        "regra": "Idade Mínima Progressiva",
        "requisitos": f"Idade mín. {idade_min_prog:.1f}a (progressiva conforme o ano da DER) + tempo mín. {tempo_min:.0f}a + carência 180.",
        "situacao": "Elegível" if elegivel_prog else "Não elegível",
        "detalhe": f"Idade na DER: {idade_der_anos:.2f}a (mín. {idade_min_prog:.1f}a) | Tempo apurado: {tempo_total_anos:.2f}a (mín. {tempo_min:.0f}a)",
        "coeficiente": f"{coef_prog*100:.1f}% da média (60% + 2%/ano de tempo acima de 20a).",
        "implementado": True,
        "observacao": "" if elegivel_prog else "Projeção assume que o coeficiente (60% + 2%/ano) recalculado na data futura de cumprimento pode ser maior que o indicado aqui, que usa o tempo apurado na DER.",
        "data_cumprimento": data_cumprimento_prog,
        "ja_cumprido": elegivel_prog,
        "rmi_estimada": rmi_prog,
    })

    # 5. Regra Permanente (Ordinária, pós-EC103 — não é regra de transição)
    tempo_min_ord = 15.0 if sexo == "F" else 20.0
    idade_min_ord = 62.0 if sexo == "F" else 65.0
    elegivel_ord = idade_der_anos >= idade_min_ord and tempo_total_anos >= tempo_min_ord
    coef_ord = 0.6 + max(0.0, (tempo_total_anos - tempo_min_ord) * 0.02)
    data_cumprimento_ord = _data_cumprimento_regra(der, data_nascimento, tempo_total_anos, tempo_min_ord, idade_min_ord)
    rmi_ord = media_pbc * coef_ord if media_pbc is not None else None
    resultados.append({
        "regra": "Regra Permanente (Ordinária, pós-EC103)",
        "requisitos": f"Idade mín. {idade_min_ord:.0f}a + tempo mín. {tempo_min_ord:.0f}a + carência 180 (Art. 19/19-A do Dec. 3.048/99, redação EC 103/2019 — não é regra de transição).",
        "situacao": "Elegível" if elegivel_ord else "Não elegível",
        "detalhe": f"Idade na DER: {idade_der_anos:.2f}a (mín. {idade_min_ord:.0f}a) | Tempo apurado: {tempo_total_anos:.2f}a (mín. {tempo_min_ord:.0f}a)",
        "coeficiente": f"{coef_ord*100:.1f}% da média (60% + 2%/ano de tempo acima de {tempo_min_ord:.0f}a).",
        "implementado": True,
        "observacao": "Regra definitiva do RGPS pós-reforma — aplica-se independentemente de regra de transição, se os requisitos forem cumpridos.",
        "data_cumprimento": data_cumprimento_ord,
        "ja_cumprido": elegivel_ord,
        "rmi_estimada": rmi_ord,
    })

    return resultados

def calcular_valores(vinculos: List[Dict[str, Any]], tabela_mps: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Processa todos os salários de contribuição das competências dos vínculos:
    1. Agrupa por competência (MM/AAAA) somando fontes concomitantes (Tema 1070 STJ).
    2. Aplica limitação ao Teto do RGPS nas competências a partir de 07/1994.
    3. Multiplica pelo índice de atualização monetária oficial do MPS.
    """
    fatores = tabela_mps.get("fatores", {})

    comp_map: Dict[str, List[Dict[str, Any]]] = {}
    for v in vinculos:
        seq = v["seq"]
        emp = v["empregador"]
        cod_rec = v.get("cod_recolhimento", "01")
        for r in v.get("remunerações", []):
            comp = r["competencia"]
            if comp not in comp_map:
                comp_map[comp] = []
            comp_map[comp].append({
                "seq": seq,
                "empregador": emp,
                "cod_rec": cod_rec,
                "remuneracao": r["remuneracao"],
                "indicadores": r.get("indicadores", "")
            })

    def comp_sort_key(c: str) -> Tuple[int, int]:
        m, y = [int(x) for x in c.split('/')]
        return y, m

    competencias_ordenadas = sorted(comp_map.keys(), key=comp_sort_key)
    linhas_valores = []

    for comp in competencias_ordenadas:
        itens = comp_map[comp]
        seqs_str = ", ".join(sorted(set(str(it["seq"]) for it in itens)))
        emps_str = " + ".join(dict.fromkeys(it["empregador"] for it in itens))
        cods_str = ", ".join(sorted(set(str(it["cod_rec"]) for it in itens)))
        ind_set: set = set()
        for it in itens:
            val = it["indicadores"]
            if isinstance(val, list):
                ind_set.update(val)
            else:
                ind_set.add(val)
        ind_str = ", ".join(sorted(filter(None, ind_set)))

        val_total_orig = sum(it["remuneracao"] for it in itens)
        sm_val, moeda = get_salario_minimo(comp)
        teto_val, _ = get_teto_rgps(comp)

        m_c, y_c = [int(x) for x in comp.split('/')]
        dt_comp = date(y_c, m_c, 1)

        rel_sm_str = f"{val_total_orig / sm_val:.2f}x S.M." if sm_val > 0 else "-"

        val_base_rmi = val_total_orig
        # S.M./teto não confirmados em fonte externa aparecem na própria linha, nunca em silêncio
        obs_comp = avisos_competencia(comp)
        if len(itens) > 1:
            obs_comp.append(f"Concomitância: {len(itens)} vínculos somados (Tema 1070 STJ)")

        if dt_comp >= date(1994, 7, 1) and teto_val > 0:
            if val_total_orig > teto_val:
                val_base_rmi = teto_val
                excesso = val_total_orig - teto_val
                obs_comp.append(f"Limitado ao Teto RGPS (Excesso: R$ {format_currency_br(excesso)})")

        if dt_comp >= date(1994, 7, 1):
            fator = fatores.get(comp)
            if fator is not None:
                fator_str = f"{fator:.6f}"
                val_atualizado = val_base_rmi * fator
                val_atualizado_str = format_currency_br(val_atualizado)
            else:
                fator_str = "1,000000"
                val_atualizado = val_base_rmi
                val_atualizado_str = format_currency_br(val_base_rmi)
        else:
            fator_str = "N/A"
            val_atualizado = 0.0
            val_atualizado_str = "N/A"

        if dt_comp >= date(2019, 11, 1):
            conta_contrib = "Sim" if val_total_orig >= sm_val else "Não (abaixo do S.M.)"
        else:
            conta_contrib = "Sim"

        # conta_rmi depende só da data (>= 07/1994) — a comparação com o SM (conta_contrib)
        # é teste de aptidão para tempo (mês cheio, só cabível >= 11/2019) e NÃO deve excluir
        # a competência do PBC/RMI; abaixo do SM, o valor real ainda compõe a média (art. 29,
        # Lei 8.213/91). Bug corrigido: antes, conta_rmi herdava a reprovação de conta_contrib
        # e removia a competência inteira da soma/contagem do PBC.
        conta_rmi = "Sim" if dt_comp >= date(1994, 7, 1) else "Não"

        if conta_contrib.startswith("Não") and len(itens) == 1:
            obs_comp.append("Abaixo do S.M. sem concomitância no mesmo mês para complementação (Tema 1070 STJ)")

        linhas_valores.append({
            "seq": seqs_str,
            "competencia": comp,
            "data_comp": dt_comp,
            "empregador": emps_str,
            "cod_recolhimento": cods_str,
            "remuneracao_orig_str": f"{moeda} {format_currency_br(val_total_orig)}",
            "remuneracao_float": val_total_orig,
            "salario_minimo_str": f"{moeda} {format_currency_br(sm_val)}",
            "salario_minimo_float": sm_val,
            "teto_rgps_str": f"{moeda} {format_currency_br(teto_val)}" if teto_val > 0 else "-",
            "teto_rgps_float": teto_val,
            "salario_base_pbc_float": val_base_rmi,
            "relacao_sm": rel_sm_str,
            "fator_correcao": fator_str,
            "fator_correcao_float": float(fator_str.replace(",", ".")) if fator_str != "N/A" else None,
            "valor_atualizado": val_atualizado_str,
            "valor_atualizado_float": val_atualizado,
            "conta_contribuicao": conta_contrib,
            "conta_rmi": conta_rmi,
            "indicadores": ind_str,
            "observacoes": "; ".join(obs_comp) or ("Apto" if conta_rmi == "Sim" else "Anterior ao PBC")
        })

    return linhas_valores

def gerar_planilha_excel(*args: Any, **kwargs: Any) -> None:
    """Compatibilidade defensiva: esta variante nunca produz planilhas."""
    raise RuntimeError("Geração de planilha desabilitada nesta skill; use analisar_cnis.py.")
