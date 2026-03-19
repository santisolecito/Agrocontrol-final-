import os
import tkinter as tk
from tkinter import ttk
import mysql.connector
from config.db_config import DB_CONFIG
import views.base_view as bv

_FAVICON = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "assets", "favicon.ico")


class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x800")
        self.minsize(1100, 650)
        self.title("AgroControl — Campos Fértiles S.A.")
        self._setup_favicon()
        self._build_header()
        self._build_notebook()
        self._load_controllers()
        self._aplicar_tema("claro")

    # ── Favicon ────────────────────────────────────────────────────────────
    def _setup_favicon(self):
        if not os.path.exists(_FAVICON):
            try:
                from utils.favicon_gen import generar_favicon
                generar_favicon(_FAVICON)
            except Exception as e:
                print(f"Favicon no generado: {e}")
        if os.path.exists(_FAVICON):
            try:
                self.iconbitmap(_FAVICON)
            except Exception:
                pass

    # ── Tema ───────────────────────────────────────────────────────────────
    def _aplicar_tema(self, nombre: str):
        bv.set_tema(nombre)
        t = bv.get_tema()
        self.configure(bg=t["BG"])

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook",
                        background=t["HEADER_BG"], tabmargins=[2, 5, 2, 0])
        style.configure("TNotebook.Tab",
                        background=t["TAB_BG"], foreground=t["HEADER_FG"],
                        padding=[12, 6], font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", t["TAB_SEL"])],
                  foreground=[("selected", t["TAB_SEL_FG"])])
        style.configure("TFrame", background=t["BG"])
        style.configure("Treeview",
                        font=("Segoe UI", 10), rowheight=26,
                        background=t["TREE_EVEN"], foreground=t["ENTRY_FG"],
                        fieldbackground=t["TREE_EVEN"])
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 10, "bold"),
                        background=t["HEADER_BG"], foreground=t["HEADER_FG"])
        style.map("Treeview",
                  background=[("selected", t["TREE_SEL"])],
                  foreground=[("selected", t["TREE_SEL_FG"])])

        self._header.configure(bg=t["HEADER_BG"])
        self._lbl_titulo.configure(bg=t["HEADER_BG"], fg=t["HEADER_FG"])
        self._conn_label.configure(bg=t["HEADER_BG"])
        self._frm_tema.configure(bg=t["HEADER_BG"])
        self._lbl_tema.configure(bg=t["HEADER_BG"], fg=t["HEADER_FG"])

    # ── Header ─────────────────────────────────────────────────────────────
    def _build_header(self):
        self._header = tk.Frame(self, bg="#2d5a27", height=60)
        self._header.pack(fill="x")
        self._header.pack_propagate(False)

        self._lbl_titulo = tk.Label(
            self._header, text="🌿 AGROCONTROL — Campos Fértiles S.A.",
            font=("Segoe UI", 16, "bold"), bg="#2d5a27", fg="white")
        self._lbl_titulo.pack(side="left", padx=20, pady=12)

        # Selector de tema
        self._frm_tema = tk.Frame(self._header, bg="#2d5a27")
        self._frm_tema.pack(side="right", padx=14)
        self._lbl_tema = tk.Label(self._frm_tema, text="🎨 Tema:",
                                  font=("Segoe UI", 10, "bold"),
                                  bg="#2d5a27", fg="white")
        self._lbl_tema.pack(side="left")
        tk.Button(self._frm_tema, text="☀️ Claro",
                  font=("Segoe UI", 9, "bold"), bg="#97BC62", fg="#1A3C1A",
                  relief="flat", cursor="hand2", padx=8, pady=3,
                  command=lambda: self._aplicar_tema("claro")
                  ).pack(side="left", padx=4)
        tk.Button(self._frm_tema, text="🌙 Oscuro",
                  font=("Segoe UI", 9, "bold"), bg="#1A3C1A", fg="#90EE90",
                  relief="flat", cursor="hand2", padx=8, pady=3,
                  command=lambda: self._aplicar_tema("oscuro")
                  ).pack(side="left", padx=4)

        # Estado de conexión a BD
        self._conn_label = tk.Label(self._header, font=("Segoe UI", 10),
                                    bg="#2d5a27")
        self._conn_label.pack(side="right", padx=16)
        try:
            _c = mysql.connector.connect(**DB_CONFIG)
            _c.close()
            self._conn_label.config(text="🟢 Conectado a agrocontrol",
                                    fg="#90EE90")
        except Exception:
            self._conn_label.config(text="🔴 Sin conexión a BD",
                                    fg="#FF6B6B")

    # ── Notebook ───────────────────────────────────────────────────────────
    def _build_notebook(self):
        self._notebook = ttk.Notebook(self)
        self._notebook.pack(expand=True, fill="both", padx=10, pady=10)
        self._tabs = {}
        for key, label in [
            ("fincas",     "  🌿 Fincas  "),
            ("cultivos",   "  🌱 Cultivos  "),
            ("insumos",    "  🧪 Insumos  "),
            ("maquinaria", "  🚜 Maquinaria  "),
            ("empleados",  "  👷 Empleados  "),
            ("cosechas",   "  🌾 Cosechas  "),
            ("clientes",   "  🤝 Clientes  "),
        ]:
            frame = ttk.Frame(self._notebook)
            self._notebook.add(frame, text=label)
            self._tabs[key] = frame

    # ── Controllers ────────────────────────────────────────────────────────
    def _load_controllers(self):
        from controllers.finca_controller      import FincaController
        from controllers.cultivo_controller    import CultivoController
        from controllers.insumo_controller     import InsumoController
        from controllers.maquinaria_controller import MaquinariaController
        from controllers.empleado_controller   import EmpleadoController
        from controllers.cosecha_controller    import CosechaController
        from controllers.cliente_controller    import ClienteController

        FincaController(self._tabs["fincas"])
        CultivoController(self._tabs["cultivos"])
        InsumoController(self._tabs["insumos"])
        MaquinariaController(self._tabs["maquinaria"])
        EmpleadoController(self._tabs["empleados"])
        CosechaController(self._tabs["cosechas"])
        ClienteController(self._tabs["clientes"])