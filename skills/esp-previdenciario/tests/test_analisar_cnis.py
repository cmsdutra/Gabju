from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"
FIXTURE = Path(__file__).parent / "fixtures" / "cnis_sintetico.json"
sys.path.insert(0, str(SCRIPTS))

from _cnis_engine import analisar_transicoes_ec103, calcular_valores, calcular_vinculos  # noqa: E402
from analisar_cnis import analisar, render_markdown  # noqa: E402


class MotorPrevidenciarioTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_vinculos_cobrem_sobreposicao_reforma_abertos_e_especialidade(self) -> None:
        vinculos, total, pre, pos = calcular_vinculos(self.data["vinculos"], "31/03/2020")
        self.assertGreater(total, 0)
        self.assertGreater(pre, 0)
        self.assertGreater(pos, 0)
        self.assertGreater(vinculos[1]["concomitancia"], 0)
        self.assertTrue(any(s["fator"] == 1.4 for s in vinculos[0]["segmentos"]))
        self.assertEqual(vinculos[2]["fim"], "29/02/2020")
        self.assertEqual(vinculos[3]["fim"], "31/03/2020")

    def test_mes_cheio_concomitancia_piso_e_teto(self) -> None:
        vinculos, *_ = calcular_vinculos(self.data["vinculos"], "31/03/2020")
        novembro = next(s for s in vinculos[0]["segmentos"] if s["inicio"] == "13/11/2019")
        self.assertGreater(novembro["dias_brutos_segmento"], 0)
        tabela = {"fatores": {"11/2019": 1.1, "12/2019": 1.1, "01/2020": 1.1, "02/2020": 1.1}}
        valores = calcular_valores(self.data["vinculos"], tabela)
        nov = next(v for v in valores if v["competencia"] == "11/2019")
        dez = next(v for v in valores if v["competencia"] == "12/2019")
        self.assertEqual(nov["remuneracao_float"], 1100.0)
        self.assertIn("Concomitância", nov["observacoes"])
        self.assertLess(dez["salario_base_pbc_float"], dez["remuneracao_float"])

    def test_todas_as_regras_de_transicao_sao_emitidas(self) -> None:
        regras = analisar_transicoes_ec103(
            "F", date(1960, 1, 1), date(2026, 1, 1), 35 * 365, 29 * 365, 22.0, 3000.0
        )
        self.assertEqual(len(regras), 5)
        nomes = {r["regra"] for r in regras}
        self.assertIn("Regra de Pontos", nomes)
        self.assertIn("Pedágio de 50%", nomes)
        self.assertIn("Pedágio de 100%", nomes)
        self.assertIn("Idade Mínima Progressiva", nomes)

    def test_sem_rmi_e_relatorio_markdown(self) -> None:
        args = argparse.Namespace(
            der="31/03/2020",
            competencia_mps=None,
            sexo="F",
            expectativa_sobrevida=22.0,
            sem_rmi=True,
        )
        resultado = analisar(self.data, args)
        self.assertIsNone(resultado["pbc"]["media"])
        self.assertEqual(len(resultado["regras_transicao"]), 5)
        markdown = render_markdown(resultado)
        self.assertIn("# Relatório técnico previdenciário", markdown)
        self.assertIn(str(resultado["tempo_contribuicao"]["dias_liquidos"]), markdown)

    def test_cli_serializa_datas_e_nao_cria_planilha(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / "resultado.json"
            subprocess.run(
                [sys.executable, str(SCRIPTS / "analisar_cnis.py"), str(FIXTURE), "--der", "31/03/2020", "--sem-rmi", "--out", str(out)],
                check=True,
            )
            resultado = json.loads(out.read_text(encoding="utf-8"))
            self.assertRegex(resultado["competencias_consolidadas"][0]["data_comp"], r"^\d{4}-\d{2}-\d{2}$")
            self.assertEqual(list(Path(temp).glob("*.xlsx")), [])


if __name__ == "__main__":
    unittest.main()
