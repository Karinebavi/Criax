"""Acesso ao banco: criação do engine, criação das tabelas e utilitários.

O banco é um arquivo SQLite (caminho vem do config.yaml). As tabelas são criadas
automaticamente na primeira execução.
"""

from __future__ import annotations

import json
from typing import Iterable

from sqlmodel import Session, SQLModel, create_engine

from app.configuracao import caminho_de

# Importa os modelos para que o SQLModel registre todas as tabelas.
from app.db import modelos  # noqa: F401

_engine = None


def obter_engine():
    """Devolve (criando na primeira vez) o engine do SQLite."""
    global _engine
    if _engine is None:
        caminho_banco = caminho_de("banco")
        # check_same_thread=False porque o Streamlit usa múltiplas threads.
        _engine = create_engine(
            f"sqlite:///{caminho_banco}",
            echo=False,
            connect_args={"check_same_thread": False},
        )
    return _engine


def criar_banco() -> None:
    """Cria o arquivo do banco e todas as tabelas, se ainda não existirem."""
    engine = obter_engine()
    SQLModel.metadata.create_all(engine)


def abrir_sessao() -> Session:
    """Abre uma sessão de banco. Use com `with abrir_sessao() as sessao:`."""
    return Session(obter_engine())


# --------------------------- utilitários de lista ---------------------------

def ler_lista(valor_json: str | None) -> list:
    """Converte uma coluna JSON texto em lista Python (vazia se nula/ inválida)."""
    if not valor_json:
        return []
    try:
        dados = json.loads(valor_json)
        return dados if isinstance(dados, list) else []
    except (ValueError, TypeError):
        return []


def guardar_lista(itens: Iterable) -> str:
    """Converte uma lista Python em JSON texto para guardar numa coluna."""
    return json.dumps(list(itens), ensure_ascii=False)
