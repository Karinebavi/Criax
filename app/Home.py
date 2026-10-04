"""Tela inicial do Esteira LIE.

Mostra a lista de OSCs cadastradas e o status de cada uma. Também cria o banco e
sincroniza as regras na primeira execução.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Garante que a raiz do projeto esteja no caminho de importação, para que
# "from app...." funcione quando o Streamlit roda este arquivo diretamente.
_RAIZ = Path(__file__).resolve().parents[1]
if str(_RAIZ) not in sys.path:
    sys.path.insert(0, str(_RAIZ))

import streamlit as st  # noqa: E402
from sqlmodel import select  # noqa: E402

from app.db.modelos import OSC, Evidencia, Projeto  # noqa: E402
from app.db.repositorio import abrir_sessao, criar_banco  # noqa: E402
from app.regras.carregar import sincronizar_regras_no_banco  # noqa: E402


def inicializar() -> None:
    """Cria o banco e sincroniza as regras (idempotente)."""
    criar_banco()
    sincronizar_regras_no_banco()


def main() -> None:
    st.set_page_config(page_title="Esteira LIE", page_icon="🏅", layout="wide")

    try:
        inicializar()
    except Exception as erro:  # mensagem de erro amigável, em português
        st.error(
            "Não foi possível preparar o sistema (banco de dados ou regras).\n\n"
            f"Detalhe técnico: {erro}"
        )
        st.stop()

    st.title("🏅 Esteira LIE")
    st.caption(
        "Sistema local para montar CTO, escrita do projeto e planilha orçamentária "
        "da Lei de Incentivo ao Esporte. Nada é enviado para fora — só são gerados "
        "arquivos no seu computador."
    )

    st.info(
        "**Fluxo da CTO já disponível** (menu à esquerda, nesta ordem):\n\n"
        "1. **Cadastro da OSC** — cadastre e selecione a entidade\n"
        "2. **Coleta** — busca reportagens e posts do Instagram\n"
        "3. **Curadoria** — aprove/descarte e marque logomarca e prática esportiva\n"
        "4. **CTO** — gera o Word com timbrado e zoom na logo\n\n"
        "As telas de Diagnóstico, Projeto, Orçamento e Conferência chegam nas próximas fases.",
        icon="🧭",
    )

    st.subheader("Organizações (OSCs)")

    with abrir_sessao() as sessao:
        oscs = sessao.exec(select(OSC)).all()

        if not oscs:
            st.write(
                "Nenhuma OSC cadastrada ainda. O cadastro será feito na **Fase 1**."
            )
            return

        linhas = []
        for osc in oscs:
            n_evid = len(
                sessao.exec(
                    select(Evidencia).where(Evidencia.osc_id == osc.id)
                ).all()
            )
            n_aprov = len(
                sessao.exec(
                    select(Evidencia).where(
                        Evidencia.osc_id == osc.id,
                        Evidencia.status == "aprovada",
                    )
                ).all()
            )
            n_proj = len(
                sessao.exec(
                    select(Projeto).where(Projeto.osc_id == osc.id)
                ).all()
            )
            linhas.append(
                {
                    "OSC": osc.nome,
                    "CNPJ": osc.cnpj,
                    "Município/UF": f"{osc.municipio or '-'}/{osc.uf or '-'}",
                    "Evidências": n_evid,
                    "Aprovadas": n_aprov,
                    "Projetos": n_proj,
                }
            )
        st.dataframe(linhas, use_container_width=True, hide_index=True)


main()
