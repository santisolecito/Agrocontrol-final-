"""
views/base_view.py
Helpers visuales reutilizables. Soporta temas claro/oscuro,
campos entry/combo/date(tkcalendar)/image, y botones con iconos.
"""
import tkinter as tk
from tkinter import ttk

# ── Temas ──────────────────────────────────────────────────────────────────
_TEMAS = {
    "claro": {
        "BG":           "#f0f4f0",
        "FORM_BG":      "#f0f4f0",
        "ENTRY_BG":     "#ffffff",
        "ENTRY_FG":     "#1a2e1a",
        "LABEL_FG":     "#1a2e1a",
        "HEADER_BG":    "#2d5a27",
        "HEADER_FG":    "#ffffff",
        "TAB_BG":       "#4a7c43",
        "TAB_SEL":      "#f0f4f0",
        "TAB_SEL_FG":   "#2d5a27",
        "BTN_FRAME":    "#f0f4f0",
        "TREE_EVEN":    "#ffffff",
        "TREE_ODD":     "#eef4ee",
        "TREE_SEL":     "#4a7c43",
        "TREE_SEL_FG":  "#ffffff",
        "SEARCH_FG":    "#2d5a27",
        "ACENTO":       "#2d5a27",
    },
    "oscuro": {
        "BG":           "#1e2b1e",
        "FORM_BG":      "#1e2b1e",
        "ENTRY_BG":     "#2a3d2a",
        "ENTRY_FG":     "#c8e6c9",
        "LABEL_FG":     "#c8e6c9",
        "HEADER_BG":    "#0d1f0d",
        "HEADER_FG":    "#90EE90",
        "TAB_BG":       "#2a4a2a",
        "TAB_SEL":      "#1e2b1e",
        "TAB_SEL_FG":   "#90EE90",
        "BTN_FRAME":    "#1e2b1e",
        "TREE_EVEN":    "#2a3d2a",
        "TREE_ODD":     "#243024",
        "TREE_SEL":     "#4CAF50",
        "TREE_SEL_FG":  "#ffffff",
        "SEARCH_FG":    "#90EE90",
        "ACENTO":       "#4CAF50",
    },
}
_tema_actual = "claro"

def set_tema(nombre: str):
    global _tema_actual
    if nombre in _TEMAS:
        _tema_actual = nombre

def get_tema() -> dict:
    return _TEMAS[_tema_actual]

def BG():
    return get_tema()["BG"]


# ── Helpers de campo ───────────────────────────────────────────────────────
LABEL_FONT = ("Segoe UI", 11)
ENTRY_FONT = ("Segoe UI", 11)
TITLE_FONT = ("Segoe UI", 14, "bold")

def make_label_entry(parent, row, text, width=26):
    t = get_tema()
    tk.Label(parent, text=text, font=LABEL_FONT,
             bg=t["FORM_BG"], fg=t["LABEL_FG"], anchor="w"
             ).grid(row=row, column=0, sticky="w", padx=(0,8), pady=5)
    e = tk.Entry(parent, width=width, font=ENTRY_FONT,
                 bg=t["ENTRY_BG"], fg=t["ENTRY_FG"],
                 insertbackground=t["ENTRY_FG"], relief="solid", bd=1)
    e.grid(row=row, column=1, sticky="w", pady=5)
    return e

def make_label_combo(parent, row, text, values, width=24):
    t = get_tema()
    tk.Label(parent, text=text, font=LABEL_FONT,
             bg=t["FORM_BG"], fg=t["LABEL_FG"], anchor="w"
             ).grid(row=row, column=0, sticky="w", padx=(0,8), pady=5)
    c = ttk.Combobox(parent, values=values, width=width,
                     font=ENTRY_FONT, state="readonly")
    c.grid(row=row, column=1, sticky="w", pady=5)
    return c

def make_label_date(parent, row, text):
    """Campo de fecha con tkcalendar (DateEntry) como campo flotante."""
    t = get_tema()
    tk.Label(parent, text=text, font=LABEL_FONT,
             bg=t["FORM_BG"], fg=t["LABEL_FG"], anchor="w"
             ).grid(row=row, column=0, sticky="w", padx=(0,8), pady=5)
    try:
        from tkcalendar import DateEntry
        cal = DateEntry(parent, width=23, font=ENTRY_FONT,
                        date_pattern="yyyy-mm-dd",
                        background="#2d5a27", foreground="white",
                        headersbackground="#1a3c1a", headersforeground="white",
                        selectbackground="#4a7c43", selectforeground="white",
                        normalbackground=t["ENTRY_BG"],
                        normalforeground=t["ENTRY_FG"])
        cal.grid(row=row, column=1, sticky="w", pady=5)
        return cal
    except ImportError:
        # Fallback a Entry si tkcalendar no está instalado
        e = tk.Entry(parent, width=26, font=ENTRY_FONT,
                     bg=t["ENTRY_BG"], fg=t["ENTRY_FG"],
                     insertbackground=t["ENTRY_FG"], relief="solid", bd=1)
        e.grid(row=row, column=1, sticky="w", pady=5)
        return e


# ── Lectura / escritura de widgets ─────────────────────────────────────────
def clear_entries(entries: dict):
    for w in entries.values():
        if isinstance(w, tk.Entry):       w.delete(0, tk.END)
        elif isinstance(w, tk.Text):      w.delete("1.0", tk.END)
        elif isinstance(w, ttk.Combobox): w.set("")
        elif hasattr(w, "set_date"):      # DateEntry de tkcalendar
            from datetime import date
            w.set_date(date.today())

def get_val(entries: dict, key: str) -> str:
    w = entries[key]
    if isinstance(w, tk.Text):
        return w.get("1.0", tk.END).strip()
    if hasattr(w, "get_date"):  # DateEntry
        return str(w.get_date())
    return w.get().strip()

def set_val(entries: dict, key: str, value):
    if key not in entries:
        return
    w = entries[key]
    v = str(value) if value is not None else ""
    if isinstance(w, tk.Entry):
        w.delete(0, tk.END); w.insert(0, v)
    elif isinstance(w, tk.Text):
        w.delete("1.0", tk.END); w.insert("1.0", v)
    elif isinstance(w, ttk.Combobox):
        w.set(v)
    elif hasattr(w, "set_date"):
        try:
            from datetime import datetime
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S"):
                try:
                    w.set_date(datetime.strptime(v[:10], fmt[:8]).date())
                    return
                except Exception:
                    continue
        except Exception:
            pass

def get_tree_data(tree):
    """Retorna (columnas, filas) visibles en el Treeview."""
    cols  = list(tree["columns"])
    filas = [tree.item(iid, "values") for iid in tree.get_children()]
    return cols, filas


# ── Constructor de panel ───────────────────────────────────────────────────
def build_panel(tab, title, fields, color="#2d5a27",
                imagen_keys: list = None):
    """
    Construye el panel dividido formulario / tabla.
    imagen_keys: lista de nombres de campos tipo 'image' para añadir widget Pillow.
    """
    t = get_tema()
    bg = t["BG"]

    btn_frame = tk.Frame(tab, bg=bg)
    btn_frame.pack(side="bottom", fill="x", pady=8)
    tk.Frame(tab, bg="#cccccc", height=1).pack(side="bottom", fill="x")

    paned = tk.PanedWindow(tab, orient="horizontal", bg=bg, sashwidth=6, bd=0)
    paned.pack(fill="both", expand=True)

    # ── Izquierda: formulario ──────────────────────────────────────────
    left_outer = tk.Frame(paned, bg=bg)
    paned.add(left_outer, minsize=440)
    canvas = tk.Canvas(left_outer, bg=bg, highlightthickness=0)
    scrollbar = ttk.Scrollbar(left_outer, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=bg)
    scroll_frame.bind("<Configure>",
                      lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0,0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tk.Label(scroll_frame, text=title, font=TITLE_FONT,
             fg=color, bg=bg).pack(pady=(14,4))
    tk.Frame(scroll_frame, bg=color, height=2).pack(fill="x", padx=20, pady=(0,10))

    form = tk.Frame(scroll_frame, bg=bg)
    form.pack(pady=4, anchor="w", padx=20)

    entries = {}
    img_estados = {}   # para campos de imagen

    for i, (name, ftype, opts) in enumerate(fields):
        if ftype == "entry":
            entries[name] = make_label_entry(form, i, name + ":")
        elif ftype == "combo":
            entries[name] = make_label_combo(form, i, name + ":", opts)
        elif ftype == "date":
            entries[name] = make_label_date(form, i, name + ":")
        elif ftype == "image":
            # Widget de imagen con Pillow
            from utils.imagen_handler import widget_imagen
            tk.Label(form, text=name + ":", font=LABEL_FONT,
                     bg=bg, fg=t["LABEL_FG"], anchor="w"
                     ).grid(row=i, column=0, sticky="nw", padx=(0,8), pady=5)
            frm_img, lbl_img, estado = widget_imagen(form)
            frm_img.grid(row=i, column=1, sticky="w", pady=5)
            entries[name]     = lbl_img   # el Label actúa de proxy
            img_estados[name] = estado    # {"ruta": ..., "photo": ...}

    # Adjuntar estados de imagen al diccionario entries para acceso externo
    entries["__img_estados__"] = img_estados

    # ── Derecha: tabla con buscador ────────────────────────────────────
    right = tk.Frame(paned, bg=bg)
    paned.add(right, minsize=500)

    search_bar = tk.Frame(right, bg=bg)
    search_bar.pack(fill="x", padx=12, pady=(14,4))
    tk.Label(search_bar, text="🔍 Buscar:", font=("Segoe UI",10,"bold"),
             bg=bg, fg=t["SEARCH_FG"]).pack(side="left")
    search_var = tk.StringVar()
    tk.Entry(search_bar, textvariable=search_var, font=("Segoe UI",10),
             width=28, relief="solid", bd=1,
             bg=t["ENTRY_BG"], fg=t["ENTRY_FG"],
             insertbackground=t["ENTRY_FG"]).pack(side="left", padx=8)
    tk.Label(search_bar, text="Registros:", font=("Segoe UI",10),
             bg=bg, fg="#666").pack(side="right", padx=(0,4))
    count_label = tk.Label(search_bar, text="0",
                            font=("Segoe UI",10,"bold"),
                            bg=bg, fg=t["SEARCH_FG"])
    count_label.pack(side="right")

    tree_frame = tk.Frame(right, bg=bg)
    tree_frame.pack(fill="both", expand=True, padx=12, pady=(0,8))
    tree = ttk.Treeview(tree_frame, show="headings", selectmode="browse")
    vsb  = ttk.Scrollbar(tree_frame, orient="vertical",   command=tree.yview)
    hsb  = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    tree_frame.rowconfigure(0, weight=1)
    tree_frame.columnconfigure(0, weight=1)
    tree._count_label = count_label
    tree._search_var  = search_var

    paned.update_idletasks()
    try:
        paned.sash_place(0, 450, 0)
    except Exception:
        pass

    return scroll_frame, entries, tree, search_var, btn_frame


def load_tree(tree, rows, cols, filter_text=""):
    t = get_tema()
    tree["columns"] = cols
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=max(90, len(col)*10), minwidth=60)
    tree.delete(*tree.get_children())
    fl = filter_text.lower()
    count = 0
    for row in rows:
        values = [str(v) if v is not None else "" for v in row]
        if fl and not any(fl in v.lower() for v in values):
            continue
        tree.insert("", "end", values=values,
                    tags=("even" if count % 2 == 0 else "odd",))
        count += 1
    tree.tag_configure("even", background=t["TREE_EVEN"])
    tree.tag_configure("odd",  background=t["TREE_ODD"])
    tree._count_label.config(text=str(count))


def make_buttons(parent, save_cmd, update_cmd, delete_cmd,
                 clear_cmd, refresh_cmd=None,
                 excel_cmd=None, pdf_cmd=None):
    t = get_tema()
    bg = t["BTN_FRAME"]

    frame = tk.Frame(parent, bg=bg)
    frame.pack(pady=10)

    # Fila 1 — CRUD
    row1 = tk.Frame(frame, bg=bg)
    row1.pack()
    crud = [
        ("💾 Guardar",    "#4CAF50", save_cmd),
        ("✏️ Actualizar", "#2196F3", update_cmd),
        ("🗑️ Eliminar",  "#f44336", delete_cmd),
        ("🧹 Limpiar",   "#FF9800", clear_cmd),
    ]
    if refresh_cmd:
        crud.append(("🔄 Actualizar", "#607D8B", refresh_cmd))
    for txt, bc, cmd in crud:
        tk.Button(row1, text=txt, font=("Segoe UI",10,"bold"),
                  bg=bc, fg="white", padx=10, pady=5,
                  relief="flat", cursor="hand2",
                  command=cmd).pack(side="left", padx=4)

    # Fila 2 — Exportación
    if excel_cmd or pdf_cmd:
        row2 = tk.Frame(frame, bg=bg)
        row2.pack(pady=(6,0))
        if excel_cmd:
            tk.Button(row2, text="📊 Exportar Excel",
                      font=("Segoe UI",10,"bold"),
                      bg="#1B5E20", fg="white", padx=10, pady=5,
                      relief="flat", cursor="hand2",
                      command=excel_cmd).pack(side="left", padx=4)
        if pdf_cmd:
            tk.Button(row2, text="📄 Exportar PDF",
                      font=("Segoe UI",10,"bold"),
                      bg="#B71C1C", fg="white", padx=10, pady=5,
                      relief="flat", cursor="hand2",
                      command=pdf_cmd).pack(side="left", padx=4)
