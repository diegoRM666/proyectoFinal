import streamlit as st
import pandas as pd
import time
from menu import menu_with_redirect
import logic.bd as bd
import random as random
from datetime import datetime
import logic.utilities as ut 


# Comprueba que el usuario este loggeado.
menu_with_redirect()

#Creamos un titulo
st.markdown("# 💼 Actividad")

# Mostrar las disintas actividades a realizar
tab_lst_activity, tab_ins_activity, tab_upd_activity, tab_del_activity= \
      st.tabs(["Listar Actividades","Crear Actividad", "Actualizar Actividad", "Terminar Actividad"])

# Pestaña para listar actividades
with tab_lst_activity:
    # Genera columnas para el formato del botón de refresco
    col1, col2 = st.columns([95,1])
    with col2: 
        # Renderiza el botón de refresco
        if st.button("🔄", key="ref_resources"):
            st.rerun()
    
    # Verifica que el rol del usuario sea admin 
    if any(role in ["admin"] for role in st.session_state["roles"]):
        # Funcion que trae todas las actividades abiertas
        activities = bd.consultar_actividades_listado(0,0)

        # Verifica que el resultado no sea vacio
        if activities is not None and not activities.empty:

            # Definir el número de columnas
            num_cols = 2
            cols = st.columns(num_cols)
            
            # Inicializar el índice para repartir a las columnas
            index = 0

            # Iterar sobre los activities en el DataFrame
            for _, activity in activities.iterrows():
                col = cols[index % num_cols]  # Alterna entre las columnas (0 y 1)
                
                # Mostrar la información del activity en la columna correspondiente
                with col:
                    with st.container(border=True):
                        st.markdown(f"## 💼 #{activity['idActividad']} - {activity['nombre']}")
                        st.markdown(f'''📆 Fecha Inicio: :green[{activity['fecha_inicio']}]''')
                        st.markdown(f"🔠 Descripción: {activity['descripcion']}")
                        st.markdown(f"#️⃣ Tipo: {activity['tipo']}")
                        st.markdown(f"🏢 Cliente: {activity['cliente_n']}")
                        st.markdown(f"👤 Atendido Por: {activity['miembro_n']}")
                        # Despliega en caso de que las acciones realizadas existan
                        if activity['acciones_realizadas'] != "" and activity['acciones_realizadas'] != "None":
                            st.markdown(f"⚙️ Acciones Realizadas: {activity['acciones_realizadas']}")
                        
                        # Muestra en distinto color y con distinto emoji de acuerdo al estado de la actividad
                        if activity['estado'] in ["Abierto"]:
                            st.markdown(f'''### 🔴 :red[{activity['estado']}]''')
                        elif activity['estado'] in ["En Curso", "Pendiente", "Escalada Con Fabricante" ]:
                            st.markdown(f'''### 🟡 :orange[{activity['estado']}]''')
                        else: 
                            st.markdown(f'''### 🟢 :green[{activity['estado']}]''')
                        
                # Actualizar el índice para alternar entre las columnas
                index += 1
        # En caso de que el resultado este vacio
        else:
            st.warning("No existen datos")

        # Seccion de Actividades Cerradas
        st.markdown("---")
        st.markdown("### Actividades Cerradas")

        # Funcion que extrae las actividades historicas
        activities_closed =bd.consultar_actividades_listado(1,0)

        # Verifica que los resultados no sea vacio
        if activities_closed is not None and not activities_closed.empty:
            
            # Iterar sobre los activities en el DataFrame
            for _, activity in activities_closed.iterrows():
                # Creamos un contenedor para desplegar la informacion        
                with st.container(border=True):
                    st.markdown(f"## 💼 #{activity['idActividad']} - {activity['nombre_a']}")
                    st.markdown(f"🔠 Descripción: {activity['descripcion_a']}")
                    st.markdown(f'''📆 Periodo: :green[{activity['fecha_inicio_a']}] - :red[{activity['fecha_fin_a']}]''')
                    st.markdown(f"⚙️ Acciones Realizadas: {activity['acciones_realizadas_a']}")
                    st.markdown(f"#️⃣ Tipo: {activity['tipo_a']}")
                    st.markdown(f"### 🏢 Cliente: #{activity['idCliente']} - {activity['nombre_c']}")
                    st.markdown(f"☎️ Telefono: {activity['telefono_c']}")
                    st.markdown(f"📧 Correo: {activity['email_c']}")
                    st.markdown(f"### 👤 Miembro: #{activity['idMiembro']} - {activity['nombre_m']}")
                    st.markdown(f"☎️ Telefono: {activity['telefono_m']}")
                    st.markdown(f"📧 Correo: {activity['email_m']}")
        
        # En caso de que el resultado sea vacio
        else:
            st.warning("No existen datos")
    
    # El caso del listado para usuario con rol user
    elif any(role in ["user"] for role in st.session_state["roles"]):
        # Consulta el identificador con el email del usuario
        state_email, result_email = bd.consultar_id_email(st.session_state['email'])
        
        # Funcion que consulta que actividades abiertas tiene el usuario
        activities = bd.consultar_actividades_listado(2, result_email)
        
        # Verifica que el resultado no sea vacio
        if activities is not None and not activities.empty:
            # Definir el número de columnas
            num_cols = 2
            cols = st.columns(num_cols)
            
            # Inicializar el índice para repartir a las columnas
            index = 0

            # Iterar sobre los activities en el DataFrame
            for _, activity in activities.iterrows():
                col = cols[index % num_cols]  # Alterna entre las columnas (0 y 1)
                
                # Mostrar la información del activity en la columna correspondiente
                with col:
                    with st.container(border=True):
                        st.markdown(f"## 💼 #{activity['idActividad']} - {activity['nombre']}")
                        st.markdown(f'''📆 Fecha Inicio: :green[{activity['fecha_inicio']}]''')
                        st.markdown(f"🔠 Descripción: {activity['descripcion']}")
                        st.markdown(f"#️⃣ Tipo: {activity['tipo']}")
                        st.markdown(f"🏢 Cliente: {activity['cliente_n']}")
                        st.markdown(f"👤 Atendido Por: {activity['miembro_n']}")
                        # Despliega en caso de que las acciones realizadas existan
                        if activity['acciones_realizadas'] != "" and activity['acciones_realizadas'] != "None":
                            st.markdown(f"⚙️ Acciones Realizadas: {activity['acciones_realizadas']}")

                        # Muestra en distinto color y con distinto emoji de acuerdo al estado de la actividad
                        if activity['estado'] in ["Abierto"]:
                            st.markdown(f'''### 🔴 :red[{activity['estado']}]''')
                        elif activity['estado'] in ["En Curso", "Pendiente"]:
                            st.markdown(f'''### 🟡 :orange[{activity['estado']}]''')
                        else: 
                            st.markdown(f'''### 🟢 :green[{activity['estado']}]''')
                        
                # Actualizar el índice para alternar entre las columnas
                index += 1

        # En caso de estar vacio, lo notifica
        else:
            st.warning("No existen datos")

        st.markdown("---")
        st.markdown("### Actividades Cerradas")

        # Hace una consulta de las actividades cerradas para el usuario
        activities_closed =bd.consultar_actividades_listado(3, result_email)

        # Verifica que el resultado no sea vacio
        if activities_closed is not None and not activities_closed.empty:
            
            # Iterar sobre los activities en el DataFrame
            for _, activity in activities_closed.iterrows():
                
                # Crea un contenedor para mostrar la actividad
                with st.container(border=True):
                    st.markdown(f"## 💼 #{activity['idActividad']} - {activity['nombre_a']}")
                    st.markdown(f"🔠 Descripción: {activity['descripcion_a']}")
                    st.markdown(f'''📆 Periodo: :green[{activity['fecha_inicio_a']}] - :red[{activity['fecha_fin_a']}]''')
                    st.markdown(f"⚙️ Acciones Realizadas: {activity['acciones_realizadas_a']}")
                    st.markdown(f"#️⃣ Tipo: {activity['tipo_a']}")
                    st.markdown(f"### 🏢 Cliente: #{activity['idCliente']} - {activity['nombre_c']}")
                    st.markdown(f"☎️ Telefono: {activity['telefono_c']}")
                    st.markdown(f"📧 Correo: {activity['email_c']}")
                    st.markdown(f"### 👤 Miembro: #{activity['idMiembro']} - {activity['nombre_m']}")
                    st.markdown(f"☎️ Telefono: {activity['telefono_m']}")
                    st.markdown(f"📧 Correo: {activity['email_m']}")

        # En caso de que el resultado sea vacio            
        else:
            st.warning("No existen datos")
    
    # En caso de que no tengamos ninguno de los dos roles
    else: 
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")

# Pestaña para insertar una actividad
with tab_ins_activity:
    # Verifica que el usuario tenga el rol de admin    
    if any(role in ["admin"] for role in st.session_state["roles"]):

        # Obtiene los clientes disponibles
        clients_available = bd.consultar_todos_clientes()
        # Obtiene los miembros 
        supports_available = bd.consultar_miembros(1) 
        
        # Verifica que los resultados no sean vacios 
        if clients_available is not None and not clients_available.empty and supports_available is not None and not supports_available.empty:
            combined_clients = [f"#{row['idCliente']} - {row['nombre']}" for index, row in clients_available.iterrows()]

            # Genera un formulario para llenar los campos de insercion de actividad
            with st.form("insert_activity", clear_on_submit=True):
                name_ins_activity = st.text_input("Nombre*: ", placeholder="Reemplazo Inyector Tinta")
                description_ins_activity = st.text_area("Descripción*: ", placeholder="Se requiere el reemplazo de...")
                type_ins_activity = st.selectbox("Tipo*: ", ["Matenimiento", "Incidencia"])
                client_ins_activity = st.selectbox("Cliente*: ", combined_clients)
                id_client_ins = int (client_ins_activity.split(' - ')[0][1:])
                state_ins_activity = "Abierto"
                
                # Obtencion de fecha de creacion, con formato 
                datestart_ins_activity = ut.get_today_date()
                
                # Asignacion automatica de actividades
                # Consulta primero la disponibilidad de los miembros que estan en estado "Libre"
                supports_available_activity = bd.consultar_dispo_miembros(0)
                # Verifica que el resultado no sea nulo, significa que le puede asignar a alguien de ellos la actividad
                if supports_available_activity is not None and not supports_available_activity.empty: 
                    # Selecciona de manera automatica a alguien 
                    support_ins_activity = random.choice(supports_available_activity['id'].tolist())
                    # Obtiene los datos de ese seleccionado de manera aleatorio
                    support_random_selected = supports_available_activity[supports_available_activity['id'] == support_ins_activity ]
                else:
                    # En caso de que todos este ocupados
                    st.warning("No hay Miembros Disponibles. Se asignará al Miembro con menos actividades")
                    # Consulta entonces la cantidad de actividades que cada quien tiene de manera activa
                    occupability_support = bd.consultar_dispo_miembros(1)
                    # Verifica que el resultado no sea vacio, ordenando primero el que tiene el menor numero de actividades
                    if occupability_support is not None and not occupability_support.empty:
                        # Luego toma el primero, que es el que tiene menos actividades
                        support_ins_activity = occupability_support.iloc[0]['id']
                        # Obtenemos los datos del miembro
                        support_random_selected = occupability_support[occupability_support['id'] == support_ins_activity]

                # Indicador de campos obligatorios
                st.markdown("*Campos Obligatorios")
            
                # Botón de envío
                submit_insert_activity = st.form_submit_button("Agregar")

                # Creamos un contenedor de mensajes, servira para luego limpiarlos
                message_container = st.empty()

                # Recuperamos la accion del boton
                if submit_insert_activity:
                    # Verifica que los campos obligatorios no esten vacios
                    if not name_ins_activity.strip() or not description_ins_activity.strip():
                        st.error("Actividad No Creada")
                        st.info("Llene todos los campos obligatorios")
                    else:
                        # Funcion que inserta la actividad, ademas modifica el estado del miembro
                        state_ins_activity, msj_ins_activity = bd.insertar_actividad(name_ins_activity, datestart_ins_activity, description_ins_activity, type_ins_activity, state_ins_activity, id_client_ins, support_ins_activity)
                        
                        # Verifica que la insercion se haya realizado de manera correcta
                        if state_ins_activity:
                            # Muesta el mensaje de exito y los datos de la insercion
                            st.success(msj_ins_activity)
                            st.info(f"{name_ins_activity} -- {description_ins_activity} -- {type_ins_activity} -- #{client_ins_activity} -- {datestart_ins_activity}")
                        else: 
                            # Muesta el mensaje de error al insertara
                            st.error(msj_ins_activity)
                    # Limpia los mensajes
                    time.sleep(5)
                    message_container.empty()
                    st.rerun()
        else: 
            st.warning("No hay Clientes o Miembros Dados de Alta")
    else: 
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")

# Pestaña para actualizar actividad
with tab_upd_activity:
    # Verifica que el usuario tenga un rol de admin
    if any(role in ["admin"] for role in st.session_state["roles"]):
        # Consula las actividades que se pueden actaulizar, los miembros y los clientes
        activities_available = bd.consultar_actividades_dispo(0, 0)
        supports_upd = bd.consultar_miembros(1)
        clients_upd = bd.consultar_todos_clientes()

        # Valida que los resultados no sean vacios
        if activities_available is not None and supports_upd is not None and not activities_available.empty and not supports_upd.empty:
            # Combina las columnas de identificador y nombre para las actividades
            combined_activities = [f"#{row['idActividad']} - {row['nombre']}" for index, row in activities_available.iterrows()]
            # Genera un objeto que permite seleccionar una actividad
            activity_selected = st.selectbox("Selecciona un Actividad", combined_activities, key="update_activities_sb")
            # Recupera el identificador de la actividad seleccionada
            id_activity_selected = int (activity_selected.split(' - ')[0][1:])
            # Obtiene la informacion de la actividad seleccionada
            activity_data = activities_available[activities_available['idActividad']==id_activity_selected]
            
            # Vamos a dar las posibilidades para los miembros
            combined_supports = [f"#{row['idMiembro']} - {row['nombre']}" for index, row in supports_upd.iterrows()]
            combined_clients = [f"#{row['idCliente']} - {row['nombre']}" for index, row in clients_upd.iterrows()]

            # Funcion para obtener indice de tipo y estatus seleccionados
            index_type, index_status = ut.dict_activity_upd(activity_data['tipo'].iloc[0], activity_data['estado'].iloc[0])

            # Obtencion de los datos del cliente y miembro
            client_data_tmp = clients_upd[clients_upd['idCliente']== activity_data['idCliente'].iloc[0]]
            support_data_tmp = supports_upd[supports_upd['idMiembro']== activity_data['idMiembro'].iloc[0]]   

            # Contendor para mostrar la información actual
            with st.container(border=True):
                # Se combinan las columnas de identificador y nombre, para el cliente y el miembro actual
                st.markdown(f"**Cliente Actual: #{client_data_tmp['idCliente'].iloc[0]} - {client_data_tmp['nombre'].iloc[0]}**")
                st.markdown(f"**Miembro Actual: #{support_data_tmp['idMiembro'].iloc[0]} - {support_data_tmp['nombre'].iloc[0]}**")

            # Renderiza un formulario
            with st.form("update_activity", clear_on_submit= True):
                name_upd_activity = st.text_input("Nombre*: ", value=f"{activity_data['nombre'].iloc[0]}", key="name_upd_activity")
                type_upd_activity = st.selectbox("Tipo*: ", ["Matenimiento", "Incidencia"], index=index_type)
                description_upd_activity = st.text_area("Descripción*: ", value=f"{activity_data['descripcion'].iloc[0]}")
                actions_upd_activity = st.text_area("Accciones: ", value=f"{activity_data['acciones_realizadas'].iloc[0]}")
                state_upd_activity = st.selectbox("Estado", ["Abierto", "En Curso", "Pendiente"], index=index_status)
                support_upd_activity = st.selectbox("Miembro: ", combined_supports, key="update_activities_support")
                clients_upd_activity = st.selectbox("Cliente: ", combined_clients, key="update_activities_client")
                st.write("*Campos Obligatorios")
                # Renderiza un boton de envio
                submit_upd_activity = st.form_submit_button("Actualizar")
            
            # Crea un contenedor de mensajes, ayuda a limpiar
            message_container = st.empty()

            # Recupera la accion de envio de datos
            if submit_upd_activity:
                # Valida que los campos obligatorios no esten vacios
                if not name_upd_activity.strip() or not description_upd_activity.strip() or not actions_upd_activity.strip():
                    st.error("Actividad No Actualizada")
                    st.info("Llene todos los campos obligatorios")
                else:
                    # Se obtienen el id del miembro que estaba primero seleccionado
                    support_selected_first = activity_data['idMiembro'].iloc[0]
                    # Se obtiene el id del miembro que se selecciono
                    id_support_selected = int (support_upd_activity.split(' - ')[0][1:])
                    # Se obtienen los datos del miembro seleccionado
                    support_data = supports_upd[supports_upd['idMiembro']==id_support_selected]

                    # Se obtiene el id del cliente seleccionado
                    id_client_selected = int (clients_upd_activity.split(' - ')[0][1:])
                    # Se obtiene los datos del cliente seleccionado
                    client_data = clients_upd[clients_upd['idCliente']==id_client_selected]

                    # Funcion que ejecuta la actualizacion de la actividad
                    st_upd_activity, ms_upd_activity = bd.actualizar_actividad(name_upd_activity, type_upd_activity, description_upd_activity, actions_upd_activity, state_upd_activity,id_support_selected, id_client_selected, support_selected_first, id_activity_selected)

                    # Valida que la actualizacion se haya logrado
                    if st_upd_activity:
                        # Imprime mensajes de exito e informacion actualizada
                        st.success(ms_upd_activity)
                        st.info(f"{name_upd_activity} -- {type_upd_activity} -- {description_upd_activity} -- {type_upd_activity} -- {description_upd_activity} -- {actions_upd_activity} -- {state_upd_activity} -- {clients_upd_activity} -- {support_upd_activity}")

                    # En caso de que la actualizacion no se haya concretado
                    else:
                        # Mensaje de error
                        st.error(ms_upd_activity)
                    # Limpia mensajes
                    time.sleep(3)
                    message_container.empty()
                    st.rerun()
        # En caso de que los resultados sean vacios
        else:
            st.warning("No hay datos para mostrar")
    
    # Valida que el rol del usaurio sea user
    elif any(role in ["user"] for role in st.session_state["roles"]):
        # Consulta el identificador del miembro al que esta asociado el usuario
        state_email, id_support_selected = bd.consultar_id_email(st.session_state['email'])
        # Consula las actividades que se pueden actualizar y los clientes
        activities_available = bd.consultar_actividades_dispo(1,id_support_selected)
        clients_upd = bd.consultar_todos_clientes()

        # Verifica que los resultados no sean vacios
        if activities_available is not None and not activities_available.empty:
            # Combina las columnas de identificador y nombre para las actividades
            combined_activities = [f"#{row['idActividad']} - {row['nombre']}" for index, row in activities_available.iterrows()]
            # Despliega un objeto que permite seleccionar una actividad
            activity_selected = st.selectbox("Selecciona un Actividad", combined_activities, key="update_activities_sb")
            # Extramos el identificador de la actividad seleccionad
            id_activity_selected = int (activity_selected.split(' - ')[0][1:])
            # Recuperamos los datos de la actividad seleccionada
            activity_data = activities_available[activities_available['idActividad']==id_activity_selected]

            # Combina las columnas identificador y nombre de los cliente
            combined_clients = [f"#{row['idCliente']} - {row['nombre']}" for index, row in clients_upd.iterrows()]
            
            # Recupera el indice de tipo y estatus para los datos actuales
            index_type, index_status = ut.dict_activity_upd(activity_data['tipo'].iloc[0], activity_data['estado'].iloc[0])

            # Obtenemos los datos del cliente
            client_data_tmp = clients_upd[clients_upd['idCliente']== activity_data['idCliente'].iloc[0]]
            
            # Crea un contenedor para mostrar la informacion del cliente actual
            with st.container(border=True):
                st.markdown(f"**Cliente Actual: #{client_data_tmp['idCliente'].iloc[0]} - {client_data_tmp['nombre'].iloc[0]}**")

            # Renderiza un formulario par actualizar los campos de la actividad
            with st.form("update_activity_indie", clear_on_submit= True):
                name_upd_activity = st.text_input("Nombre*: ", value=f"{activity_data['nombre'].iloc[0]}", key="name_upd_activity")
                type_upd_activity = st.selectbox("Tipo*: ", ["Matenimiento", "Incidencia"], index=index_type)
                description_upd_activity = st.text_area("Descripción*: ", value=f"{activity_data['descripcion'].iloc[0]}")
                actions_upd_activity = st.text_area("Accciones: ", value=f"{activity_data['acciones_realizadas'].iloc[0]}")
                state_upd_activity = st.selectbox("Estado", ["Abierto", "En Curso", "Pendiente"], index=index_status)
                clients_upd_activity = st.selectbox("Cliente: ", combined_clients, key="update_activities_client")
                
                st.write("*Campos Obligatorios")
                # Crea un boton para envio
                submit_upd_activity = st.form_submit_button("Actualizar")
            
            # Crea un contenedor para los mensajes, permite que despues sean limpiados
            message_container = st.empty()

            # Recupera la accion del boton
            if submit_upd_activity:
                # Valida que los campos obligatorios esten llenos
                if not name_upd_activity.strip() or not description_upd_activity.strip() or not actions_upd_activity.strip():
                    st.error("Actividad No Actualizada")
                    st.info("Llene todos los campos obligatorios")
                else:
                    # Obtiene el miembro seleccionado primero, solamente el identificador
                    support_selected_first = activity_data['idMiembro'].iloc[0]

                    # Obtiene el identificador del cliente seleccionado
                    id_client_selected = int (clients_upd_activity.split(' - ')[0][1:])
                    # Recupera los datos del cliente seleccionado
                    client_data = clients_upd[clients_upd['idCliente']==id_client_selected]

                    # Funcion que actualiza la actividad
                    st_upd_activity, ms_upd_activity = bd.actualizar_actividad(name_upd_activity, type_upd_activity, description_upd_activity, actions_upd_activity, state_upd_activity,id_support_selected, id_client_selected, support_selected_first, id_activity_selected)

                    # Si la ejecucion de la actualizacion es correcta
                    if st_upd_activity:
                        # Muestra el mensaje de exito y los campos actualizados
                        st.success(ms_upd_activity)
                        st.info(f"{name_upd_activity} -- {type_upd_activity} -- {description_upd_activity} -- {type_upd_activity} -- {description_upd_activity} -- {actions_upd_activity} -- {state_upd_activity} -- {clients_upd_activity}")
                    # Actualizacion Fallida
                    else:
                        # Mensaje de error
                        st.error(ms_upd_activity)
                    # Limpieza de mensajes
                    time.sleep(3)
                    message_container.empty()
                    st.rerun()
        # En caso de que el resultado este vacio
        else: 
            st.warning("No hay datos para mostrar")
    # En caso de que no se tenga permisos para modificar.
    else: 
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")

# Pestaña para terminar actividad
with tab_del_activity:
    # Valida que el rol de usuario se el de admin
    if any(role in ["admin"] for role in st.session_state["roles"]):
        # Advertencias
        st.info("Un actividad terminada no podrá modificarse.")
        st.info("Si cierra una actividad se cerrarán todas las facturas asociadas, en caso de estar abiertas")

        # Consulta las actividades que pueden ser terminadas
        activities_delete_available = bd.consultar_actividades_eliminacion()

        # Verifica que el resultado no sea vacio
        if activities_delete_available is not None and not activities_delete_available.empty:
            # Combina las columnas de identificador y nombre de las actividades
            combined_activities_delete = [f"#{row['idActividad']} - {row['nombre']}" for index, row in activities_delete_available.iterrows()]
            # Genera un selector de actividad
            activity_selected_delete = st.selectbox("Selecciona una Actividad", combined_activities_delete, key="delete_activities_sb")
            # Obtenemos el identificador de la actividad a terminar
            id_activity_selected_delete = int (activity_selected_delete.split(' - ')[0][1:])
            # Obtenemos la informacion de la actividad a terminar
            activity_data_delete = activities_delete_available[activities_delete_available['idActividad']==id_activity_selected_delete]

            # Genera un contenedor para mostrar informacion de la actividad que quiere ser cerrad
            with st.container(border = True):
                st.markdown(f"## 💼 #{activity_data_delete["idActividad"].iloc[0]} - {activity_data_delete["nombre"].iloc[0]}")
                st.markdown(f"📆 Fecha Inicio: {activity_data_delete["fecha_inicio"].iloc[0]}")
                st.markdown(f"🔠 Descripcion: {activity_data_delete["descripcion"].iloc[0]}")
                st.markdown(f"🏢 Cliente: #{activity_data_delete["idCliente"].iloc[0]} - {activity_data_delete["nombre_c"].iloc[0]}")
                st.markdown(f"👤 Miembro: #{activity_data_delete["idMiembro"].iloc[0]} - {activity_data_delete["nombre_m"].iloc[0]}")

            # Doble verificacion para terminar la actividad
            with st.popover(f"Cerrar", use_container_width=True):
                    st.write(f"¿Seguro que quieres cerrar a {activity_data_delete["nombre"].iloc[0]}?")
                    # Renderiza y recupera la accion de cerrar la actividad
                    if st.button("Si. Estoy Seguro"):
                        # Obtiene la fecha de modificacion y quien lo modifico
                        datemodified_del_activity= ut.get_today_date()
                        modifyby_del_activity = st.session_state['name']

                        # Funcion que ejecuta la transaccion de cerrar la actividad, hace insercion en historicos y actualiza otras tablas
                        state_close_activity, msj_close_activity = bd.cerrar_actividad(id_activity_selected_delete, datemodified_del_activity, datemodified_del_activity, modifyby_del_activity)

                        # Si la transaccion se ejecuto correctamente
                        if state_close_activity == 1:
                            # Muestra los mensajes de actividad cerrada
                            st.success("Actividad Cerrada")
                            st.info(msj_close_activity)
                        else:
                            # Muesta los mensajes de actividad no cerrada y la razon
                            st.error("Actividad No Cerrada")
                            st.info(msj_close_activity)
                        # Limpia mensajes
                        message_container.empty()
                        time.sleep(3)
                        st.rerun()
        # En caso de tengamos un resultado vacio
        else: 
            st.warning("No hay actividades por cerrar")
    # En caso de no tener permisos
    else: 
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")
