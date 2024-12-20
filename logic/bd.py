import pandas as pd
from sqlalchemy import create_engine
import platform
from sqlalchemy.sql import text
from sqlalchemy.orm import Session

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

def consultar_nombre_insensible(nombre, base_datos):
    """Consulta si hay un nombre igual en la base de datos, insensible a mayúsculas y minúsculas."""
    # Asegurarse de que el nombre esté en minúsculas para la comparación
    query = f"""
    SELECT * FROM erp.{base_datos}
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

def cerrar_actividad(id_activity, date_end, datemodified, modifyby):
    """
    Cierra una actividad realizando las actualizaciones, inserciones y eliminaciones necesarias de forma atómica,
    y verifica que el miembro no tenga más actividades abiertas para actualizar su disponibilidad.
    """
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return 0, "No se pudo establecer la conexión a la base de datos."

    try:
        with connection.begin() as transaction:
            # Actualizar fecha de fin de la actividad
            connection.execute(text(f"""
                UPDATE actividad 
                SET fecha_fin = '{date_end}' 
                WHERE idActividad = '{id_activity}';
            """))

            # Insertar en actividad_hist
            connection.execute(text(f"""
                INSERT INTO actividad_hist 
                SELECT a.idActividad, a.nombre, a.fecha_inicio, a.fecha_fin, a.descripcion, a.acciones_realizadas, a.tipo, 
                       c.idCliente, c.nombre, c.telefono, c.email, 
                       m.idMiembro, m.nombre, m.telefono, m.email 
                FROM actividad a 
                INNER JOIN cliente c ON a.idCliente = c.idCliente 
                INNER JOIN miembro m ON a.idMiembro = m.idMiembro 
                WHERE idActividad = '{id_activity}';
            """))

            # Obtener el miembro asociado a la actividad
            result = connection.execute(text(f"""
                SELECT idMiembro 
                FROM actividad 
                WHERE idActividad = '{id_activity}';
            """))
            miembro_id = result.scalar()

            # Insertar en recurso_hist si no existe
            connection.execute(text(f"""
                INSERT INTO recurso_hist (idRecurso, nombre, tipo, descripcion, no_serie)
                SELECT r.idRecurso, r.nombre, r.tipo, r.descripcion, r.no_serie 
                FROM recurso r 
                INNER JOIN actividad_has_recurso ahr ON r.idRecurso = ahr.idRecurso 
                WHERE ahr.idActividad = '{id_activity}' 
                AND NOT EXISTS (
                    SELECT 1 
                    FROM recurso_hist rh 
                    WHERE rh.idRecurso = r.idRecurso
                );
            """))

            # Actualizar factura
            connection.execute(text(f"""
                UPDATE factura 
                SET fecha_modificacion = '{datemodified}', 
                    modificado_por = '{modifyby}', 
                    estatus = 'Cerrada' 
                WHERE idActividad = '{id_activity}';
            """))

            # Insertar en factura_hist
            connection.execute(text(f"""
                INSERT INTO factura_hist 
                SELECT idFactura, nombre, fecha_emision, costo, tipo, impuesto, estatus, 
                       creado_por, fecha_modificacion, modificado_por, idActividad 
                FROM factura 
                WHERE idActividad = '{id_activity}';
            """))

            # Insertar en actividad_has_recurso_hist
            connection.execute(text(f"""
                INSERT INTO actividad_has_recurso_hist 
                SELECT * 
                FROM actividad_has_recurso 
                WHERE idActividad = '{id_activity}';
            """))

            # Comprobar si el miembro tiene más actividades abiertas
            result = connection.execute(text(f"""
                SELECT COUNT(*) 
                FROM actividad 
                WHERE idMiembro = '{miembro_id}' AND fecha_fin IS NULL;
            """))
            actividades_abiertas = result.scalar()

            # Si no tiene más actividades abiertas, actualizar el estado del miembro
            if actividades_abiertas == 0:
                connection.execute(text(f"""
                    UPDATE miembro 
                    SET disponibilidad = 'Disponible', estatus = 'Libre' 
                    WHERE idMiembro = '{miembro_id}';
                """))
                print(f"El miembro {miembro_id} ahora está disponible.")

            # Eliminar registros de tablas originales
            connection.execute(text(f"""
                DELETE FROM factura 
                WHERE idActividad = '{id_activity}';
            """))

            connection.execute(text(f"""
                DELETE FROM actividad_has_recurso 
                WHERE idActividad = '{id_activity}';
            """))

            connection.execute(text(f"""
                DELETE FROM actividad 
                WHERE idActividad = '{id_activity}';
            """))

            return 1, "Transacción completada con éxito."

    except Exception as e:
        # Rollback automático al salir del bloque si hay un error
        print("Error al ejecutar la transacción:", e)
        return 0, f"Error al ejecutar la transacción: {e}"

    finally:
        cerrarConexion(connection)


