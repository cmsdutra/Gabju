# Juros Compostos — Critérios de Regularidade

## O que a rotina verifica

`scripts/rotinas/juros_compostos.py verificar` compara um montante informado (ex.: constante de um demonstrativo de débito apresentado por uma das partes) contra dois montantes esperados, calculados a partir do mesmo principal, taxa e prazo:

- capitalização **simples**: M = P × (1 + i × n);
- capitalização **composta**: M = P × (1 + i)ⁿ.

O resultado indica com qual dos dois regimes o valor informado é compatível, dentro de uma tolerância.

## Como interpretar o resultado

- **Compatível apenas com capitalização simples**, quando o título judicial, a lei ou o contrato determinam capitalização simples: regular.
- **Compatível apenas com capitalização composta**, quando o regime autorizado é o simples (ou vice-versa): indício de irregularidade — mas a conclusão sobre se a capitalização composta é ou não permitida no caso concreto depende do título judicial, do tipo de dívida e da legislação aplicável, que devem ser verificados na wiki (`references/manual-de-calculos-2025/`) ou informados pelo usuário. A rotina não decide isso sozinha.
- **Incompatível com ambos os regimes**: não presuma irregularidade automaticamente — primeiro confira se a taxa, o prazo ou o próprio montante informado foram transcritos corretamente, pois um erro de transcrição produz o mesmo sintoma.
- **Compatível com ambos dentro da tolerância**: comum em prazos curtos ou taxas baixas, quando a diferença entre os regimes ainda é pequena — não é possível, nesse caso, concluir qual regime foi efetivamente usado só por esse teste.

## Limitação importante

Este teste identifica **incompatibilidade aritmética** com um regime de capitalização; não substitui a análise jurídica sobre qual regime é o legalmente cabível para o tipo de dívida em questão (isso é a controvérsia frequentemente chamada de "anatocismo"). Não cite jurisprudência sobre a matéria a menos que fornecida integralmente pelo usuário, conforme as Limitações Absolutas do `SKILL.md`.
