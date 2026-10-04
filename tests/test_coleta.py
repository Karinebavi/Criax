"""Testes da coleta: parsing de RSS e classificação na estrutura CTO.

NÃO acessam a internet — usam um RSS de exemplo embutido.
"""

from __future__ import annotations

import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[1]
if str(_RAIZ) not in sys.path:
    sys.path.insert(0, str(_RAIZ))

from app.coleta.classificar import (  # noqa: E402
    evidencia_de_noticia,
    evidencia_de_post_instagram,
    forca_da_evidencia,
)
from app.coleta.noticias import montar_consulta, parsear_rss  # noqa: E402

RSS_EXEMPLO = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
<item>
  <title>Projeto esportivo forma 200 atletas - Jornal da Cidade</title>
  <link>https://exemplo.com/materia-1</link>
  <pubDate>Mon, 15 Jan 2024 10:00:00 GMT</pubDate>
  <source url="https://jornaldacidade.com">Jornal da Cidade</source>
</item>
<item>
  <title>Entidade recebe premio estadual - Portal Esporte</title>
  <link>https://exemplo.com/materia-2</link>
  <pubDate>Tue, 20 Feb 2024 12:00:00 GMT</pubDate>
  <source url="https://portalesporte.com">Portal Esporte</source>
</item>
</channel></rss>""".encode("utf-8")


def test_montar_consulta_une_variacoes_e_cidade():
    q = montar_consulta(["Instituto Exemplo", "IEE"], "São Paulo/SP")
    assert '"Instituto Exemplo"' in q
    assert '"IEE"' in q
    assert "OR" in q
    assert "São Paulo/SP" in q


def test_parsear_rss_extrai_titulo_veiculo_data_link():
    itens = parsear_rss(RSS_EXEMPLO)
    assert len(itens) == 2
    primeiro = itens[0]
    assert primeiro["veiculo"] == "Jornal da Cidade"
    # O sufixo " - Veículo" sai do título.
    assert primeiro["titulo"] == "Projeto esportivo forma 200 atletas"
    assert primeiro["data"] == "2024-01-15"
    assert primeiro["url"] == "https://exemplo.com/materia-1"


def test_parsear_rss_respeita_maximo():
    itens = parsear_rss(RSS_EXEMPLO, max_resultados=1)
    assert len(itens) == 1


def test_evidencia_de_noticia_vai_para_bloco1_como_terceiros_com_link():
    ev = evidencia_de_noticia(parsear_rss(RSS_EXEMPLO)[0])
    assert ev["bloco_cto"] == "1"
    assert ev["eh_de_terceiros"] == "sim"
    assert ev["forma"] == "link"
    assert ev["tipo"] == "reportagem"


def test_evidencia_de_post_instagram_eh_proprio():
    ev = evidencia_de_post_instagram(
        {"url": "https://instagram.com/p/x/", "data": "2024-03-01", "legenda": "treino"}
    )
    assert ev["bloco_cto"] == "1"
    assert ev["eh_de_terceiros"] == "nao"
    assert ev["origem"] == "instagram"


def test_hierarquia_reportagem_de_terceiros_mais_forte_que_post_proprio():
    reportagem = evidencia_de_noticia(parsear_rss(RSS_EXEMPLO)[0])
    post = evidencia_de_post_instagram({"url": "x", "data": "2024-01-01", "legenda": "y"})
    assert forca_da_evidencia(reportagem) > forca_da_evidencia(post)
