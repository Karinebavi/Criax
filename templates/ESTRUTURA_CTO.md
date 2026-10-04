# Estrutura da CTO — Comprovação de Capacidade Técnico-Operativa

Método extraído do **Checklist CTO v3** enviado pela Karine
(`templates/referencia_cto/Checklist_CTO_v3.xlsx`). É a estrutura oficial que a
trilha CTO (Fase 4) e a coleta (Fase 2) seguem. **A coleta de notícias,
reportagens, posts e publicações existe para alimentar o Bloco 1.**

> As regras de descarte e a hierarquia abaixo viraram regras `CTO-*` no
> `normas/regras.yaml` (status `pendente`). Fonte: Checklist CTO v3 (equipe CASE)
> + Manual do Proponente LIE 2023, a confirmar na Portaria MESP nº 10/2026.

## Princípios inegociáveis da CTO (lembretes do painel)

1. **Hierarquia:** Fotos/Reportagens/Publicações → Parcerias → Currículos
   (currículo é o **último recurso**). Não deixar a entidade pular direto para o
   currículo sem tentar as evidências mais fortes.
2. **Comprovações esportivas ANTES dos termos de parceria** na montagem.
3. **LINK > PRINT.** Se for print, a **data de publicação** tem que estar visível.
4. **Foto sem logomarca/identidade visual da entidade é descartada** pelo técnico
   do MESP (falta nexo de autoria).
5. **Autodeclaração isolada NÃO é aceita** como prova de CTO.
6. Sem CTO adequada → projeto **diligenciado ou arquivado** pela CTLIE.

## Os 4 blocos (37 itens — itens com ★ são obrigatórios)

### Bloco 1 — Relatório de Eventos e Evidências (14 itens)
Fotos de atividades esportivas realizadas (★), com **logomarca visível** (★);
pelo menos 2 eventos em datas distintas; boa resolução; **reportagens de imprensa
citando a entidade** (★), de preferência de **terceiros**; **posts em redes com
link funcional** (★); **todos os links testados** (★); posts que mostrem a
entidade como organizadora; súmulas oficiais; certificados de federações/ligas;
publicações no DOU; ofícios de órgãos públicos; **atestados de capacidade técnica
emitidos por terceiros** (nunca autodeclaração).

### Bloco 2 — Capacidade Técnica Instalada / Equipe e Notório Saber (8 itens)
**Currículo direcionado** à função e ao projeto (★) — currículo genérico/Lattes é
rejeitado; currículo que evidencie a **modalidade** do projeto; **RG/CNH** de cada
profissional (★); **Declaração de Ciência e Responsabilidade assinada PELO
PROFISSIONAL** (★) — não pelo presidente; **Documento de Notório Saber** em modelo
validado (★); pelo menos **1 profissional com notório saber esportivo** (★); ata
da diretoria registrada com ações ligadas ao esporte; descrição das ações
esportivas da diretoria.

### Bloco 3 — Termos de Parceria e Cooperação (8 itens)
**Termo de parceria assinado por ambas as partes** (★) — carta de intenção/acordo
verbal não valem; **identificação dos assinantes (RG e CPF)** (★); **objeto do
termo claramente esportivo** (★); parceria com federação/confederação/liga;
parceria com prefeitura/secretaria; termo de cessão de uso de espaço (vigência
compatível com o projeto); parceria com clube/associação/escola/universidade;
**documentação regular da entidade parceira** (a irregularidade do parceiro
contamina a CTO).

### Bloco 4 — Conferência Final, Ordem e Revisão (7 itens)
**Evidências esportivas antes dos termos** (★); **links testados na data de
envio** (★); **documentos legíveis, sem cortes** (★); sem duplicatas; **nenhuma
autodeclaração como único documento** (★); **revisão cruzada** por outro
mentor/coordenação antes do envio (★); CTO montada seguindo a **hierarquia de
evidências** (★).

## Ordem recomendada de montagem (o técnico avalia na ordem em que aparece)

1. Fotos de eventos/atividades esportivas (com logomarca)
2. Reportagens de imprensa (com link)
3. Prints de redes sociais (com link e data)
4. Súmulas de campeonatos / certificados de federações
5. Publicações no DOU (se houver)
6. Atestados de Capacidade Técnica (de terceiros)
7. Ofícios de órgãos públicos / entidades esportivas
8. Currículos direcionados dos profissionais
9. RG/CNH dos profissionais
10. Declaração de Ciência e Responsabilidade
11. Documento de Notório Saber
12. Ata da diretoria + descrição de ações esportivas
13. Termos de Parceria
14. Termos de Cessão de Uso de espaço
15. Documentação da entidade parceira

Legenda de cores do checklist: laranja = evidências visuais/midiáticas (vêm
primeiro); verde = equipe técnica; roxo = parcerias (vêm por último).

## O que isso muda no sistema

- **Coleta (Fase 2):** busca de notícias/reportagens (por nome da entidade + cidade
  + variações) e de posts, classificando cada achado por **bloco**, marcando se é
  **link ou print**, se é **de terceiros** e se **mostra prática esportiva com
  logomarca**. Reportagem de terceiro com link funcional é a evidência mais forte.
- **Curadoria (Fase 3):** além de aprovar/descartar, marca logomarca, prática
  esportiva, origem (terceiros?) e testa o link. Foto sem logomarca → descartada.
- **CTO (Fase 4):** a tela organiza as evidências aprovadas nos 4 blocos e exporta
  o `.docx` **na ordem de montagem** acima, com rastreabilidade `[EV-####]`.
- **Modelo de dados:** a Evidência ganha os campos `forma` (link/print),
  `eh_de_terceiros`, `mostra_pratica_esportiva`, `link_testado` e `bloco_cto`.

## Painel de acompanhamento (resumo por bloco)

A planilha traz um painel com % de completude por bloco (14 / 8 / 8 / 7 itens) e
status geral. A tela da CTO vai reproduzir esse painel para a Karine acompanhar o
quanto cada bloco já está comprovado antes de gerar o documento.
