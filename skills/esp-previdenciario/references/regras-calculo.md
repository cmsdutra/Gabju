# Regras de Cálculo Previdenciário — CNIS Calculator

Este documento especifica o regramento técnico e normativo adotado pela skill para contagem de tempo de contribuição e apuração dos salários de contribuição para cálculo de benefícios do RGPS (INSS).

---

## 1. Tempo de Contribuição e Dias Líquidos

### 1.1. Períodos Anteriores à Reforma da Previdência (até 12/11/2019)
- **Regra**: Contagem dia a dia (dias corridos de calendário).
- **Fórmula**: `Dias = (Data Fim - Data Início) + 1`.
- **Dispositivos**: Lei 8.213/1991 e Decreto 3.048/1999 (redação anterior ao Decreto 10.410/2020).
- **Exceção — categorias 05 a 10** (contribuinte individual, MEI, facultativo): contagem por competência, 30 dias cada, do mês de início ao mês de fim (um vínculo de 15/04 a 10/05 são 2 competências, 60 dias), sem teste de salário mínimo.

### 1.2. Períodos Posteriores à Reforma da Previdência (a partir de 13/11/2019)
- **Regra do Mês Cheio**: A competência com salário de contribuição igual ou superior ao limite mínimo (Salário Mínimo nacional) é computada integralmente como tempo de contribuição, independentemente do número de dias trabalhados no mês.
- **Duração**: Cada mês integralmente computado equivale a **30 dias líquidos** (mês padrão previdenciário).
- **Condição de Piso**: Competências com remuneração inferior ao piso de Salário Mínimo não são computadas para tempo de contribuição ou carência, salvo se houver complementação, utilização de excedente ou agrupamento.
- **Dispositivos**: Art. 195, § 14 da Constituição Federal de 1988 (incluído pela EC 103/2019) c/c Art. 19-B e Art. 19-C do Decreto 3.048/1999 (com redação dada pelo Decreto 10.410/2020).

### 1.3. Vínculos Híbridos (Início antes e Fim após 13/11/2019)
- **Fase 1 (Início até 12/11/2019)**: Apuração em dias corridos de calendário.
- **Fase 2 (13/11/2019 até Data Fim)**: Apuração por meses cheios (30 dias por competência elegível com remuneração >= Salário Mínimo).
- **Classificação**: Campo `Mês Cheio` registrado como `Parcial` (com detalhamento das parcelas nas Observações).
- **Mês da Reforma (11/2019)**: a competência aparece nas duas fases; a fase 2 desconta os dias da fase 1 (ex.: 12 dias corridos até 12/11 + 18 = 30), para que a competência não passe de 30 dias.

### 1.4. Vínculo sem Data Fim
- Prevalece o último dia da competência da `Últ. Remun.` do próprio CNIS.
- A DER (`--der`) só fecha o vínculo que não tem Data Fim nem `Últ. Remun.` — ela é corte operacional, não prova de que o vínculo seguiu ativo até ela. Sem essa ordem, vínculos antigos sem baixa no CNIS seriam esticados até a DER (tempo inexistente).

---

## 2. Tratamento de Concomitância e Sobreposições

Implementado deterministicamente em `calcular_vinculos`; a saída detalha cada segmento e o desconto aplicado.

1. **Linhas**: cada vínculo vira uma ou mais linhas (cortes na Reforma e nos períodos de fator de especialidade), sempre a partir da data de início original, na ordem dos vínculos. A linha de cima tem prioridade.
2. **Cobertura da linha** (colunas ocultas P/Q): em mês cheio, o mês inteiro (dia 1 ao último dia) de cada competência; em dias corridos, de Data Início a Data Fim.
3. **Concomit. em dias corridos**: número de dias do período já cobertos por linhas anteriores.
4. **Concomit. em mês cheio**: para cada competência computada da linha, a parcela do mês já coberta por linhas anteriores, a 30 ÷ (dias do mês) por dia coberto. Competência inteiramente coberta desconta 30; parcialmente coberta, a fração (ex.: empregado que sai em 12/11/2019 e segue em mês cheio: 12 + 18). Assim uma competência nunca gera mais que 30 dias no total, mesmo entre vínculos concomitantes ou de categorias diferentes.
5. **Dias Líquidos** = arredondamento de (Dias Brutos − Concomit.) × Fator. Linha integralmente coberta fica com 0, com registro nas `Observações`.
6. **Tema 1070 STJ**: a soma das remunerações concomitantes vale para o teste de salário mínimo da competência e para a RMI; não multiplica o tempo de contribuição.

---

## 3. Conversão de Dias Líquidos para A-M-D (Anos-Meses-Dias)

- **Critério Oficial do INSS**:
  - Ano = 365 dias
  - Mês = 30 dias
  - `Anos = dias // 365`
  - `Meses = (dias % 365) // 30`
  - `Dias = (dias % 365) % 30`

---

## 4. Salários de Contribuição, Atualização Monetária e RMI

### 4.1. Período Básico de Cálculo (PBC)
- Sob as regras do art. 29 da Lei 8.213/1991 (e regras de transição da EC 103/2019), o PBC compreende exclusivamente as competências a partir de **julho de 1994** (início do Plano Real).
- Competências anteriores a 07/1994 são computadas para fins de tempo de contribuição, mas assinaladas com `Conta RMI = Não` e `Fator Correção = N/A` no relatório de valores padrão.
- **`Conta RMI` depende só da data (>= 07/1994), nunca do valor**: uma competência com remuneração abaixo do salário mínimo continua entrando na soma/contagem da média do PBC — o teto legal do salário mínimo (`Conta Contribuição`, coluna informativa) é um teste de **aptidão para tempo/mês cheio**, aplicável só a partir de 11/2019, e não pode excluir a competência do cálculo monetário da RMI.

### 4.2. Índices de Atualização Monetária (Art. 33 do Decreto 3.048/1999)
- Divulgados mensalmente pelo Ministério da Previdência Social (MPS) via Portaria específica.
- Cada competência a partir de 07/1994 possui fator multiplicador com 6 casas decimais.
- O valor atualizado do salário de contribuição é calculado por:
  `Valor Atualizado = Remuneração CNIS * Fator MPS`

---

## 5. Regras de Transição da EC 103/2019 (ativadas via `--ec103-transicao`)

> **Aviso de uso jurídico**: os números de artigo abaixo seguem a sistematização doutrinária usual da EC 103/2019. Confira-os contra o texto oficial da emenda antes de citá-los em peça formal. As tabelas numéricas (pontos, idade mínima, percentuais de coeficiente) são parâmetros normativos estáveis e amplamente consolidados — alta confiabilidade.

Implementado em `_pontos_minimos_ec103`, `_idade_minima_progressiva_ec103`, `calcular_fator_previdenciario` e `analisar_transicoes_ec103` (`scripts/_cnis_engine.py`), expostos por `scripts/analisar_cnis.py`. Exige `sexo` explícito (nunca inferido).

### 5.1. Regra de Pontos
- Tempo mínimo de contribuição: 30 anos (mulher) / 35 anos (homem). Carência: 180 contribuições.
- Pontos mínimos (idade + tempo de contribuição na DER), tabela progressiva por ano:
  - Mulher: 86 (2019) → +1/ano → 100 (a partir de 2033).
  - Homem: 96 (2019) → +1/ano → 105 (a partir de 2028).
- Coeficiente: **100%** da média aritmética simples de todo o PBC (sem redutor).
- **Status**: totalmente implementado.

### 5.2. Pedágio de 50%
- Aplicável somente a quem, em 13/11/2019, tinha **até 2 anos faltantes** para completar o tempo mínimo da regra anterior (35a/30a). Se o tempo já estava completo ou faltava mais de 2 anos, a regra não se aplica (verificação exige revisão humana).
- Tempo exigido = tempo já cumprido em 13/11/2019 + (tempo faltante nessa data × 1,5).
- Carência: 180.
- RMI = maior valor entre (média × fator previdenciário) e (100% da média). O fator previdenciário depende da **expectativa de sobrevida IBGE** (tábua do ano/idade da DER), que a skill **não possui internamente** — deve ser informada via `--expectativa-sobrevida <anos>`.
  - Fórmula do fator previdenciário (Lei 9.876/1999, art. 7º): `Fp = (Tc×a/Es) × [1 + ((Id + Tc×a)/100)]`, onde `Tc` = tempo de contribuição (anos), `a` = 0,31 (alíquota fixa), `Id` = idade (anos), `Es` = expectativa de sobrevida (anos).
- **Status**: elegibilidade (tempo/data) sempre calculada; RMI (fator previdenciário) **pendente** sem `--expectativa-sobrevida` — o relatório sinaliza isso explicitamente.

### 5.3. Pedágio de 100%
- Idade mínima: 57 anos (mulher) / 60 anos (homem).
- Pedágio de 100% sobre o tempo faltante em 13/11/2019 para completar o tempo mínimo da regra anterior (35a/30a): o tempo faltante nessa data é **dobrado**, não apenas somado uma vez.
  `Tempo exigido = Tempo cumprido até 12/11/2019 + 2 × Tempo faltante nessa data` (equivalente a `Tempo mínimo + Tempo faltante`).
- Carência: 180.
- Coeficiente: **100%** da média aritmética simples, sem fator previdenciário.
- **Status**: totalmente implementado.

### 5.4. Idade Mínima Progressiva
- Idade mínima progressiva (+6 meses/ano a partir de 2019):
  - Mulher: 56 (2019) → 62 (estabiliza).
  - Homem: 61 (2019) → 65 (estabiliza).
- Tempo mínimo: 30a (mulher) / 35a (homem). Carência: 180.
- Coeficiente: reaproveita a fórmula da Regra Geral — 60% + 2%/ano de tempo de contribuição acima de 20 anos.
- **Status**: totalmente implementado.

### 5.5. Regra Permanente (Ordinária, pós-EC103 — não é regra de transição)
- Regra definitiva do RGPS após a reforma (Art. 19/19-A do Dec. 3.048/99, redação dada pela EC 103/2019), aplicável independentemente de qualquer regra de transição, desde que cumpridos os requisitos.
- Idade mínima: 65 anos (homem) / 62 anos (mulher), sem progressão. Tempo mínimo: 20 anos (homem) / 15 anos (mulher). Carência: 180.
- Coeficiente: 60% + 2%/ano de tempo de contribuição acima do mínimo da própria regra (20a homem / 15a mulher).
- **Status**: totalmente implementado. Incluída junto às 4 regras de transição na análise comparativa do Quadro-Resumo (item 5.6), já que concorre com elas.

### 5.6. Análise Comparativa — Sem Eleição Automática de "Melhor Regra"
- O Quadro-Resumo mostra as 5 regras (4 de transição + a Regra Permanente) lado a lado, cada uma com: situação de elegibilidade na DER, data de cumprimento (já atingida ou projetada), e RMI estimada com o coeficiente correto daquela regra especificamente (não a fórmula única da Regra Geral).
- Linhas de regras já elegíveis/cumpridas são destacadas em verde claro no Quadro-Resumo, para identificação visual rápida.
- A ferramenta **não elege automaticamente** uma regra como "mais vantajosa" — a decisão de qual regra utilizar cabe ao operador/advogado, considerando o caso concreto (ex.: prioridade do cliente entre data de elegibilidade mais próxima ou maior RMI).

### 5.7. Método de Projeção de Data de Cumprimento
- Para regras ainda não cumpridas na DER, a data futura de cumprimento é projetada assumindo **contribuição ordinária continuada a partir da DER**, sob a regra do mês cheio pós-EC103 (1 mês corrido = 1 mês cheio de 30 dias líquidos) — premissa confirmada com o usuário, ajustável manualmente depois conforme o caso.
- Data de cumprimento = a mais tardia entre a projeção do tempo faltante e a data em que a idade mínima da regra (quando houver) é atingida (calculada diretamente a partir da data de nascimento).
- Na Regra de Pontos, idade e tempo avançam juntos (1 ano de idade + 1 ano de tempo por ano corrido), então os pontos sobem 2/ano; a projeção usa a tabela de pontos vigente no ano da DER — se a data projetada cruzar virada de ano, o requisito de pontos pode mudar e deve ser revisado manualmente.
- A RMI estimada por regra usa a média do PBC apurada **na DER** (não projetada) — a projeção de valores futuros de PBC introduziria hipóteses adicionais fora do escopo da skill.

---

## 6. Fator de Especialidade (Conversão de Tempo Especial em Comum)

- **Opcional, anotado manualmente** pelo usuário no JSON canônico (módulo 1), já que o CNIS não traz essa informação — depende de prova externa (PPP, LTCAT, laudo pericial etc.).
- Schema por vínculo: `"especialidade": [{"inicio": "DD/MM/AAAA", "fim": "DD/MM/AAAA", "fator": 1.4, "fundamento": "PPP nº..."}]`. Vínculo sem o campo mantém fator 1.0 (comportamento padrão, sem conversão).
- **Cálculo**: o vínculo é quebrado em segmentos cronológicos exatos nos pontos de corte da Reforma (13/11/2019) e dos períodos de especialidade informados — cada segmento fica com fase (pré/pós-reforma) e fator homogêneos, é apurado normalmente (dias corridos ou mês cheio, conforme a fase) e o resultado é multiplicado pelo fator do próprio segmento (1.0 fora de período especial). Sem estimativa proporcional — o corte é exato por data.
- Exibido na saída estruturada como um item por segmento: `Dias Líquidos = ARRED((Dias Brutos - Concomit.) × Fator)`. Todos os segmentos usam suas datas reais; a sobreposição é descontada em `concomitancia` (seção 2), e o fator incide só sobre o tempo líquido do segmento.
- **Análise jurídica anterior ao cálculo**: siga [tempo-especial.md](tempo-especial.md) para decidir o enquadramento e a possibilidade de conversão, inclusive à luz da ADI 6309. O motor só multiplica os fatores informados e não valida esses requisitos. Não anote fator maior que 1 em período cuja conversão seja vedada; mantenha a contagem da exposição especial separada do tempo comum convertido. Confira também a inclusão do dia-limite legal: o corte interno do motor em 13/11/2019 não resolve, por si, essa questão.
