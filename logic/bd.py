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
    """
    Establece la conexión a la base de datos MySQL y la devuelve usando SQLAlchemy.

    Este método configura la conexión de acuerdo al sistema operativo (MacOS o cualquier otro),
    definiendo credenciales específicas para cada caso. Utiliza `SQLAlchemy` para crear un motor 
    de conexión y establece una conexión a la base de datos.

    Returns:
        connection: Objeto de conexión a la base de datos si la conexión es exitosa, de lo contrario `None`.
    """
    # Determina el sistema operativo en el que se ejecuta el código
    s_o = platform.system()
    try:
        # Define las credenciales de acceso dependiendo del sistema operativo
        if s_o == "Darwin":  # Darwin corresponde a MacOS
            user = 'root'
            password = '15122121B'
        else:
            user = 'admin'
            password = 'password'
        
        # Crea la URL de conexión para SQLAlchemy con las credenciales definidas
        db_url = f"mysql+pymysql://{user}:{password}@localhost/erp"
        
        # Crea el motor de conexión a la base de datos utilizando SQLAlchemy
        engine = create_engine(db_url)

        # Establece la conexión a la base de datos
        connection = engine.connect()
        
        print("Conectado a la base de datos MySQL con SQLAlchemy.")
        return connection

    except Exception as e:
        # Maneja cualquier excepción que ocurra al intentar conectarse a la base de datos
        print("Error al conectar a MySQL:", e)
        return None

############################################################### Cliente ###############################################################
# Listo
def consultar_todos_clientes():
    """
    Ejecuta una consulta en la base de datos para obtener todos los registros de clientes y los devuelve como un DataFrame.

    La función establece una conexión a la base de datos utilizando la función `conectarBase()`. 
    Si la conexión es exitosa, ejecuta una consulta SQL para seleccionar todos los registros de la tabla `cliente`. 
    Los resultados se devuelven en un objeto `DataFrame` de `pandas`. Si ocurre algún error durante la consulta, 
    se maneja la excepción y se devuelve un mensaje de error. Finalmente, la conexión a la base de datos se cierra.

    Retorna:
        DataFrame: Un `DataFrame` de `pandas` con los registros de la tabla `cliente` si la consulta es exitosa.
        str: Un mensaje de error si ocurre un problema al conectarse a la base de datos o al ejecutar la consulta.
    """
    # Establecer conexión a la base de datos
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        # Ejecutar la consulta SQL y almacenar el resultado en un DataFrame
        df = pd.read_sql("SELECT * FROM cliente", connection)
        return df

    except Exception as e:
        # Manejar errores durante la ejecución de la consulta
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión a la base de datos
        cerrarConexion(connection)

def insertar_cliente(name, phone, email, address, comments):
    """
    Inserta un nuevo cliente en la base de datos si no existe, utilizando una transacción para asegurar la integridad de los datos.

    Esta función establece una conexión a la base de datos y ejecuta dos operaciones dentro de una transacción:
    1. Verifica si un cliente con el nombre dado ya existe en la base de datos.
    2. Si el cliente no existe, lo inserta en la base de datos.

    Si ocurre algún error durante la operación, la transacción se revierte automáticamente, asegurando que no se realicen cambios parciales en la base de datos.

    Parámetros:
        name (str): El nombre del cliente.
        phone (str): El número de teléfono del cliente.
        email (str): El correo electrónico del cliente.
        address (str): La dirección del cliente.
        comments (str): Comentarios adicionales sobre el cliente.

    Retorna:
        tuple: Una tupla que contiene:
            - bool: `True` si el cliente fue agregado exitosamente, `False` si no.
            - str: Un mensaje que indica el resultado de la operación.
    """
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

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

            return True, "Cliente agregado"

    except SQLAlchemyError as e:
        print("Error durante la operación:", e)
        return False, f"Cliente No Agregado. Error durante la operación: {e}"

    finally:
        cerrarConexion(connection)

def actualizar_cliente(name, phone, email, address, comments, id_client):
    """
    Actualiza los datos de un cliente existente en la base de datos.

    Esta función establece una conexión a la base de datos y ejecuta una consulta `UPDATE` dentro de una transacción para modificar 
    la información de un cliente específico. Si ocurre un error durante la actualización, la transacción se revierte automáticamente.

    Parámetros:
        name (str): El nuevo nombre del cliente.
        phone (str): El nuevo número de teléfono del cliente.
        email (str): El nuevo correo electrónico del cliente.
        address (str): La nueva dirección del cliente.
        comments (str): Nuevos comentarios sobre el cliente.
        id_client (int): El identificador único del cliente en la base de datos.

    Returns:
        tuple: Una tupla que contiene:
            - bool: `True` si la actualización fue exitosa, `False` si no.
            - str: Un mensaje que indica el resultado de la operación.
    """
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
    """
    Elimina un cliente de la base de datos si no tiene actividades abiertas.

    Esta función verifica primero si el cliente especificado tiene actividades abiertas asociadas. Si no hay actividades abiertas, 
    procede a eliminar el cliente. La operación se realiza dentro de una transacción para garantizar la integridad de los datos. 

    Parámetros:
        id_client_selected (int): El identificador único del cliente que se desea eliminar.

    Retorna:
        tuple: Una tupla que contiene:
            - bool: `True` si el cliente fue eliminado exitosamente, `False` si no.
            - str: Un mensaje que indica el resultado de la operación.
    """
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

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
                    return False, f"Cliente con ID #{id_client_selected} tiene actividades abiertas."
            else:
                return False, f"Cliente con ID #{id_client_selected} no encontrado."

    except SQLAlchemyError as e:
        # Si ocurre un error, se revierte automáticamente la transacción
        print("Error durante la operación:", e)
        return False, f"Error durante la operación: {e}"

    finally:
        cerrarConexion(connection)

def consultar_dispo_miembros(type):
    """
    Ejecuta una consulta en la base de datos y devuelve los miembros disponibles
    o el número de actividades de cada miembro, dependiendo del parámetro 'type'.
    
    Parámetros:
        type (int): Tipo de consulta que se ejecutará:
            - 0: Consulta los miembros disponibles (id y nombre).
            - 1: Consulta el número de actividades de cada miembro (id y número de actividades).
    
    Retorna:
        pd.DataFrame: DataFrame con los resultados de la consulta o un mensaje de error
                      si ocurre algún problema en la conexión o ejecución de la consulta.
    """
    # Establecer la conexión a la base de datos
    connection = conectarBase()
    
    # Verificar si la conexión fue exitosa
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        # Si el tipo de consulta es 0, se obtienen los miembros disponibles
        if type == 0:
            # Consulta para obtener miembros disponibles
            df = pd.read_sql("SELECT idMiembro as id, nombre FROM miembro WHERE disponibilidad='Disponible';", connection)
            return df

        # Si el tipo de consulta es 1, se obtienen el número de actividades de cada miembro
        elif type == 1:
            # Consulta para obtener el número de actividades por miembro
            df = pd.read_sql("SELECT idMiembro as id, count(*) as no_actividades FROM actividad GROUP BY idMiembro ORDER BY no_actividades ASC;", connection)
            return df

    except Exception as e:
        # Capturar cualquier excepción que ocurra durante la ejecución de la consulta
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión a la base de datos después de ejecutar la consulta
        cerrarConexion(connection)

############################################################### Recurso ###############################################################
# Listo
def consultar_recursos():
    """
    Ejecuta una consulta en la base de datos para obtener todos los recursos.

    Esta función se conecta a la base de datos, ejecuta una consulta para seleccionar todos los registros de la tabla `recurso`,
    y devuelve los resultados en un DataFrame de pandas.

    Retorna:
        pandas.DataFrame | str: Un DataFrame que contiene los datos de los recursos si la consulta es exitosa, o un mensaje de error si ocurre algún problema.
    """
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        # Ejecutar la consulta SQL y cargar los resultados en un DataFrame
        df = pd.read_sql("SELECT * FROM recurso;", connection)
        return df

    except Exception as e:
        # Manejar errores durante la consulta
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Asegurar que la conexión se cierre después de la operación
        cerrarConexion(connection)

def consultar_recursos_disponible():
    """
    Ejecuta una consulta en la base de datos para obtener todos los recursos disponibles.

    Esta función se conecta a la base de datos, ejecuta una consulta para seleccionar todos los registros 
    de la tabla `recurso` donde el `estado_recurso` es "En Stock", y devuelve los resultados en un DataFrame de pandas.

    Retorna:
        pandas.DataFrame | str: Un DataFrame que contiene los datos de los recursos disponibles si la consulta es exitosa, 
        o un mensaje de error si ocurre algún problema.
    """
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        # Ejecutar la consulta SQL y cargar los resultados en un DataFrame
        df = pd.read_sql("SELECT * FROM recurso WHERE estado_recurso = 'En Stock';", connection)
        return df

    except Exception as e:
        # Manejar errores durante la consulta
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Asegurar que la conexión se cierre después de la operación
        cerrarConexion(connection)

def recursos_asignados_a_actividad(id_activity):
    """
    Obtiene los recursos asignados a una actividad desde la base de datos.

    Esta función ejecuta una consulta SQL que devuelve todos los recursos (por su ID y nombre)
    asignados a una actividad específica, identificada por su `id_activity`. Utiliza la conexión
    a la base de datos establecida mediante la función `conectarBase()` y cierra la conexión
    al finalizar.

    Parámetros:
    id_activity (str): El identificador único de la actividad a consultar en la base de datos.

    Retorna:
    pd.DataFrame: Un DataFrame de pandas con las columnas `idRecurso` y `nombre` de los recursos 
    asignados a la actividad, o un mensaje de error en caso de que se produzca un fallo en la ejecución.
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.
    
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        # Ejecuta la consulta SQL para obtener los recursos asignados a la actividad
        df = pd.read_sql(f"""
            SELECT r.idRecurso, r.nombre
            FROM actividad_has_recurso ahr
            INNER JOIN recurso r ON r.idRecurso = ahr.idRecurso
            INNER JOIN actividad a ON a.idActividad = ahr.idActividad
            WHERE ahr.idActividad = '{id_activity}'
        """, connection)
        
        return df  # Devuelve los recursos en un DataFrame

    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj  # Devuelve un mensaje de error si la consulta falla

    finally:
        # Cierra la conexión con la base de datos
        cerrarConexion(connection)

def desvincular_recurso(id_activity, id_resource):
    """
    Desvincula un recurso de una actividad y actualiza su estado a 'En Stock'.

    Esta función realiza una transacción en la base de datos para eliminar la asignación
    de un recurso a una actividad en la tabla 'actividad_has_recurso' y actualizar el estado
    del recurso a 'En Stock' en la tabla 'recurso'.

    Parámetros:
    id_activity (str): El identificador único de la actividad de la cual se desvinculará el recurso.
    id_resource (str): El identificador único del recurso que se desvinculará.

    Retorna:
    tuple: Un tuple que contiene dos valores:
        - Un valor booleano (True si la operación fue exitosa, False si ocurrió un error).
        - Un mensaje que describe el resultado de la operación (éxito o error).
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.
    
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        # Inicia una transacción en la conexión
        with connection.begin() as transaction:
            # Eliminar la relación entre la actividad y el recurso
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

            # Si todo ha salido bien, confirma el éxito
            return True, f"Recurso con ID #{id_resource} desvinculado de actividad #{id_activity} y actualizado a 'En Stock'."

    except SQLAlchemyError as e:
        # Si ocurre un error, la transacción se revierte automáticamente
        print("Error durante la operación:", e)
        return False, f"Error durante la operación: {e}"

    finally:
        # Cierra la conexión con la base de datos
        cerrarConexion(connection)

def vincular_recurso(id_activity, id_resource):
    """
    Asigna un recurso a una actividad y actualiza su estado a 'En Uso'.

    Esta función realiza una transacción en la base de datos para insertar una nueva asignación
    de un recurso a una actividad en la tabla 'actividad_has_recurso' y actualizar el estado
    del recurso a 'En Uso' en la tabla 'recurso'.

    Parámetros:
    id_activity (str): El identificador único de la actividad a la cual se asignará el recurso.
    id_resource (str): El identificador único del recurso que será asignado a la actividad.

    Retorna:
    tuple: Un tuple que contiene dos valores:
        - Un valor booleano (True si la operación fue exitosa, False si ocurrió un error).
        - Un mensaje que describe el resultado de la operación (éxito o error).

    """
    connection = conectarBase()  # Establece la conexión con la base de datos.
    
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        # Inicia una transacción en la conexión
        with connection.begin() as transaction:
            # Insertar la relación entre la actividad y el recurso
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

            # Si todo ha salido bien, confirma el éxito
            return True, f"Recurso #{id_resource} asignado correctamente a la actividad #{id_activity}."

    except SQLAlchemyError as e:
        # Si ocurre un error, la transacción se revierte automáticamente
        print("Error durante la operación:", e)
        return False, f"Error durante la operación: {e}"

    finally:
        # Cierra la conexión con la base de datos
        cerrarConexion(connection)

def insertar_recurso(serial, name, description, category, life, comments, type):
    """
    Verifica si un recurso existe e inserta uno nuevo si no existe, todo dentro de una transacción.

    Esta función primero verifica si un recurso con el mismo número de serie ya existe en la base de datos.
    Si el recurso ya existe, se devuelve un mensaje de error. Si el recurso no existe, se inserta un nuevo registro
    con los datos proporcionados y se confirma la transacción.

    Parámetros:
    serial (str): El número de serie del recurso, que debe ser único.
    name (str): El nombre del recurso.
    description (str): La descripción del recurso.
    category (str): La categoría del recurso.
    life (int): La vida útil del recurso.
    comments (str): Comentarios adicionales sobre el recurso.
    type (str): El tipo del recurso.

    Retorna:
    tuple: Un tuple que contiene dos valores:
        - Un valor booleano (True si la operación fue exitosa, False si ocurrió un error).
        - Un mensaje que describe el resultado de la operación (éxito o error).
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.
    
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        # Inicia una transacción en la conexión
        with connection.begin() as transaction:
            # Verificar si el recurso ya existe en la base de datos por su número de serie
            query_existe = text(f"""
                SELECT 1 FROM recurso 
                WHERE no_serie = :serial
                LIMIT 1;
            """)
            result = connection.execute(query_existe, {"serial": serial}).fetchone()

            # Si el recurso ya existe, no se agrega y se retorna un mensaje de error
            if result:
                return False, "Recurso No Agregado. El recurso ya existe en la base de datos."

            # Insertar el nuevo recurso en la base de datos
            query_insert = text("""
                INSERT INTO recurso (nombre, tipo, descripcion, categoria, no_serie, estado_recurso, vida_util, fecha_ingreso, notas)
                VALUES (:name, :type, :description, :category, :serial, 'En Stock', :life, :today, :comments);
            """)
            
            connection.execute(query_insert, {
                "name": name,
                "type": type,
                "description": description,
                "category": category,
                "serial": serial,
                "life": life,
                "today": ut.get_today_date(),  # Asume que `ut.get_today_date()` devuelve la fecha actual.
                "comments": comments
            })

            # Si todo ha salido bien, confirma el éxito
            return True, "Recurso agregado correctamente."

    finally:
        # Cierra la conexión con la base de datos
        cerrarConexion(connection)

def actualizar_recurso(name, type, description, category, serial_number, life, state, comments, id_resource_selected):
    """
    Actualiza un recurso en la base de datos y elimina asociaciones de actividades dentro de una transacción.

    Esta función realiza dos operaciones dentro de una transacción:
    1. Actualiza los detalles de un recurso específico en la base de datos utilizando el ID del recurso seleccionado.
    2. Elimina todas las asociaciones de actividades relacionadas con el recurso.

    Parámetros:
    name (str): El nuevo nombre del recurso.
    type (str): El nuevo tipo del recurso.
    description (str): La nueva descripción del recurso.
    category (str): La nueva categoría del recurso.
    serial_number (str): El nuevo número de serie del recurso.
    life (int): La nueva vida útil del recurso.
    state (str): El nuevo estado del recurso.
    comments (str): Nuevos comentarios sobre el recurso.
    id_resource_selected (int): El ID del recurso que se desea actualizar.

    Retorna:
    tuple: Un tuple con dos valores:
        - Un valor booleano (True si la operación fue exitosa, False si ocurrió un error).
        - Un mensaje que describe el resultado de la operación (éxito o error).
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.
    
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        # Inicia una transacción en la conexión
        with connection.begin() as transaction:
            # Consulta para actualizar el recurso en la base de datos
            update_query = text("""
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
            connection.execute(update_query, {
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

            # Consulta para eliminar las asociaciones de actividades del recurso
            delete_query = text("""
                DELETE FROM actividad_has_recurso 
                WHERE idRecurso = :id_resource;
            """)
            connection.execute(delete_query, {"id_resource": id_resource_selected})

        # Si la operación es exitosa, se retorna un mensaje
        msj = "Actualización y eliminación exitosas."
        return True, msj

    except Exception as e:
        # Si ocurre un error, se captura la excepción y se devuelve el mensaje de error
        print("Error al ejecutar la operación:", e)
        msj = f"Error al ejecutar la operación: {e}"
        return False, msj

    finally:
        # Cierra la conexión con la base de datos
        cerrarConexion(connection)

def eliminar_recurso(id_resource):
    """
    Verifica si el recurso está asociado a actividades. Si no lo está, elimina el recurso de la base de datos.

    Esta función realiza dos operaciones dentro de una transacción:
    1. Verifica si el recurso está asociado a alguna actividad.
    2. Si el recurso no está asociado a ninguna actividad, elimina el recurso de la base de datos.

    Parámetros:
    id_resource (int): El ID del recurso que se desea eliminar.

    Retorna:
    tuple: Un tuple con dos valores:
        - Un valor booleano (True si la operación fue exitosa, False si ocurrió un error).
        - Un mensaje que describe el resultado de la operación (éxito o error).
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.

    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        # Inicia una transacción en la conexión
        with connection.begin() as transaction:
            # Consulta para verificar si el recurso está asociado a alguna actividad
            query_actividades = text("""
                SELECT count(*) as act_abiertas 
                FROM actividad_has_recurso a 
                WHERE a.idRecurso = :id_resource;
            """)
            result = connection.execute(query_actividades, {"id_resource": id_resource}).fetchone()

            # Verificar si el recurso está asociado a alguna actividad
            if result and result[0] > 0:
                return False, f"Recurso con ID #{id_resource} está asociado a actividades y no puede ser eliminado."
            
            # Si no hay actividades asociadas, proceder a eliminar el recurso
            query_eliminar_recurso = text("""
                DELETE FROM recurso WHERE idRecurso = :id_resource;
            """)
            connection.execute(query_eliminar_recurso, {"id_resource": id_resource})

            # Confirmar eliminación exitosa
            return True, f"Recurso con ID #{id_resource} eliminado exitosamente."

    except SQLAlchemyError as e:
        # Si ocurre un error durante la operación, se captura la excepción
        print("Error durante la operación:", e)
        return False, f"Error durante la operación: {e}"

    finally:
        # Cierra la conexión con la base de datos
        cerrarConexion(connection)

def consultar_peticiones_recursos(type):
    """
    Ejecuta una consulta en la base de datos y devuelve todas las peticiones de recursos.

    Esta función permite consultar las peticiones de recursos de acuerdo con el tipo solicitado:
    - Si `type` es 0, devuelve las peticiones junto con el nombre del miembro que las solicitó.
    - Si `type` es 1, devuelve todas las peticiones de recursos sin detalles adicionales.

    Parámetros:
    type (int): Tipo de consulta a realizar:
        - 0: Consulta con el nombre del miembro que solicitó el recurso.
        - 1: Consulta sin detalles del miembro.

    Retorna:
    DataFrame o str: Un DataFrame con los resultados de la consulta, o un mensaje de error en caso de fallo.
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.
    
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        # Si 'type' es 0, incluye el nombre del miembro en la consulta
        if type == 0:
            df = pd.read_sql("SELECT pnr.*, m.nombre as nombre_m FROM peticion_nuevo_recurso pnr INNER JOIN miembro m ON m.idMiembro=pnr.idMiembro;", connection)
            return df
        # Si 'type' es 1, consulta solo las peticiones sin detalles adicionales
        if type == 1:
            df = pd.read_sql("SELECT * FROM peticion_nuevo_recurso;", connection)
            return df
    except Exception as e:
        # Si ocurre un error, se captura la excepción y se devuelve un mensaje de error
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cierra la conexión con la base de datos
        cerrarConexion(connection)

def consultar_peticiones_por_id(id_miembro):
    """
    Ejecuta una consulta en la base de datos y devuelve todas las peticiones de recursos de un miembro específico.

    Esta función consulta las peticiones de recursos realizadas por un miembro en particular, identificado por su ID.

    Parámetros:
    id_miembro (int): El ID del miembro cuyas peticiones de recursos se desean consultar.

    Retorna:
    DataFrame o str: Un DataFrame con los resultados de la consulta, o un mensaje de error en caso de fallo.
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.
    
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        # Consulta para obtener las peticiones de un miembro específico
        df = pd.read_sql(f"SELECT * FROM peticion_nuevo_recurso WHERE idMiembro='{id_miembro}';", connection)
        return df
    except Exception as e:
        # Si ocurre un error, se captura la excepción y se devuelve un mensaje de error
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cierra la conexión con la base de datos
        cerrarConexion(connection)

def insertar_peticion_nuevo_recurso(name_new_resource, type_new_resource, description_new_resource, date_new_resource, quantity_new_resource, comments_ins_resource, id_support_ins):
    """
    Inserta una nueva petición de recurso en la base de datos utilizando una transacción.

    Esta función permite insertar una nueva solicitud de recurso en la base de datos. La operación se realiza dentro de una transacción, lo que garantiza la consistencia de los datos.

    Parámetros:
    - name_new_resource (str): Nombre del nuevo recurso solicitado.
    - type_new_resource (str): Tipo del recurso solicitado.
    - description_new_resource (str): Descripción del recurso solicitado.
    - date_new_resource (str): Fecha de la solicitud del recurso.
    - quantity_new_resource (int): Cantidad del recurso solicitado.
    - comments_ins_resource (str): Comentarios adicionales sobre la solicitud del recurso.
    - id_support_ins (int): ID del miembro que realiza la solicitud.

    Retorna:
    - Tuple: Un par de valores:
        - bool: `True` si la operación fue exitosa, `False` si ocurrió un error.
        - str: Mensaje de éxito o error.
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.
    
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        # Iniciar una transacción
        with connection.begin() as transaction:
            query = text("""
                INSERT INTO peticion_nuevo_recurso 
                (nombre, tipo, descripcion, fecha_peticion, cantidad, notas, idMiembro) 
                VALUES (:name, :type, :description, :date, :quantity, :comments, :id_member);
            """)

            connection.execute(query, {
                "name": name_new_resource,
                "type": type_new_resource,
                "description": description_new_resource,
                "date": date_new_resource,
                "quantity": quantity_new_resource,
                "comments": comments_ins_resource,
                "id_member": id_support_ins,
            })

        # Confirmar éxito al finalizar la transacción
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

    Esta función permite eliminar una solicitud de recurso previamente realizada, identificada por su ID único. La operación se realiza dentro de una transacción para garantizar la integridad de los datos.

    Parámetros:
    - new_id_resource_selected (int): ID de la solicitud de recurso que se desea eliminar.

    Retorna:
    - Tuple: Un par de valores:
        - bool: `True` si la eliminación fue exitosa, `False` si no se encontró la petición o ocurrió un error.
        - str: Mensaje de éxito o error.
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.

    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        # Iniciar una transacción
        with connection.begin() as transaction:
            query = text("""
                DELETE FROM peticion_nuevo_recurso WHERE idNuevoRecurso = :id_resource;
            """)
            result = connection.execute(query, {"id_resource": new_id_resource_selected})

            # Verificar si se eliminó alguna fila
            if result.rowcount > 0:
                return True, f"Petición con ID #{new_id_resource_selected} eliminada exitosamente."
            else:
                return False, f"No se encontró una petición con ID #{new_id_resource_selected}."

    except Exception as e:
        # Si ocurre un error, la transacción se revierte automáticamente
        print("Error al eliminar la petición de recurso:", e)
        return False, f"Error al eliminar la petición de recurso: {e}"

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

############################################################### Actividad ###############################################################
# Listo
def consultar_actividades():
    """
    Ejecuta una consulta en la base de datos y devuelve todas las actividades.

    Esta función recupera todas las actividades registradas en la tabla `actividad` de la base de datos
    y las devuelve en formato de DataFrame de Pandas para su procesamiento.

    Retorna:
    - DataFrame: Un objeto Pandas DataFrame con los registros de la tabla `actividad`, o
    - str: En caso de error, retorna un mensaje con los detalles del error.
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.

    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        # Realizar la consulta para obtener todas las actividades
        df = pd.read_sql("SELECT * FROM actividad", connection)
        return df

    except Exception as e:
        # En caso de error en la consulta
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def consultar_actividades_id(id_support):
    """
    Ejecuta una consulta en la base de datos y devuelve todas las actividades asociadas a un miembro específico.

    Esta función recupera todas las actividades que están asociadas a un miembro determinado por su `idMiembro`
    y las devuelve en formato de DataFrame de Pandas para su procesamiento.

    Parámetros:
    - id_support (int): El identificador del miembro cuya actividades se desean consultar.

    Retorna:
    - DataFrame: Un objeto Pandas DataFrame con los registros de la tabla `actividad` filtrados por `idMiembro`, o
    - str: En caso de error, retorna un mensaje con los detalles del error.
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.

    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        # Realizar la consulta para obtener las actividades del miembro específico
        df = pd.read_sql(f"SELECT * FROM actividad WHERE idMiembro={id_support}", connection)
        return df

    except Exception as e:
        # En caso de error en la consulta
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def consultar_actividades_eliminacion():
    """
    Ejecuta una consulta en la base de datos y devuelve todas las actividades con detalles adicionales.

    Esta función recupera todas las actividades y sus correspondientes detalles de los clientes y miembros
    asociados. Devuelve la información en un formato de DataFrame de Pandas para su posterior procesamiento.

    Retorna:
    - DataFrame: Un objeto Pandas DataFrame con los registros de la tabla `actividad`, incluyendo el nombre
      del cliente y del miembro asociados a cada actividad, o
    - str: En caso de error, retorna un mensaje con los detalles del error.
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.

    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        # Realizar la consulta para obtener las actividades con información adicional de cliente y miembro
        df = pd.read_sql("""
            SELECT a.*, c.nombre as nombre_c, m.nombre as nombre_m
            FROM actividad a
            INNER JOIN cliente c ON a.idCliente = c.idCliente
            INNER JOIN miembro m ON a.idMiembro = m.idMiembro;
        """, connection)
        return df

    except Exception as e:
        # En caso de error en la consulta
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def consultar_actividades_listado(type, id_miembro):
    """
    Ejecuta una consulta en la base de datos y devuelve todas las actividades según el tipo de consulta y el ID de miembro.
    
    Esta función permite consultar actividades de diferentes maneras, basándose en el parámetro `type`:
    - **type == 0**: Obtiene todas las actividades con información de cliente y miembro.
    - **type == 1**: Obtiene todas las actividades del historial.
    - **type == 2**: Obtiene actividades de un miembro específico con información de cliente y miembro.
    - **type == 3**: Obtiene actividades del historial de un miembro específico.

    Parametros:
    - type (int): El tipo de consulta (0, 1, 2 o 3).
    - id_miembro (int): El ID del miembro para consultas relacionadas con actividades de un miembro específico.
    
    Retorna:
    - DataFrame: Un objeto Pandas DataFrame con los registros de la consulta solicitada, o
    - str: En caso de error, retorna un mensaje con los detalles del error.
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.

    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        # Dependiendo del tipo de consulta, realiza una consulta diferente
        if type == 0:
            df = pd.read_sql("""
                SELECT a.*, m.nombre as miembro_n, c.nombre as cliente_n
                FROM actividad a
                INNER JOIN miembro m ON a.idMiembro = m.idMiembro
                INNER JOIN cliente c ON a.idCliente = c.idCliente;
            """, connection)
            return df

        elif type == 1:
            df = pd.read_sql("SELECT * FROM actividad_hist;", connection)
            return df

        elif type == 2:
            df = pd.read_sql(f"""
                SELECT a.*, m.nombre as miembro_n, c.nombre as cliente_n
                FROM actividad a
                INNER JOIN miembro m ON a.idMiembro = m.idMiembro
                INNER JOIN cliente c ON a.idCliente = c.idCliente
                WHERE a.idMiembro = '{id_miembro}';
            """, connection)
            return df

        elif type == 3:
            df = pd.read_sql(f"SELECT * FROM actividad_hist WHERE idMiembro='{id_miembro}';", connection)
            return df

    except Exception as e:
        # En caso de error en la consulta
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def insertar_actividad(name_ins_activity, datestart_ins_activity, description_ins_activity, type_ins_activity, state_ins_activity, id_client_ins, support_ins_activity):
    """
    Inserta una nueva actividad en la base de datos y actualiza el estado del miembro asociado utilizando una transacción.

    Esta función realiza dos acciones:
    1. Inserta una nueva actividad con los detalles proporcionados en la tabla `actividad`.
    2. Actualiza el estado del miembro asociado con la actividad, cambiando su disponibilidad a 'No Disponible' y su estatus a 'En Actividad'.

    Parametros:
    - name_ins_activity (str): El nombre de la actividad.
    - datestart_ins_activity (str): La fecha y hora de inicio de la actividad.
    - description_ins_activity (str): Descripción de la actividad.
    - type_ins_activity (str): El tipo de la actividad.
    - state_ins_activity (str): El estado de la actividad.
    - id_client_ins (int): El ID del cliente asociado con la actividad.
    - support_ins_activity (int): El ID del miembro de soporte asociado con la actividad.

    Retorna:
    - bool: `True` si la inserción de la actividad y la actualización del miembro fueron exitosas, de lo contrario, `False`.
    - str: Un mensaje de éxito o error detallado.
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.

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
        # Cerrar la conexión
        cerrarConexion(connection)

def cerrar_actividad(id_activity, date_end, datemodified, modifyby):
    """
    Cierra una actividad realizando las actualizaciones, inserciones y eliminaciones necesarias de forma atómica,
    y verifica que el miembro no tenga más actividades abiertas para actualizar su disponibilidad.

    Esta función realiza varias acciones relacionadas con el cierre de una actividad:
    1. Actualiza la fecha de fin de la actividad.
    2. Inserta un registro en `actividad_hist` con los datos de la actividad.
    3. Inserta los recursos asociados a la actividad en `recurso_hist` si no existen.
    4. Actualiza la factura asociada con la actividad, estableciendo su estatus como "Cerrada".
    5. Inserta la factura en `factura_hist`.
    6. Inserta los recursos asociados en `actividad_has_recurso_hist`.
    7. Verifica si el miembro de soporte tiene más actividades abiertas; si no, actualiza su estado de disponibilidad.
    8. Elimina los registros originales de las tablas `factura`, `actividad_has_recurso` y `actividad`.

    Parametros:
    - id_activity (int): ID de la actividad a cerrar.
    - date_end (str): Fecha de fin de la actividad.
    - datemodified (str): Fecha de modificación de la factura.
    - modifyby (str): Nombre de la persona que modificó la factura.

    Retorna:
    - int: `1` si la transacción se completó con éxito, `0` si hubo un error.
    - str: Un mensaje de éxito o error detallado.
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
    """
    Ejecuta una consulta en la base de datos y devuelve las actividades que están disponibles para actualizar,
    basándose en el estado de la actividad y el miembro especificado.

    Esta función consulta la tabla de actividades para devolver las actividades que tienen uno de los siguientes estados:
    'Abierto', 'En Curso' o 'Pendiente', según el tipo de consulta solicitada:
    
    - Si `type == 0`: Devuelve todas las actividades con el estado 'Abierto', 'En Curso' o 'Pendiente'.
    - Si `type == 1`: Devuelve las actividades con el estado 'Abierto', 'En Curso' o 'Pendiente' para un miembro específico, basado en su `idMiembro`.

    Parametros:
    - type (int): Tipo de consulta:
        - `0` para obtener todas las actividades disponibles.
        - `1` para obtener las actividades disponibles de un miembro específico.
    - id_miembro (int, opcional): El ID del miembro, necesario cuando `type == 1`.

    Retorna:
    - DataFrame de pandas con las actividades disponibles para actualizar, o un mensaje de error si no se pudo ejecutar la consulta.
    """
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

    Esta función actualiza una actividad con nueva información y ajusta la disponibilidad de los miembros involucrados.
    Si el miembro asignado a la actividad cambia, se realiza una verificación para asegurarse de que el miembro anterior
    tenga actividades pendientes, y si no es el caso, su disponibilidad y estatus se actualizan.

    Además, se actualiza el estado del nuevo miembro asignado a la actividad.

    Parametros:
    - name_upd_activity (str): Nuevo nombre de la actividad.
    - type_upd_activity (str): Nuevo tipo de actividad.
    - description_upd_activity (str): Nueva descripción de la actividad.
    - actions_upd_activity (str): Nuevas acciones realizadas en la actividad.
    - state_upd_activity (str): Nuevo estado de la actividad.
    - id_support_selected (int): ID del nuevo miembro asignado a la actividad.
    - id_client_selected (int): ID del cliente asociado a la actividad.
    - support_selected_first (int): ID del miembro previamente asignado a la actividad.
    - id_activity_selected (int): ID de la actividad a actualizar.

    Retorna:
    - tuple: (bool, str) donde:
        - `bool` es True si la transacción se completó con éxito, False en caso contrario.
        - `str` es un mensaje que describe el resultado de la operación.
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
    """
    Ejecuta una consulta en la base de datos y devuelve los miembros según el tipo de consulta solicitado.

    La función realiza una consulta en la base de datos para obtener información sobre los miembros.
    Según el valor del parámetro `type`, devuelve todos los miembros o solo sus identificadores y nombres.

    Parametros:
    - type (int): Tipo de consulta que determina qué datos de los miembros se deben devolver:
        - 0: Devuelve todos los campos de la tabla `miembro`.
        - 1: Devuelve solo el `idMiembro` y `nombre` de los miembros.

    Returns:
    - pd.DataFrame: Un dataframe de Pandas que contiene los resultados de la consulta.
    - str: Un mensaje de error si no se puede establecer la conexión o si ocurre un problema durante la consulta.
    """
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        if type == 0:
            df = pd.read_sql("SELECT * FROM miembro;", connection)
            return df
        elif type == 1:
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
    """
    Consulta el ID del miembro en la base de datos basado en su correo electrónico.

    Esta función busca un miembro específico utilizando su correo electrónico como parámetro. Si el miembro es encontrado,
    se devuelve su ID; si no se encuentra, se devuelve un mensaje indicativo.
    
    Parámetros:
    - email (str): El correo electrónico del miembro cuya ID se desea consultar.

    Retorna:
    - bool: Un valor booleano que indica si se encontró el miembro (True si se encontró, False si no).
    - int/str: Si se encontró el miembro, retorna su ID (int); si no, retorna un mensaje indicando que no se encontró el miembro (str),
      o un mensaje de error si ocurre un fallo en la consulta.

    
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.

    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        # Realizar la consulta para obtener el ID del miembro basado en el email
        query = text("SELECT idMiembro FROM miembro WHERE email = :email LIMIT 1;")
        result = connection.execute(query, {"email": email}).fetchone()

        if result is not None:
            # Retornar True y el ID del miembro encontrado
            return True, result[0]
        else:
            # Retornar False y mensaje si no se encontró el miembro
            return False, "No se encontró un miembro con ese email."

    except Exception as e:
        # Captura cualquier error en la consulta o en la conexión
        print("Error al ejecutar la consulta:", e)
        return False, f"Error al ejecutar la consulta: {e}"

    finally:
        # Asegurarse de cerrar la conexión con la base de datos
        cerrarConexion(connection)

def obtener_actividades_y_promedio(support_id):
    """
    Obtiene el número de actividades por soporte, actividades históricas y el tiempo promedio de actividades históricas, 
    devolviendo tres DataFrames.

    Esta función realiza tres consultas en la base de datos relacionadas con un miembro específico (por su `support_id`):
    1. El número de actividades activas asociadas al miembro.
    2. El número de actividades históricas asociadas al miembro.
    3. El tiempo promedio de duración de las actividades históricas asociadas al miembro.

    Parámetros:
    - support_id (int): El identificador del miembro cuya información se desea obtener.

    Retorna:
    - bool: Un valor booleano que indica si las consultas fueron exitosas (True) o no (False).
    - DataFrames: Tres objetos Pandas DataFrame con los resultados de las consultas realizadas:
        - El primer DataFrame contiene el número de actividades activas por soporte.
        - El segundo DataFrame contiene el número de actividades históricas por soporte.
        - El tercer DataFrame contiene el promedio de tiempo de las actividades históricas.
    - str: En caso de error, retorna un mensaje con los detalles del error.
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.
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
                SELECT AVG(DATEDIFF(fecha_fin_a, fecha_inicio_a)) AS promTiempo 
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
        # Cierra la conexión si fue abierta
        cerrarConexion(connection)

def insertar_miembro(name_ins_support, phone_ins_support, email_ins_support, address_ins_support, 
                     disponibility_ins_support, status_ins_support, comments_ins_support):
    """
    Inserta un nuevo miembro en la base de datos dentro de una transacción si el correo no está registrado.

    Esta función primero verifica si ya existe un miembro con el correo proporcionado. Si el correo no está 
    registrado, inserta un nuevo miembro en la base de datos con los valores especificados para nombre, teléfono, 
    correo electrónico, dirección, disponibilidad, estatus y notas.

    Parámetros:
    - name_ins_support (str): El nombre del miembro a insertar.
    - phone_ins_support (str): El número de teléfono del miembro a insertar.
    - email_ins_support (str): El correo electrónico del miembro a insertar.
    - address_ins_support (str): La dirección del miembro a insertar.
    - disponibility_ins_support (str): La disponibilidad del miembro a insertar.
    - status_ins_support (str): El estatus del miembro a insertar.
    - comments_ins_support (str): Los comentarios relacionados con el miembro a insertar.

    Retorna:
    - bool: Un valor booleano que indica si la inserción fue exitosa (True) o no (False).
    - str: En caso de éxito, retorna un mensaje indicando que el miembro fue insertado correctamente.
    - str: En caso de error, retorna un mensaje con los detalles del error, como si el correo ya está registrado.
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."
    
    try:
        # Inicia la transacción
        with connection.begin():  # Transacción
            
            # Verificar si ya existe un miembro con el correo proporcionado
            query_check_email = text("""
                SELECT COUNT(*) AS count 
                FROM miembro 
                WHERE email = :email;
            """)
            result = connection.execute(query_check_email, {"email": email_ins_support}).fetchone()

            # Si existe un miembro con el correo, detener el proceso
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
    """
    Verifica si un miembro tiene actividades asociadas. Si no tiene, elimina la petición y luego al miembro en una transacción.

    Esta función realiza una transacción que primero verifica si el miembro con el `id_support_selected` tiene 
    actividades asociadas. Si el miembro tiene actividades abiertas, no se permite la eliminación. Si no tiene 
    actividades asociadas, se elimina la petición relacionada con el miembro y luego se elimina al miembro de la base de datos.

    Parámetros:
    - id_support_selected (int): El ID del miembro que se desea eliminar.

    Retorna:
    - bool: Un valor booleano que indica si la operación fue exitosa (True) o no (False).
    - str: En caso de éxito, retorna un mensaje indicando que el miembro y su petición fueron eliminados correctamente.
    - str: En caso de error o si el miembro tiene actividades asociadas, retorna un mensaje con los detalles del error.
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.
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
    """
    Ejecuta una consulta en la base de datos y devuelve uno de los miembros de acuerdo a su id.

    Esta función consulta la base de datos para recuperar los detalles de un miembro específico 
    identificado por su `id_miembro`. La consulta devuelve todos los datos del miembro solicitado 
    en formato de DataFrame de Pandas, si el miembro es encontrado.

    Parámetros:
    - id_miembro (int): El identificador único del miembro que se desea consultar.

    Retorna:
    - DataFrame: Un objeto Pandas DataFrame con los detalles del miembro, o
    - str: En caso de error, retorna un mensaje con los detalles del error.
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        # Realiza la consulta para obtener los detalles del miembro por su id
        df = pd.read_sql(f"SELECT * FROM miembro WHERE idMiembro='{id_miembro}' LIMIT 1;", connection)
        return df

    except Exception as e:
        # En caso de error en la consulta
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

    Esta función actualiza los detalles de un miembro existente en la base de datos, basándose en su 
    `id_support_selected`. La actualización se realiza dentro de una transacción para garantizar la 
    integridad de los datos. Si se produce un error durante la operación, la transacción se revierte.

    Parámetros:
    - id_support_selected (int): El identificador único del miembro que se desea actualizar.
    - name_upd_support (str): El nuevo nombre del miembro.
    - phone_upd_support (str): El nuevo teléfono del miembro.
    - email_upd_support (str): El nuevo email del miembro.
    - address_upd_support (str): La nueva dirección del miembro.
    - disponibility_upd_support (str): La nueva disponibilidad del miembro.
    - status_upd_support (str): El nuevo estatus del miembro.
    - comments_upd_support (str): Los nuevos comentarios sobre el miembro.

    Retorna:
    - bool: `True` si la actualización fue exitosa, `False` si hubo un error.
    - str: Un mensaje indicando el resultado de la operación.
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        with connection.begin():  # Inicia la transacción
            # Definir la consulta de actualización
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

            # Ejecutar la consulta
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

        # Si la transacción fue exitosa
        return True, f"Miembro con ID #{id_support_selected} actualizado exitosamente."

    except Exception as e:
        # Si ocurre un error, la transacción se revierte automáticamente
        print("Error al actualizar el miembro:", e)
        return False, f"Error al actualizar el miembro: {e}"

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def actualizar_miembro_indie(id_support_selected, name_upd_support, phone_upd_support, address_upd_support, comments_upd_support):
    """
    Actualiza los datos de un miembro en la base de datos utilizando una transacción.

    Esta función actualiza los detalles de un miembro existente en la base de datos, basándose en su 
    `id_support_selected`. La actualización incluye solo los campos de nombre, teléfono, dirección 
    y comentarios del miembro. La operación se realiza dentro de una transacción para asegurar la 
    integridad de los datos. Si ocurre un error durante la operación, la transacción se revierte.

    Parámetros:
    - id_support_selected (int): El identificador único del miembro que se desea actualizar.
    - name_upd_support (str): El nuevo nombre del miembro.
    - phone_upd_support (str): El nuevo teléfono del miembro.
    - address_upd_support (str): La nueva dirección del miembro.
    - comments_upd_support (str): Los nuevos comentarios sobre el miembro.

    Retorna:
    - bool: `True` si la actualización fue exitosa, `False` si hubo un error.
    - str: Un mensaje indicando el resultado de la operación.
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, "No se pudo establecer la conexión a la base de datos."

    try:
        with connection.begin():  # Inicia la transacción
            # Definir la consulta de actualización
            query_actualizar = text("""
                UPDATE miembro 
                SET nombre = :name,
                    telefono = :phone,
                    direccion = :address,
                    notas = :comments
                WHERE idMiembro = :id;
            """)

            # Ejecutar la consulta
            connection.execute(query_actualizar, {
                "name": name_upd_support,
                "phone": phone_upd_support,
                "address": address_upd_support,
                "comments": comments_upd_support,
                "id": id_support_selected,
            })

        # Si la transacción fue exitosa
        return True, f"Miembro con ID #{id_support_selected} actualizado exitosamente."

    except Exception as e:
        # Si ocurre un error, la transacción se revierte automáticamente
        print("Error al actualizar el miembro:", e)
        return False, f"Error al actualizar el miembro: {e}"

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

############################################################### Factura ###############################################################
# Listo
def consultar_facturas(type, email):
    """
    Ejecuta una consulta en la base de datos y devuelve las facturas, de acuerdo con el tipo y los miembros.

    Esta función permite obtener las facturas de la base de datos, filtradas por un tipo específico:
    - Si `type` es 0, se obtienen todas las facturas.
    - Si `type` es 1, se obtienen solo las facturas correspondientes al miembro con el email proporcionado.
    
    La consulta también incluye detalles adicionales de las actividades asociadas a cada factura y los miembros relacionados.

    Parámetros:
    - type (int): Un valor que determina el tipo de consulta.
        - 0: Recupera todas las facturas.
        - 1: Recupera las facturas filtradas por el email del miembro.
    - email (str): El correo electrónico del miembro para filtrar las facturas (solo se utiliza cuando `type` es 1).

    Retorna:
    - DataFrame: Un objeto Pandas DataFrame con los registros de las facturas, incluyendo el ID y nombre de actividad, y el ID y nombre del miembro.
    - str: En caso de error, retorna un mensaje con los detalles del error.
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.

    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        # Consulta para obtener todas las facturas
        if type == 0:
            df = pd.read_sql("""
                SELECT f.*, a.idActividad as idA, a.nombre as nombre_a, 
                    m.idMiembro as idM, m.nombre as nombre_m 
                FROM factura f 
                INNER JOIN miembro m ON f.idMiembro = m.idMiembro 
                INNER JOIN actividad a ON f.idActividad = a.idActividad;
            """, connection)
            return df

        # Consulta para obtener las facturas de un miembro específico por email
        elif type == 1:
            df = pd.read_sql(f"""
                SELECT f.*, a.idActividad as idA, a.nombre as nombre_a, 
                    m.idMiembro as idM, m.nombre as nombre_m 
                FROM factura f 
                INNER JOIN miembro m ON f.idMiembro = m.idMiembro 
                INNER JOIN actividad a ON f.idActividad = a.idActividad 
                WHERE m.email = '{email}';
            """, connection)
            return df

    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def consultar_facturas_hist(id_activity_closed):
    """
    Ejecuta una consulta en la base de datos y devuelve las facturas históricas asociadas a una actividad cerrada.

    Esta función permite obtener las facturas históricas de la base de datos para una actividad cerrada específica,
    junto con los detalles del miembro y la actividad correspondiente.

    Parámetros:
    - id_activity_closed (int): El ID de la actividad cerrada para la cual se desean obtener las facturas históricas.

    Retorna:
    - DataFrame: Un objeto Pandas DataFrame con los registros de las facturas históricas, incluyendo el nombre de la actividad,
      el nombre del miembro, y el ID del miembro asociado a la actividad.
    - str: En caso de error, retorna un mensaje con los detalles del error.
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.

    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        # Consulta para obtener las facturas históricas asociadas a una actividad cerrada específica
        df = pd.read_sql(f"""
            SELECT fh.*, ah.nombre_a, ah.nombre_m, ah.idMiembro as idM 
            FROM factura_hist fh 
            INNER JOIN actividad_hist ah ON fh.idActividad = ah.idActividad 
            WHERE fh.idActividad = '{id_activity_closed}';
        """, connection)
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

    Retorna:
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

    Parámetros:
        name_ins_bill (str): Nombre de la factura.
        dateemission_ins_bill (str): Fecha de emisión de la factura.
        cost_ins_bill (float): Costo de la factura.
        type_ins_bill (str): Tipo de factura.
        tax_ins_bill (float): Impuesto aplicado a la factura.
        createby_ins_bill (str): Usuario que creó la factura.
        id_activity_ins (int): ID de la actividad asociada.
        id_support_ins (int): ID del miembro asociado.

    Retorna:
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
    """
    Ejecuta una consulta en la base de datos y devuelve todas las facturas que no están cerradas para actualización.

    Esta función obtiene todas las facturas cuyo estatus no es 'Cerrada', junto con los detalles de los miembros
    y las actividades asociadas a cada factura, permitiendo su posterior actualización.

    Retorna:
    - DataFrame: Un objeto Pandas DataFrame con los registros de las facturas no cerradas, incluyendo información
      adicional sobre el miembro y la actividad asociada a cada factura.
    - str: En caso de error, retorna un mensaje con los detalles del error.
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.

    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        # Consulta para obtener las facturas no cerradas, junto con los detalles de los miembros y actividades
        df = pd.read_sql("""
            SELECT f.*, m.idMiembro as idM, a.idActividad as idA, m.nombre as nombre_m, a.nombre as nombre_a 
            FROM factura f 
            INNER JOIN miembro m ON f.idMiembro = m.idMiembro 
            INNER JOIN actividad a ON a.idActividad = f.idActividad 
            WHERE f.estatus != 'Cerrada';
        """, connection)
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

    Parámetros:
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

    Retorna:
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

    Parametros:
        id_bill_selected_delete (int): ID de la factura a cerrar.
        datemodified_del_bill (str): Fecha de modificación.
        modifyby_del_bill (str): Usuario que realiza el cierre.

    Retorna:
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

############################################################### Reportes ############################################################### 
def consultar_actividades_report(start_date, end_date):
    """
    Ejecuta consultas en la base de datos para obtener estadísticas sobre las actividades realizadas
    durante un período específico, incluyendo el número de actividades cerradas, actividades abiertas
    y el promedio de tiempo de solución.

    Esta función realiza tres consultas:
    1. Contar el número de actividades cerradas en el rango de fechas especificado.
    2. Contar el número de actividades abiertas en el rango de fechas especificado.
    3. Calcular el tiempo promedio de solución de las actividades cerradas en el rango de fechas.

    Parámetros:
    - start_date (str): Fecha de inicio en formato 'YYYY-MM-DD'.
    - end_date (str): Fecha de fin en formato 'YYYY-MM-DD'.

    Retorna:
    - Tuple: Un tuple con tres DataFrames de Pandas:
        1. Un DataFrame con el número de actividades cerradas por fecha de cierre.
        2. Un DataFrame con el número de actividades abiertas por fecha de inicio.
        3. Un DataFrame con el promedio de tiempo de solución de las actividades cerradas.
    - str: En caso de error, retorna un mensaje con los detalles del error.
    """
    connection = conectarBase()  # Establece la conexión con la base de datos.

    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        # Consulta 1: Número de actividades cerradas en el rango de fechas
        df = pd.read_sql(f"""
            SELECT fecha_fin_a as fecha_cierre, count(*) as actividades_cerradas 
            FROM actividad_hist 
            WHERE fecha_fin_a >= '{start_date}' AND fecha_fin_a <= '{end_date}' 
            GROUP BY fecha_fin_a;
        """, connection)

        # Consulta 2: Número de actividades abiertas en el rango de fechas
        df2 = pd.read_sql(f"""
            SELECT fecha_inicio as fecha_apertura, count(*) as actividades_abiertas 
            FROM actividad 
            WHERE fecha_inicio >= '{start_date}' AND fecha_inicio <= '{end_date}' 
            GROUP BY fecha_inicio;
        """, connection)

        # Consulta 3: Promedio de tiempo de solución de las actividades cerradas
        df3 = pd.read_sql(f"""
            SELECT AVG(fecha_fin_a - fecha_inicio_a) as promedio_solucion 
            FROM actividad_hist 
            WHERE fecha_fin_a >= '{start_date}' AND fecha_fin_a <= '{end_date}';
        """, connection)

        return df, df2, df3

    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

def obtener_metricas_facturacion_report(start_date, end_date):
    """
    Obtiene métricas de facturación por actividades y clientes dentro de un rango de fechas especificado.

    Realiza dos consultas dentro de una transacción:
    1. Métricas de facturación por actividad, que incluyen el total de costo e impuestos asociados.
    2. Métricas de facturación por cliente, que incluyen el total de costo e impuestos para cada cliente.

    Parámetros:
    - start_date (str): Fecha de inicio en formato 'YYYY-MM-DD'.
    - end_date (str): Fecha de fin en formato 'YYYY-MM-DD'.

    Retorna:
    - tuple: Un tuple con tres valores:
        1. bool: Indica si la operación fue exitosa.
        2. pd.DataFrame: Métricas de facturación por actividad.
        3. pd.DataFrame: Métricas de facturación por cliente.
    """
    connection = conectarBase()

    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return False, None, None

    try:
        # Inicia la transacción
        with connection.begin():  # Inicia una transacción
            # Consulta para obtener métricas de facturación por actividad
            query_activities_metrics = text(f"""
                SELECT 
                    fh.idActividad, 
                    ah.nombre_a, 
                    SUM(fh.costo + fh.impuesto) AS total
                FROM factura_hist fh
                INNER JOIN actividad_hist ah ON fh.idActividad = ah.idActividad
                WHERE fh.fecha_modificacion >= '{start_date}' AND fh.fecha_modificacion <= '{end_date}'
                GROUP BY fh.idActividad;
            """)
            activities_result = connection.execute(query_activities_metrics)
            activities_df = pd.DataFrame(activities_result.fetchall(), columns=activities_result.keys())

            # Consulta para obtener métricas de facturación por cliente
            query_client_metrics = text(f"""
                SELECT 
                    ah.idCliente, 
                    ah.nombre_c, 
                    SUM(fh.costo + fh.impuesto) AS total
                FROM factura_hist fh
                INNER JOIN actividad_hist ah ON fh.idActividad = ah.idActividad
                WHERE fh.fecha_modificacion >= '{start_date}' AND fh.fecha_modificacion <= '{end_date}'
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

def obtener_recursos_tipo(start_date, end_date):
    """
    Ejecuta las consultas para obtener la cantidad de recursos agrupados por fecha de finalización,
    separados por los tipos 'Material' y 'Herramienta'.

    Las consultas se realizan en dos partes:
    1. Cuenta la cantidad de recursos de tipo 'Material' por fecha de finalización.
    2. Cuenta la cantidad de recursos de tipo 'Herramienta' por fecha de finalización.

    Parámetros:
    - start_date (str): Fecha de inicio en formato 'YYYY-MM-DD'.
    - end_date (str): Fecha de fin en formato 'YYYY-MM-DD'.

    Retorna:
    - tuple: Un tuple con tres elementos:
        1. `result_material` (pd.DataFrame): Resultados para 'Material'.
        2. `result_herramienta` (pd.DataFrame): Resultados para 'Herramienta'.
        3. `success` (bool): Indica si las consultas se ejecutaron correctamente. Si es `True`, las consultas fueron exitosas; de lo contrario, fue `False`.
    """
    # Obtener la conexión a la base de datos
    connection = conectarBase()

    # Verificar si la conexión fue exitosa
    if connection is None:
        print("No se pudo conectar a la base de datos.")
        return None, None, False

    # Consultas SQL
    query_material = f"""
    SELECT 
        ah.fecha_fin_a as fecha, 
        count(*) as no_materiales
    FROM 
        actividad_hist ah
    INNER JOIN 
        actividad_has_recurso_hist arh ON ah.idActividad = arh.idActividad
    INNER JOIN 
        recurso_hist rh ON arh.idRecurso = rh.idRecurso
    WHERE 
        rh.tipo = 'Material'
    AND 
        ah.fecha_fin_a >= '{start_date}'  AND ah.fecha_fin_a <= '{end_date}'
    GROUP BY 
        ah.fecha_fin_a;
    """

    query_herramienta = f"""
    SELECT 
        ah.fecha_fin_a as fecha, 
        count(*) as no_herramientas
    FROM 
        actividad_hist ah
    INNER JOIN 
        actividad_has_recurso_hist arh ON ah.idActividad = arh.idActividad
    INNER JOIN 
        recurso_hist rh ON arh.idRecurso = rh.idRecurso
    WHERE 
        rh.tipo = 'Herramienta'
    AND 
        ah.fecha_fin_a >= '{start_date}'  
    AND 
        ah.fecha_fin_a <= '{end_date}'
    GROUP BY 
        ah.fecha_fin_a;
    """

    try:
        # Ejecutar ambas consultas
        result_material = pd.read_sql_query(query_material, connection)
        result_herramienta = pd.read_sql_query(query_herramienta, connection)

        # Retornar los resultados junto con un indicador de éxito
        return result_material, result_herramienta, True

    except Exception as e:
        print(f"Error al ejecutar las consultas: {e}")
        return None, None, False

    finally:
        # Cerrar la conexión a la base de datos
        connection.close()

def obtener_actividades_miembro(start_date, end_date):
    """
    Ejecuta una consulta para obtener el promedio de actividades por miembro,
    dentro de una transacción segura.

    La función cuenta el número de actividades realizadas por cada miembro 
    dentro del rango de fechas proporcionado. Utiliza una transacción 
    para garantizar que la consulta se ejecute de manera segura.

    Parámetros:
    - start_date (str): Fecha de inicio en formato 'YYYY-MM-DD'.
    - end_date (str): Fecha de fin en formato 'YYYY-MM-DD'.

    Retorna:
    - tuple: Un tuple con dos elementos:
        1. `result` (pd.DataFrame): DataFrame que contiene las columnas:
            - `idMiembro`: ID del miembro.
            - `nombre_m`: Nombre del miembro.
            - `actividades`: Número total de actividades realizadas por el miembro en el rango de fechas especificado.
        2. `success` (bool): Indicador de éxito, `True` si la consulta fue exitosa, `False` si ocurrió un error.
    """
    # Obtener la conexión a la base de datos
    connection = conectarBase()

    if connection is None:
        print("No se pudo conectar a la base de datos.")
        return None, False

    # Consulta SQL
    query = f"""
    SELECT idMiembro, 
           nombre_m, 
           COUNT(*) as actividades
    FROM actividad_hist
    WHERE fecha_fin_a >= '{start_date}' AND  fecha_fin_a <= '{end_date}'
    GROUP BY idMiembro, nombre_m;
    """

    try:
        # Iniciar una transacción
        with connection.begin() as transaction:
            # Ejecutar la consulta y cargar los resultados en un DataFrame
            result = pd.read_sql_query(query, connection)

        # Devolver los resultados y éxito
        return result, True

    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None, False

    finally:
        # Cerrar la conexión
        connection.close()

############################################################### General ############################################################### 
#def consultar_nombre_insensible(nombre, base_datos):

    """Consulta si hay un nombre igual en la base de datos, insensible a mayúsculas y minúsculas."""
    # Importar la conexión desde conectarBase
    connection = conectarBase()

    # Verificar si la conexión fue exitosa
    if connection is None:
        print("No se pudo conectar a la base de datos.")
        return False

    # Asegurarse de que el nombre esté en minúsculas para la comparación
    query = f"""
    SELECT * FROM erp.{base_datos}
    WHERE nombre COLLATE utf8_general_ci = %s;
    """

    try:
        # Ejecutar la consulta directamente
        result = pd.read_sql_query(query, connection, params=(nombre,))
        
        # Verificar si se encontraron resultados
        if not result.empty:
            return True  # Se encontró el campo
        return False  # No se encontró el campo

    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return False

    finally:
        # Cerrar la conexión
        connection.close()

#def existe_cliente(nombre):
    """
    Consulta si hay un cliente con el nombre especificado en la base de datos, 
    insensible a mayúsculas y minúsculas.

    :param nombre: Nombre del cliente a buscar.
    :return: True si se encuentra el cliente, False en caso contrario.
    """
    # Obtener conexión a la base de datos
    connection = conectarBase()

    # Verificar si la conexión fue exitosa
    if connection is None:
        print("No se pudo conectar a la base de datos.")
        return False

    # Consulta SQL con parámetros para evitar inyección SQL
    query = """
    SELECT * FROM erp.cliente
    WHERE nombre COLLATE utf8_general_ci = %s;
    """

    try:
        # Ejecutar la consulta y cargar resultados en un DataFrame
        result = pd.read_sql_query(query, connection, params=(nombre,))
        
        # Verificar si se encontraron resultados
        if not result.empty:
            return True  # Se encontró el cliente
        return False  # No se encontró el cliente

    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return False

    finally:
        # Cerrar la conexión a la base de datos
        connection.close()

#def eliminar(query):
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

def cerrarConexion(connection):
    """
    Cierra la conexión a la base de datos.

    Esta función asegura que la conexión a la base de datos se cierre correctamente,
    liberando los recursos asociados con ella. Si la conexión no es `None`, la cierra 
    y muestra un mensaje indicando que la conexión ha sido cerrada.

    Parámetros:
    - connection: Objeto de conexión a la base de datos que se desea cerrar.
    
    No retorna valor.
    """
    if connection is not None:
        connection.close()
        print("Conexión cerrada")




