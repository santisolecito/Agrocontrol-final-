# Vista Fincas — incluye campo imagen (requisito Pillow, mínimo 2 formularios)
FIELDS = [
    ("Código Finca",        "entry", []),
    ("Nombre",              "entry", []),
    ("Ubicación",           "entry", []),
    ("Latitud",             "entry", []),
    ("Longitud",            "entry", []),
    ("Extensión (ha)",      "entry", []),
    ("Altitud (msnm)",      "entry", []),
    ("Temp. Promedio (°C)", "entry", []),
    ("Tipo de Suelo",       "combo", ["Franco","Arcilloso","Arenoso",
                                      "Limoso","Franco-Arcilloso"]),
    ("Región",              "entry", []),
    ("Fotografía",          "image", []),
]
