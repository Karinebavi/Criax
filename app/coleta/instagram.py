"""Coleta de posts públicos do Instagram via instaloader.

Sem login por padrão, com pausa entre requisições e limite configurável. Se o
Instagram bloquear, a função avisa e sugere upload manual — NUNCA tenta contornar
o bloqueio.

Por privacidade, guardamos texto (legenda, data, métricas) e o link do post. As
imagens só são baixadas se explicitamente solicitado (padrão: não baixar).
"""

from __future__ import annotations

import datetime as dt
import time
from typing import Optional

from app.coleta.noticias import ResultadoColeta  # reaproveita o mesmo formato


def coletar_instagram(
    handle: str,
    limite_posts: int = 300,
    meses_retroativos: int = 24,
    pausa_segundos: float = 5,
    baixar_imagens: bool = True,
    pasta_midia: str | None = None,
) -> ResultadoColeta:
    """Coleta posts públicos de um perfil do Instagram.

    Devolve ResultadoColeta com itens (data, legenda, curtidas, comentários, url,
    caminho_arquivo). Quando baixar_imagens=True e pasta_midia é informado, baixa
    a imagem de cada post para a pasta local (as fotos ficam só no computador).
    Nunca levanta exceção — bloqueios e erros viram mensagem em português.
    """
    handle = (handle or "").lstrip("@").strip()
    if not handle:
        return ResultadoColeta(ok=False, erro="handle vazio", mensagem="Informe o @ do Instagram.")

    try:
        import instaloader
    except ImportError:
        return ResultadoColeta(
            ok=False,
            erro="instaloader ausente",
            mensagem="A biblioteca instaloader não está instalada. Rode o instalador novamente.",
        )

    carregador = instaloader.Instaloader(
        download_pictures=baixar_imagens,
        download_videos=False,
        download_video_thumbnails=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
        quiet=True,
    )

    try:
        perfil = instaloader.Profile.from_username(carregador.context, handle)
    except Exception as erro:  # perfil privado, inexistente ou bloqueio
        return ResultadoColeta(
            ok=False,
            erro=str(erro),
            mensagem=(
                f"Não foi possível acessar o perfil @{handle}. Pode estar privado, "
                "não existir, ou o Instagram bloqueou a coleta automática. "
                "Nesse caso, faça o upload manual das fotos e cole os links dos posts."
            ),
        )

    corte = dt.datetime.now() - dt.timedelta(days=30 * meses_retroativos)
    itens: list[dict] = []
    try:
        for indice, post in enumerate(perfil.get_posts()):
            if indice >= limite_posts:
                break
            data_post = post.date_utc
            if data_post < corte:
                break
            caminho_arquivo = None
            if baixar_imagens and pasta_midia:
                caminho_arquivo = _baixar_imagem(
                    getattr(post, "url", None), pasta_midia, post.shortcode
                )
            itens.append(
                {
                    "data": data_post.date().isoformat(),
                    "legenda": post.caption or "",
                    "curtidas": post.likes,
                    "comentarios": post.comments,
                    "url": f"https://www.instagram.com/p/{post.shortcode}/",
                    "caminho_arquivo": caminho_arquivo,
                }
            )
            time.sleep(pausa_segundos)  # respeita o Instagram, evita bloqueio
    except Exception as erro:
        # Devolve o que já coletou + aviso (coleta parcial é melhor que nada).
        return ResultadoColeta(
            ok=bool(itens),
            itens=itens,
            erro=str(erro),
            mensagem=(
                "A coleta do Instagram foi interrompida (provável limite de "
                f"requisições). Foram coletados {len(itens)} posts antes da parada. "
                "Para o restante, faça upload manual."
            ),
        )

    return ResultadoColeta(ok=True, itens=itens)


def _baixar_imagem(url: str | None, pasta_midia: str, shortcode: str) -> str | None:
    """Baixa a imagem do post para a pasta local. Devolve o caminho ou None."""
    if not url:
        return None
    from pathlib import Path

    import httpx

    try:
        pasta = Path(pasta_midia)
        pasta.mkdir(parents=True, exist_ok=True)
        destino = pasta / f"{shortcode}.jpg"
        resp = httpx.get(url, timeout=30, follow_redirects=True, trust_env=True,
                         headers={"User-Agent": "Mozilla/5.0 (EsteiraLIE)"})
        if resp.status_code == 200 and resp.content:
            destino.write_bytes(resp.content)
            return str(destino)
    except Exception:
        return None
    return None
