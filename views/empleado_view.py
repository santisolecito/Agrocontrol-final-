# Vista Empleados — incluye campo imagen y fechas con tkcalendar
FIELDS = [
    ("Código Empleado",    "entry", []),
    ("DNI",                "entry", []),
    ("Nombres",            "entry", []),
    ("Apellidos",          "entry", []),
    ("Fecha Nacimiento",   "date",  []),
    ("Dirección",          "entry", []),
    ("Teléfono",           "entry", []),
    ("Especialidad",       "combo", ["Agrónomo","Agrónoma","Operario",
                                     "Técnica agrícola","Administrador",
                                     "Conductor","Mecánico","Supervisora"]),
    ("Fecha Contratación", "date",  []),
    ("Salario",            "entry", []),
    ("Foto Empleado",      "image", []),
]
