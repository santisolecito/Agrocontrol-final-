from config.database import ejecutar

SQL = ("SELECT Codigo_id, nombre_comercial, Tipo, unidad_medida, "
       "cantidad_stok, ubicacion, fecha_caducidad, precio FROM inventario")

class InsumoModel:
    @staticmethod
    def get_all():
        return ejecutar(SQL, fetch=True)

    @staticmethod
    def insert(nombre, tipo, unidad, ubicacion, cantidad, caducidad, precio):
        return ejecutar("CALL sp_InsertInsumo(%s,%s,%s,%s,%s,%s,%s)",
                        (nombre, tipo, unidad, ubicacion, cantidad, caducidad, precio))

    @staticmethod
    def update(iid, nombre, tipo, unidad, ubicacion, cantidad, caducidad, precio):
        return ejecutar("CALL sp_UpdateInsumo(%s,%s,%s,%s,%s,%s,%s,%s)",
                        (iid, nombre, tipo, unidad, ubicacion, cantidad, caducidad, precio))

    @staticmethod
    def delete(iid):
        return ejecutar("CALL sp_DeleteInsumo(%s)", (iid,))
