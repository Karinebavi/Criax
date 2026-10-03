"""Testes da Fase 0: carregamento das regras e funções de checagem.

Os testes NÃO chamam a API da Anthropic nem a internet.
"""

from __future__ import annotations

import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[1]
if str(_RAIZ) not in sys.path:
    sys.path.insert(0, str(_RAIZ))

import pytest  # noqa: E402

from app.regras.carregar import (  # noqa: E402
    CAMPOS_OBRIGATORIOS,
    STATUS_VALIDOS,
    TIPOS_CHECAGEM_VALIDOS,
    carregar_regras,
)
from app.regras.checar import (  # noqa: E402
    ALERTA,
    OK,
    checar_min_max_itens,
    checar_obrigatorios,
    checar_percentual_maximo,
)


# ----------------------------- carregamento --------------------------------

def test_regras_yaml_carrega_e_tem_itens():
    regras = carregar_regras()
    assert isinstance(regras, list)
    assert len(regras) > 0


def test_toda_regra_tem_campos_obrigatorios_e_valores_validos():
    for regra in carregar_regras():
        assert CAMPOS_OBRIGATORIOS <= set(regra.keys()), regra.get("id")
        assert regra["tipo_checagem"] in TIPOS_CHECAGEM_VALIDOS
        assert regra["status"] in STATUS_VALIDOS


def test_seed_inteiro_nasce_pendente():
    # Na Fase 0, nada foi validado ainda.
    for regra in carregar_regras():
        assert regra["status"] == "pendente", regra["id"]


def test_ids_de_regra_sao_unicos():
    ids = [r["id"] for r in carregar_regras()]
    assert len(ids) == len(set(ids))


def test_regra_do_limite_de_atividade_meio_existe():
    regras = {r["id"]: r for r in carregar_regras()}
    assert "ORC-001" in regras
    orc = regras["ORC-001"]
    assert orc["tipo_checagem"] == "percentual_maximo"
    assert orc["parametros"]["limite"] == 0.15


# --------------------------- percentual_maximo ------------------------------

def test_percentual_dentro_do_limite_eh_ok():
    # 15 de 100 = 15%, no limite de 15% -> OK
    r = checar_percentual_maximo(15, 100, 0.15)
    assert r.situacao == OK


def test_percentual_acima_do_limite_eh_alerta():
    # 20 de 100 = 20%, acima de 15% -> ALERTA
    r = checar_percentual_maximo(20, 100, 0.15)
    assert r.situacao == ALERTA


def test_percentual_com_denominador_zero_nao_quebra():
    r = checar_percentual_maximo(10, 0, 0.15)
    assert r.situacao == ALERTA
    assert r.detalhes["percentual"] is None


# ---------------------------- min_max_itens ---------------------------------

@pytest.mark.parametrize("quantidade,esperado", [(1, ALERTA), (2, OK), (5, OK), (6, ALERTA)])
def test_min_max_itens_metas(quantidade, esperado):
    # Metas: mínimo 2, máximo 5.
    r = checar_min_max_itens(quantidade, 2, 5)
    assert r.situacao == esperado


# ---------------------------- obrigatorios ----------------------------------

def test_obrigatorios_completos_eh_ok():
    r = checar_obrigatorios(
        itens_presentes=["indicador", "marco_de_referencia", "instrumento_de_verificacao"],
        itens_obrigatorios=["indicador", "marco_de_referencia", "instrumento_de_verificacao"],
    )
    assert r.situacao == OK
    assert r.detalhes["faltando"] == []


def test_obrigatorios_faltando_eh_alerta_e_lista_o_que_falta():
    r = checar_obrigatorios(
        itens_presentes=["indicador"],
        itens_obrigatorios=["indicador", "marco_de_referencia", "instrumento_de_verificacao"],
    )
    assert r.situacao == ALERTA
    assert "marco_de_referencia" in r.detalhes["faltando"]
    assert "instrumento_de_verificacao" in r.detalhes["faltando"]
