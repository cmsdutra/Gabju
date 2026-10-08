# Documentos Auxiliares

São documentos auxiliares:
- Laudos, perícias e pareceres técnicos ou jurídicos
- Certidões, atas e registros de audiência
- Relatórios, ofícios e comunicações oficiais
- Requerimentos e decisões administrativas, atos normativos
- Provas documentais em geral (contratos, prontuários, comprovantes, correspondências etc.)

Excluem-se:
- Petições (ver `references/peticoes.md`)
- Atos judiciais (ver `references/atos-judiciais.md`)
- Ofício que apenas encaminha ato judicial ou petição principal (processar o documento principal encaminhado, conforme instrução em `SKILL.md`)

# Saída

```markdown

# DOCUMENTOS AUXILIARES

<loop condição="cada documento auxiliar" ordem="crescente de id.">

## [TIPO DOCUMENTAL] - [ID]

-----
**Aspectos Gerais:**
- ID do Documento: [ID atribuído ao documento no processo]
- Título: [título ou descrição presumida]
- Tipo Documental: [prova, comunicação oficial, relatório, laudo, parecer, certidão, ata, requerimento administrativo, decisão administrativa, ato normativo, outro]
- Data do Documento: [DD-MM-AAAA]
- Emissor: [órgão, entidade ou servidor]
- Data da Juntada: [DD-MM-AAAA]
- Quem juntou: [NOME (autor/réu/terceiro/perito etc)]
- Legível: [sim/não]
- Estrutura Documental:
    - Parte de Documento Composto: [sim/não]
    - Posição no Documento Composto: [posição relativa no conjunto, se aplicável]
---
**Conteúdo:**
- Objeto do Documento:
    `Nesta seção, faça um resumo detalhado e minucioso do conteúdo do documento, indicando seu contexto, objeto, fundamentos, parte atingida e efeitos jurídicos. Reuna de 10 a 15 blocos informativos completos e detalhados sobre o documento, se se tratar de ata, registro de audiência ou laudo pericial, ou de 5 a 10 blocos informativos completos e detalhados, se for outro tipo de documento. Havendo especial necessidade, os limites de blocos informativos podem ser violados, desde que garantidas a não prolixidade e a não concisão excessiva.`
    - [informação 1]
    - ...
    - [informação n]
- Transcrição:
    `Liste de 10 a 15 trechos textuais mais importantes, completos, literais e fiéis extraídos do documento, se se tratar de ata, registro de audiência ou laudo pericial, ou de 5 a 10 trechos mais importantes, se for outro tipo de documento. Havendo necessidade, os limites de blocos de transcrição podem ser violados, desde que garantidas a não prolixidade e a não concisão excessiva`
    - [trecho 1]
    - ...
    - [trecho n]
- Precedentes jurisprudenciais citados:
    `lista dos precedentes jurisprudenciais citados no documento, se houver (aplicável sobretudo a pareceres e decisões administrativas)`
- Dispositivos legais citados:
    `lista dos dispositivos legais citados no documento, se houver (aplicável sobretudo a pareceres e decisões administrativas)`
---
**Conclusão:**
- Conclusão:
    - [síntese da demonstração ou informação final do documento]
- Relevância para Minuta:
    - [alta/média/baixa/minuta não informada]
---
**Síntese:**
- Síntese Técnica:
    - [resumo técnico do documento de até 200 palavras]
- Palavras-chave: `listar, em um único parágrafo, separadas por vírgula e espaço, de 10 a 15 (em função da complexidade do documento) palavras-chave`
---
**Controle:**
- Vinculatividade: `informar a qual controvérsia de fato ou de direito o documento se vincula, conforme a decisão de saneamento (se já proferida) ou os fatos narrados nas petições (na ausência de saneamento)`
- Confiabilidade:
    - [percentual] `de acordo com legibilidade, integridade, fé pública, vinculação às controvérsias de fato, se foi ou não contestado`
-----
</loop>

```

# ORIENTAÇÕES GERAIS
- Não apresente justificativas, apenas o conteúdo organizado.
- Se algum dado não for localizado, registrar "não localizado".
- Mantenha máximo rigor técnico e clareza textual.
- Atenção especial à fidelidade ao conteúdo do documento.
- Evitar qualquer narrativa ou inferência que não esteja expressamente extraída do documento.
