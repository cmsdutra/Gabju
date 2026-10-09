---
name: esp-previdenciario
description: Analisa CNIS, tempo especial, PPP/LTCAT e requisitos de aposentadoria especial, inclusive os efeitos da ADI 6309; confere tempo, concomitâncias, salários e RMI. Use em demandas previdenciárias que exijam análise jurídica da especialidade ou apuração técnica.
---

# Especialista Previdenciário

## Leitura dos anexos

Quando precisar consultar anexos, tente primeiro a leitura direta. Se houver dificuldade concreta que impeça acessar o conteúdo necessário, acione $indexar-pdf somente para os PDFs afetados, informando a dificuldade observada. Tamanho e quantidade de páginas isolados não justificam indexação. Reutilize os textos recuperados e os diagnósticos ao retomar esta skill, preservando seu escopo e checkpoints.

A recuperação da leitura não substitui a extração canônica de CNIS exigida abaixo para o cálculo.

## Seleção do fluxo

- Para CNIS, totais de contribuição, RMI e transições calculáveis, siga o fluxo de cálculo abaixo.
- Para reconhecimento de tempo especial, exame de PPP/LTCAT, conversão ou aposentadoria especial, leia [references/tempo-especial.md](references/tempo-especial.md) e siga o fluxo jurídico dessa referência. Esse exame pode ser feito sem CNIS; a extração canônica é obrigatória quando houver cálculo baseado nele.
- Quando o pedido reunir os dois objetos, examine primeiro o enquadramento jurídico dos períodos e a admissibilidade da conversão; depois forneça ao calculador apenas os fatores justificados. Períodos controvertidos podem compor cenários separados, identificados como hipóteses.
- Se o usuário mencionar ADI 6039 em matéria de aposentadoria especial, confira a identificação e explique a distinção em relação à ADI 6309. Não atribua efeitos previdenciários à ADI 6039 nem substitua silenciosamente o precedente indicado.

## Fluxo obrigatório de cálculo

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
- O CNIS isolado não comprova atividade especial. Examine os documentos e o regime probatório vigente no período; orientação expressa pode fixar uma premissa de cálculo, mas não substitui prova nem autoriza apresentar hipótese como reconhecimento jurídico.
- O motor calcula fatores informados, mas não decide a especialidade, não valida o limite temporal da conversão e não automatiza os requisitos ou a RMI da aposentadoria especial. A análise jurídica cabe ao fluxo próprio; não use o resultado de aposentadoria comum como resposta automática sobre aposentadoria especial.
- Exponha todas as regras de transição calculáveis, sem eleger automaticamente a mais vantajosa.
- Preserve como pendência qualquer DER, sexo, expectativa de sobrevida, remuneração ou índice ausente/ilegível.
- Destaque indicadores, divergências e fatores desatualizados que dependam de conferência humana.

## Recursos

- `references/tempo-especial.md`: leia para reconhecimento de especialidade, PPP/LTCAT, EPI, conversão, aposentadoria especial ou aplicação da ADI 6309.
- `scripts/extrair_cnis.py`: extração determinística e normalização; use sempre antes do cálculo, salvo JSON canônico já conferido.
- `scripts/analisar_cnis.py`: cálculo e serialização determinísticos; use sempre para totais, RMI e transições.
- `references/regras-calculo.md`: leia ao explicar metodologia, resolver divergência ou avaliar regra de transição.
- `references/mps-indices-spec.md`: leia quando houver RMI, dúvida sobre fatores ou necessidade de atualizar a competência MPS.
- `references/parametros-rgps-spec.md`: leia quando salário mínimo, teto ou avisos de parâmetros afetarem o resultado.
- `assets/relatorio-tecnico.md`: estrutura do relatório solicitado pelo usuário.
