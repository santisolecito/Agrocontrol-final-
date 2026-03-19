import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

VERDE_OSCURO = colors.HexColor("#2C5F2D")
VERDE_MEDIO  = colors.HexColor("#4A7C43")
VERDE_CLARO  = colors.HexColor("#EEF4EE")

def _ventana_filtros_pdf(titulo, columnas, filas):
    resultado = {"filas": None, "desc": None}
    win = tk.Toplevel()
    win.title(f"Filtros — Exportar {titulo} a PDF")
    win.geometry("480x360")
    win.resizable(False, False)
    win.configure(bg="#f0f4f0")
    win.grab_set()
    BG = "#f0f4f0"

    header = tk.Frame(win, bg="#c0392b", height=45)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(header, text=f"📄 Exportar {titulo} a PDF",
             font=("Segoe UI", 12, "bold"), bg="#c0392b", fg="white"
             ).pack(pady=10)

    frm = tk.Frame(win, bg=BG)
    frm.pack(fill="x", padx=20, pady=10)

    tk.Label(frm, text="Filtrar por columna:", font=("Segoe UI", 10, "bold"), bg=BG
             ).grid(row=0, column=0, sticky="w", pady=4)
    col_var = tk.StringVar(value="(Sin filtro)")
    combo_col = ttk.Combobox(frm, textvariable=col_var,
                              values=["(Sin filtro)"] + list(columnas),
                              state="readonly", width=22)
    combo_col.grid(row=0, column=1, sticky="w", padx=8)

    tk.Label(frm, text="Valor a buscar:", font=("Segoe UI", 10, "bold"), bg=BG
             ).grid(row=1, column=0, sticky="w", pady=4)
    val_entry = tk.Entry(frm, width=25, font=("Segoe UI", 10), relief="solid", bd=1)
    val_entry.grid(row=1, column=1, sticky="w", padx=8)

    tk.Label(frm, text="─"*50, bg=BG, fg="#cccccc"
             ).grid(row=2, column=0, columnspan=2, pady=4)

    tk.Label(frm, text="Columna de fecha:", font=("Segoe UI", 10, "bold"), bg=BG
             ).grid(row=3, column=0, sticky="w", pady=4)
    fecha_col_var = tk.StringVar(value="(Ninguna)")
    combo_fecha = ttk.Combobox(frm, textvariable=fecha_col_var,
                                values=["(Ninguna)"] + list(columnas),
                                state="readonly", width=22)
    combo_fecha.grid(row=3, column=1, sticky="w", padx=8)

    tk.Label(frm, text="Desde (YYYY-MM-DD):", font=("Segoe UI", 10, "bold"), bg=BG
             ).grid(row=4, column=0, sticky="w", pady=4)
    desde_entry = tk.Entry(frm, width=16, font=("Segoe UI", 10), relief="solid", bd=1)
    desde_entry.grid(row=4, column=1, sticky="w", padx=8)

    tk.Label(frm, text="Hasta (YYYY-MM-DD):", font=("Segoe UI", 10, "bold"), bg=BG
             ).grid(row=5, column=0, sticky="w", pady=4)
    hasta_entry = tk.Entry(frm, width=16, font=("Segoe UI", 10), relief="solid", bd=1)
    hasta_entry.grid(row=5, column=1, sticky="w", padx=8)

    def aplicar():
        filas_f = list(filas)
        desc_parts = []
        col_sel = col_var.get()
        val_sel = val_entry.get().strip().lower()
        if col_sel != "(Sin filtro)" and val_sel:
            idx = list(columnas).index(col_sel)
            filas_f = [f for f in filas_f if val_sel in str(f[idx]).lower()]
            desc_parts.append(f"{col_sel}='{val_entry.get().strip()}'")
        col_fecha = fecha_col_var.get()
        desde_str = desde_entry.get().strip()
        hasta_str = hasta_entry.get().strip()
        if col_fecha != "(Ninguna)" and (desde_str or hasta_str):
            idx_f = list(columnas).index(col_fecha)
            def en_rango(fila):
                try:
                    val = str(fila[idx_f])[:10]
                    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
                        try:
                            fecha = datetime.strptime(val, fmt).date(); break
                        except ValueError: continue
                    else: return True
                    if desde_str:
                        if fecha < datetime.strptime(desde_str, "%Y-%m-%d").date(): return False
                    if hasta_str:
                        if fecha > datetime.strptime(hasta_str, "%Y-%m-%d").date(): return False
                    return True
                except Exception: return True
            filas_f = [f for f in filas_f if en_rango(f)]
            if desde_str: desc_parts.append(f"desde {desde_str}")
            if hasta_str: desc_parts.append(f"hasta {hasta_str}")
        if not filas_f:
            messagebox.showwarning("Sin resultados", "El filtro no devuelve registros."); return
        resultado["filas"] = filas_f
        resultado["desc"]  = " | Filtro: " + ", ".join(desc_parts) if desc_parts else ""
        win.destroy()

    def sin_filtro():
        resultado["filas"] = list(filas)
        resultado["desc"]  = ""
        win.destroy()

    btn_frame = tk.Frame(win, bg=BG)
    btn_frame.pack(side="bottom", pady=14)
    for txt, bg, cmd in [
        ("📄 Exportar con filtro", "#c0392b", aplicar),
        ("📋 Exportar todo",       "#2196F3", sin_filtro),
        ("✖ Cancelar",             "#9E9E9E", win.destroy),
    ]:
        tk.Button(btn_frame, text=txt, font=("Segoe UI", 10, "bold"),
                  bg=bg, fg="white", padx=10, pady=5, relief="flat",
                  cursor="hand2", command=cmd).pack(side="left", padx=5)

    win.wait_window()
    return resultado["filas"], resultado["desc"]


def exportar_pdf(titulo, columnas, filas):
    filas_f, desc_filtro = _ventana_filtros_pdf(titulo, columnas, filas)
    if filas_f is None:
        return
    ruta = filedialog.asksaveasfilename(
        defaultextension=".pdf", filetypes=[("PDF", "*.pdf")],
        title=f"Guardar {titulo}.pdf",
        initialfile=f"{titulo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )
    if not ruta:
        return

    doc = SimpleDocTemplate(ruta, pagesize=landscape(A4),
                             rightMargin=1.5*cm, leftMargin=1.5*cm,
                             topMargin=1.5*cm, bottomMargin=1.5*cm)
    estilos = getSampleStyleSheet()
    est_titulo = ParagraphStyle("T", parent=estilos["Title"],
                                 fontSize=15, textColor=VERDE_OSCURO, spaceAfter=4)
    est_sub    = ParagraphStyle("S", parent=estilos["Normal"],
                                 fontSize=9, textColor=colors.grey, spaceAfter=10)
    elementos = []
    elementos.append(Paragraph(f"AgroControl — Reporte de {titulo}{desc_filtro}", est_titulo))
    elementos.append(Paragraph(
        f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}  |  Registros: {len(filas_f)}",
        est_sub))
    elementos.append(Spacer(1, 0.3*cm))

    data = [list(columnas)] + [[str(v) if v is not None else "" for v in f] for f in filas_f]
    tabla = Table(data, repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND",      (0,0), (-1,0), VERDE_OSCURO),
        ("TEXTCOLOR",       (0,0), (-1,0), colors.white),
        ("FONTNAME",        (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",        (0,0), (-1,0), 9),
        ("ALIGN",           (0,0), (-1,0), "CENTER"),
        ("TOPPADDING",      (0,0), (-1,0), 7),
        ("BOTTOMPADDING",   (0,0), (-1,0), 7),
        ("ROWBACKGROUNDS",  (0,1), (-1,-1), [colors.white, VERDE_CLARO]),
        ("FONTNAME",        (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE",        (0,1), (-1,-1), 8),
        ("TOPPADDING",      (0,1), (-1,-1), 4),
        ("BOTTOMPADDING",   (0,1), (-1,-1), 4),
        ("GRID",            (0,0), (-1,-1), 0.4, colors.HexColor("#CCCCCC")),
        ("LINEBELOW",       (0,0), (-1,0), 1.5, VERDE_MEDIO),
        ("VALIGN",          (0,0), (-1,-1), "MIDDLE"),
    ]))
    elementos.append(tabla)
    doc.build(elementos)
    messagebox.showinfo("PDF exportado", f"✅ {len(filas_f)} registros guardados en:\n{ruta}")
