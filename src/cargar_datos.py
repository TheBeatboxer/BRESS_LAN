import psycopg2
from psycopg2 import Error
from conexion import crear_conexion, ejecutar_consulta

def cargar_datos_postgres():
    """Función para cargar datos desde PostgreSQL"""
    try:
        conexion = crear_conexion()
        if conexion is not None:
            # Consulta con JOIN para obtener datos de clientes y planes
            consulta = """
                SELECT 
                    c.*, 
                    p.idplan, 
                    p.titulo, 
                    p.descripcion,
                    p.precio
                FROM 
                    clientes c
                JOIN 
                    planes p 
                ON 
                    c.idplan = p.idplan;
            """
            datos = ejecutar_consulta(conexion, consulta)
            return datos
        else:
            print("No se pudo conectar a la base de datos.")
            return []
    except Exception as e:
        print(f"Error cargando datos desde PostgreSQL: {e}")
        return []
    
datos = cargar_datos_postgres()
