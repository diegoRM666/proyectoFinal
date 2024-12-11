import pandas as pd
from sqlalchemy import create_engine
import platform
from sqlalchemy.sql import text

# Generar la conexión a la base de datos
def conectarBase():
    """Establece la conexión a la base de datos y la devuelve usando SQLAlchemy."""
    s_o = platform.system()
    try:
        if s_o == "Darwin":
            password = '15122121B'
        else:
            password = 'gogo219715122121B$'
        
        # Crear la URL de conexión de SQLAlchemy
        db_url = f"mysql+pymysql://root:{password}@localhost/erp"
        
        # Crear el motor de conexión con SQLAlchemy
        engine = create_engine(db_url)

        # Conectar al motor (esto también verifica si la conexión es válida)
        connection = engine.connect()
        
        print("Conectado a la base de datos MySQL con SQLAlchemy.")
        return connection

    except Exception as e:
        print("Error al conectar a MySQL:", e)
        return None

# Ejecutar una actualización
def actualizar(query):
    """Actualiza una o varias tablas en la base de datos y devuelve un mensaje de éxito o error."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."
    
    try:
        # Ejecuta la consulta de actualización
        with connection.begin():  # Asegura una transacción
            connection.execute(text(query))  # Envolver en 'text'
        msj = "Actualización exitosa."
        return 1, msj

    except Exception as e:
        print("Error al ejecutar la actualización:", e)
        msj = f"Error al ejecutar la actualización: {e}"
        return 0, msj

    finally:
        # Cierra la conexión si fue establecida
        cerrarConexion(connection)


# Hacer una consulta de datos
def consultar(query):
    """Ejecuta una consulta en la base de datos y devuelve los resultados en un DataFrame."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        # Ejecutar la consulta y obtener los resultados en un DataFrame usando pandas y SQLAlchemy
        df = pd.read_sql(query, connection)
        return df

    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

# Realizar una inserción
def insertar(query):
    """Inserta datos en la base de datos y devuelve un mensaje de éxito o error."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."
    
    try:
        # Ejecuta la consulta de inserción
        with connection.begin():  # Asegura una transacción
            connection.execute(text(query))  # Envolver la consulta en 'text'
        msj = "Inserción exitosa."
        return msj

    except Exception as e:
        print("Error al ejecutar la inserción:", e)
        msj = f"Error al ejecutar la inserción: {e}"
        return msj

    finally:
        # Cierra la conexión si fue establecida
        cerrarConexion(connection)

def consultar_nombre_insensible(nombre):
    """Consulta si hay un nombre igual en la base de datos, insensible a mayúsculas y minúsculas."""
    # Asegurarse de que el nombre esté en minúsculas para la comparación
    query = f"""
    SELECT * FROM erp.cliente
    WHERE nombre COLLATE utf8_general_ci = '{nombre}';
    """
    
    # Ejecutar la consulta usando la función consultar
    result = consultar(query)
    
    # Verificar si se encontraron resultados
    if isinstance(result, pd.DataFrame) and not result.empty:
        return True  # Se encontró el nombre
    return False  # No se encontró el nombre

def eliminar(query):
    """Elimina registros de la base de datos y devuelve un mensaje de éxito o error."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return 0, "No se pudo establecer la conexión a la base de datos."
    
    try:
        # Ejecutar la consulta de eliminación
        with connection.begin():  # Asegura una transacción
            connection.execute(text(query))  # Envolver la consulta en 'text'
        msj = "Eliminación exitosa."
        return 1, msj

    except Exception as e:
        print("Error al ejecutar la eliminación:", e)
        msj = f"Error al ejecutar la eliminación: {e}"
        return 0, msj

    finally:
        # Cierra la conexión si fue establecida
        cerrarConexion(connection)

# Cerrar la conexión de BD
def cerrarConexion(connection):
    """Cierra la conexión a la base de datos."""
    if connection is not None:
        connection.close()
        print("Conexión cerrada")
