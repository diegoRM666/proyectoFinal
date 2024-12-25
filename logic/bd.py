import pandas as pd
from sqlalchemy import create_engine
import platform
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import streamlit as st
import logic.utilities as ut

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
#def actualizar(query):
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
#def consultar(query):
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
#def insertar(query):
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

############################################################### Cliente ###############################################################
# Listo
def consultar_todos_clientes():
    """Ejecuta una consulta en la base de datos y devuelve todos los clientes."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        df = pd.read_sql("SELECT * FROM cliente", connection)
        return df

    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def insertar_cliente(name, phone, email, address, comments):
    """
    Verifica si un cliente existe e inserta uno nuevo si no existe, todo en una transacción.
    """
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False,"No se pudo establecer la conexión a la base de datos."

    try:
        with connection.begin() as transaction:
            # Verificar si el cliente ya existe
            query_existe = text(f"""
                SELECT 1 FROM cliente 
                WHERE nombre COLLATE utf8_general_ci = :name
                LIMIT 1;
            """)
            result = connection.execute(query_existe, {"name": name}).fetchone()

            if result:
                return False, "El cliente ya existe en la base de datos."

            # Insertar el nuevo cliente
            query_insert = text("""
                INSERT INTO cliente (nombre, telefono, email, direccion, notas)
                VALUES (:name, :phone, :email, :address, :comments);
            """)
            connection.execute(query_insert, {
                "name": name,
                "phone": phone,
                "email": email,
                "address": address,
                "comments": comments
            })

            # Si todo se ejecuta correctamente, se confirma la transacción automáticamente
            return True,"Cliente agregado"

    except SQLAlchemyError as e:
        # Si ocurre un error, se revierte automáticamente la transacción
        print("Error durante la operación:", e)
        return False, f"Cliente No Agregado. Error durante la operación: {e}"

    finally:
        cerrarConexion(connection)

def actualizar_cliente(name, phone, email, address, comments, id_client):
    """Actualiza un cliente en la base de datos dentro de una transacción."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."
    
    try:
        # Iniciar transacción
        with connection.begin() as transaction:
            query = text("""
                UPDATE cliente 
                SET nombre = :name, 
                    telefono = :phone, 
                    email = :email, 
                    direccion = :address, 
                    notas = :comments 
                WHERE idCliente = :id_client;
            """)
            
            connection.execute(query, {
                "name": name,
                "phone": phone,
                "email": email,
                "address": address,
                "comments": comments,
                "id_client": id_client,
            })

        msj = "Actualización exitosa."
        return True, msj

    except Exception as e:
        print("Error al ejecutar la actualización:", e)
        msj = f"Error al ejecutar la actualización: {e}"
        return False, msj

    finally:
        # Cierra la conexión si fue establecida
        cerrarConexion(connection)

def eliminar_cliente(id_client_selected):
    """Verifica si el cliente tiene actividades abiertas. Si no, elimina el cliente."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return  False, "No se pudo establecer la conexión a la base de datos."

    try:
        with connection.begin() as transaction:
            # Consultar si el cliente tiene actividades abiertas
            query_actividades = text("""
                SELECT count(*) as act_abiertas 
                FROM actividad a 
                INNER JOIN cliente c ON a.idCliente = c.idCliente 
                WHERE a.idCliente = :id_cliente;
            """)
            result = connection.execute(query_actividades, {"id_cliente": id_client_selected}).fetchone()

            # Verificar si el resultado es un tuple
            if result:
                # result[0] es el conteo de actividades
                if result[0] == 0:
                    # Eliminar el cliente si no tiene actividades
                    query_eliminar_cliente = text("""
                        DELETE FROM cliente WHERE idCliente = :id_cliente;
                    """)
                    connection.execute(query_eliminar_cliente, {"id_cliente": id_client_selected})

                    # Confirmar eliminación
                    return True, f"Cliente con ID #{id_client_selected} eliminado exitosamente."
                else:
                    return False,f"Cliente con ID #{id_client_selected} tiene actividades abiertas."
            else:
                return False,f"Cliente con ID #{id_client_selected} no encontrado."

    except SQLAlchemyError as e:
        # Si ocurre un error, se revierte automáticamente la transacción
        print("Error durante la operación:", e)
        return False,f"Error durante la operación: {e}"

    finally:
        cerrarConexion(connection)

def consultar_dispo_clientes(type):
    """Ejecuta una consulta en la base de datos y devuelve todos los clientes que estan disponibles."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        if type==0:
            df = pd.read_sql("SELECT idMiembro as id, nombre FROM miembro WHERE disponibilidad='Disponible';", connection)
            return df
        elif type==1:
            df = pd.read_sql("SELECT idMiembro as id, count(*) as no_actividades FROM actividad GROUP BY idMiembro;", connection)
            return df

    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

############################################################### Recurso ###############################################################
# Listo
def consultar_recursos():
    """Ejecuta una consulta en la base de datos y devuelve todos los recursos."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        df = pd.read_sql("SELECT * FROM recurso;", connection)
        return df

    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def consultar_recursos_disponible():
    """Ejecuta una consulta en la base de datos y devuelve todos los recursos con estado_recurso = En Stock."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        df = pd.read_sql("SELECT * FROM recurso WHERE estado_recurso = 'En Stock';", connection)
        return df

    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def recursos_asginados_a_actividad(id_activity):
    """Ejecuta una consulta en la base de datos y devuelve todos los recursos asignados a una actividad."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        df = pd.read_sql(f"SELECT r.idRecurso, r.nombre FROM actividad_has_recurso ahr INNER JOIN recurso r ON r.idRecurso = ahr.idRecurso INNER JOIN actividad a ON a.idActividad = ahr.idActividad WHERE ahr.idActividad = '{id_activity}'", connection)
        return df

    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def desvincular_recurso(id_activity, id_resource):
    """
    Realiza una transacción para eliminar una asignación en 'actividad_has_recurso'
    y actualizar el estado de un recurso a 'En Stock'.
    """
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        with connection.begin() as transaction:
            # Eliminar la relación de la actividad con el recurso
            query_eliminar = text("""
                DELETE FROM actividad_has_recurso 
                WHERE idActividad = :id_actividad AND idRecurso = :id_recurso;
            """)
            connection.execute(query_eliminar, {
                "id_actividad": id_activity,
                "id_recurso": id_resource
            })

            # Actualizar el estado del recurso a 'En Stock'
            query_actualizar = text("""
                UPDATE recurso 
                SET estado_recurso = 'En Stock' 
                WHERE idRecurso = :id_recurso;
            """)
            connection.execute(query_actualizar, {"id_recurso": id_resource})

            # Confirmar éxito
            return True, f"Recurso con ID #{id_resource} desvinculado de actividad #{id_activity} y actualizado a 'En Stock'."

    except SQLAlchemyError as e:
        # Si ocurre un error, la transacción se revierte automáticamente
        print("Error durante la operación:", e)
        return False, f"Error durante la operación: {e}"

    finally:
        cerrarConexion(connection)

def vincular_recurso(id_activity, id_resource):
    """
    Realiza una transacción para asignar un recurso a una actividad
    y actualizar el estado del recurso a 'En Uso'.
    """
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        with connection.begin() as transaction:
            # Insertar la relación entre actividad y recurso
            query_insertar = text("""
                INSERT INTO actividad_has_recurso (idActividad, idRecurso)
                VALUES (:id_actividad, :id_recurso);
            """)
            connection.execute(query_insertar, {
                "id_actividad": id_activity,
                "id_recurso": id_resource
            })

            # Actualizar el estado del recurso a 'En Uso'
            query_actualizar = text("""
                UPDATE recurso 
                SET estado_recurso = 'En Uso'
                WHERE idRecurso = :id_recurso;
            """)
            connection.execute(query_actualizar, {"id_recurso": id_resource})

            # Confirmar éxito
            return True, f"Recurso #{id_resource} asignado correctamente a la actividad #{id_activity}."

    except SQLAlchemyError as e:
        # Si ocurre un error, la transacción se revierte automáticamente
        print("Error durante la operación:", e)
        return False, f"Error durante la operación: {e}"

    finally:
        cerrarConexion(connection)

def insertar_recurso(serial, name, description, category, life, comments, type):
    """
    Verifica si un recurso existe e inserta uno nuevo si no existe, todo en una transacción.
    """
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False,"No se pudo establecer la conexión a la base de datos."

    try:
        with connection.begin() as transaction:
            # Verificar si el cliente ya existe
            query_existe = text(f"""
                SELECT 1 FROM recurso 
                WHERE no_serie = :serial
                LIMIT 1;
            """)
            result = connection.execute(query_existe, {"serial": serial}).fetchone()

            if result:
                return False, "Recurso No Agregado.El recruso ya existe en la base de datos."

            # Insertar el nuevo cliente
            query_insert = text("""
                INSERT INTO recurso (nombre, tipo, descripcion, categoria, no_serie, estado_recurso, vida_util, fecha_ingreso, notas ) 
                VALUES (:name, :type, :description, :category, :serial, 'En Stock', :life, :today , :comments);;
                """)
            
            connection.execute(query_insert, {
                "name": name,
                "type": type,
                "description": description,
                "category": category,
                "serial": serial,
                "life": life,
                "today": ut.get_today_date(),
                "comments": comments
            })

            # Si todo se ejecuta correctamente, se confirma la transacción automáticamente
            return True,"Recurso agregado"

    except SQLAlchemyError as e:
        # Si ocurre un error, se revierte automáticamente la transacción
        print("Error durante la operación:", e)
        return False, f"Recurso No Agregado. Error durante la operación: {e}"

    finally:
        cerrarConexion(connection)

def actualizar_recurso(name, type, description, category, serial_number, life, state, comments, id_resource_selected):
    """Actualiza un recurso en la base de datos dentro de una transacción."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."
    
    try:
        # Iniciar transacción
        with connection.begin() as transaction:
            query = text("""
                UPDATE recurso 
                SET nombre = :name, 
                    tipo = :type, 
                    descripcion = :description, 
                    categoria = :category, 
                    no_serie = :serial_number, 
                    vida_util = :life, 
                    estado_recurso = :state, 
                    notas = :comments 
                WHERE idRecurso = :id_resource_selected;
            """)

            connection.execute(query, {
                "name": name,
                "type": type,
                "description": description,
                "category": category,
                "serial_number": serial_number,
                "life": life,
                "state": state,
                "comments": comments,
                "id_resource_selected": id_resource_selected,
            })

        msj = "Actualización exitosa."
        return True, msj

    except Exception as e:
        print("Error al ejecutar la actualización:", e)
        msj = f"Error al ejecutar la actualización: {e}"
        return False, msj

    finally:
        # Cierra la conexión si fue establecida
        cerrarConexion(connection)

def eliminar_recurso(id_resource):
    """Verifica si el recurso está asociado a actividades. Si no, elimina el recurso."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        with connection.begin() as transaction:
            # Consultar si el recurso está asociado a actividades
            query_actividades = text("""
                SELECT count(*) as act_abiertas 
                FROM actividad_has_recurso a 
                WHERE a.idRecurso = :id_resource;
            """)
            result = connection.execute(query_actividades, {"id_resource": id_resource}).fetchone()

            # Verificar si el resultado es válido y el recurso tiene actividades asociadas
            if result and result[0] > 0:
                return False, f"Recurso con ID #{id_resource} está asociado a actividades y no puede ser eliminado."
            
            # Si no hay actividades asociadas, proceder a eliminar el recurso
            query_eliminar_recurso = text("""
                DELETE FROM recurso WHERE idRecurso = :id_resource;
            """)
            connection.execute(query_eliminar_recurso, {"id_resource": id_resource})

            # Confirmar eliminación
            return True, f"Recurso con ID #{id_resource} eliminado exitosamente."

    except SQLAlchemyError as e:
        # Manejar errores durante la operación
        print("Error durante la operación:", e)
        return False, f"Error durante la operación: {e}"

    finally:
        cerrarConexion(connection)

def consultar_peticiones_recursos(type):
    """Ejecuta una consulta en la base de datos y devuelve todos las peticiones de recursos."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        if type==0:
            df = pd.read_sql("SELECT pnr.*, m.nombre as nombre_m FROM peticion_nuevo_recurso pnr INNER JOIN miembro m ON m.idMiembro=pnr.idMiembro;", connection)
            return df
        if type==1:
            df = pd.read_sql("SELECT * FROM peticion_nuevo_recurso;", connection)
            return df
    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def consultar_peticiones_por_id(id_miembro):
    """Ejecuta una consulta en la base de datos y devuelve todos las peticciones de recursos, para un miembro."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        df = pd.read_sql(f"SELECT * FROM peticion_nuevo_recurso WHERE idMiembro='{id_miembro}';", connection)
        return df
    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def insertar_peticion_nuevo_recurso(name_new_resource, type_new_resource, description_new_resource, date_new_resource, quantity_new_resource, state_new_resource, comments_ins_resource, id_support_ins):
    """
    Inserta una nueva petición de recurso en la base de datos utilizando una transacción.
    """
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        # Iniciar una transacción
        with connection.begin() as transaction:
            query = text("""
                INSERT INTO peticion_nuevo_recurso 
                (nombre, tipo, descripcion, fecha_peticion, cantidad, estado_peticion, notas, idMiembro) 
                VALUES (:name, :type, :description, :date, :quantity, :state, :comments, :id_member);
            """)

            connection.execute(query, {
                "name": name_new_resource,
                "type": type_new_resource,
                "description": description_new_resource,
                "date": date_new_resource,
                "quantity": quantity_new_resource,
                "state": state_new_resource,
                "comments": comments_ins_resource,
                "id_member": id_support_ins,
            })

        # Si todo va bien, la transacción se confirma automáticamente al salir del bloque `with`
        return True, "Inserción de la petición de recurso realizada con éxito."

    except Exception as e:
        # Si ocurre un error, la transacción se revierte automáticamente
        print("Error al insertar la petición de recurso:", e)
        return False, f"Error al insertar la petición de recurso: {e}"

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def eliminar_peticion_nuevo_recurso(new_id_resource_selected):
    """
    Elimina una petición de nuevo recurso en la base de datos.
    """
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        with connection.begin() as transaction:
            query = text("""
                DELETE FROM peticion_nuevo_recurso WHERE idNuevoRecurso = :id_resource;
            """)
            result = connection.execute(query, {"id_resource": new_id_resource_selected})

            if result.rowcount > 0:  # Verificar si se eliminó alguna fila
                return True, f"Petición con ID #{new_id_resource_selected} eliminada exitosamente."
            else:
                return False, f"No se encontró una petición con ID #{new_id_resource_selected}."

    except Exception as e:
        print("Error al eliminar la petición de recurso:", e)
        return False, f"Error al eliminar la petición de recurso: {e}"

    finally:
        cerrarConexion(connection)

############################################################### Actividad ###############################################################
# Listo
def consultar_actividades():
    """Ejecuta una consulta en la base de datos y devuelve todos las actividades."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        df = pd.read_sql("SELECT * FROM actividad", connection)
        return df

    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def consultar_actividades_id(id_support):
    """Ejecuta una consulta en la base de datos y devuelve todos las actividades."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        df = pd.read_sql(f"SELECT * FROM actividad WHERE idMiembro={id_support}", connection)
        return df

    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def consultar_actividades_eliminacion():
    """Ejecuta una consulta en la base de datos y devuelve todos las actividades."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        df = pd.read_sql("SELECT a.*, c.nombre as nombre_c, m.nombre as nombre_m  FROM actividad a INNER JOIN cliente c ON a.idCliente=c.idCliente INNER JOIN miembro m ON a.idMiembro=m.idMiembro;", connection)
        return df

    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def consultar_actividades_listado(type, id_miembro):
    """Ejecuta una consulta en la base de datos y devuelve todos las actividades."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        if type==0:
            df = pd.read_sql("SELECT a.*, m.nombre as miembro_n, c.nombre as cliente_n FROM actividad a INNER JOIN miembro m ON a.idMiembro = m.idMiembro INNER JOIN cliente c ON a.idCliente = c.idCliente;", connection)
            return df
        elif type==1:
            df = pd.read_sql("SELECT * FROM actividad_hist;", connection)
            return df
        elif type==2:
            df = pd.read_sql(f"SELECT a.*, m.nombre as miembro_n, c.nombre as cliente_n FROM actividad a INNER JOIN miembro m ON a.idMiembro = m.idMiembro INNER JOIN cliente c ON a.idCliente = c.idCliente WHERE a.idMiembro = '{id_miembro}';", connection)
            return df
        elif type==3:
            df = pd.read_sql(f"SELECT * FROM actividad_hist WHERE idMiembro='{id_miembro}';", connection)
            return df

    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def insertar_actividad(name_ins_activity, datestart_ins_activity, description_ins_activity, type_ins_activity, state_ins_activity, id_client_ins, support_ins_activity):
    """
    Inserta una nueva actividad en la base de datos y actualiza el estado del miembro asociado utilizando una transacción.
    """
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        with connection.begin():  # Inicia la transacción
            # Insertar la actividad
            query_insertar_actividad = text("""
                INSERT INTO actividad 
                (nombre, fecha_inicio, descripcion, acciones_realizadas, tipo, estado, idCliente, idMiembro) 
                VALUES (:name, :datestart, :description, 'None', :type, :state, :id_client, :id_support);
            """)
            connection.execute(query_insertar_actividad, {
                "name": name_ins_activity,
                "datestart": datestart_ins_activity,
                "description": description_ins_activity,
                "type": type_ins_activity,
                "state": state_ins_activity,
                "id_client": id_client_ins,
                "id_support": support_ins_activity,
            })

            # Actualizar el estado del miembro
            query_actualizar_miembro = text("""
                UPDATE miembro
                SET disponibilidad = 'No Disponible', estatus = 'En Actividad'
                WHERE idMiembro = :id_support;
            """)
            connection.execute(query_actualizar_miembro, {
                "id_support": support_ins_activity,
            })

        # Si todo fue exitoso, la transacción se confirma automáticamente
        return True, "Actividad insertada y estado del miembro actualizado exitosamente."

    except Exception as e:
        # Si ocurre un error, la transacción se revierte automáticamente
        print("Error al insertar la actividad o actualizar el miembro:", e)
        return False, f"Error al insertar la actividad o actualizar el miembro: {e}"

    finally:
        cerrarConexion(connection)

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

def consultar_actividades_dispo(type, id_miembro):
    """Ejecuta una consulta en la base de datos y devuelve todos las actividades que estan disponibles para actualizar."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        if type == 0:
            df = pd.read_sql("SELECT * FROM actividad WHERE estado='Abierto' OR estado='En Curso' OR estado='Pendiente';", connection)
            return df
        elif type == 1: 
            df = pd.read_sql(f"SELECT * FROM actividad WHERE (estado='Abierto' OR estado='En Curso' OR estado='Pendiente') AND idMiembro='{id_miembro}';", connection)
            return df
    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def actualizar_actividad(name_upd_activity, type_upd_activity, description_upd_activity, 
                                         actions_upd_activity, state_upd_activity, id_support_selected, 
                                         id_client_selected, support_selected_first, id_activity_selected):
    """
    Actualiza una actividad, ajusta la disponibilidad de los miembros relacionados,
    y asegura consistencia usando una transacción.
    """
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        with connection.begin() as transaction:  # Inicia explícitamente la transacción
            # Actualizar la actividad
            query_update_activity = text("""
                UPDATE actividad 
                SET nombre = :name, tipo = :type, descripcion = :description, acciones_realizadas = :actions,
                    estado = :state, idMiembro = :new_support_id, idCliente = :new_client_id
                WHERE idActividad = :activity_id;
            """)
            connection.execute(query_update_activity, {
                "name": name_upd_activity,
                "type": type_upd_activity,
                "description": description_upd_activity,
                "actions": actions_upd_activity,
                "state": state_upd_activity,
                "new_support_id": id_support_selected,
                "new_client_id": id_client_selected,
                "activity_id": id_activity_selected,
            })

            # Verificar si el miembro anterior tiene actividades restantes
            query_check_support = text("""
                SELECT idMiembro, count(*) as no_actividades 
                FROM actividad 
                WHERE idMiembro = :old_support_id 
                GROUP BY idMiembro;
            """)
            result = connection.execute(query_check_support, {"old_support_id": support_selected_first}).fetchone()

            # Si no hay más actividades, actualizar el estado del miembro anterior
            if result is None or result[1] == 0:  # Usa índices para acceder a la segunda columna
                query_update_old_support = text("""
                    UPDATE miembro 
                    SET disponibilidad = 'Disponible', estatus = 'Libre' 
                    WHERE idMiembro = :old_support_id;
                """)
                connection.execute(query_update_old_support, {"old_support_id": support_selected_first})

            # Actualizar el estado del nuevo miembro
            query_update_new_support = text("""
                UPDATE miembro 
                SET disponibilidad = 'No Disponible', estatus = 'En Actividad' 
                WHERE idMiembro = :new_support_id;
            """)
            connection.execute(query_update_new_support, {"new_support_id": id_support_selected})

        # Si todo se ejecuta sin errores, la transacción se confirma automáticamente
        return True, "Transacción completada: Actividad y miembros actualizados exitosamente."

    except Exception as e:
        # Si ocurre un error, la transacción se revierte automáticamente
        print("Error en la transacción:", e)
        return False, f"Error en la transacción: {e}"

    finally:
        cerrarConexion(connection)

############################################################### Miembro ###############################################################
# Listo
def consultar_miembros(type):
    """Ejecuta una consulta en la base de datos y devuelve todos los miembros."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        if type==0:
            df = pd.read_sql("SELECT * FROM miembro;", connection)
            return df
        elif type==1:
            df = pd.read_sql("SELECT idMiembro, nombre FROM miembro;", connection)
            return df

    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def consultar_id_email(email):
    """Devuelve el ID del miembro de acuerdo al email, o None si no se encuentra."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        query = text("SELECT idMiembro FROM miembro WHERE email = :email LIMIT 1;")
        result = connection.execute(query, {"email": email}).fetchone()

        if result is not None:
            # Retornar el ID encontrado
            return True, result[0]
        else:
            # Retornar None si no se encontró el email
            return False, "No se encontró un miembro con ese email."

    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        return False, f"Error al ejecutar la consulta: {e}"

    finally:
        cerrarConexion(connection)

def obtener_actividades_y_promedio(support_id):
    """Obtiene el número de actividades por soporte, actividades históricas y el tiempo promedio de actividades históricas, devolviendo tres DataFrames."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."
    
    try:
        # Iniciar transacción
        with connection.begin() as transaction:
            # Consulta 1: Actividades por soporte
            query_actividades = text("""
                SELECT idMiembro, count(*) as no_actividades 
                FROM actividad 
                WHERE idMiembro = :support_id
                GROUP BY idMiembro;
            """)
            activities_by_support = pd.read_sql(query_actividades, connection, params={"support_id": support_id})

            # Consulta 2: Actividades históricas por soporte
            query_actividades_hist = text("""
                SELECT idMiembro, count(*) as no_actividades 
                FROM actividad_hist 
                WHERE idMiembro = :support_id 
                GROUP BY idMiembro;
            """)
            activities_by_support_hist = pd.read_sql(query_actividades_hist, connection, params={"support_id": support_id})

            # Consulta 3: Promedio de tiempo de las actividades históricas
            query_avg_time_support = text("""
                SELECT AVG(fecha_fin_a - fecha_inicio_a) AS promTiempo 
                FROM actividad_hist 
                WHERE idMiembro = :support_id;
            """)
            avg_time_support = pd.read_sql(query_avg_time_support, connection, params={"support_id": support_id})

        return True, activities_by_support, activities_by_support_hist, avg_time_support

    except Exception as e:
        print("Error al ejecutar las consultas:", e)
        msj = f"Error al ejecutar las consultas: {e}"
        return False, msj

    finally:
        # Cierra la conexión si fue establecida
        cerrarConexion(connection)

def insertar_miembro(name_ins_support, phone_ins_support, email_ins_support, address_ins_support, 
                     disponibility_ins_support, status_ins_support, comments_ins_support):
    """
    Inserta un nuevo miembro en la base de datos dentro de una transacción si el correo no está registrado.
    """
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."
    
    try:
        # Inicia la transacción
        with connection.begin():  # Transacción
            
            # Verificar si ya existe un cliente con el correo proporcionado
            query_check_email = text("""
                SELECT COUNT(*) AS count 
                FROM miembro 
                WHERE email = :email;
            """)
            result = connection.execute(query_check_email, {"email": email_ins_support}).fetchone()

            # Si existe un cliente con el correo, detener el proceso
            if result[0] > 0:  # Acceso por índice porque `fetchone()` devuelve una tupla
                return False, f"El correo {email_ins_support} ya está registrado. No se puede agregar el miembro."

            # Insertar el nuevo miembro si el correo no está registrado
            query_insert = text("""
                INSERT INTO miembro (nombre, telefono, email, direccion, disponibilidad, estatus, notas) 
                VALUES (:name, :phone, :email, :address, :disponibility, :status, :comments);
            """)
            connection.execute(query_insert, {
                "name": name_ins_support,
                "phone": phone_ins_support,
                "email": email_ins_support,
                "address": address_ins_support,
                "disponibility": disponibility_ins_support,
                "status": status_ins_support,
                "comments": comments_ins_support,
            })

        return True, "Miembro insertado correctamente."

    except Exception as e:
        print("Error al insertar el miembro:", e)
        return False, f"Error al insertar el miembro: {e}"

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def eliminar_miembro(id_support_selected):
    """Verifica si un miembro tiene actividades asociadas. Si no tiene, elimina la petición y luego al miembro en una transacción."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        # Iniciar una transacción
        with connection.begin():  # Comienza la transacción
            # Verificar si el miembro tiene actividades asociadas
            query_verificar_actividades = text("""
                SELECT a.idMiembro, count(*) as act_abiertas
                FROM actividad a
                INNER JOIN miembro m ON a.idMiembro = m.idMiembro
                WHERE a.idMiembro = :id_support_selected
                GROUP BY a.idMiembro;
            """)

            result = connection.execute(query_verificar_actividades, {"id_support_selected": id_support_selected}).fetchone()

            # Verificar si el miembro tiene actividades asociadas (usando índice en lugar de clave de cadena)
            if result and result[1] > 0:  # Accede al conteo de actividades con el índice 1
                return False, f"El miembro con ID #{id_support_selected} tiene actividades asociadas y no puede ser eliminado."

            # Si el miembro no tiene actividades, proceder con la eliminación de la petición
            query_eliminar_peticion = text("""
                DELETE FROM peticion_nuevo_recurso WHERE idMiembro = :id_support_selected;
            """)

            connection.execute(query_eliminar_peticion, {"id_support_selected": id_support_selected})

            # Luego, eliminar al miembro
            query_eliminar_miembro = text("""
                DELETE FROM miembro WHERE idMiembro = :id_support_selected;
            """)

            connection.execute(query_eliminar_miembro, {"id_support_selected": id_support_selected})

            # Si todo fue exitoso, la transacción se confirma automáticamente al salir del bloque 'with'
            return True, f"Petición y miembro con ID #{id_support_selected} eliminados exitosamente."

    except Exception as e:
        # Si ocurre algún error, la transacción se revierte automáticamente
        print("Error al realizar la operación:", e)
        return False, f"Error al realizar la operación: {e}"

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def consultar_miembro_id(id_miembro):
    """Ejecuta una consulta en la base de datos y devuelve uno de los miembros de acuerdo a su id"""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        df = pd.read_sql(f"SELECT * FROM miembro WHERE idMiembro='{id_miembro}' LIMIT 1;", connection)
        return df

    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def actualizar_miembro(id_support_selected, name_upd_support, phone_upd_support, email_upd_support, 
                       address_upd_support, disponibility_upd_support, status_upd_support, comments_upd_support):
    """
    Actualiza los datos de un miembro en la base de datos utilizando una transacción.
    """
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        with connection.begin():  # Inicia la transacción
            query_actualizar = text("""
                UPDATE miembro 
                SET nombre = :name,
                    telefono = :phone,
                    email = :email,
                    direccion = :address,
                    disponibilidad = :disponibility,
                    estatus = :status,
                    notas = :comments
                WHERE idMiembro = :id;
            """)

            connection.execute(query_actualizar, {
                "name": name_upd_support,
                "phone": phone_upd_support,
                "email": email_upd_support,
                "address": address_upd_support,
                "disponibility": disponibility_upd_support,
                "status": status_upd_support,
                "comments": comments_upd_support,
                "id": id_support_selected,
            })

        # Si todo fue exitoso, la transacción se confirma automáticamente
        return True, f"Miembro con ID #{id_support_selected} actualizado exitosamente."

    except Exception as e:
        # Si ocurre un error, la transacción se revierte automáticamente
        print("Error al actualizar el miembro:", e)
        return False, f"Error al actualizar el miembro: {e}"

    finally:
        cerrarConexion(connection)

def actualizar_miembro_indie(id_support_selected, name_upd_support, phone_upd_support, address_upd_support, comments_upd_support):
    """
    Actualiza los datos de un miembro en la base de datos utilizando una transacción.
    """
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        with connection.begin():  # Inicia la transacción
            query_actualizar = text("""
                UPDATE miembro 
                SET nombre = :name,
                    telefono = :phone,
                    direccion = :address,
                    notas = :comments
                WHERE idMiembro = :id;
            """)

            connection.execute(query_actualizar, {
                "name": name_upd_support,
                "phone": phone_upd_support,
                "address": address_upd_support,
                "comments": comments_upd_support,
                "id": id_support_selected,
            })

        # Si todo fue exitoso, la transacción se confirma automáticamente
        return True, f"Miembro con ID #{id_support_selected} actualizado exitosamente."

    except Exception as e:
        # Si ocurre un error, la transacción se revierte automáticamente
        print("Error al actualizar el miembro:", e)
        return False, f"Error al actualizar el miembro: {e}"

    finally:
        cerrarConexion(connection)

############################################################### Factura ###############################################################
# Listo
def consultar_facturas(type, email):
    """Ejecuta una consulta en la base de datos y devuelve todos las facturas, y de acuerdo tambien con los miembros."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        if type==0:
            df = pd.read_sql("SELECT f.*, a.idActividad as idA, a.nombre as nombre_a, m.idMiembro as idM, m.nombre as nombre_m FROM factura f INNER JOIN miembro m ON f.idMiembro=m.idMiembro INNER JOIN actividad a ON f.idActividad=a.idActividad;", connection)
            return df
        elif type==1:
            df = pd.read_sql(f"SELECT f.*, a.idActividad as idA, a.nombre as nombre_a, m.idMiembro as idM, m.nombre as nombre_m FROM factura f INNER JOIN miembro m ON f.idMiembro=m.idMiembro INNER JOIN actividad a ON f.idActividad=a.idActividad WHERE m.email='{email}';", connection)
            return df

    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def consultar_facturas_hist(id_activity_closed):
    """Ejecuta una consulta en la base de datos y devuelve todos las facturas, y de acuerdo tambien con los miembros."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        df = pd.read_sql(f"SELECT fh.*, ah.nombre_a, ah.nombre_m, ah.idMiembro as idM FROM factura_hist fh INNER JOIN actividad_hist ah ON fh.idActividad = ah.idActividad WHERE fh.idActividad='{id_activity_closed}';", connection)
        return df

    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def obtener_metricas_facturacion():
    """
    Obtiene métricas de facturación por actividades y clientes dentro de una transacción.

    Returns:
        tuple: (bool, pd.DataFrame, pd.DataFrame)
            - bool: Indica si la operación fue exitosa.
            - pd.DataFrame: Métricas de facturación por actividad.
            - pd.DataFrame: Métricas de facturación por cliente.
    """
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, None, None

    try:
        # Inicia la transacción
        with connection.begin():  # Transacción
            # Consulta para obtener métricas de facturación por actividad
            query_activities_metrics = text("""
                SELECT 
                    fh.idActividad, 
                    ah.nombre_a, 
                    SUM(fh.costo + fh.impuesto) AS total
                FROM factura_hist fh
                INNER JOIN actividad_hist ah ON fh.idActividad = ah.idActividad
                GROUP BY fh.idActividad;
            """)
            activities_result = connection.execute(query_activities_metrics)
            activities_df = pd.DataFrame(activities_result.fetchall(), columns=activities_result.keys())

            # Consulta para obtener métricas de facturación por cliente
            query_client_metrics = text("""
                SELECT 
                    ah.idCliente, 
                    ah.nombre_c, 
                    SUM(fh.costo + fh.impuesto) AS total
                FROM factura_hist fh
                INNER JOIN actividad_hist ah ON fh.idActividad = ah.idActividad
                GROUP BY ah.idCliente, ah.nombre_c;
            """)
            client_result = connection.execute(query_client_metrics)
            client_df = pd.DataFrame(client_result.fetchall(), columns=client_result.keys())

        return True, activities_df, client_df

    except Exception as e:
        print("Error al obtener las métricas de facturación:", e)
        return False, None, None

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def insertar_factura(name_ins_bill, dateemission_ins_bill, cost_ins_bill, type_ins_bill, tax_ins_bill, createby_ins_bill, id_activity_ins, id_support_ins):
    """
    Inserta una factura en la base de datos dentro de una transacción.

    Args:
        name_ins_bill (str): Nombre de la factura.
        dateemission_ins_bill (str): Fecha de emisión de la factura.
        cost_ins_bill (float): Costo de la factura.
        type_ins_bill (str): Tipo de factura.
        tax_ins_bill (float): Impuesto aplicado a la factura.
        createby_ins_bill (str): Usuario que creó la factura.
        id_activity_ins (int): ID de la actividad asociada.
        id_support_ins (int): ID del miembro asociado.

    Returns:
        tuple: (bool, str)
            - bool: Indica si la operación fue exitosa.
            - str: Mensaje con el resultado de la operación.
    """
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        # Inicia la transacción
        with connection.begin():  # Transacción
            # Consulta para insertar la factura
            query = text("""
                INSERT INTO factura (
                    nombre, fecha_emision, costo, tipo, impuesto, estatus, 
                    creado_por, fecha_modificacion, modificado_por, idActividad, idMiembro
                ) 
                VALUES (
                    :name, :fecha_emision, :costo, :tipo, :impuesto, 'Abierta', 
                    :creado_por, :fecha_modificacion, :modificado_por, :id_actividad, :id_miembro
                );
            """)

            # Ejecutar la consulta
            connection.execute(query, {
                "name": name_ins_bill,
                "fecha_emision": dateemission_ins_bill,
                "costo": cost_ins_bill,
                "tipo": type_ins_bill,
                "impuesto": tax_ins_bill,
                "creado_por": createby_ins_bill,
                "fecha_modificacion": dateemission_ins_bill,
                "modificado_por": createby_ins_bill,
                "id_actividad": id_activity_ins,
                "id_miembro": id_support_ins
            })

        return True, "Factura insertada correctamente."

    except Exception as e:
        print("Error al insertar la factura:", e)
        return False, f"Error al insertar la factura: {e}"

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def consultar_factura_actualizar():
    """Ejecuta una consulta en la base de datos y devuelve todos las facturas para actualizar"""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        df = pd.read_sql("SELECT f.*, m.idMiembro as idM, a.idActividad as idA, m.nombre as nombre_m, a.nombre as nombre_a FROM factura f INNER JOIN miembro m ON f.idMiembro=m.idMiembro INNER JOIN actividad a ON a.idActividad=f.idActividad WHERE f.estatus != 'Cerrada';", connection)
        return df

    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def actualizar_factura(id_bill_selected, name_upd_bill, cost_upd_bill, type_upd_bill, tax_upd_bill, status_upd_bill, datemodified_upd_bill, modifyby_upd_bill, id_supportbill_selected, id_activitybill_selected):
    """
    Actualiza una factura en la base de datos dentro de una transacción.

    Args:
        id_bill_selected (int): ID de la factura a actualizar.
        name_upd_bill (str): Nuevo nombre de la factura.
        cost_upd_bill (float): Nuevo costo de la factura.
        type_upd_bill (str): Nuevo tipo de factura.
        tax_upd_bill (float): Nuevo impuesto aplicado a la factura.
        status_upd_bill (str): Nuevo estado de la factura.
        datemodified_upd_bill (str): Fecha de modificación.
        modifyby_upd_bill (str): Usuario que realizó la modificación.
        id_supportbill_selected (int): ID del miembro asociado.
        id_activitybill_selected (int): ID de la actividad asociada.

    Returns:
        tuple: (bool, str)
            - bool: Indica si la operación fue exitosa.
            - str: Mensaje con el resultado de la operación.
    """
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        # Inicia la transacción
        with connection.begin():  # Transacción
            # Consulta para actualizar la factura
            query = text("""
                UPDATE factura
                SET
                    nombre = :name,
                    costo = :costo,
                    tipo = :tipo,
                    impuesto = :impuesto,
                    estatus = :estatus,
                    fecha_modificacion = :fecha_modificacion,
                    modificado_por = :modificado_por,
                    idMiembro = :id_miembro,
                    idActividad = :id_actividad
                WHERE idFactura = :id_factura;
            """)

            # Ejecutar la consulta
            connection.execute(query, {
                "name": name_upd_bill,
                "costo": cost_upd_bill,
                "tipo": type_upd_bill,
                "impuesto": tax_upd_bill,
                "estatus": status_upd_bill,
                "fecha_modificacion": datemodified_upd_bill,
                "modificado_por": modifyby_upd_bill,
                "id_miembro": id_supportbill_selected,
                "id_actividad": id_activitybill_selected,
                "id_factura": id_bill_selected,
            })

        return True, "Factura actualizada correctamente."

    except Exception as e:
        print("Error al actualizar la factura:", e)
        return False, f"Error al actualizar la factura: {e}"

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def cerrar_factura(id_bill_selected_delete, datemodified_del_bill, modifyby_del_bill):
    """
    Cierra una factura actualizando su estado a 'Cerrada'.

    Args:
        id_bill_selected_delete (int): ID de la factura a cerrar.
        datemodified_del_bill (str): Fecha de modificación.
        modifyby_del_bill (str): Usuario que realiza el cierre.

    Returns:
        tuple: (bool, str)
            - bool: Indica si la operación fue exitosa.
            - str: Mensaje con el resultado de la operación.
    """
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        # Inicia la transacción
        with connection.begin():  # Transacción
            # Consulta para cerrar la factura
            query = text("""
                UPDATE factura
                SET
                    fecha_modificacion = :fecha_modificacion,
                    modificado_por = :modificado_por,
                    estatus = 'Cerrada'
                WHERE idFactura = :id_factura;
            """)

            # Ejecutar la consulta
            connection.execute(query, {
                "fecha_modificacion": datemodified_del_bill,
                "modificado_por": modifyby_del_bill,
                "id_factura": id_bill_selected_delete,
            })

        return True, f"Factura con ID #{id_bill_selected_delete} cerrada correctamente."

    except Exception as e:
        print("Error al cerrar la factura:", e)
        return False, f"Error al cerrar la factura: {e}"

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

############################################################### General ############################################################### 
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
        return True  # Se encontró el campo
    return False  # No se encontró el campo

def existe_cliente(nombre):
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




