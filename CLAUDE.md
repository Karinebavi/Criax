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
- **Fase 1 — Cadastro da OSC** ✅ (tela `1_Cadastro_OSC.py`; entrada manual de
  evidências/parcerias/equipe ainda a completar)
- **Fase 2 — Coleta automática** ✅ parcial (notícias + Instagram em
  `2_Coleta.py`; Facebook/site a completar). Instagram só funciona em IP
  residencial (na nuvem dá 429).
- **Fase 3 — Curadoria** ✅ (tela `3_Curadoria.py`: aprovar/descartar, marcar
  logomarca/prática/terceiros/link, bbox do realce). **Diagnóstico por IA**
  (Fase 3 parte 2) ainda não iniciado.
- **Fase 4 — Trilha CTO (.docx)** ✅ (tela `5_CTO.py` + `gerar_cto.py`: timbrado,
  4 blocos, galeria de fotos com zoom+seta, rastreabilidade). Template docxtpl
  substituível ainda a fazer.
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
  - **Modelos de planilha orçamentária (enviados pela Karine):** quatro arquivos,
    mesmo layout. Guardados em `templates/referencia_orcamento/` e mapeados em
    `templates/ESTRUTURA_ORCAMENTO.md`. Layout por etapa (Atividade Fim/Meio),
    blocos de categoria com detalhamento, Total do item = `Valor Unit × Duração ×
    Quantidade`, 3 orçamentos + MÉDIA, memória de cálculo inline na coluna
    "Resumo do Detalhamento". Fechamento: % Meio/Fim (ORC-001), Elaboração/Captação
    (% variável com teto R$ 100.000 → nova regra `ORC-CAP-001`, pendente), Total.
    Percentual de captação (5/7/10%) e fator de encargos CLT (0,678 / 68,5%) são
    **premissas variáveis da Karine**, não números fixos do sistema. A Fase 6
    acrescenta abas Resumo / Memória de cálculo / Checagens sobre esse layout.
  - **CTO reestruturada pelo Checklist CTO v3 (equipe CASE):** guardado em
    `templates/referencia_cto/` e mapeado em `templates/ESTRUTURA_CTO.md`. A CTO
    passa a ter 4 blocos / 37 itens, hierarquia de evidências (fotos/reportagens/
    publicações → parcerias → currículos) e ordem de montagem (evidências
    esportivas antes dos termos). Regras de descarte firmes: foto sem logomarca
    descartada; LINK > PRINT (print só com data visível); links testados;
    autodeclaração isolada não aceita; evidências de terceiros valem mais. A
    seção `cto` do `regras.yaml` passou de 1 para 9 regras (CTO-BLOCOS-001,
    CTO-HIER-001, CTO-DOC-001, CTO-EV-LOGO-001, CTO-EV-LINK-001,
    CTO-EV-TERCEIROS-001, CTO-EQUIPE-001, CTO-PARC-001, CTO-REV-001). Total: 25
    regras. O modelo `Evidencia` ganhou os campos `forma` (link/print),
    `eh_de_terceiros`, `mostra_pratica_esportiva`, `link_testado`, `bloco_cto`.
  - **Impacto nas fases:** a Coleta (Fase 2) de notícias/reportagens/posts passa a
    classificar cada achado por bloco e a marcar link/print, de-terceiros, prática
    esportiva e logomarca; a Curadoria (Fase 3) testa link e descarta foto sem
    logomarca; a trilha CTO (Fase 4) organiza as evidências nos 4 blocos e exporta
    na ordem de montagem, com painel de completude por bloco (14/8/8/7).
  - **Protótipo de coleta (a pedido da Karine):** criados `app/coleta/noticias.py`
    (Google Notícias via httpx+feedparser — httpx para passar pelo proxy),
    `app/coleta/instagram.py` (instaloader, sem login, degrada com aviso se
    bloquear), `app/coleta/classificar.py` (converte em evidências do Bloco 1 com
    força probatória) e `scripts/prototipo_coleta.py` (roda para 1 OSC e gera
    relatório HTML). Testes `tests/test_coleta.py` sem rede. Total: 24 testes.
  - **REDE liberada (2026-10-04):** após a Karine abrir o Network access, o
    news.google.com passou a responder 200 e a coleta de notícias RODA aqui.
    PORÉM: (a) o Instagram responde **429 Too Many Requests** — é o Instagram
    bloqueando o IP de datacenter desta nuvem, NÃO a config de rede; não dá para
    coletar posts/fotos do Instagram daqui de forma confiável, e o projeto proíbe
    burlar; a coleta de Instagram é confiável na máquina da Karine (IP
    residencial). (b) O site guerreirasemacao.com.br devolve 403 ao robô.
    (c) Mesmo com rede boa, a busca de imprensa para a Guerreiras em Ação trouxe
    quase nada (1 item não confirmado). Conclusão: a montagem AUTOMÁTICA com fotos
    do Instagram só acontece na máquina da Karine; daqui dá para automatizar
    notícias + site (quando o site permitir) + o esqueleto da CTO.
  - **gerar_cto.py (base da Fase 4):** `app/documentos/gerar_cto.py` monta o .docx
    na estrutura do Checklist (4 blocos, ordem, rastreabilidade EV-####), com
    [PREENCHER] só no que faltar. Não inventa foto/documento. Tem timbrado
    (`_timbrado`) e galeria de fotos (`_galeria_fotos`) com zoom+seta
    (`app/documentos/realce_logo.py`, Pillow).
  - **Sistema no ar (2026-10-04):** telas Streamlit do fluxo da CTO prontas
    (`1_Cadastro_OSC`, `2_Coleta`, `3_Curadoria`, `5_CTO`; stubs 4/6/7/8).
    Repositório com CRUD (`salvar_osc`, `salvar_evidencias`, `listar_evidencias`,
    `atualizar_evidencia`). Fluxo validado ponta a ponta (cadastro→notícias→
    curadoria→CTO). **Atalho 1 clique Windows:** `EsteiraLIE_Windows.bat`
    (instala na 1ª vez e abre); guia em `GUIA_WINDOWS.md`.
  - **Instagram exige login (2026):** a leitura anônima foi desativada pelo
    Instagram (falha mesmo em IP residencial). Soluções no sistema:
    (1) **sessão do navegador** via `browser_cookie3` (Chrome/Edge/Firefox/Brave)
    — a Karine fica logada no navegador e o sistema usa os cookies, sem senha
    (`_carregar_sessao_navegador` + `test_login`); é a opção recomendada e
    escolhida pela Karine. (2) login usuário/senha opcional. Coleta aceita link
    completo ou @ (`_normalizar_handle`). Para a nuvem (futuro), a opção seria uma
    API paga de terceiros (HikerAPI), que não precisa da senha e roda em datacenter.
  - **Ajustes SQLModel 0.0.47:** datetime precisa de fuso → `_agora()` grava em
    UTC; `Evidencia.data_do_fato` virou texto ISO (evita conflito de tipo date no
    SQLite). OSC ganhou `telefone`, `email`, `logo_path`; Evidencia ganhou
    `realce_bbox_json`.

## 10. Convenções de código

- Código comentado em **português**, funções pequenas.
- Nenhuma credencial em código ou log.
- `.gitignore` cobre `.env`, `dados/osc/`, `*.db`, `.venv`.
- Tratar erros de rede/coleta sem derrubar a aplicação.
