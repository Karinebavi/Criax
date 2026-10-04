"""Geração do documento Word (.docx) da CTO.

Monta a CTO na estrutura do Checklist CTO v3 (ver templates/ESTRUTURA_CTO.md):
4 blocos, na ordem de montagem (evidências esportivas antes dos termos), com
rastreabilidade por código de evidência (EV-####) e marcadores
`[PREENCHER: ...]` em tudo que falta — NUNCA inventando foto, documento ou dado.

Esta é a base da trilha CTO (Fase 4). Gera o Word programaticamente com
python-docx; mais adiante pode usar um template docxtpl que a Karine substitua.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.text import WD_COLOR_INDEX
from docx.shared import Inches, Pt, RGBColor

TEAL = RGBColor(0x0F, 0x76, 0x6E)
CINZA = RGBColor(0x5B, 0x6A, 0x68)


def _timbrado(doc, osc: dict) -> None:
    """Monta o timbrado (cabeçalho institucional) no topo do documento.

    Usa a logo (osc['logo_path']) quando houver; senão, deixa marcador. Abaixo,
    nome em destaque e uma linha com CNPJ · endereço · contato.
    """
    logo = osc.get("logo_path")
    topo = doc.add_paragraph()
    topo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if logo:
        try:
            topo.add_run().add_picture(str(logo), width=Inches(1.4))
        except Exception:
            _preencher(topo, "inserir a logomarca da instituição (arquivo de imagem)")
    else:
        _preencher(topo, "inserir a logomarca da instituição (arquivo de imagem)")

    nome = doc.add_paragraph()
    nome.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rn = nome.add_run((osc.get("nome") or "").upper())
    rn.bold = True
    rn.font.size = Pt(15)
    rn.font.color.rgb = TEAL

    partes = []
    if osc.get("cnpj"):
        partes.append(f"CNPJ {osc['cnpj']}")
    if osc.get("endereco"):
        partes.append(osc["endereco"])
    contato = " · ".join(filter(None, [osc.get("telefone"), osc.get("email"), osc.get("site")]))
    if contato:
        partes.append(contato)
    if partes:
        linha = doc.add_paragraph()
        linha.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = linha.add_run("  |  ".join(partes))
        r.font.size = Pt(9)
        r.font.color.rgb = CINZA

    # Linha divisória (regra horizontal simples).
    regua = doc.add_paragraph()
    regua.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rr = regua.add_run("_" * 60)
    rr.font.color.rgb = TEAL


def _preencher(paragrafo, texto: str) -> None:
    """Insere um marcador [PREENCHER: ...] destacado em amarelo."""
    run = paragrafo.add_run(f"[PREENCHER: {texto}]")
    run.bold = True
    run.font.highlight_color = WD_COLOR_INDEX.YELLOW


def _titulo(doc, texto: str, nivel: int = 1) -> None:
    p = doc.add_heading(texto, level=nivel)
    for run in p.runs:
        run.font.color.rgb = TEAL


def _legenda(doc, texto: str) -> None:
    p = doc.add_paragraph()
    run = p.add_run(texto)
    run.italic = True
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x5B, 0x6A, 0x68)


def _tabela_evidencias(doc, titulo_colunas: list[str], linhas: list[list[str]]) -> None:
    tabela = doc.add_table(rows=1, cols=len(titulo_colunas))
    tabela.style = "Light Grid Accent 1"
    for i, titulo in enumerate(titulo_colunas):
        cel = tabela.rows[0].cells[i]
        cel.text = titulo
        for p in cel.paragraphs:
            for run in p.runs:
                run.bold = True
    for linha in linhas:
        cels = tabela.add_row().cells
        for i, valor in enumerate(linha):
            cels[i].text = str(valor or "")


def _galeria_fotos(doc, fotos: list[dict], por_pagina: int = 4) -> None:
    """Insere a galeria de fotos (2 colunas), com legenda e zoom+seta na logo.

    Cada foto com `realce_bbox` (x,y,w,h) recebe o recorte ampliado da logomarca.
    """
    import tempfile

    from app.documentos.realce_logo import realcar_logo

    tabela = doc.add_table(rows=0, cols=2)
    for i in range(0, len(fotos), 2):
        linha = tabela.add_row().cells
        for j, foto in enumerate(fotos[i : i + 2]):
            caminho = foto.get("caminho_arquivo")
            bbox = foto.get("realce_bbox")
            if bbox:
                try:
                    tmp = Path(tempfile.gettempdir()) / f"realce_{foto.get('codigo','x')}.png"
                    caminho = str(realcar_logo(caminho, tuple(bbox), tmp))
                except Exception:
                    pass
            cel = linha[j]
            par = cel.paragraphs[0]
            par.alignment = WD_ALIGN_PARAGRAPH.CENTER
            try:
                par.add_run().add_picture(str(caminho), width=Inches(2.7))
            except Exception:
                _preencher(par, "não foi possível inserir a foto; conferir o arquivo")
            leg = cel.add_paragraph()
            leg.alignment = WD_ALIGN_PARAGRAPH.CENTER
            data = foto.get("data_do_fato") or "sem data"
            origem = foto.get("origem") or ""
            rleg = leg.add_run(f"{foto.get('codigo','')} · {data} · {origem}")
            rleg.italic = True
            rleg.font.size = Pt(8)
            rleg.font.color.rgb = CINZA


def gerar_cto(
    osc: dict,
    evidencias: list[dict],
    equipe: Optional[list[dict]] = None,
    parcerias: Optional[list[dict]] = None,
    caminho_saida: Optional[Path] = None,
) -> Path:
    """Gera o .docx da CTO e devolve o caminho do arquivo.

    - osc: dados da entidade (nome, cnpj, endereco, dirigente, site, instagram...).
    - evidencias: lista de dicts já classificados (tipo, origem, url_origem, data,
      legenda, eh_de_terceiros, bloco_cto, codigo).
    - equipe / parcerias: listas opcionais; quando vazias, geram [PREENCHER].
    """
    equipe = equipe or []
    parcerias = parcerias or []
    doc = Document()

    # ----------------------------------------------------------- CABEÇALHO
    _timbrado(doc, osc)  # timbrado da instituição no topo
    titulo = doc.add_heading("COMPROVAÇÃO DE CAPACIDADE TÉCNICO-OPERATIVA (CTO)", level=0)
    for run in titulo.runs:
        run.font.color.rgb = TEAL
    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rsub = sub.add_run(osc.get("nome", "") or "")
    rsub.bold = True
    rsub.font.size = Pt(13)

    # ---------------------------------------------------- IDENTIFICAÇÃO
    _titulo(doc, "Identificação da entidade", 1)
    ident = [
        ("Entidade", osc.get("nome")),
        ("CNPJ", osc.get("cnpj")),
        ("Endereço", osc.get("endereco")),
        ("Município/UF", osc.get("municipio_uf")),
        ("Dirigente", osc.get("dirigente")),
        ("Site", osc.get("site")),
        ("Instagram", osc.get("instagram")),
        ("Facebook", osc.get("facebook")),
    ]
    for rotulo, valor in ident:
        p = doc.add_paragraph()
        p.add_run(f"{rotulo}: ").bold = True
        if valor:
            p.add_run(str(valor))
        else:
            _preencher(p, f"informar {rotulo.lower()}")

    # agrupa evidências por bloco
    def do_bloco(n: str) -> list[dict]:
        return [e for e in evidencias if str(e.get("bloco_cto")) == n]

    reportagens = [e for e in do_bloco("1") if e.get("tipo") == "reportagem"]
    posts = [e for e in do_bloco("1") if e.get("tipo") == "post"]
    sites = [e for e in do_bloco("1") if e.get("tipo") in ("site", "registro")]

    # ---------------------------------------------- BLOCO 1 (ordem: evidências)
    _titulo(doc, "Bloco 1 — Relatório de Eventos e Evidências", 1)

    _titulo(doc, "1.1 Fotos de atividades esportivas (datadas, com logomarca)", 2)
    _legenda(doc, "Regra CTO-EV-LOGO-001: foto sem logomarca é descartada. 2 a 4 por página, legenda com data e origem.")
    fotos = [e for e in do_bloco("1") if e.get("caminho_arquivo")]
    if fotos:
        _galeria_fotos(doc, fotos)
    else:
        p = doc.add_paragraph()
        _preencher(p, "inserir fotos datadas de atividades ESPORTIVAS com a logomarca da entidade visível (coletadas do Instagram ou do acervo da entidade)")

    _titulo(doc, "1.2 Reportagens de imprensa (de terceiros)", 2)
    _legenda(doc, "Regra CTO-EV-TERCEIROS-001: matérias de veículos independentes citando a entidade. Link preferível ao print.")
    if reportagens:
        _tabela_evidencias(
            doc,
            ["EV", "Veículo", "Data", "Título", "Link"],
            [[e.get("codigo", ""), e.get("veiculo", ""), e.get("data_do_fato", ""),
              e.get("legenda", ""), e.get("url_origem", "")] for e in reportagens],
        )
    else:
        p = doc.add_paragraph()
        _preencher(p, "nenhuma reportagem de imprensa localizada na busca — pautar veículos locais (release) e inserir aqui veículo, data, título e link")

    _titulo(doc, "1.3 Publicações em redes sociais (com link e data)", 2)
    if posts:
        _tabela_evidencias(
            doc,
            ["EV", "Rede", "Data", "Descrição", "Link"],
            [[e.get("codigo", ""), e.get("origem", ""), e.get("data_do_fato", ""),
              (e.get("legenda", "") or "")[:120], e.get("url_origem", "")] for e in posts],
        )
    else:
        p = doc.add_paragraph()
        _preencher(p, "selecionar posts de atividades esportivas com logomarca (link e data visíveis)")

    _titulo(doc, "1.4 Súmulas, certificados de federação, DOU, ofícios e atestados de terceiros", 2)
    _legenda(doc, "Evidências emitidas por terceiros têm peso elevado (CTO-EV-TERCEIROS-001). Atestado nunca pode ser autodeclaração.")
    p = doc.add_paragraph()
    _preencher(p, "anexar súmulas/certificados de federações, publicações no DOU, ofícios de órgãos públicos e atestados de capacidade técnica de terceiros, se houver")

    _titulo(doc, "1.5 Site e redes institucionais", 2)
    if sites:
        _tabela_evidencias(
            doc,
            ["EV", "Tipo", "Link"],
            [[e.get("codigo", ""), e.get("tipo", ""), e.get("url_origem", "")] for e in sites],
        )
    else:
        p = doc.add_paragraph()
        _preencher(p, "informar site e redes da entidade")

    # ---------------------------------------------- BLOCO 2 (equipe)
    _titulo(doc, "Bloco 2 — Capacidade Técnica Instalada / Equipe e Notório Saber", 1)
    _legenda(doc, "Regra CTO-EQUIPE-001: currículo direcionado + RG/CNH + Declaração de Ciência assinada PELO PROFISSIONAL + notório saber esportivo.")
    if equipe:
        _tabela_evidencias(
            doc,
            ["Nome", "Função", "Formação", "Registro (CREF)", "Vínculo"],
            [[p.get("nome", ""), p.get("funcao", ""), p.get("formacao", ""),
              p.get("registro", ""), p.get("vinculo", "")] for p in equipe],
        )
    else:
        p = doc.add_paragraph()
        _preencher(p, "listar os profissionais com currículo direcionado à modalidade, RG/CNH, Declaração de Ciência assinada pelo profissional e documento de notório saber")

    # ---------------------------------------------- BLOCO 3 (parcerias)
    _titulo(doc, "Bloco 3 — Termos de Parceria e Cooperação", 1)
    _legenda(doc, "Regra CTO-PARC-001: termo assinado por ambas as partes, com RG/CPF dos assinantes, objeto esportivo explícito e parceiro regular.")
    if parcerias:
        _tabela_evidencias(
            doc,
            ["Parceiro", "Tipo", "Objeto (esportivo)", "Vigência"],
            [[p.get("parceiro", ""), p.get("tipo", ""), p.get("objeto", ""),
              p.get("vigencia", "")] for p in parcerias],
        )
    else:
        p = doc.add_paragraph()
        _preencher(p, "anexar termos de parceria/cooperação e cessão de uso de espaço esportivo (prefeitura de Nova Era, APAE, federação), com objeto esportivo e documentação regular do parceiro")

    # ---------------------------------------------- BLOCO 4 (conferência)
    _titulo(doc, "Bloco 4 — Conferência Final, Ordem e Revisão", 1)
    for item in [
        "Comprovações esportivas vêm ANTES dos termos de parceria.",
        "Todos os links testados e funcionando na data de envio.",
        "Documentos legíveis, sem cortes, em boa resolução.",
        "Nenhum documento repetido ou duplicado.",
        "NÃO há autodeclaração como único documento de comprovação.",
        "CTO revisada por outro mentor ou pela coordenação antes do envio.",
        "Montagem seguindo a hierarquia de evidências (fotos/reportagens → parcerias → currículos).",
    ]:
        doc.add_paragraph(item, style="List Bullet")

    # ---------------------------------------------- RASTREABILIDADE
    _titulo(doc, "Relatório de rastreabilidade", 1)
    _legenda(doc, "Evidências usadas nesta CTO, com código, origem e link (regra inegociável de rastreabilidade).")
    if evidencias:
        _tabela_evidencias(
            doc,
            ["EV", "Tipo", "Origem", "De terceiros?", "Data", "Link"],
            [[e.get("codigo", ""), e.get("tipo", ""), e.get("origem", ""),
              e.get("eh_de_terceiros", ""), e.get("data_do_fato", ""),
              e.get("url_origem", "")] for e in evidencias],
        )
    else:
        doc.add_paragraph("Nenhuma evidência registrada ainda.")

    caminho_saida = Path(caminho_saida or "CTO.docx")
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(caminho_saida))
    return caminho_saida
