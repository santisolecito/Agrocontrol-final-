# Vista Insumos — usa tkcalendar en fecha de caducidad
FIELDS = [
    ("Código Insumo",      "entry", []),
    ("Nombre Comercial",   "entry", []),
    ("Tipo",               "combo", ["Semilla","Fertilizante","Plaguicida",
                                     "Herbicida","Fungicida","Otro"]),
    ("Unidad de Medida",   "combo", ["kg","litro","unidad","bulto","tonelada"]),
    ("Cantidad en Stock",  "entry", []),
    ("Ubicación Almacén",  "entry", []),
    ("Fecha de Caducidad", "date",  []),
    ("Precio Unitario",    "entry", []),
]
