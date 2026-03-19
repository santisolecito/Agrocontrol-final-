# Vista Cosechas — usa tkcalendar en campos de fecha
FIELDS = [
    ("Código Cosecha", "entry", []),
    ("Parcela ID",     "entry", []),
    ("Cultivo ID",     "entry", []),
    ("Fecha Inicio",   "date",  []),
    ("Fecha Fin",      "date",  []),
    ("Cantidad (kg)",  "entry", []),
    ("Calidad",        "combo", ["Alta","Media","Baja","Premium",
                                 "Primera","Segunda","Tercera"]),
    ("Método Cosecha", "combo", ["Manual","Mecanizada","Semi-mecanizada"]),
]
