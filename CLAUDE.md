# CLAUDE.md — Memória do projeto Esteira LIE

Este arquivo é a memória de longo prazo para mim (Claude Code) trabalhar neste
projeto de forma consistente entre sessões. **Leia este arquivo inteiro antes de
mexer em qualquer código.**

## 1. O que é o Esteira LIE

Sistema **local** (roda só no computador da Karine) que transforma a presença
pública de uma OSC (Instagram, Facebook, notícias, site) + material que a Karine
complementa manualmente em três entregáveis para o SLI (Sistema da Lei de
Incentivo ao Esporte):

1. **CTO** — Comprovação de Capacidade Técnico-Operativa (`.docx`) → olha para
   **trás**: o que a OSC já fez, provado com fotos datadas, reportagens,
   publicações.
2. **Escrita do projeto** (`.docx`) → olha para **frente**: Objetivos,
   Justificativa, Metodologia, Metas qualitativas e quantitativas, Público
   beneficiário.
3. **Planilha orçamentária** (`.xlsx`) → por etapa orçamentária, com memória de
   cálculo e checagem de limites.

As duas trilhas (CTO e Projeto+Orçamento) usam os **mesmos dados coletados**, mas
são processamentos **SEPARADOS**. **Nunca gerar CTO e projeto na mesma chamada de
IA.**

## 2. Quem é a usuária

Karine — consultora especialista em Lei de Incentivo ao Esporte (LIE federal e
estaduais). **Não é desenvolvedora.** Precisa de:
- comandos simples para rodar (`instalar` e `rodar`);
- mensagens de erro em **português**;
- interface visual no navegador (Streamlit).

## 3. Regras inegociáveis (valem para todo código e todo prompt de IA)

1. **Nunca inventar norma, número, valor ou artigo legal.** Toda regra normativa
   vem de `normas/regras.yaml`, com fonte e status. A IA nunca "sabe" regra da
   LIE de memória — ela **recebe** as regras no prompt.
2. **Nunca inventar dado da OSC.** Se faltar informação, o texto gerado usa o
   marcador `[PREENCHER: descrição do que falta]` e o item aparece numa lista de
   pendências na tela.
3. **Nunca inventar preço.** O orçamento só usa valores de `dados/catalogo_itens.xlsx`.
   Item fora do catálogo entra com valor em branco e sinalizado em amarelo.
4. **Rastreabilidade.** Todo parágrafo de CTO e todo dado factual do projeto cita
   o ID da evidência que o sustenta (ex.: `[EV-0042]`). No `.docx` final as
   citações podem ser ocultadas, mas ficam num relatório de rastreabilidade.
5. **Gate humano obrigatório.** Nada vira documento final sem curadoria
   (evidências aprovadas) e validação (texto revisado). O sistema **nunca envia
   nada para lugar nenhum**; só gera arquivos locais.
6. **Regras com status `pendente`** não bloqueiam, mas geram alerta visível:
   "regra ainda não validada pela Karine".
7. **Tudo em português do Brasil.** Linguagem técnica, direta, sem floreio.

## 4. Stack (usar exatamente isto, salvo impedimento — aí perguntar à Karine)

- Python 3.11+, ambiente virtual `.venv`
- **Streamlit** (interface local multipáginas)
- **SQLModel/sqlite3** (dados); mídia em pasta local
- **Anthropic API (Claude)** — chave em `.env` (`ANTHROPIC_API_KEY`), nunca
  versionada. Modelo configurável em `config.yaml` (Claude Sonnet mais recente).
- **instaloader** (Instagram público, sem login por padrão)
- **feedparser + trafilatura** (notícias via RSS do Google Notícias)
- **httpx + trafilatura** (site da entidade)
- **docxtpl** (Word a partir de modelos com tags)
- **openpyxl** (Excel com FÓRMULAS reais, não valores fixos)
- **Pillow** (miniaturas/redimensionamento)
- **PyYAML** (regras e config)
- **pytest** (testes — testes NÃO chamam a API)

## 5. Como rodar

```
./instalar.sh      # ou instalar.bat no Windows  → cria .venv e instala tudo
./rodar.sh         # ou rodar.bat no Windows      → abre a interface no navegador
```

O banco (`esteira_lie.db`) é criado automaticamente na primeira execução.

## 6. Estrutura de pastas

Ver seção 4 do prompt original. Resumo:
- `app/` — código Streamlit (`Home.py`, `pages/`, `coleta/`, `ia/`, `documentos/`,
  `regras/`, `db/`)
- `normas/` — `regras.yaml` (base estruturada) e `fontes/` (PDFs das normas, a
  Karine coloca aqui)
- `templates/` — modelos `.docx` com tags docxtpl
- `dados/` — `catalogo_itens.xlsx` e `dados/osc/<cnpj>/` (mídia e saídas por OSC)
- `tests/` — testes pytest

## 7. Base de regras

`normas/regras.yaml` guarda cada regra com: `id`, `tema`, `descricao`,
`tipo_checagem`, `parametros`, `fonte`, `vigencia`, `status`.

**Todo o seed inicial nasce com `status: pendente`**, porque o Manual do
Proponente LIE 2023 é regido pela Portaria 424/2020 e Decreto 6.180/2007, e a
regulamentação mudou (LC 222/2025, Decreto 12.861/2026, Portaria MESP nº 10/2026).
A Portaria 10/2026 será lida na **Fase 5** (texto em `normas/fontes/`), e só então
regras novas/alteradas são propostas **sempre citando o artigo exato**. Dúvidas
sobre o texto vão para `normas/duvidas.md`.

A página `9_Regras.py` permite ver/filtrar regras por status e mudar para
`validada` com um clique (registrando a data).

## 8. Fases de construção (entregar UMA por vez, rodar testes, PARAR e esperar aprovação)

- **Fase 0 — Fundação** ✅ *(em andamento / entregue nesta sessão)*: estrutura de
  pastas, `CLAUDE.md`, `README.md`, `config.yaml`, `.env.example`, scripts
  instalar/rodar, banco criado, Home do Streamlit abrindo, página de Regras
  mostrando o seed.
- **Fase 1 — Cadastro da OSC + entrada manual** (ainda não iniciada)
- **Fase 2 — Coleta automática** (ainda não iniciada)
- **Fase 3 — Curadoria + Diagnóstico** (gate humano nº 1) (ainda não iniciada)
- **Fase 4 — Trilha CTO (.docx)** (ainda não iniciada)
- **Fase 5 — Regras da Portaria 10 + Trilha de escrita** (ainda não iniciada)
- **Fase 6 — Planilha orçamentária (.xlsx)** (ainda não iniciada)
- **Fase 7 — Conferência final e pacote** (gate humano nº 2) (ainda não iniciada)

Ao fim de cada fase: rodar testes, explicar em linguagem simples o que testar na
tela, atualizar este `CLAUDE.md` e PARAR até a Karine aprovar.

## 9. Decisões tomadas (log)

- **2026-10-03 (Fase 0):**
  - ORM: **SQLModel** (sobre SQLAlchemy) para o banco; SQLite em arquivo
    `esteira_lie.db` na raiz do projeto.
  - Campos de lista (ex.: `modalidades`) são guardados como **JSON em coluna
    texto** nesta fase, para manter o esquema simples; podem virar tabelas
    próprias se necessário mais adiante.
  - Código de evidência (`EV-0001`) é derivado do `id` inteiro no momento da
    exibição/geração, via `codigo` persistido após o insert.
  - `regras.yaml` é a **fonte da verdade** do texto das regras; o banco espelha
    as regras só para guardar o **status** e a **data de validação** feita pela
    Karine (sincronização não sobrescreve o status já gravado no banco).
  - Nome do modelo de IA fica em `config.yaml` (`ia.modelo`), padrão
    `claude-sonnet-5-5`. Nenhuma chamada de IA existe ainda na Fase 0.
  - **Modelos textuais oficiais (enviados pela Karine):** os quatro arquivos
    seguem o mesmo esqueleto de 8 blocos do formulário textual do SLI. Guardados
    em `templates/referencia_textual/` e mapeados em `templates/ESTRUTURA_TEXTUAL.md`.
    Servem de base para o `projeto_modelo.docx` da Fase 5.
  - **Limites de caracteres** do formulário (Objeto 1.000; Objetivos 1.000;
    Metodologia 10.000; Justificativa 10.000; Metas 500/item) viraram regras
    `ESC-LIM-*` no `regras.yaml` (status `pendente`, fonte = formulário oficial).
    Novo `tipo_checagem: limite_caracteres` + `checar_limite_caracteres()`.

## 10. Convenções de código

- Código comentado em **português**, funções pequenas.
- Nenhuma credencial em código ou log.
- `.gitignore` cobre `.env`, `dados/osc/`, `*.db`, `.venv`.
- Tratar erros de rede/coleta sem derrubar a aplicação.
