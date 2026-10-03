"""Funções de checagem das regras.

São funções puras (sem banco, sem IA), fáceis de testar. Cada checagem devolve um
`ResultadoChecagem` com situação OK/ALERTA/PENDENTE, mensagem em português e a
fonte da regra.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

# Situações possíveis de uma checagem.
OK = "OK"
ALERTA = "ALERTA"
PENDENTE = "PENDENTE"  # regra ainda não validada pela Karine


@dataclass
class ResultadoChecagem:
    """Resultado de uma checagem de regra."""

    id_regra: str
    situacao: str  # OK | ALERTA | PENDENTE
    mensagem: str
    fonte: str = ""
    detalhes: dict[str, Any] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.situacao == OK


def checar_percentual_maximo(
    valor_numerador: float,
    valor_denominador: float,
    limite: float,
    id_regra: str = "",
    fonte: str = "",
) -> ResultadoChecagem:
    """Checa se numerador/denominador não ultrapassa o limite (ex.: 0.15 = 15%).

    Ex.: Atividade Meio (numerador) não pode passar de 15% da Atividade Fim
    (denominador).
    """
    if valor_denominador <= 0:
        return ResultadoChecagem(
            id_regra=id_regra,
            situacao=ALERTA,
            mensagem=(
                "Não foi possível calcular o percentual: o valor de referência "
                "(denominador) é zero ou negativo."
            ),
            fonte=fonte,
            detalhes={"percentual": None, "limite": limite},
        )

    percentual = valor_numerador / valor_denominador
    dentro = percentual <= limite + 1e-9  # tolerância para arredondamento
    situacao = OK if dentro else ALERTA
    mensagem = (
        f"{percentual * 100:.2f}% "
        f"({'dentro do' if dentro else 'ACIMA do'} limite de {limite * 100:.0f}%)."
    )
    return ResultadoChecagem(
        id_regra=id_regra,
        situacao=situacao,
        mensagem=mensagem,
        fonte=fonte,
        detalhes={"percentual": percentual, "limite": limite},
    )


def checar_min_max_itens(
    quantidade: int,
    minimo: int,
    maximo: int,
    id_regra: str = "",
    fonte: str = "",
) -> ResultadoChecagem:
    """Checa se a quantidade de itens está entre o mínimo e o máximo (inclusive)."""
    dentro = minimo <= quantidade <= maximo
    if dentro:
        mensagem = f"{quantidade} item(ns) (dentro do intervalo de {minimo} a {maximo})."
        situacao = OK
    elif quantidade < minimo:
        mensagem = f"{quantidade} item(ns): abaixo do mínimo de {minimo}."
        situacao = ALERTA
    else:
        mensagem = f"{quantidade} item(ns): acima do máximo de {maximo}."
        situacao = ALERTA
    return ResultadoChecagem(
        id_regra=id_regra,
        situacao=situacao,
        mensagem=mensagem,
        fonte=fonte,
        detalhes={"quantidade": quantidade, "minimo": minimo, "maximo": maximo},
    )


def checar_obrigatorios(
    itens_presentes: Iterable[str],
    itens_obrigatorios: Iterable[str],
    id_regra: str = "",
    fonte: str = "",
) -> ResultadoChecagem:
    """Checa se todos os itens obrigatórios estão presentes.

    Devolve ALERTA listando o que está faltando.
    """
    presentes = set(itens_presentes)
    obrigatorios = list(itens_obrigatorios)
    faltando = [item for item in obrigatorios if item not in presentes]
    if faltando:
        mensagem = "Faltam itens obrigatórios: " + ", ".join(faltando) + "."
        situacao = ALERTA
    else:
        mensagem = "Todos os itens obrigatórios estão presentes."
        situacao = OK
    return ResultadoChecagem(
        id_regra=id_regra,
        situacao=situacao,
        mensagem=mensagem,
        fonte=fonte,
        detalhes={"faltando": faltando, "obrigatorios": obrigatorios},
    )
