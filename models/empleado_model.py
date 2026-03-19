from config.database import ejecutar

SQL = ("SELECT empleados_id, DNI, nombres, apellidos, fecha_nacimiento, "
       "direccion, telefono, especialidad, fecha_contratacion, salario FROM empleados")

class EmpleadoModel:
    @staticmethod
    def get_all():
        return ejecutar(SQL, fetch=True)

    @staticmethod
    def insert(dni, nombres, apellidos, fec_nac, direccion, telefono, especialidad, fec_cont, salario):
        return ejecutar("CALL sp_InsertEmpleado(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (dni, nombres, apellidos, fec_nac, direccion, telefono, especialidad, fec_cont, salario))

    @staticmethod
    def update(eid, dni, nombres, apellidos, fec_nac, direccion, telefono, especialidad, fec_cont, salario):
        return ejecutar("CALL sp_UpdateEmpleado(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (eid, dni, nombres, apellidos, fec_nac, direccion, telefono, especialidad, fec_cont, salario))

    @staticmethod
    def delete(eid):
        return ejecutar("CALL sp_DeleteEmpleado(%s)", (eid,))
