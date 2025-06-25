from conexion import Conexion


class Empleado:

    def __init__(self):
        self.id = 0
        self.nombre = ""
        self.apellido = ""
        self.edad = ""
        self.correo = ""
        self.direccion = ""
        self.salario = 0.0
        self.con = Conexion()
        self.sql = ""

        
    def eliminar(self, id_empleado):
        try:
            conn = self.con.conectar()
            cursor = conn.cursor()
            sql = "DELETE FROM tb_empleados WHERE id = %s"
            cursor.execute(sql, (id_empleado,))
            conn.commit()
            conn.close()
            return cursor.rowcount == 1
        except Exception as e:
            print(f"Error al eliminar: {e}")
            return False
