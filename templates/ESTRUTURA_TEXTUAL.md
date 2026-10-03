# Estrutura do textual do projeto esportivo (SLI)

Mapa extraído dos modelos enviados pela Karine (ver `templates/referencia_textual/`).
Os quatro arquivos seguem **o mesmo esqueleto**: 8 blocos (tabelas). As diferenças
entre eles são apenas os exemplos de conteúdo (modalidades/público). Este mapa
guia a geração do `projeto_<osc>.docx` na **Fase 5**.

> **Importante:** os limites de caracteres abaixo saem do próprio formulário
> oficial e estão registrados em `normas/regras.yaml` (regras `ESC-LIM-*`), com
> status `pendente` — porque a norma mudou (LC 222/2025, Decreto 12.861/2026,
> Portaria MESP nº 10/2026) e os limites precisam ser confirmados.

## Blocos (na ordem do formulário)

### 1. CADASTRO DO PROPONENTE
Preenchido com dados da OSC (Fase 1): Proponente, CNPJ, E-mail, Endereço,
Telefone (DDD), Nome do Titular/Responsável Legal. → **dados manuais da OSC**.

### 2. IDENTIFICAÇÃO DO PROJETO
- **Título** → premissa da Karine
- **Objeto do Projeto** — *limite 1.000 caracteres* → redigido pela IA
- **Período de Execução** (ex.: 12 meses) → premissa
- **Destinação**: ( ) Evento ( ) Atividade Regular → premissa
- **Locais de Execução** → premissa / dado da OSC
- **Manifestação Desportiva**: ( ) Rendimento ( ) Esporte para toda a vida ( ) Educacional → premissa
  > Atenção: as categorias podem ter mudado para as da Lei Geral do Esporte
  > (Formação Esportiva / Esporte para Toda a Vida / Excelência Esportiva).
  > Confirmar na Portaria MESP nº 10/2026 (Fase 5).
- **Tipo**: ( ) Desportivo ( ) Paradesportivo → premissa
- **Detalhamento**: Capacitação / Escolinha / Oficina / Treinamento / Pesquisa / Seminário → premissa
- **Modalidade(s)** → premissa

### 3. BREVE DESCRIÇÃO DO PÚBLICO BENEFICIÁRIO
Grade por faixa etária × sexo + total de beneficiários diretos:
Crianças (0–11), Adolescentes (12–18), Adultos (19–59), Idosos (60+),
Pessoas com deficiência; Sexo Masculino/Feminino por faixa. → **números da Karine**
(nunca inventados; se faltar, `[PREENCHER: ...]`).

### 4. Quadro de enquadramento (Sim/Não)
Cinco perguntas de enquadramento (vulnerabilidade social; manifestação educacional;
continuidade; contrato de patrocínio ≥ 20%; competições do calendário oficial).
→ **premissa/decisão da Karine**.

### 5. INFORMAÇÃO DA CONTA CORRENTE
Banco, Agência, DV. → **dado manual da OSC**.

### 6. OBJETIVOS
Citar o objeto e o que se pretende alcançar. — *limite 1.000 caracteres* → IA.

### 7. METODOLOGIA — *limite 10.000 caracteres* → IA
O formulário exige cobrir: desenvolvimento/execução e método; **fases de execução
com cronograma**; **grade horária** (modalidades, nº de turmas, beneficiários por
turma, frequência semanal por turno e faixa etária); **quadro de horário dos
profissionais** com atribuições; **calendário de eventos** (datas e duração);
**critério de seleção** de participantes e profissionais; acessibilidade;
adequação à manifestação; destinação do material permanente; fontes de recursos.
→ cobre a regra `ESC-MET-001`.

### 8. JUSTIFICATIVA — *limite 10.000 caracteres* → IA
Por que o projeto, importância para o esporte na região, conveniência do apoio
incentivado. Indicadores sociais/econômicos **não podem ser inventados**
(`[PREENCHER: indicador + fonte]`). → cobre `ESC-JUS-001` e `ESC-JUS-002`.

### 9. METAS QUALITATIVAS e QUANTITATIVAS — *limite 500 caracteres por item* → IA
Cada meta com **Meta / Indicador / Instrumento de verificação** (cobre `ESC-MTA-001`).
Quantidade de metas conforme `ESC-MTQ-001` e `ESC-MTN-001` (mín. 2 / máx. 5 cada).

## Marcadores encontrados nos exemplos

Os modelos usam marcadores do tipo `[EDITAR: TÍTULO DO PROJETO]`,
`[ MODALIDADES]`, `[PÚBLICO BENEFICIÁRIO]`, `[XX]`. No sistema, padronizamos para
`[PREENCHER: descrição]` (dado da OSC/Karine que falta) — ver regra inegociável nº 2.

## Como isso vira o modelo da Fase 5

Na Fase 5 criaremos `templates/projeto_modelo.docx` (com tags docxtpl) reproduzindo
esses 8 blocos. A Karine poderá substituí-lo pelo seu próprio Word, desde que
mantenha as mesmas tags. A IA redige Objeto, Objetivos, Metodologia, Justificativa
e Metas em chamadas **separadas**, cada uma recebendo as regras do tema `escrita`
(incluindo os limites de caracteres) + premissas + diagnóstico + evidências.
