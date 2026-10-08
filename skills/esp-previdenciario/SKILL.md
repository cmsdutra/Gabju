---
name: esp-previdenciario
description: Analisa CNIS e confere cálculos previdenciários de tempo, concomitâncias, salários e RMI. Use em demandas previdenciárias que exijam apuração técnica ou relatório sob demanda.
---

# Especialista Previdenciário

## Leitura dos anexos

Quando precisar consultar anexos, tente primeiro a leitura direta. Se houver dificuldade concreta que impeça acessar o conteúdo necessário, acione $indexar-pdf somente para os PDFs afetados, informando a dificuldade observada. Tamanho e quantidade de páginas isolados não justificam indexação. Reutilize os textos recuperados e os diagnósticos ao retomar esta skill, preservando seu escopo e checkpoints.

A recuperação da leitura não substitui a extração canônica de CNIS exigida abaixo para o cálculo.

## Fluxo obrigatório

1. Confira legibilidade, completude e tipo dos anexos.
2. Execute `scripts/extrair_cnis.py` para converter PDF, TXT ou JSON em JSON canônico.
3. Compare `avisos_extracao` e amostras dos vínculos/remunerações com o documento original; corrija o JSON somente com base verificável.
4. Obtenha DER, sexo e expectativa de sobrevida quando necessários. Trate parâmetros ausentes como pendências, sem inferência pelo nome.
5. Execute `scripts/analisar_cnis.py <json> [--der DD/MM/AAAA] [--competencia-mps MM/AAAA] [--sexo M|F] [--expectativa-sobrevida N]`. Use `--sem-rmi` quando a demanda se limitar ao tempo.
6. Confira totais, sobreposições, indicadores e competências contra o extrato.
7. Apresente no chat uma síntese técnica, distinguindo resultado aritmético de conclusão jurídica.
8. Somente sob pedido expresso de relatório, repita com `--relatorio --out <arquivo.md>` e use a estrutura de `assets/relatorio-tecnico.md`.

## Limites

- Produza saída estruturada em JSON ou relatório Markdown. A skill não oferece formatos tabulares, PDF ou Word.
- Trate atividade especial como dado informado e documentado por PPP/LTCAT ou orientação expressa; o CNIS isolado não a comprova.
- Exponha todas as regras de transição calculáveis, sem eleger automaticamente a mais vantajosa.
- Preserve como pendência qualquer DER, sexo, expectativa de sobrevida, remuneração ou índice ausente/ilegível.
- Destaque indicadores, divergências e fatores desatualizados que dependam de conferência humana.

## Recursos

- `scripts/extrair_cnis.py`: extração determinística e normalização; use sempre antes do cálculo, salvo JSON canônico já conferido.
- `scripts/analisar_cnis.py`: cálculo e serialização determinísticos; use sempre para totais, RMI e transições.
- `references/regras-calculo.md`: leia ao explicar metodologia, resolver divergência ou avaliar regra de transição.
- `references/mps-indices-spec.md`: leia quando houver RMI, dúvida sobre fatores ou necessidade de atualizar a competência MPS.
- `references/parametros-rgps-spec.md`: leia quando salário mínimo, teto ou avisos de parâmetros afetarem o resultado.
- `assets/relatorio-tecnico.md`: estrutura do relatório solicitado pelo usuário.
