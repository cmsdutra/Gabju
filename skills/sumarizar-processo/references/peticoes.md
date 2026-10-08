# Petições

São petições:
- Petição inicial, contestação e réplica;
- Petição intercorrente;
- Informação de interposição de agravo;
- Manifestações em geral.

Excluem-se:
- Meros substabelecimentos ou renúncia de mandato;
- Manifestação de ciência.

# Saída

```markdown

# PETIÇÕES

<loop condição="cada petição" ordem="crescente de id.">

## [TIPO] - [ID]

-----
**Aspectos Gerais:**
- ID da Petição: [ID atribuído à petição no processo]
- Tipo: [inicial/contestação/réplica/embargos/pedido de reconsideração/alegações finais/impugnação/pedido de cumprimento de sentença/outro]
- Peticionante:
    - Nome: [nome do peticionante]
    - Papel Processual: [parte autora, ré, embargante, embargado, terceiro interessado, etc.]
- Data de Protocolo: [DD-MM-AAAA]
- Classificação: [mérito/processual/misto]
- Referência: [ato judicial ou petição anterior a que se vincula, se houver]
---
**Fundamentos:**
- Fundamentos de Fato: 
    `narrativa de fatos detalhada, com eventos, relações e cronologia, devendo contemplar todos os fatos narrados na petição. Reflita a perspectiva do peticionante, mesmo se houver sobreposição com a parte jurídica`
    `liste de 5 a 10 blocos narrativos (unidade contextual) completos, sempre que possível, se se tratar de petição inicial, contestação, alegações finais ou outra petição mais complexa; em outros casos, liste de 3 a 7 blocos narrativos completos`
    - [fundamento fático 1]
    - ...
    - [fundamento fático n]
- Fundamentos de Direito:
    `relacione separadamente, de forma mais detalhada possível, cada argumento jurídico utilizado na petição, incluindo: - referências a dispositivo legais e institutos jurídicos; - princípios jurídicos invocados; - interpretações doutrinárias; - jurisprudência`
    `reuna de 5 a 10 blocos argumentativos, sempre que possível`
    - [fundamento jurídico 1]
    - ...
    - [fundamento jurídico n]
- Precedentes jurisprudenciais citados:
    `lista dos precedentes jurisprudenciais citados no ato, se houver`
- Dispositivos legais citados:
    `lista dos dispositivos legais citados no ato, se houver`
- Declaração/Confissão/Reconhecimento/Desistência:
  - [descrever de forma sintética eventual reconhecimento do pedido, confissão, desistência de pedido ou outra manifestação relevante]
---
**Conclusão:**
- Lista de Pedidos:
    `transcrever, de forma literal, completa e detalhada, todos os pedidos formulados na petição`
    - [pedido 1]
    ...
    - [pedido n]
- Pedido de Prova:
  - Há Pedido Específico de Prova: [sim/não] `Atenção: protesto genérico não equivale a pedido específico de prova`
  - Detalhamento: [se for o caso, descrever tipo de prova requerida: pericial, testemunhal, documental, etc.]
- Alteração de Valor da Causa:
  - Atribui ou altera o valor da causa: [sim/não]
  - Novo valor: [se aplicável, indicar valor]
---
**Síntese:**
- Síntese Técnica:
  - `resumo técnico da peticao de até 150 palavras`
- Palavras-chave: `listar entre 5 e 10 palavras-chave, separadas por vírgula e espaço`
-----
</loop>
```
# ORIENTAÇÕES GERAIS
- Não apresente justificativas, apenas o conteúdo organizado.
- Se algum dado não for localizado, registrar "não localizado".
- Mantenha máximo rigor técnico e clareza textual.
- Atenção especial à fidelidade ao conteúdo da petição.
- Evitar qualquer narrativa ou descrição fática que não esteja expressamente extraída da petição.