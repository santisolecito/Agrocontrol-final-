"""
utils/imagen_handler.py
Manejo profesional de imágenes con Pillow.
"""
import os
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageEnhance

FORMATOS_OK   = (".jpg", ".jpeg", ".png", ".gif")
TAMANO_MAX_MB = 5
MINIATURA_DEF = (180, 180)


def seleccionar_imagen() -> str | None:
    """Abre diálogo y valida formato y tamaño. Retorna ruta o None."""
    ruta = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[
            ("Imágenes", "*.jpg *.jpeg *.png *.gif"),
            ("JPEG", "*.jpg *.jpeg"),
            ("PNG",  "*.png"),
            ("GIF",  "*.gif"),
            ("Todos los archivos", "*.*"),
        ]
    )
    if not ruta:
        return None

    ext = os.path.splitext(ruta)[1].lower()
    if ext not in FORMATOS_OK:
        messagebox.showerror("❌ Formato inválido",
                             f"Formato '{ext}' no soportado.\n"
                             f"Use: JPG, PNG o GIF.")
        return None

    mb = os.path.getsize(ruta) / (1024 * 1024)
    if mb > TAMANO_MAX_MB:
        messagebox.showerror("❌ Archivo muy grande",
                             f"El archivo pesa {mb:.1f} MB.\n"
                             f"Límite: {TAMANO_MAX_MB} MB.")
        return None

    return ruta


def cargar_miniatura(ruta: str,
                     tamaño: tuple = MINIATURA_DEF) -> ImageTk.PhotoImage | None:
    """Carga, redimensiona y retorna PhotoImage para un Label de Tkinter."""
    try:
        img = Image.open(ruta)
        img = img.convert("RGBA") if img.mode in ("P", "RGBA") else img.convert("RGB")
        img.thumbnail(tamaño, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        messagebox.showerror("❌ Error de imagen", f"No se pudo cargar:\n{e}")
        return None


def guardar_imagen(ruta_origen: str,
                   carpeta_destino: str,
                   nombre_archivo: str,
                   max_px: int = 800) -> str | None:
    """
    Redimensiona y guarda la imagen en carpeta_destino.
    Retorna la ruta final o None si falla.
    """
    os.makedirs(carpeta_destino, exist_ok=True)
    ext       = os.path.splitext(ruta_origen)[1].lower()
    ruta_dest = os.path.join(carpeta_destino, nombre_archivo + ext)
    try:
        img = Image.open(ruta_origen)
        # Redimensionar si supera max_px en cualquier lado
        if max(img.size) > max_px:
            img.thumbnail((max_px, max_px), Image.LANCZOS)
        # Conversión de formato para guardar correctamente
        if ext in (".jpg", ".jpeg"):
            img = img.convert("RGB")
            img.save(ruta_dest, "JPEG", quality=90)
        elif ext == ".png":
            img = img.convert("RGBA")
            img.save(ruta_dest, "PNG")
        elif ext == ".gif":
            img.save(ruta_dest, "GIF")
        return ruta_dest
    except Exception as e:
        messagebox.showerror("❌ Error al guardar", str(e))
        return None


def convertir_formato(ruta_origen: str, formato_destino: str = "PNG") -> str | None:
    """Convierte imagen a otro formato. Retorna la ruta convertida."""
    try:
        img  = Image.open(ruta_origen)
        base = os.path.splitext(ruta_origen)[0]
        ext  = formato_destino.lower()
        ruta_dest = f"{base}_convertida.{ext}"
        if formato_destino == "JPEG":
            img = img.convert("RGB")
        img.save(ruta_dest, formato_destino)
        messagebox.showinfo("✅ Convertida",
                            f"Imagen guardada como {formato_destino}:\n{ruta_dest}")
        return ruta_dest
    except Exception as e:
        messagebox.showerror("❌ Error al convertir", str(e))
        return None


def aplicar_filtro(ruta: str, filtro: str = "BLUR") -> Image.Image | None:
    """
    Aplica un filtro a la imagen y retorna el objeto Image.
    filtros: BLUR, SHARPEN, CONTOUR, DETAIL, EDGE_ENHANCE
    """
    filtros = {
        "BLUR":         ImageFilter.BLUR,
        "SHARPEN":      ImageFilter.SHARPEN,
        "CONTOUR":      ImageFilter.CONTOUR,
        "DETAIL":       ImageFilter.DETAIL,
        "EDGE_ENHANCE": ImageFilter.EDGE_ENHANCE,
    }
    try:
        img = Image.open(ruta)
        if filtro in filtros:
            img = img.filter(filtros[filtro])
        return img
    except Exception as e:
        messagebox.showerror("❌ Filtro", str(e))
        return None


def widget_imagen(parent, tamaño=(180, 180)):
    """
    Crea y retorna un Frame con Label de imagen + botón Seleccionar.
    Uso: frame, label_img, var_ruta = widget_imagen(parent_frame)
    """
    import tkinter as tk
    from tkinter import ttk

    estado = {"ruta": None, "photo": None}

    frame = tk.Frame(parent, bg=parent.cget("bg"),
                     relief="solid", bd=1, pady=4)

    lbl_img = tk.Label(frame, text="📷 Sin imagen",
                       font=("Segoe UI", 9), bg="#e8f0e8",
                       width=tamaño[0]//7, height=tamaño[1]//16,
                       relief="flat", cursor="hand2")
    lbl_img.pack(padx=6, pady=(6, 2))

    def _seleccionar():
        ruta = seleccionar_imagen()
        if not ruta:
            return
        photo = cargar_miniatura(ruta, tamaño)
        if photo:
            estado["ruta"]  = ruta
            estado["photo"] = photo
            lbl_img.config(image=photo, text="", bg="white")
            lbl_img.image = photo  # evitar GC

    tk.Button(frame, text="🖼️ Seleccionar imagen",
              font=("Segoe UI", 9, "bold"),
              bg="#4A7C43", fg="white", relief="flat",
              cursor="hand2", command=_seleccionar).pack(padx=6, pady=(2, 6))

    return frame, lbl_img, estado
