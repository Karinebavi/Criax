"""Carregamento e sincronização das regras.

O regras.yaml é a FONTE DA VERDADE do texto das regras. O banco só espelha o
status (pendente/validada/revogada) e a data de validação feita pela Karine.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from app.configuracao import caminho_de

CAMPOS_OBRIGATORIOS = {
    "id",
    "tema",
    "descricao",
    "tipo_checagem",
    "parametros",
    "fonte",
    "vigencia",
    "status",
}
TIPOS_CHECAGEM_VALIDOS = {
    "percentual_maximo",
    "min_max_itens",
    "obrigatorio",
    "texto_orientativo",
    "limite_caracteres",
}
STATUS_VALIDOS = {"pendente", "validada", "revogada"}


def carregar_regras(caminho: Path | None = None) -> list[dict[str, Any]]:
    """Lê o regras.yaml e devolve a lista de regras (dicionários).

    Valida que cada regra tem os campos obrigatórios e valores coerentes,
    levantando erro claro em português caso contrário.
    """
    caminho = caminho or caminho_de("regras")
    if not caminho.exists():
        raise FileNotFoundError(
            f"Arquivo de regras não encontrado: {caminho}. "
            "Confira se o normas/regras.yaml existe."
        )

    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = yaml.safe_load(arquivo) or []

    if not isinstance(dados, list):
        raise ValueError(
            "O regras.yaml deve conter uma LISTA de regras (cada item começando com '- id:')."
        )

    ids_vistos: set[str] = set()
    for regra in dados:
        faltando = CAMPOS_OBRIGATORIOS - set(regra.keys())
        if faltando:
            raise ValueError(
                f"Regra {regra.get('id', '(sem id)')} está sem os campos: "
                f"{', '.join(sorted(faltando))}."
            )
        if regra["tipo_checagem"] not in TIPOS_CHECAGEM_VALIDOS:
            raise ValueError(
                f"Regra {regra['id']} tem tipo_checagem inválido: "
                f"'{regra['tipo_checagem']}'. Use um de: "
                f"{', '.join(sorted(TIPOS_CHECAGEM_VALIDOS))}."
            )
        if regra["status"] not in STATUS_VALIDOS:
            raise ValueError(
                f"Regra {regra['id']} tem status inválido: '{regra['status']}'. "
                f"Use um de: {', '.join(sorted(STATUS_VALIDOS))}."
            )
        if regra["id"] in ids_vistos:
            raise ValueError(f"Há duas regras com o mesmo id: {regra['id']}.")
        ids_vistos.add(regra["id"])

    return dados


def sincronizar_regras_no_banco() -> None:
    """Garante que cada regra do YAML exista na tabela Regra do banco.

    - Regra nova (ainda não no banco): é inserida com o status do YAML.
    - Regra já existente: atualiza só os campos descritivos (texto, fonte etc.),
      PRESERVANDO o status e a data de validação já gravados pela Karine.
    """
    # Import tardio para evitar dependência circular e custo no import do módulo.
    from sqlmodel import select

    from app.db.modelos import Regra
    from app.db.repositorio import abrir_sessao, criar_banco

    criar_banco()
    regras_yaml = carregar_regras()

    with abrir_sessao() as sessao:
        for item in regras_yaml:
            existente = sessao.get(Regra, item["id"])
            if existente is None:
                sessao.add(
                    Regra(
                        id=item["id"],
                        tema=item["tema"],
                        descricao=item["descricao"],
                        tipo_checagem=item["tipo_checagem"],
                        fonte=item["fonte"],
                        vigencia=item["vigencia"],
                        status=item["status"],
                    )
                )
            else:
                # Atualiza texto/metadados, mas NÃO mexe no status nem na validação.
                existente.tema = item["tema"]
                existente.descricao = item["descricao"]
                existente.tipo_checagem = item["tipo_checagem"]
                existente.fonte = item["fonte"]
                existente.vigencia = item["vigencia"]
                sessao.add(existente)
        sessao.commit()


def validar_regra(id_regra: str) -> None:
    """Marca uma regra como 'validada', registrando a data (usado pela tela)."""
    from app.db.modelos import Regra
    from app.db.repositorio import abrir_sessao

    with abrir_sessao() as sessao:
        regra = sessao.get(Regra, id_regra)
        if regra is None:
            raise ValueError(f"Regra {id_regra} não encontrada no banco.")
        regra.status = "validada"
        regra.data_validacao = datetime.now()
        sessao.add(regra)
        sessao.commit()
