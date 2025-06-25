from tkinter import *
from tkinter import ttk, messagebox
from conexion import Conexion
from empleado import Empleado

class Ventana(Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Empleados")
        self.state("zoomed")

        self.conn = Conexion()
        self.empleado = Empleado()

        # Búsqueda
        self.buscador = Entry(self)
        self.buscador.pack(pady=5)
        Button(self, text="Buscar", command=self.buscar_empleado).pack()

        # Tabla
        self.tree = ttk.Treeview(self, columns=("ID", "Nombre", "Apellido", "Edad", "Correo", "Direccion", "Salario"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=BOTH, expand=True)

        # Botones
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Editar", command=self.editar_empleado).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_empleado).grid(row=0, column=1, padx=10)

        self.cargar_datos()

    def cargar_datos(self):
        for fila in self.tree.get_children():
            self.tree.delete(fila)
        for fila in self.conn.visualizar():
            self.tree.insert("", END, values=fila)

    def buscar_empleado(self):
        id_buscar = self.buscador.get().strip()
        if not id_buscar.isdigit():
            messagebox.showerror("Error", "Por favor ingresa un ID válido.")
            return

        resultados = self.conn.buscar(int(id_buscar))

        for fila in self.tree.get_children():
            self.tree.delete(fila)

        if resultados:
            for fila in resultados:
                self.tree.insert("", END, values=fila)
        else:
            messagebox.showinfo("Sin resultados", "No se encontró ningún empleado con ese ID.")

    def eliminar_empleado(self):
        seleccion = self.tree.focus()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un empleado para eliminar.")
            return
        valores = self.tree.item(seleccion)["values"]
        id_empleado = valores[0]
        if messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este empleado?"):
            if self.empleado.eliminar(id_empleado):
                messagebox.showinfo("Éxito", "Empleado eliminado.")
                self.cargar_datos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el empleado.")

    def editar_empleado(self):
        seleccion = self.tree.focus()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un empleado para editar.")
            return
        valores = self.tree.item(seleccion)["values"]
        EditarVentana(self, valores, self.empleado, self.cargar_datos)

class EditarVentana(Toplevel):
    def __init__(self, parent, datos, empleado_modelo, callback):
        super().__init__(parent)
        self.title("Editar Empleado")
        self.empleado_modelo = empleado_modelo
        self.callback = callback
        self.id_empleado = datos[0]

        etiquetas = ["Nombre", "Apellido", "Edad", "Correo", "Direccion", "Salario"]
        self.entries = []

        for i, texto in enumerate(etiquetas):
            Label(self, text=texto).grid(row=i, column=0, padx=10, pady=5)
            entry = Entry(self)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(0, datos[i + 1])
            self.entries.append(entry)

        Button(self, text="Guardar Cambios", command=self.guardar_cambios).grid(row=len(etiquetas), column=0, columnspan=2, pady=10)

    def guardar_cambios(self):
        nuevos_datos = [entry.get().strip() for entry in self.entries]

        if not all(nuevos_datos):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        if not nuevos_datos[2].isdigit():
            messagebox.showerror("Error", "La edad debe ser un número.")
            return
        if "@" not in nuevos_datos[3] or "." not in nuevos_datos[3]:
            messagebox.showerror("Error", "Correo inválido.")
            return
        try:
            float(nuevos_datos[5])
        except ValueError:
            messagebox.showerror("Error", "El salario debe ser numérico.")
            return

        try:
            conn = self.empleado_modelo.con.conectar()
            cursor = conn.cursor()
            sql = """
            UPDATE tb_empleados
            SET nombre=%s, apellido=%s, edad=%s, correo=%s, direccion=%s, salario=%s
            WHERE id=%s
            """
            cursor.execute(sql, (*nuevos_datos, self.id_empleado))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Éxito", "Empleado actualizado.")
            self.callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")

def main():
    app = Ventana()
    app.mainloop()

if __name__ == "__main__":
    main()
