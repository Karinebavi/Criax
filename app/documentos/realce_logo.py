"""Realce de logomarca em fotos (zoom + seta).

Quando a logomarca/identidade visual da entidade não aparece claramente numa foto
(regra CTO-EV-LOGO-001), este módulo gera uma versão da imagem com um RECORTE
AMPLIADO da área da logo, num canto, e uma SETA apontando da ampliação para a
posição original da logo. Ajuda o técnico do MESP a reconhecer o nexo de autoria.

Usa Pillow. A área da logo (bbox) vem da curadoria (a Karine marca na tela).
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw


def realcar_logo(
    caminho_imagem: str | Path,
    bbox: tuple[int, int, int, int],
    caminho_saida: str | Path,
    fator_zoom: float = 2.6,
    canto: str = "superior_direito",
) -> Path:
    """Gera uma cópia da foto com a logo ampliada num canto e uma seta apontando.

    - bbox: (x, y, largura, altura) da logomarca na imagem original.
    - fator_zoom: quanto ampliar o recorte.
    - canto: onde colocar a ampliação (superior_direito, superior_esquerdo,
      inferior_direito, inferior_esquerdo).
    """
    imagem = Image.open(caminho_imagem).convert("RGB")
    larg, alt = imagem.size
    x, y, w, h = bbox

    # Recorte da logo, com uma folga ao redor.
    folga = int(min(w, h) * 0.25)
    cx0 = max(0, x - folga)
    cy0 = max(0, y - folga)
    cx1 = min(larg, x + w + folga)
    cy1 = min(alt, y + h + folga)
    recorte = imagem.crop((cx0, cy0, cx1, cy1))

    # Amplia o recorte.
    novo_w = int(recorte.width * fator_zoom)
    novo_h = int(recorte.height * fator_zoom)
    # Limita o inset a no máximo ~40% da imagem, para não cobrir a foto.
    max_lado = int(min(larg, alt) * 0.4)
    if max(novo_w, novo_h) > max_lado and max(novo_w, novo_h) > 0:
        escala = max_lado / max(novo_w, novo_h)
        novo_w = max(1, int(novo_w * escala))
        novo_h = max(1, int(novo_h * escala))
    inset = recorte.resize((novo_w, novo_h))

    desenho = ImageDraw.Draw(imagem)
    margem = int(min(larg, alt) * 0.03)

    # Posição do inset conforme o canto escolhido.
    if "superior" in canto:
        iy = margem
    else:
        iy = alt - novo_h - margem
    if "direito" in canto:
        ix = larg - novo_w - margem
    else:
        ix = margem

    # Moldura branca em volta do inset.
    moldura = 4
    desenho.rectangle(
        [ix - moldura, iy - moldura, ix + novo_w + moldura, iy + novo_h + moldura],
        fill=(255, 255, 255),
        outline=(15, 118, 110),
        width=moldura,
    )
    imagem.paste(inset, (ix, iy))

    # Realça a logo original com um retângulo.
    desenho.rectangle([x, y, x + w, y + h], outline=(180, 35, 42), width=max(2, larg // 400))

    # Seta do inset até o centro da logo original.
    origem = (ix + novo_w // 2, iy + novo_h // 2)
    destino = (x + w // 2, y + h // 2)
    _desenhar_seta(desenho, origem, destino, cor=(180, 35, 42), largura=max(2, larg // 350))

    caminho_saida = Path(caminho_saida)
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    imagem.save(caminho_saida)
    return caminho_saida


def _desenhar_seta(desenho, origem, destino, cor=(180, 35, 42), largura=3) -> None:
    """Desenha uma linha de origem a destino com uma ponta de seta no destino."""
    import math

    desenho.line([origem, destino], fill=cor, width=largura)
    ang = math.atan2(destino[1] - origem[1], destino[0] - origem[0])
    tam = largura * 5  # tamanho da ponta
    for desvio in (math.radians(25), math.radians(-25)):
        px = destino[0] - tam * math.cos(ang - desvio)
        py = destino[1] - tam * math.sin(ang - desvio)
        desenho.line([destino, (px, py)], fill=cor, width=largura)
