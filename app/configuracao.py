"""Leitura do config.yaml e resolução de caminhos do projeto.

Mantém tudo relativo à raiz do projeto, para funcionar igual no Windows, Mac e
Linux, independentemente de onde o Streamlit for iniciado.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

# Raiz do projeto = pasta que contém este arquivo subindo dois níveis
# (app/configuracao.py -> app -> raiz).
RAIZ = Path(__file__).resolve().parent.parent


@lru_cache(maxsize=1)
def carregar_config() -> dict[str, Any]:
    """Lê o config.yaml uma única vez e devolve como dicionário."""
    caminho = RAIZ / "config.yaml"
    if not caminho.exists():
        raise FileNotFoundError(
            f"Arquivo de configuração não encontrado: {caminho}. "
            "Confira se o config.yaml está na raiz do projeto."
        )
    with caminho.open("r", encoding="utf-8") as arquivo:
        return yaml.safe_load(arquivo) or {}


def caminho_de(chave: str) -> Path:
    """Devolve um caminho absoluto a partir da seção 'caminhos' do config.

    Exemplo: caminho_de("banco") -> <raiz>/esteira_lie.db
    """
    config = carregar_config()
    caminhos = config.get("caminhos", {})
    if chave not in caminhos:
        raise KeyError(f"Caminho '{chave}' não está definido em config.yaml > caminhos.")
    return (RAIZ / caminhos[chave]).resolve()
