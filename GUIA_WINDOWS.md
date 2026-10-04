# Guia rápido — Esteira LIE no Windows

Feito para não-programador. Siga na ordem.

## 1. Baixar o sistema
- Entre em: https://github.com/Karinebavi/Criax/tree/claude/blissful-wright-bk40r8
- Botão verde **Code** → **Download ZIP**.
- Clique com o botão direito no ZIP baixado → **Extrair tudo** → escolha uma pasta
  fácil (ex.: `Documentos\EsteiraLIE`).

## 2. Ter o Python (uma vez só)
- Baixe em https://www.python.org/downloads/ e instale.
- **IMPORTANTE:** na primeira tela da instalação, marque a caixa
  **"Add Python to PATH"**. Depois clique em Install.

## 3. Abrir o sistema
- Entre na pasta que você extraiu.
- Dê **dois cliques** em **`EsteiraLIE_Windows.bat`**.
  - Na **primeira vez** ele instala tudo sozinho (demora alguns minutos; aparece
    uma janela preta escrevendo coisas — é normal, não feche).
  - Quando terminar, o **navegador abre sozinho** na tela do Esteira LIE.
- Se o Windows mostrar um aviso azul ("Windows protegeu o computador"), clique em
  **Mais informações** → **Executar assim mesmo** (o arquivo é só um atalho local).

## 4. Usar (fluxo da CTO)
No menu à esquerda, siga a ordem:
1. **Cadastro da OSC** — preencha os dados da entidade e clique em Salvar.
2. **Coleta** — clique em *Buscar reportagens* e em *Coletar Instagram*
   (no seu computador o Instagram funciona normalmente).
3. **Curadoria** — para cada evidência: marque se tem logomarca e prática
   esportiva, e **Aprovar** ou **Descartar**. Em foto com logo pequena, marque
   "aplicar zoom+seta".
4. **CTO** — clique em *Gerar CTO em Word* e depois em *Baixar CTO (.docx)*.

## 5. Fechar
- Feche a **janela preta** (o terminal). Pronto.

## Dúvidas comuns
- **"Python não encontrado"**: refaça o passo 2 marcando "Add Python to PATH".
- **O navegador não abriu**: na janela preta aparece um endereço `http://localhost:8501`
  — copie e cole no navegador.
- **Quero recomeçar do zero**: feche tudo e apague o arquivo `esteira_lie.db` da
  pasta. Ele é recriado vazio.
