from config.database import ejecutar

# SQL base para consultar la tabla
_SQL = (
    "SELECT Finca_ID, Nombre, ubicacion, Hectareas, "
    "altitud, Temperatura, tipo_suelo, region FROM Fincas"
)


class FincaModel:
    """Capa de acceso a datos para la entidad Finca."""

    @staticmethod
    def get_all():
        return ejecutar(_SQL, fetch=True)

    @staticmethod
    def insert(nombre, ubicacion, latitud, longitud,
               hectareas, altitud, temperatura, tipo_suelo, region):
        params = (nombre, ubicacion, latitud, longitud,
                  hectareas, altitud, temperatura, tipo_suelo, region)
        return ejecutar("CALL sp_InsertFinca(%s,%s,%s,%s,%s,%s,%s,%s,%s)", params)

    @staticmethod
    def update(fid, nombre, ubicacion, latitud, longitud,
               hectareas, altitud, temperatura, tipo_suelo, region):
        params = (fid, nombre, ubicacion, latitud, longitud,
                  hectareas, altitud, temperatura, tipo_suelo, region)
        return ejecutar("CALL sp_UpdateFinca(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", params)

    @staticmethod
    def delete(fid):
        return ejecutar("CALL sp_DeleteFinca(%s)", (fid,))
