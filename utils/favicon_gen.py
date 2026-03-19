"""
utils/favicon_gen.py
Genera el favicon de AgroControl programáticamente con Pillow.
Se ejecuta una sola vez — el .ico queda en assets/favicon.ico
"""
import os
from PIL import Image, ImageDraw, ImageFont


def generar_favicon(ruta_salida: str = None) -> str:
    """
    Genera favicon.ico con logo de hoja verde de AgroControl.
    Retorna la ruta del archivo generado.
    """
    if ruta_salida is None:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_salida = os.path.join(base, "assets", "favicon.ico")

    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

    # Tamaños estándar de favicon
    tamaños = [256, 128, 64, 48, 32, 16]
    imagenes = []

    for size in tamaños:
        img  = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Fondo círculo verde oscuro
        margen = size // 10
        draw.ellipse(
            [margen, margen, size - margen, size - margen],
            fill=(44, 95, 45, 255)
        )

        # Hoja estilizada (polígono)
        cx, cy = size // 2, size // 2
        r = size * 0.35

        # Cuerpo de la hoja (elipse inclinada simulada con polígono)
        hoja = [
            (cx,           cy - r * 0.9),   # punta superior
            (cx + r * 0.7, cy - r * 0.2),   # derecha arriba
            (cx + r * 0.5, cy + r * 0.6),   # derecha abajo
            (cx,           cy + r * 0.9),   # punta inferior
            (cx - r * 0.3, cy + r * 0.4),   # izquierda abajo
            (cx - r * 0.6, cy - r * 0.1),   # izquierda arriba
        ]
        hoja = [(int(x), int(y)) for x, y in hoja]
        draw.polygon(hoja, fill=(151, 188, 98, 255))

        # Nervio central de la hoja
        grosor = max(1, size // 32)
        draw.line(
            [(cx, int(cy - r * 0.85)), (cx, int(cy + r * 0.85))],
            fill=(44, 95, 45, 200), width=grosor
        )

        # Punto blanco (brillo)
        br = max(1, size // 20)
        draw.ellipse(
            [cx - br * 2, int(cy - r * 0.5) - br,
             cx,          int(cy - r * 0.5) + br],
            fill=(255, 255, 255, 120)
        )

        imagenes.append(img)

    # Guardar como ICO multi-tamaño
    imagenes[0].save(
        ruta_salida,
        format="ICO",
        sizes=[(s, s) for s in tamaños],
        append_images=imagenes[1:]
    )
    return ruta_salida


if __name__ == "__main__":
    ruta = generar_favicon()
    print(f"Favicon generado: {ruta}")
