import openpyxl
from connect_db import connect

def insert_morfotipo():
    cursor = None
    try:
        cursor = connect()
        print("Conexión a la base de datos exitosa")
        
    except Exception as ex:
        print(f"Error conectando a la base de datos: {ex}")
        return
    
    try:
        # Cargar el archivo Excel
        book = openpyxl.load_workbook(r'C:\Users\Chemilab\Downloads\Bases_datos_HB_marino.xlsx')
        sheet = book['721_PASTOS']
        max_row = 796
        start_row = 2
        print("Archivo Excel cargado exitosamente")
        
    except Exception as ex:
        print(f"Error cargando Excel: {ex}")
        if cursor:
            cursor.close()
        return
    
    try:
        # Query de inserción
        insert_query = "INSERT INTO TAXPHYLUM (TAXPHILUM, IDTAXREINO) VALUES (?, 3)"
        
        # Contador para llevar registro de inserciones
        inserted_count = 0
        error_count = 0
        
        # Iterar sobre las filas desde start_row hasta max_row
        for row in range(start_row, max_row + 1):
            # Obtener el valor de la columna A
            cell_value = sheet[f'B{row}'].value
            
            # Verificar que el valor no sea None o vacío
            if cell_value is not None and str(cell_value).strip():
                try:
                    # Ejecutar la inserción
                    cursor.execute(insert_query, (str(cell_value).strip(),))
                    inserted_count += 1
                    
                    if inserted_count % 50 == 0:  # Mostrar progreso cada 50 registros
                        print(f"Insertados {inserted_count} registros...")
                        
                except Exception as ex:
                    print(f"Error insertando fila {row} (valor: {cell_value}): {ex}")
                    error_count += 1
            else:
                print(f"Fila {row}: Celda vacía o None, omitiendo...")
        
        # Confirmar los cambios
        cursor.commit()
        print(f"\nInserción completada:")
        print(f"- Registros insertados: {inserted_count}")
        print(f"- Errores: {error_count}")
        print(f"- Total filas procesadas: {max_row - start_row + 1}")
        
    except Exception as ex:
        print(f"Error durante la inserción: {ex}")
        if cursor:
            cursor.rollback()
    
    finally:
        # Cerrar conexiones
        if cursor:
            cursor.close()
            print("Conexión cerrada")

# Ejecutar la función
if __name__ == "__main__":
    insert_morfotipo()