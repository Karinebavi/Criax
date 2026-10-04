"""Página 5 — Trilha CTO (.docx).

Gera o documento Word da CTO para a OSC ativa, usando as evidências APROVADAS,
na estrutura do Checklist CTO v3, com timbrado e zoom+seta nas logos marcadas.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[2]
if str(_RAIZ) not in sys.path:
    sys.path.insert(0, str(_RAIZ))

import streamlit as st  # noqa: E402

from app.configuracao import RAIZ  # noqa: E402
from app.db.repositorio import listar_evidencias, obter_osc  # noqa: E402
from app.documentos.gerar_cto import gerar_cto  # noqa: E402

st.set_page_config(page_title="CTO — Esteira LIE", page_icon="📄", layout="wide")
st.title("📄 Gerar CTO (Word)")

osc_id = st.session_state.get("osc_id")
osc = obter_osc(osc_id) if osc_id else None
if not osc:
    st.warning("Nenhuma OSC ativa. Vá em **Cadastro da OSC** e selecione uma.")
    st.stop()
st.caption(f"OSC ativa: **{osc.nome}**")

aprovadas = listar_evidencias(osc.id, "aprovada")
st.write(f"Evidências aprovadas: **{len(aprovadas)}**")
if not aprovadas:
    st.info("Nenhuma evidência aprovada ainda. Aprove na tela **Curadoria** antes de gerar a CTO.")

logo = st.file_uploader("Logomarca da instituição (opcional, para o timbrado)", type=["png", "jpg", "jpeg"])

if st.button("Gerar CTO em Word", type="primary", disabled=not aprovadas):
    def chave_osc():
        return (osc.cnpj or osc.nome or "osc").replace("/", "_").replace(".", "").replace(" ", "_")

    pasta = RAIZ / "dados" / "osc" / chave_osc()
    logo_path = None
    if logo is not None:
        pasta_midia = pasta / "midia"
        pasta_midia.mkdir(parents=True, exist_ok=True)
        logo_path = pasta_midia / f"logo_{logo.name}"
        logo_path.write_bytes(logo.getbuffer())

    osc_dict = {
        "nome": osc.nome,
        "cnpj": osc.cnpj,
        "endereco": osc.logradouro,
        "municipio_uf": f"{osc.municipio or ''}/{osc.uf or ''}".strip("/"),
        "dirigente": osc.dirigente_nome,
        "telefone": osc.telefone,
        "email": osc.email,
        "site": osc.site,
        "instagram": osc.instagram,
        "facebook": osc.facebook_url,
        "logo_path": str(logo_path) if logo_path else osc.logo_path,
    }

    evid = []
    for e in aprovadas:
        bbox = None
        if e.realce_bbox_json:
            try:
                bbox = json.loads(e.realce_bbox_json)
            except Exception:
                bbox = None
        evid.append({
            "codigo": e.codigo, "tipo": e.tipo, "origem": e.origem,
            "url_origem": e.url_origem, "data_do_fato": str(e.data_do_fato or ""),
            "legenda": e.legenda, "eh_de_terceiros": e.eh_de_terceiros,
            "bloco_cto": e.bloco_cto or "1", "caminho_arquivo": e.caminho_arquivo,
            "realce_bbox": bbox,
        })

    saida = pasta / "saidas" / f"CTO_{chave_osc()}.docx"
    with st.spinner("Montando o documento..."):
        caminho = gerar_cto(osc_dict, evid, caminho_saida=saida)
    st.success("CTO gerada!")
    with open(caminho, "rb") as fh:
        st.download_button(
            "⬇️ Baixar CTO (.docx)",
            data=fh.read(),
            file_name=caminho.name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    st.caption(f"Também salva em: {caminho}")
