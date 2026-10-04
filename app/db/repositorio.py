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


# =============================== OSC =======================================

def salvar_osc(dados: dict):
    """Cria uma OSC a partir de um dicionário de campos e devolve o objeto salvo."""
    from app.db.modelos import OSC

    criar_banco()
    with abrir_sessao() as sessao:
        osc = OSC(**{k: v for k, v in dados.items() if v is not None})
        sessao.add(osc)
        sessao.commit()
        sessao.refresh(osc)
        return osc


def listar_oscs() -> list:
    """Lista todas as OSCs cadastradas (mais recentes primeiro)."""
    from sqlmodel import select

    from app.db.modelos import OSC

    criar_banco()
    with abrir_sessao() as sessao:
        return list(sessao.exec(select(OSC).order_by(OSC.id.desc())).all())


def obter_osc(osc_id: int):
    from app.db.modelos import OSC

    with abrir_sessao() as sessao:
        return sessao.get(OSC, osc_id)


# ============================= EVIDÊNCIAS ===================================

def salvar_evidencias(osc_id: int, itens: list[dict]) -> int:
    """Salva uma lista de evidências (dicts) para a OSC, gerando o código EV-####.

    Devolve quantas foram salvas. Evita duplicar pela url_origem.
    """
    from sqlmodel import select

    from app.db.modelos import Evidencia

    criar_banco()
    salvas = 0
    with abrir_sessao() as sessao:
        existentes = {
            e.url_origem
            for e in sessao.exec(
                select(Evidencia).where(Evidencia.osc_id == osc_id)
            ).all()
            if e.url_origem
        }
        for item in itens:
            if item.get("url_origem") and item["url_origem"] in existentes:
                continue
            campos = {k: v for k, v in item.items() if hasattr(Evidencia, k)}
            campos["osc_id"] = osc_id
            ev = Evidencia(**campos)
            sessao.add(ev)
            sessao.commit()
            sessao.refresh(ev)
            ev.codigo = f"EV-{ev.id:04d}"  # código derivado do id
            sessao.add(ev)
            sessao.commit()
            salvas += 1
    return salvas


def listar_evidencias(osc_id: int, status: str | None = None) -> list:
    """Lista evidências da OSC, opcionalmente filtrando por status."""
    from sqlmodel import select

    from app.db.modelos import Evidencia

    criar_banco()
    with abrir_sessao() as sessao:
        consulta = select(Evidencia).where(Evidencia.osc_id == osc_id)
        if status:
            consulta = consulta.where(Evidencia.status == status)
        return list(sessao.exec(consulta.order_by(Evidencia.id)).all())


def atualizar_evidencia(ev_id: int, **campos) -> None:
    """Atualiza campos de uma evidência (ex.: status, tem_logomarca)."""
    from app.db.modelos import Evidencia

    with abrir_sessao() as sessao:
        ev = sessao.get(Evidencia, ev_id)
        if ev is None:
            return
        for chave, valor in campos.items():
            if hasattr(ev, chave):
                setattr(ev, chave, valor)
        sessao.add(ev)
        sessao.commit()
