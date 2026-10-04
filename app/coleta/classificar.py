"""Classificação das evidências coletadas na estrutura do Checklist CTO v3.

Converte os itens brutos (notícias, posts) em evidências já marcadas por bloco e
com os sinais que o checklist exige (link/print, de terceiros, etc.).
Ver templates/ESTRUTURA_CTO.md.
"""

from __future__ import annotations


def evidencia_de_noticia(item: dict) -> dict:
    """Reportagem de imprensa → evidência do Bloco 1 (forte: de terceiros, com link)."""
    titulo = item.get("titulo", "")
    veiculo = item.get("veiculo", "")
    legenda = f"{titulo} — {veiculo}".strip(" —")
    return {
        "tipo": "reportagem",
        "origem": "notícia",
        "url_origem": item.get("url", ""),
        "data_do_fato": item.get("data"),
        "legenda": legenda,
        "forma": "link",
        "eh_de_terceiros": "sim",  # imprensa independente: maior peso probatório
        "mostra_pratica_esportiva": "nao_verificado",
        "link_testado": "nao_verificado",
        "tem_logomarca": "nao_verificado",
        "bloco_cto": "1",
        "status": "pendente",
    }


def evidencia_de_post_instagram(item: dict) -> dict:
    """Post público do Instagram → evidência do Bloco 1 (autoproduzido, com link)."""
    return {
        "tipo": "post",
        "origem": "instagram",
        "url_origem": item.get("url", ""),
        "data_do_fato": item.get("data"),
        "legenda": item.get("legenda", ""),
        "forma": "link",
        "eh_de_terceiros": "nao",  # conteúdo da própria entidade: peso menor
        "mostra_pratica_esportiva": "nao_verificado",
        "link_testado": "nao_verificado",
        "tem_logomarca": "nao_verificado",
        "bloco_cto": "1",
        "status": "pendente",
        "caminho_arquivo": item.get("caminho_arquivo"),
    }


def forca_da_evidencia(evidencia: dict) -> int:
    """Pontua a força probatória para ordenar (maior = mais forte), por CTO-HIER-001.

    Reportagem de terceiros > post próprio. Usado para sugerir a ordem de montagem.
    """
    pontos = 0
    if evidencia.get("bloco_cto") == "1":
        pontos += 10  # evidências visuais/midiáticas vêm primeiro
    if evidencia.get("eh_de_terceiros") == "sim":
        pontos += 5
    if evidencia.get("forma") == "link":
        pontos += 2
    if evidencia.get("tem_logomarca") == "sim":
        pontos += 3
    return pontos
