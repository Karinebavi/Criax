"""Página 3 — Curadoria (gate humano nº 1).

Para cada evidência coletada, a Karine aprova ou descarta e marca os sinais que o
Checklist CTO exige: logomarca visível, prática esportiva, de terceiros, link
testado. Em fotos, pode marcar a área da logo para o zoom+seta na CTO.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[2]
if str(_RAIZ) not in sys.path:
    sys.path.insert(0, str(_RAIZ))

import streamlit as st  # noqa: E402

from app.db.repositorio import atualizar_evidencia, listar_evidencias, obter_osc  # noqa: E402

st.set_page_config(page_title="Curadoria — Esteira LIE", page_icon="✅", layout="wide")
st.title("✅ Curadoria das evidências")

osc_id = st.session_state.get("osc_id")
osc = obter_osc(osc_id) if osc_id else None
if not osc:
    st.warning("Nenhuma OSC ativa. Vá em **Cadastro da OSC** e selecione uma.")
    st.stop()
st.caption(f"OSC ativa: **{osc.nome}**")

filtro = st.radio("Mostrar", ["pendente", "aprovada", "descartada", "todas"], horizontal=True)
evidencias = listar_evidencias(osc.id, None if filtro == "todas" else filtro)

if not evidencias:
    st.info("Nenhuma evidência neste filtro. Colete na tela **Coleta** ou mude o filtro.")
    st.stop()

sim_nao = ["nao_verificado", "sim", "nao"]

for ev in evidencias:
    with st.container(border=True):
        col_img, col_dados = st.columns([1, 2])
        with col_img:
            if ev.caminho_arquivo and Path(ev.caminho_arquivo).exists():
                st.image(ev.caminho_arquivo, use_container_width=True)
            else:
                st.markdown(f"**{ev.tipo or 'evidência'}**")
            st.caption(f"{ev.codigo or ''} · {ev.origem or ''} · {ev.data_do_fato or 'sem data'}")
            if ev.url_origem:
                st.markdown(f"[Abrir link]({ev.url_origem})")
        with col_dados:
            st.write((ev.legenda or "")[:300] or "_(sem legenda)_")
            c1, c2, c3 = st.columns(3)
            logo = c1.selectbox("Logomarca?", sim_nao, index=sim_nao.index(ev.tem_logomarca or "nao_verificado"), key=f"logo_{ev.id}")
            pratica = c2.selectbox("Prática esportiva?", sim_nao, index=sim_nao.index(ev.mostra_pratica_esportiva or "nao_verificado"), key=f"prat_{ev.id}")
            link_ok = c3.selectbox("Link testado?", sim_nao, index=sim_nao.index(ev.link_testado or "nao_verificado"), key=f"link_{ev.id}")

            bbox_atual = ev.realce_bbox_json or ""
            realce = st.checkbox("Logo pouco visível → aplicar zoom+seta na CTO", value=bool(bbox_atual), key=f"rea_{ev.id}")
            bbox_val = ""
            if realce:
                st.caption("Informe a posição aproximada da logo na foto (em pixels): x, y, largura, altura.")
                try:
                    atual = json.loads(bbox_atual) if bbox_atual else [10, 10, 120, 60]
                except Exception:
                    atual = [10, 10, 120, 60]
                cc = st.columns(4)
                x = cc[0].number_input("x", 0, 10000, int(atual[0]), key=f"x_{ev.id}")
                y = cc[1].number_input("y", 0, 10000, int(atual[1]), key=f"y_{ev.id}")
                w = cc[2].number_input("larg", 1, 10000, int(atual[2]), key=f"w_{ev.id}")
                h = cc[3].number_input("alt", 1, 10000, int(atual[3]), key=f"h_{ev.id}")
                bbox_val = json.dumps([int(x), int(y), int(w), int(h)])

            b1, b2, b3 = st.columns(3)
            if b1.button("💾 Salvar marcações", key=f"save_{ev.id}"):
                atualizar_evidencia(ev.id, tem_logomarca=logo, mostra_pratica_esportiva=pratica,
                                     link_testado=link_ok, realce_bbox_json=bbox_val or None)
                st.toast(f"{ev.codigo} atualizada.")
                st.rerun()
            if b2.button("✅ Aprovar", key=f"ap_{ev.id}"):
                atualizar_evidencia(ev.id, status="aprovada", tem_logomarca=logo, mostra_pratica_esportiva=pratica,
                                     link_testado=link_ok, realce_bbox_json=bbox_val or None)
                st.rerun()
            if b3.button("🗑️ Descartar", key=f"dc_{ev.id}"):
                atualizar_evidencia(ev.id, status="descartada")
                st.rerun()

st.divider()
st.metric("Aprovadas", len(listar_evidencias(osc.id, "aprovada")))
st.caption("Próximo passo: tela **CTO** para gerar o Word com as evidências aprovadas.")
