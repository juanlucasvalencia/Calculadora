
import pyodbc

def connect():
    
    connection_string = (
        
        "DRIVER=ODBC Driver 17 for SQL Server;"
        "SERVER=192.168.1.78;" 
        "DATABASE=SamplerV3_ChemilabPru4;"
        "UID=samplerlogin;"
        "PWD=Ch3m1L4b231.*;"
        
    )
    
    conn = pyodbc.connect(connection_string)
    
    if conn:
        print("CONECTADO A LA BD")
    
    return conn.cursor()


connect()