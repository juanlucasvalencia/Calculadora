import mysql.connector 

class Conexion():
    def __init__(self):
        self.con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="crud"
        )
    def conectar(self):
        return self.con
    
    def buscar(self, id):
        conn = self.conectar()
        cursor = conn.cursor()
        consulta = "SELECT * FROM tb_empleados WHERE id = %s"
        cursor.execute(consulta, (id,))
        resultado = cursor.fetchall()
        cursor.close()
        return resultado
    
    def guardar_seguro(self, nombre, apellido, edad, correo, direccion, salario):
        try:
            conn = self.con.conectar()
            cursor = conn.cursor()
            self.sql = """
            INSERT INTO tb_empleados(nombre, apellido, edad, correo, direccion, salario)
            VALUES(%s, %s, %s, %s, %s, %s)
            """
            valores = (nombre, apellido, edad, correo, direccion, salario)
            cursor.execute(self.sql, valores)
            conn.commit()
            resp = cursor.rowcount
            conn.close()
            return resp == 1
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False
        


    def visualizar(self):
        try:
            conn = self.con.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tb_empleados")
            resultados = cursor. fetchall()
            conn.close()
            return resultados
        except Exception as e:
            print(f"Error al consultar_ {e}")
            return None