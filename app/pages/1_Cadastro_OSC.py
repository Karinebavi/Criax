"""Página 1 — Cadastro da OSC.

Cadastra uma nova OSC e permite escolher a OSC ativa (usada nas outras telas).
"""

from __future__ import annotations

import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[2]
if str(_RAIZ) not in sys.path:
    sys.path.insert(0, str(_RAIZ))

import streamlit as st  # noqa: E402

from app.db.repositorio import criar_banco, listar_oscs, salvar_osc  # noqa: E402

st.set_page_config(page_title="Cadastro da OSC — Esteira LIE", page_icon="📝", layout="wide")
criar_banco()

st.title("📝 Cadastro da OSC")
st.caption("Cadastre a entidade. A OSC escolhida aqui é usada nas telas de Coleta, Curadoria e CTO.")

# ------------------------------------------------- escolher OSC ativa
oscs = listar_oscs()
if oscs:
    nomes = {f"{o.nome} ({o.cnpj or 'sem CNPJ'})": o.id for o in oscs}
    escolha = st.selectbox("OSC ativa", options=list(nomes.keys()))
    st.session_state["osc_id"] = nomes[escolha]
    st.success(f"OSC ativa: {escolha}")
else:
    st.info("Nenhuma OSC cadastrada ainda. Cadastre a primeira abaixo.")

st.divider()
st.subheader("Cadastrar nova OSC")

with st.form("nova_osc"):
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome da entidade *")
        cnpj = st.text_input("CNPJ")
        telefone = st.text_input("Telefone")
        email = st.text_input("E-mail")
        instagram = st.text_input("Instagram (@ ou link)")
    with col2:
        municipio = st.text_input("Município")
        uf = st.text_input("UF", max_chars=2)
        logradouro = st.text_input("Endereço (logradouro, nº)")
        site = st.text_input("Site")
        facebook_url = st.text_input("Facebook (link)")
    dirigente_nome = st.text_input("Dirigente (nome)")
    dirigente_cargo = st.text_input("Cargo do dirigente")
    enviado = st.form_submit_button("Salvar OSC")

    if enviado:
        if not nome.strip():
            st.error("O nome da entidade é obrigatório.")
        else:
            osc = salvar_osc(
                {
                    "nome": nome.strip(),
                    "cnpj": cnpj.strip() or None,
                    "telefone": telefone.strip() or None,
                    "email": email.strip() or None,
                    "instagram": instagram.strip() or None,
                    "municipio": municipio.strip() or None,
                    "uf": uf.strip().upper() or None,
                    "logradouro": logradouro.strip() or None,
                    "site": site.strip() or None,
                    "facebook_url": facebook_url.strip() or None,
                    "dirigente_nome": dirigente_nome.strip() or None,
                    "dirigente_cargo": dirigente_cargo.strip() or None,
                }
            )
            st.session_state["osc_id"] = osc.id
            st.success(f"OSC '{osc.nome}' cadastrada e selecionada. Vá para a tela de Coleta.")
            st.rerun()
