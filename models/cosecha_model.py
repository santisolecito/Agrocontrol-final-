from config.database import ejecutar

SQL = ("SELECT cosecha_id, parcela, cultivo, inicio, fin, "
       "cantidad, calidad_producto, metodo_cosecha FROM cosecha")

class CosechaModel:
    @staticmethod
    def get_all():
        return ejecutar(SQL, fetch=True)

    @staticmethod
    def insert(parcela, cultivo, inicio, fin, cantidad, calidad, metodo):
        return ejecutar("CALL sp_InsertCosecha(%s,%s,%s,%s,%s,%s,%s)",
                        (parcela, cultivo, inicio, fin, cantidad, calidad, metodo))

    @staticmethod
    def update(hid, parcela, cultivo, inicio, fin, cantidad, calidad, metodo):
        return ejecutar("CALL sp_UpdateCosecha(%s,%s,%s,%s,%s,%s,%s,%s)",
                        (hid, parcela, cultivo, inicio, fin, cantidad, calidad, metodo))

    @staticmethod
    def delete(hid):
        return ejecutar("CALL sp_DeleteCosecha(%s)", (hid,))
