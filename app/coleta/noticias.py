"""Coleta de notícias/reportagens via RSS do Google Notícias.

Busca pelo nome da entidade (e variações) e devolve título, veículo, data e link.
No documento final usamos só título, veículo, data e link — nunca reproduzimos o
texto da matéria (apenas guardamos para análise interna, se preciso).

Importante: a requisição passa pelo httpx (que respeita o proxy do ambiente).
O feedparser sozinho não usa o proxy, então baixamos os bytes com httpx e só
depois entregamos ao feedparser.
"""

from __future__ import annotations

import datetime as dt
import urllib.parse
from dataclasses import dataclass, field
from typing import Optional

import feedparser
import httpx

BASE_RSS = "https://news.google.com/rss/search"


@dataclass
class ResultadoColeta:
    """Resultado de uma coleta: ok/erro + itens encontrados."""

    ok: bool
    itens: list[dict] = field(default_factory=list)
    erro: Optional[str] = None
    mensagem: Optional[str] = None


def montar_consulta(variacoes: list[str], cidade: str | None = None) -> str:
    """Monta a query do Google Notícias a partir das variações do nome + cidade.

    Cada variação vira uma frase exata ("..."), unidas por OR; a cidade restringe.
    """
    variacoes = [v.strip() for v in variacoes if v and v.strip()]
    frase = " OR ".join(f'"{v}"' for v in variacoes)
    if cidade:
        frase = f"({frase}) {cidade}"
    return frase


def buscar_noticias(
    variacoes: list[str],
    cidade: str | None = None,
    max_resultados: int = 30,
    timeout: int = 20,
) -> ResultadoColeta:
    """Busca reportagens pelo nome da entidade.

    Devolve ResultadoColeta. Nunca levanta exceção de rede — erros viram
    mensagem em português para a tela.
    """
    consulta = montar_consulta(variacoes, cidade)
    url = (
        f"{BASE_RSS}?q={urllib.parse.quote(consulta)}"
        "&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    )
    try:
        resposta = httpx.get(
            url,
            timeout=timeout,
            follow_redirects=True,
            trust_env=True,
            headers={"User-Agent": "Mozilla/5.0 (EsteiraLIE)"},
        )
    except Exception as erro:  # rede indisponível/bloqueada
        return ResultadoColeta(
            ok=False,
            erro=str(erro),
            mensagem=(
                "Não foi possível acessar o Google Notícias (rede bloqueada ou "
                "indisponível). Verifique a conexão ou libere o domínio "
                "news.google.com no ambiente. Você também pode colar os links "
                "das reportagens manualmente."
            ),
        )

    if resposta.status_code != 200:
        return ResultadoColeta(
            ok=False,
            erro=f"HTTP {resposta.status_code}",
            mensagem=(
                f"O Google Notícias respondeu com erro HTTP {resposta.status_code}. "
                "Tente novamente mais tarde ou cole os links manualmente."
            ),
        )

    return ResultadoColeta(ok=True, itens=parsear_rss(resposta.content, max_resultados))


def parsear_rss(conteudo: bytes, max_resultados: int = 30) -> list[dict]:
    """Converte o RSS do Google Notícias em uma lista de dicionários.

    Separado da rede para poder ser testado com um RSS de exemplo (sem internet).
    """
    feed = feedparser.parse(conteudo)
    itens: list[dict] = []
    for entrada in feed.entries[:max_resultados]:
        titulo = getattr(entrada, "title", "") or ""
        veiculo = _extrair_veiculo(entrada, titulo)
        itens.append(
            {
                "titulo": _limpar_titulo(titulo, veiculo),
                "veiculo": veiculo,
                "data": _extrair_data(entrada),
                "url": getattr(entrada, "link", "") or "",
            }
        )
    return itens


def _extrair_veiculo(entrada, titulo: str) -> str:
    """Pega o veículo da matéria (campo source do Google Notícias)."""
    fonte = getattr(entrada, "source", None)
    if fonte is not None:
        titulo_fonte = getattr(fonte, "title", None)
        if titulo_fonte:
            return titulo_fonte
        if isinstance(fonte, dict) and fonte.get("title"):
            return fonte["title"]
    # Fallback: o Google costuma colocar " - Veículo" no fim do título.
    if " - " in titulo:
        return titulo.rsplit(" - ", 1)[-1].strip()
    return ""


def _limpar_titulo(titulo: str, veiculo: str) -> str:
    """Remove o sufixo ' - Veículo' do título quando presente."""
    if veiculo and titulo.endswith(f" - {veiculo}"):
        return titulo[: -(len(veiculo) + 3)].strip()
    return titulo.strip()


def _extrair_data(entrada) -> Optional[str]:
    """Devolve a data de publicação no formato ISO (YYYY-MM-DD), se houver."""
    estrutura = getattr(entrada, "published_parsed", None)
    if estrutura:
        return dt.date(estrutura.tm_year, estrutura.tm_mon, estrutura.tm_mday).isoformat()
    return None
