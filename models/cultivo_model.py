from config.database import ejecutar

SQL = ("SELECT cultivo_id, nombre_cientifico, nombre_comun, "
       "tiempo_crecimiento, temperatura_optima, agua FROM cultivos")

class CultivoModel:
    @staticmethod
    def get_all():
        return ejecutar(SQL, fetch=True)

    @staticmethod
    def insert(nombre_cientifico, nombre_comun, tiempo, temperatura, agua):
        return ejecutar("CALL sp_InsertCultivo(%s,%s,%s,%s,%s)",
                        (nombre_cientifico, nombre_comun, tiempo, temperatura, agua))

    @staticmethod
    def update(cid, nombre_cientifico, nombre_comun, tiempo, temperatura, agua):
        return ejecutar("CALL sp_UpdateCultivo(%s,%s,%s,%s,%s,%s)",
                        (cid, nombre_cientifico, nombre_comun, tiempo, temperatura, agua))

    @staticmethod
    def delete(cid):
        return ejecutar("CALL sp_DeleteCultivo(%s)", (cid,))
