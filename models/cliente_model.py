from config.database import ejecutar

SQL = ("SELECT cliente_id, nombre, RUC_o_DNI, direccion_fiscal, "
       "telefono, correo_electronico, linea_credito FROM clientes")

class ClienteModel:
    @staticmethod
    def get_all():
        return ejecutar(SQL, fetch=True)

    @staticmethod
    def insert(nombre, ruc, direccion, telefono, correo, credito):
        return ejecutar("CALL sp_InsertCliente(%s,%s,%s,%s,%s,%s)",
                        (nombre, ruc, direccion, telefono, correo, credito))

    @staticmethod
    def update(cid, nombre, ruc, direccion, telefono, correo, credito):
        return ejecutar("CALL sp_UpdateCliente(%s,%s,%s,%s,%s,%s,%s)",
                        (cid, nombre, ruc, direccion, telefono, correo, credito))

    @staticmethod
    def delete(cid):
        return ejecutar("CALL sp_DeleteCliente(%s)", (cid,))
