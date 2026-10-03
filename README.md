# Esteira LIE

Sistema local para montar, a partir da presença pública de uma OSC e do material
que você complementa à mão, os três entregáveis da Lei de Incentivo ao Esporte:

1. **CTO** — Comprovação de Capacidade Técnico-Operativa (Word)
2. **Escrita do projeto** (Word)
3. **Planilha orçamentária** (Excel)

Tudo roda **no seu computador**. Nada é enviado para fora: o sistema só gera
arquivos locais.

---

## Passo a passo para começar (linguagem simples)

Você vai usar dois comandos. Faça uma vez a instalação; depois, sempre que quiser
usar, use o comando de rodar.

### 1. Instalar (uma vez só)

**Windows:** dê dois cliques em `instalar.bat` (ou, no terminal, digite `instalar.bat`).

**Mac/Linux:** abra o Terminal na pasta do projeto e digite:

```
./instalar.sh
```

Esse passo cria um ambiente isolado (`.venv`) e baixa tudo que o sistema precisa.
Pode demorar alguns minutos na primeira vez. Se aparecer erro, ele vem em
português explicando o que fazer.

### 2. Colocar sua chave da IA (uma vez só)

1. Faça uma cópia do arquivo `.env.example` e renomeie a cópia para `.env`.
2. Abra o `.env` e cole sua chave da Anthropic no lugar indicado:

   ```
   ANTHROPIC_API_KEY=sua_chave_aqui
   ```

O arquivo `.env` **nunca** é compartilhado nem versionado. Nesta Fase 0 o sistema
ainda **não** usa a chave — ela só será necessária nas fases de diagnóstico e
geração de texto.

### 3. Rodar

**Windows:** dê dois cliques em `rodar.bat`.

**Mac/Linux:** no Terminal, digite:

```
./rodar.sh
```

O navegador abre sozinho numa página chamada **Esteira LIE**. Se não abrir,
copie o endereço que aparecer no terminal (algo como `http://localhost:8501`) e
cole no navegador.

Para **fechar**, volte ao terminal e aperte `Ctrl + C`.

---

## O que já dá para ver nesta Fase 0

- A tela inicial (**Home**) com a lista de OSCs (ainda vazia) e o status de cada uma.
- A página **Regras**, mostrando todas as regras da LIE que já cadastramos, com o
  status de cada uma. Todas começam como **pendente**, porque precisam da sua
  validação (a norma mudou e ainda vamos conferir na Portaria MESP nº 10/2026).
  Você pode marcar uma regra como **validada** com um clique.

As demais telas (Cadastro, Coleta, Curadoria, Diagnóstico, CTO, Projeto,
Orçamento, Conferência) chegam nas próximas fases.

---

## Onde ficam seus arquivos

- **Normas (PDFs):** coloque em `normas/fontes/`.
- **Base de regras:** `normas/regras.yaml` (texto estruturado das regras).
- **Catálogo de itens e preços:** `dados/catalogo_itens.xlsx` (criado na Fase 6).
- **Modelos Word:** `templates/` (criados nas Fases 4 e 5; você pode trocar pelos seus).
- **Mídia e saídas de cada OSC:** `dados/osc/<cnpj>/`.

---

## Problemas comuns

- **"Python não encontrado":** instale o Python 3.11 ou superior em
  <https://www.python.org/downloads/> e tente de novo.
- **O navegador não abriu:** copie o endereço do terminal e cole no navegador.
- **Quero recomeçar o banco do zero:** feche o sistema e apague o arquivo
  `esteira_lie.db`. Ele é recriado vazio na próxima vez que você rodar.
