from config.database import ejecutar

SQL = ("SELECT codigo_maquina, marca, modelo, anio_fabricacion, "
       "potencia, tipo_combustible, horometro, estado FROM maquinaria")

class MaquinariaModel:
    @staticmethod
    def get_all():
        return ejecutar(SQL, fetch=True)

    @staticmethod
    def insert(marca, modelo, anio, potencia, combustible, horometro, estado):
        return ejecutar("CALL sp_InsertMaquinaria(%s,%s,%s,%s,%s,%s,%s)",
                        (marca, modelo, anio, potencia, combustible, horometro, estado))

    @staticmethod
    def update(mid, marca, modelo, anio, potencia, combustible, horometro, estado):
        return ejecutar("CALL sp_UpdateMaquinaria(%s,%s,%s,%s,%s,%s,%s,%s)",
                        (mid, marca, modelo, anio, potencia, combustible, horometro, estado))

    @staticmethod
    def delete(mid):
        return ejecutar("CALL sp_DeleteMaquinaria(%s)", (mid,))
