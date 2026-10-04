"""Protótipo de coleta da CTO para UMA OSC.

Uso:
    python scripts/prototipo_coleta.py \
        --nome "Instituto Exemplo de Esporte" \
        --variacoes "Instituto Exemplo;IEE" \
        --cidade "São Paulo/SP" \
        --instagram institutoexemplo \
        --max-noticias 30 --max-posts 60

Roda a busca de reportagens (Google Notícias) + posts do Instagram, classifica
tudo na estrutura do Checklist CTO v3 e gera um relatório HTML em
dados/osc/<slug>/saidas/relatorio_coleta.html.

Não chama IA. Depende de acesso à internet (news.google.com e instagram.com).
"""

from __future__ import annotations

import argparse
import html
import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[1]
if str(_RAIZ) not in sys.path:
    sys.path.insert(0, str(_RAIZ))

from app.coleta.classificar import (  # noqa: E402
    evidencia_de_noticia,
    evidencia_de_post_instagram,
    forca_da_evidencia,
)
from app.coleta.instagram import coletar_instagram  # noqa: E402
from app.coleta.noticias import buscar_noticias  # noqa: E402


def _slug(texto: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in texto.lower()).strip("_")


def executar(args) -> Path:
    variacoes = [args.nome] + [v for v in (args.variacoes or "").split(";") if v.strip()]

    print(f"Buscando reportagens para: {variacoes} | cidade={args.cidade} ...")
    res_noticias = buscar_noticias(variacoes, args.cidade, args.max_noticias)
    if res_noticias.ok:
        print(f"  → {len(res_noticias.itens)} reportagens encontradas.")
    else:
        print(f"  → ERRO: {res_noticias.mensagem}")

    evid_instagram = []
    res_insta = None
    if args.instagram:
        print(f"Coletando Instagram @{args.instagram} ...")
        res_insta = coletar_instagram(args.instagram, limite_posts=args.max_posts)
        if res_insta.ok:
            print(f"  → {len(res_insta.itens)} posts coletados.")
        else:
            print(f"  → ERRO: {res_insta.mensagem}")
        evid_instagram = [evidencia_de_post_instagram(i) for i in res_insta.itens]

    evid_noticias = [evidencia_de_noticia(i) for i in res_noticias.itens]
    evidencias = evid_noticias + evid_instagram
    # Ordena pela força probatória (hierarquia da CTO).
    evidencias.sort(key=forca_da_evidencia, reverse=True)

    destino = _RAIZ / "dados" / "osc" / _slug(args.nome) / "saidas"
    destino.mkdir(parents=True, exist_ok=True)
    caminho = destino / "relatorio_coleta.html"
    caminho.write_text(
        _montar_html(args, evid_noticias, evid_instagram, res_noticias, res_insta),
        encoding="utf-8",
    )
    print(f"\nRelatório salvo em: {caminho}")
    print(f"Total de evidências classificadas: {len(evidencias)}")
    return caminho


def _linha(ev: dict) -> str:
    data = ev.get("data_do_fato") or "sem data"
    legenda = html.escape((ev.get("legenda") or "")[:180])
    url = html.escape(ev.get("url_origem") or "")
    terceiros = "terceiros" if ev.get("eh_de_terceiros") == "sim" else "próprio"
    return (
        f"<tr><td>{html.escape(ev['tipo'])}</td><td>{data}</td>"
        f"<td>{legenda}</td><td>{terceiros}</td>"
        f"<td><a href='{url}'>{url[:50]}</a></td></tr>"
    )


def _montar_html(args, noticias, instagram, res_noticias, res_insta) -> str:
    def tabela(titulo, evidencias, erro):
        if erro:
            return f"<h2>{titulo}</h2><p class='erro'>{html.escape(erro)}</p>"
        linhas = "".join(_linha(e) for e in evidencias) or "<tr><td colspan=5>Nada encontrado.</td></tr>"
        return (
            f"<h2>{titulo} ({len(evidencias)})</h2>"
            "<table><thead><tr><th>Tipo</th><th>Data</th><th>Descrição</th>"
            "<th>Origem</th><th>Link</th></tr></thead><tbody>"
            f"{linhas}</tbody></table>"
        )

    erro_n = res_noticias.mensagem if not res_noticias.ok else ""
    erro_i = res_insta.mensagem if (res_insta and not res_insta.ok) else ""
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Coleta CTO — {html.escape(args.nome)}</title>
<style>
body{{font-family:system-ui,sans-serif;max-width:900px;margin:24px auto;padding:0 16px;color:#17201f}}
h1{{font-size:1.4rem}} h2{{font-size:1.1rem;margin-top:28px}}
table{{width:100%;border-collapse:collapse;font-size:.85rem}}
th,td{{border:1px solid #dde4e3;padding:6px 8px;text-align:left;vertical-align:top}}
th{{background:#eef2f2}} .erro{{color:#9a5b08;background:#fbeed9;padding:10px;border-radius:8px}}
.cap{{color:#5b6a68}}
</style></head><body>
<h1>Coleta CTO — {html.escape(args.nome)}</h1>
<p class="cap">Bloco 1 do Checklist CTO v3 · evidências midiáticas · cidade: {html.escape(args.cidade or '-')}</p>
{tabela('Reportagens (de terceiros — evidência mais forte)', noticias, erro_n)}
{tabela('Posts do Instagram (próprios)', instagram, erro_i)}
<p class="cap">Próximo passo: curadoria — testar cada link, marcar logomarca e prática esportiva, aprovar/descartar.</p>
</body></html>"""


def main():
    p = argparse.ArgumentParser(description="Protótipo de coleta da CTO para 1 OSC.")
    p.add_argument("--nome", required=True)
    p.add_argument("--variacoes", default="", help="variações do nome separadas por ;")
    p.add_argument("--cidade", default="")
    p.add_argument("--instagram", default="")
    p.add_argument("--max-noticias", type=int, default=30)
    p.add_argument("--max-posts", type=int, default=60)
    executar(p.parse_args())


if __name__ == "__main__":
    main()
