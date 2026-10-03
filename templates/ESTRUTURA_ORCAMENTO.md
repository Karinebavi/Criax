# Estrutura da planilha orçamentária (PO) — modelos do SLI

Mapa extraído dos modelos enviados pela Karine (ver `templates/referencia_orcamento/`).
Os quatro arquivos seguem **o mesmo layout**. Guia a geração do `orcamento_<osc>.xlsx`
na **Fase 6**.

> Os percentuais e fatores observados abaixo variam entre os modelos (a Karine
> define caso a caso). Só o que é regra firme virou `regras.yaml`; o resto é
> premissa de cálculo que a Karine informa. **Nenhum número é inventado pela IA.**

## Layout da aba de orçamento

Uma aba (ex.: "Planilha Orçamentária"), dividida em **seções = etapas**:

```
ATIVIDADE FIM
  <Bloco de categoria 1>  (ex.: Recursos Humanos, Encargos, Uniformes, Material...)
  <Bloco de categoria 2>
  ...
  Total Despesas Atividade Fim

ATIVIDADE MEIO
  <Bloco de categoria 1>  (ex.: Serviços de Terceiros, Divulgação/Promoção...)
  ...
  Total Despesas Atividade Meio        (+ % sobre a Atividade Fim)

Total Atividade Fim + Meio
Valor de Elaboração / Captação         (percentual sobre o total, com teto)
Valor Total do Projeto
```

### Bloco de categoria (padrão que se repete)

1. **Linha de cabeçalho da categoria:**
   `Nº | Ações | Quantidade | Duração | Fontes | Total (R$)`
   O **Total** da categoria é `=SUM(...)` das linhas de detalhe abaixo.

2. **Linha de cabeçalho do detalhamento:**
   `Nº | Detalhamento das Ações | Resumo do Detalhamento | Quantidade (D) |
   Unidade | Duração (F) | Unidade | Valor Unitário (H) | Total (R$) (I) |
   ORÇAMENTO 01 | VALOR | ORÇAMENTO 02 | VALOR | ORÇAMENTO 03 | VALOR | MÉDIA (Q)`

3. **Linhas de detalhe (itens):**
   - Coluna **C "Resumo do Detalhamento"** traz a **memória de cálculo** inline,
     no formato `MC: <quantidade> x <período> ...`.
   - **Total do item (I)** = `Valor Unitário (H) × Duração (F) × Quantidade (D)`.
   - Colunas **K–P**: até **3 orçamentos** (nome da fonte + valor) para justificar
     o preço. Coluna **Q "MÉDIA"** = média dos 3 orçamentos preenchidos
     (`=AVERAGE(...)`, com variações `IFERROR`/`COUNT` para não quebrar quando
     faltam cotações).

### Totais e fórmulas de fechamento (observadas nos modelos)

| Linha | Fórmula (exemplo) | Significado |
|---|---|---|
| Total Atividade Fim | `=SUM(<subtotais das categorias Fim>)` | soma das categorias |
| Total Atividade Meio | `=SUM(<subtotais das categorias Meio>)` | soma das categorias |
| % Meio sobre Fim | `=TotalMeio / TotalFim` | **checagem ORC-001 (≤ 15%)** |
| Total Fim + Meio | `=TotalMeio + TotalFim` | base da captação |
| Elaboração / Captação | `=IF((Base * X%) > 100000; 100000; Base * X%)` | **% variável, teto R$ 100.000** (ORC-CAP-001) |
| % Captação sobre total | `=Captação / Base` | conferência |
| Valor Total do Projeto | `=Fim + Meio + Captação` | total final |

- **Percentual de captação observado:** varia entre os modelos (5%, 7%, 10%). É
  escolha da Karine por projeto. O **teto de R$ 100.000** é constante.
- **Encargos trabalhistas (CLT):** aparecem como um fator sobre o salário
  (ex.: `H × 0,678` ou `H × 68,5%`). O fator **varia** e é premissa da Karine —
  não é número fixo do sistema.

## Fontes de preço citadas nos modelos

Os itens citam fontes como *"Planilha de Referência do Ministério"*, *"Painel de
Preços"*, *"Item NNNN da Planilha de Referência"*. No sistema, o **preço só vem do
catálogo** (`dados/catalogo_itens.xlsx`); item fora do catálogo entra com valor em
branco (amarelo). As 3 colunas de orçamento servem para registrar as cotações que
justificam o valor de referência.

## O que a Fase 6 vai gerar (sobre este layout)

Mantendo o layout por etapa acima, a planilha gerada terá, além das abas de etapa:
- **Resumo** (totais por etapa e do projeto);
- **Memória de cálculo** (consolidando os `MC:` de cada item);
- **Checagens** (aplica as regras de `regras.yaml` — ex.: ORC-001 e ORC-CAP-001 —
  com resultado OK/ALERTA e a fonte de cada regra).

Destaques visuais: **amarelo** = item sem valor; **vermelho** = regra violada;
**cinza** = regra pendente de validação.

Todas as fórmulas são **fórmulas reais do Excel** (openpyxl), não valores fixos.
