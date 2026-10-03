"""Página de Regras.

Mostra todas as regras da LIE (do regras.yaml, com status vindo do banco),
permite filtrar por status e marcar uma regra como 'validada' com um clique
(registrando a data).
"""

from __future__ import annotations

import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[2]
if str(_RAIZ) not in sys.path:
    sys.path.insert(0, str(_RAIZ))

import streamlit as st  # noqa: E402
from sqlmodel import select  # noqa: E402

from app.db.modelos import Regra  # noqa: E402
from app.db.repositorio import abrir_sessao, criar_banco  # noqa: E402
from app.regras.carregar import sincronizar_regras_no_banco, validar_regra  # noqa: E402

# Ícones/cores por status, para leitura rápida.
ICONE_STATUS = {
    "pendente": "🟡 pendente",
    "validada": "🟢 validada",
    "revogada": "⚫ revogada",
}


def inicializar() -> None:
    criar_banco()
    sincronizar_regras_no_banco()


def main() -> None:
    st.set_page_config(page_title="Regras — Esteira LIE", page_icon="📋", layout="wide")

    try:
        inicializar()
    except Exception as erro:
        st.error(
            "Não foi possível carregar as regras.\n\n"
            f"Detalhe técnico: {erro}"
        )
        st.stop()

    st.title("📋 Regras da LIE")
    st.caption(
        "Estas são as regras que o sistema usa. A IA nunca inventa regra — ela "
        "sempre recebe estas. Todas começam como **pendente**: a norma mudou "
        "(LC 222/2025, Decreto 12.861/2026, Portaria MESP nº 10/2026) e cada regra "
        "precisa da sua validação antes de valer por aqui."
    )

    st.warning(
        "⚠️ Enquanto uma regra estiver **pendente**, ela não bloqueia nada, mas "
        "aparece como alerta: 'regra ainda não validada pela Karine'.",
        icon="⚠️",
    )

    # ---------------------------------------------------------------- filtros
    col1, col2 = st.columns(2)
    with col1:
        filtro_status = st.multiselect(
            "Filtrar por status",
            options=["pendente", "validada", "revogada"],
            default=["pendente", "validada", "revogada"],
        )
    with col2:
        with abrir_sessao() as sessao:
            temas = sorted(
                {r.tema for r in sessao.exec(select(Regra)).all() if r.tema}
            )
        filtro_tema = st.multiselect(
            "Filtrar por tema", options=temas, default=temas
        )

    # ---------------------------------------------------------------- listagem
    with abrir_sessao() as sessao:
        regras = sessao.exec(select(Regra).order_by(Regra.id)).all()

        # Resumo rápido por status.
        total = len(regras)
        n_pend = sum(1 for r in regras if r.status == "pendente")
        n_val = sum(1 for r in regras if r.status == "validada")
        n_rev = sum(1 for r in regras if r.status == "revogada")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total", total)
        c2.metric("🟡 Pendentes", n_pend)
        c3.metric("🟢 Validadas", n_val)
        c4.metric("⚫ Revogadas", n_rev)

        st.divider()

        visiveis = [
            r
            for r in regras
            if r.status in filtro_status and (not filtro_tema or r.tema in filtro_tema)
        ]

        if not visiveis:
            st.write("Nenhuma regra com os filtros escolhidos.")
            return

        for regra in visiveis:
            with st.container(border=True):
                esq, dir_ = st.columns([5, 1])
                with esq:
                    st.markdown(
                        f"**{regra.id}** · {ICONE_STATUS.get(regra.status, regra.status)} "
                        f"· _tema: {regra.tema}_ · _checagem: {regra.tipo_checagem}_"
                    )
                    st.write(regra.descricao)
                    st.caption(f"Fonte: {regra.fonte}")
                    if regra.vigencia:
                        st.caption(f"Vigência: {regra.vigencia}")
                    if regra.data_validacao:
                        st.caption(
                            "Validada em "
                            f"{regra.data_validacao.strftime('%d/%m/%Y %H:%M')}"
                        )
                with dir_:
                    if regra.status == "pendente":
                        if st.button("✅ Validar", key=f"validar_{regra.id}"):
                            validar_regra(regra.id)
                            st.rerun()
                    elif regra.status == "validada":
                        st.success("Validada")
                    else:
                        st.write("—")


main()
