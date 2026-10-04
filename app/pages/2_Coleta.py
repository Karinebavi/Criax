"""Página 2 — Coleta automática.

Para a OSC ativa, busca reportagens (Google Notícias) e posts do Instagram,
classifica na estrutura da CTO (Bloco 1) e salva como evidências pendentes.
"""

from __future__ import annotations

import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[2]
if str(_RAIZ) not in sys.path:
    sys.path.insert(0, str(_RAIZ))

import streamlit as st  # noqa: E402

from app.configuracao import RAIZ, carregar_config  # noqa: E402
from app.coleta.classificar import evidencia_de_noticia, evidencia_de_post_instagram  # noqa: E402
from app.coleta.instagram import coletar_instagram  # noqa: E402
from app.coleta.noticias import buscar_noticias  # noqa: E402
from app.db.repositorio import listar_evidencias, obter_osc, salvar_evidencias  # noqa: E402

st.set_page_config(page_title="Coleta — Esteira LIE", page_icon="🛰️", layout="wide")

st.title("🛰️ Coleta automática")

osc_id = st.session_state.get("osc_id")
osc = obter_osc(osc_id) if osc_id else None
if not osc:
    st.warning("Nenhuma OSC ativa. Vá em **Cadastro da OSC** e selecione uma.")
    st.stop()

st.caption(f"OSC ativa: **{osc.nome}** ({osc.municipio or '-'}/{osc.uf or '-'})")

config = carregar_config()
cfg_insta = config.get("coleta", {}).get("instagram", {})
cfg_not = config.get("coleta", {}).get("noticias", {})


def pasta_midia():
    chave = (osc.cnpj or osc.nome or "osc").replace("/", "_").replace(".", "").replace(" ", "_")
    return RAIZ / "dados" / "osc" / chave / "midia"


col1, col2 = st.columns(2)

# --------------------------------------------------------- NOTÍCIAS
with col1:
    st.subheader("Reportagens / notícias")
    variacoes_txt = st.text_area(
        "Nome e variações (uma por linha)",
        value=osc.nome,
        help="Ex.: nome oficial, sigla, nome fantasia.",
    )
    cidade = st.text_input("Cidade/UF para refinar", value=f"{osc.municipio or ''} {osc.uf or ''}".strip())
    if st.button("Buscar reportagens", type="primary"):
        variacoes = [v.strip() for v in variacoes_txt.splitlines() if v.strip()]
        with st.spinner("Buscando no Google Notícias..."):
            res = buscar_noticias(variacoes, cidade or None, int(cfg_not.get("max_resultados", 30)))
        if not res.ok:
            st.error(res.mensagem)
        else:
            evid = [evidencia_de_noticia(i) for i in res.itens]
            n = salvar_evidencias(osc.id, evid)
            st.success(f"{len(res.itens)} reportagens encontradas · {n} novas salvas como evidência.")
            for it in res.itens[:10]:
                st.write(f"- [{it['data']}] **{it['veiculo']}**: {it['titulo']}")

# --------------------------------------------------------- INSTAGRAM
with col2:
    st.subheader("Instagram (posts e fotos)")
    handle = st.text_input("@ do Instagram", value=(osc.instagram or "").lstrip("@"))
    limite = st.number_input("Máximo de posts", 1, 1000, int(cfg_insta.get("limite_posts", 300)))
    st.caption(
        "Observação: em servidores de nuvem o Instagram costuma bloquear (erro 429). "
        "No seu computador, funciona normalmente."
    )
    if st.button("Coletar Instagram"):
        with st.spinner("Coletando posts (respeitando pausa entre requisições)..."):
            res = coletar_instagram(
                handle,
                limite_posts=int(limite),
                meses_retroativos=int(cfg_insta.get("meses_retroativos", 24)),
                pausa_segundos=float(cfg_insta.get("pausa_segundos", 5)),
                baixar_imagens=True,
                pasta_midia=str(pasta_midia()),
            )
        if not res.ok and not res.itens:
            st.error(res.mensagem)
        else:
            if res.mensagem:
                st.warning(res.mensagem)
            evid = [evidencia_de_post_instagram(i) for i in res.itens]
            n = salvar_evidencias(osc.id, evid)
            st.success(f"{len(res.itens)} posts coletados · {n} novos salvos como evidência.")

st.divider()
total = len(listar_evidencias(osc.id))
pend = len(listar_evidencias(osc.id, "pendente"))
st.metric("Evidências desta OSC", total, f"{pend} pendentes de curadoria")
st.caption("Próximo passo: tela **Curadoria** para aprovar/descartar as evidências.")
