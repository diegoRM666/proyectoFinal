import streamlit as st
import pandas as pd
import time
from menu import menu_with_redirect
import logic.bd as bd
import random as random
from datetime import datetime
import logic.utilities as ut 


# Primero hacemos las comprobacion
menu_with_redirect()

#Creamos un titulo
st.markdown("# 💼 Actividad")

# Mostrar las disintas actividades a realizar
tab_lst_activity, tab_ins_activity, tab_upd_activity, tab_del_activity= \
      st.tabs(["Listar Actividades","Crear Actividad", "Actualizar Actividad", "Terminar Actividad"])


with tab_lst_activity:
    col1, col2 = st.columns([95,1])
    with col2: 
        if st.button("🔄", key="ref_resources"):
            st.rerun()
    if any(role in ["admin"] for role in st.session_state["roles"]):
        activities = bd.consultar_actividades_listado(0,0)

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
                        if activity['acciones_realizadas'] != "" and activity['acciones_realizadas'] != "None":
                            st.markdown(f"⚙️ Acciones Realizadas: {activity['acciones_realizadas']}")
                        
                        if activity['estado'] in ["Abierto"]:
                            st.markdown(f'''### 🔴 :red[{activity['estado']}]''')
                        elif activity['estado'] in ["En Curso", "Pendiente", "Escalada Con Fabricante" ]:
                            st.markdown(f'''### 🟡 :orange[{activity['estado']}]''')
                        else: 
                            st.markdown(f'''### 🟢 :green[{activity['estado']}]''')
                        
                
                # Actualizar el índice para alternar entre las columnas
                index += 1

        else:
            st.warning("No existen datos")

        st.markdown("---")
        st.markdown("### Actividades Cerradas")

        activities_closed =bd.consultar_actividades_listado(1,0)

        if activities_closed is not None and not activities_closed.empty:
            col1, col2, col3 = st.columns(3)
            
            # Iterar sobre los activities en el DataFrame
            for _, activity in activities_closed.iterrows():
                
                with st.container(border=True):
                    st.markdown(f"## 💼 #{activity['idActividad']} - {activity['nombre_a']}")
                    st.markdown(f"🔠 {activity['descripcion_a']}")
                    st.markdown(f'''📆 Periodo: :green[{activity['fecha_inicio_a']}] - :red[{activity['fecha_fin_a']}]''')
                    st.markdown(f"⚙️ Acciones Realizadas: {activity['acciones_realizadas_a']}")
                    st.markdown(f"#️⃣ Tipo: {activity['tipo_a']}")
                    st.markdown(f"### 🏢 #{activity['idCliente']} - {activity['nombre_c']}")
                    st.markdown(f"☎️ {activity['telefono_c']}")
                    st.markdown(f"📧 {activity['email_c']}")
                    st.markdown(f"### 👤 #{activity['idMiembro']} - {activity['nombre_m']}")
                    st.markdown(f"☎️ {activity['telefono_m']}")
                    st.markdown(f"📧 {activity['email_m']}")

                    
        else:
            st.warning("No existen datos")
    
    elif any(role in ["user"] for role in st.session_state["roles"]):
        state_email, result_email = bd.consultar_id_email(st.session_state['email'])
        activities = bd.consultar_actividades_listado(2, result_email)

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
                        if activity['acciones_realizadas'] != "" and activity['acciones_realizadas'] != "None":
                            st.markdown(f"⚙️ Acciones Realizadas: {activity['acciones_realizadas']}")
                        
                        if activity['estado'] in ["Abierto"]:
                            st.markdown(f'''### 🔴 :red[{activity['estado']}]''')
                        elif activity['estado'] in ["En Curso", "Pendiente", "Escalada Con Fabricante" ]:
                            st.markdown(f'''### 🟡 :orange[{activity['estado']}]''')
                        else: 
                            st.markdown(f'''### 🟢 :green[{activity['estado']}]''')
                        
                
                # Actualizar el índice para alternar entre las columnas
                index += 1

        else:
            st.warning("No existen datos")

        st.markdown("---")
        st.markdown("### Actividades Cerradas")

        activities_closed =bd.consultar_actividades_listado(3, result_email)

        if activities_closed is not None and not activities_closed.empty:
            col1, col2, col3 = st.columns(3)
            
            # Iterar sobre los activities en el DataFrame
            for _, activity in activities_closed.iterrows():
                
                with st.container(border=True):
                    st.markdown(f"## 💼 #{activity['idActividad']} - {activity['nombre_a']}")
                    st.markdown(f"🔠 {activity['descripcion_a']}")
                    st.markdown(f'''📆 Periodo: :green[{activity['fecha_inicio_a']}] - :red[{activity['fecha_fin_a']}]''')
                    st.markdown(f"⚙️ Acciones Realizadas: {activity['acciones_realizadas_a']}")
                    st.markdown(f"#️⃣ Tipo: {activity['tipo_a']}")
                    st.markdown(f"### 🏢 #{activity['idCliente']} - {activity['nombre_c']}")
                    st.markdown(f"☎️ {activity['telefono_c']}")
                    st.markdown(f"📧 {activity['email_c']}")
                    st.markdown(f"### 👤 #{activity['idMiembro']} - {activity['nombre_m']}")
                    st.markdown(f"☎️ {activity['telefono_m']}")
                    st.markdown(f"📧 {activity['email_m']}")

                    
        else:
            st.warning("No existen datos")

    else: 
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")

with tab_ins_activity:    
    if any(role in ["admin"] for role in st.session_state["roles"]):
        with st.form("insert_activity", clear_on_submit=True):
            # Obtenemos los clientes disponibles
            clients_available = bd.consultar_todos_clientes()
            combined_clients = [f"#{row['idCliente']} - {row['nombre']}" for index, row in clients_available.iterrows()]
            
            name_ins_activity = st.text_input("Nombre*: ", placeholder="Reemplazo Inyector Tinta")
            description_ins_activity = st.text_area("Descripción*: ", placeholder="Se requiere el reemplazo de...")
            type_ins_activity = st.selectbox("Tipo*: ", ["Matenimiento", "Incidencia"])
            client_ins_activity = st.selectbox("Cliente*: ", combined_clients)

            id_client_ins = int (client_ins_activity.split(' - ')[0][1:])

            # Generación automatica del resto de campos necesarios para la inserción
            datestart_ins_activity = ut.get_today_date()
            state_ins_activity = "Abierto"

            # Esta parte asigna de manera automatica. 
            supports_available_activity = bd.consultar_dispo_clientes(0)
            if supports_available_activity is not None and not supports_available_activity.empty: 
                support_ins_activity = random.choice(supports_available_activity['id'].tolist())
                support_random_selected = supports_available_activity[supports_available_activity['id'] == support_ins_activity ]
            else:
                st.warning("No hay Miembros Disponibles. Se asignará al Miembro con menos actividades")
                occupability_support = bd.consultar_dispo_clientes(1)
                support_ins_activity = random.choice(occupability_support['id'].tolist())
                support_random_selected = occupability_support[occupability_support['id'] == support_ins_activity]


            # Indicador de campos obligatorios
            st.markdown("*Campos Obligatorios")
            
            # Botón de envío
            submit_insert_activity = st.form_submit_button("Agregar")

            message_container = st.empty()

            if submit_insert_activity:
                if not name_ins_activity.strip() or not description_ins_activity.strip():
                    st.error("Actividad No Creada")
                    st.info("Llene todos los campos obligatorios")
                else:
                    state_ins_activity, msj_ins_activity = bd.insertar_actividad(name_ins_activity, datestart_ins_activity, description_ins_activity, type_ins_activity, state_ins_activity, id_client_ins, support_ins_activity)
                    
                    if state_ins_activity:
                        st.success(msj_ins_activity)
                        st.info(f"{name_ins_activity} -- {description_ins_activity} -- {type_ins_activity} -- #{client_ins_activity} -- {datestart_ins_activity}")
                    else: 
                        st.error(msj_ins_activity)
                time.sleep(5)
                message_container.empty()
                st.rerun()
    else: 
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")

with tab_upd_activity:
    if any(role in ["admin"] for role in st.session_state["roles"]):
        activities_available = bd.consultar_actividades_dispo(0, 0)
        supports_upd = bd.consultar_miembros(1)
        clients_upd = bd.consultar_todos_clientes()

        if activities_available is not None and supports_upd is not None:
            combined_activities = [f"#{row['idActividad']} - {row['nombre']}" for index, row in activities_available.iterrows()]
            activity_selected = st.selectbox("Selecciona un Actividad", combined_activities, key="update_activities_sb")
            id_activity_selected = int (activity_selected.split(' - ')[0][1:])
            activity_data = activities_available[activities_available['idActividad']==id_activity_selected]
            
            # Vamos a dar las posibilidades para los miembros
            combined_supports = [f"#{row['idMiembro']} - {row['nombre']}" for index, row in supports_upd.iterrows()]
            combined_clients = [f"#{row['idCliente']} - {row['nombre']}" for index, row in clients_upd.iterrows()]

            index_type, index_status = ut.dict_activity_upd(activity_data['tipo'].iloc[0], activity_data['estado'].iloc[0])

            client_data_tmp = clients_upd[clients_upd['idCliente']== activity_data['idCliente'].iloc[0]]
            support_data_tmp = supports_upd[supports_upd['idMiembro']== activity_data['idMiembro'].iloc[0]]   

            with st.container(border=True):
                st.markdown(f"**Cliente Actual: #{client_data_tmp['idCliente'].iloc[0]} - {client_data_tmp['nombre'].iloc[0]}**")
                st.markdown(f"**Miembro Actual: #{support_data_tmp['idMiembro'].iloc[0]} - {support_data_tmp['nombre'].iloc[0]}**")

            with st.form("update_activity", clear_on_submit= True):
                name_upd_activity = st.text_input("Nombre*: ", value=f"{activity_data['nombre'].iloc[0]}", key="name_upd_activity")
                type_upd_activity = st.selectbox("Tipo*: ", ["Matenimiento", "Incidencia"], index=index_type)
                description_upd_activity = st.text_area("Descripción*: ", value=f"{activity_data['descripcion'].iloc[0]}")
                actions_upd_activity = st.text_area("Accciones: ", value=f"{activity_data['acciones_realizadas'].iloc[0]}")
                state_upd_activity = st.selectbox("Estado", ["Abierto", "En Curso", "Pendiente"], index=index_status)
                support_upd_activity = st.selectbox("Miembro: ", combined_supports, key="update_activities_support")
                clients_upd_activity = st.selectbox("Cliente: ", combined_clients, key="update_activities_client")
                
                st.write("*Campos Obligatorios")
                submit_upd_activity = st.form_submit_button("Actualizar")
            

            message_container = st.empty()

            if submit_upd_activity:
                if not name_upd_activity.strip() or not description_upd_activity.strip() or not actions_upd_activity.strip():
                    st.error("Actividad No Actualizada")
                    st.info("Llene todos los campos obligatorios")
                else:
                    #Parte en la que obtenemos el cliente y el miembro...
                    support_selected_first = activity_data['idMiembro'].iloc[0]
                    id_support_selected = int (support_upd_activity.split(' - ')[0][1:])
                    support_data = supports_upd[supports_upd['idMiembro']==id_support_selected]
                
                    id_client_selected = int (clients_upd_activity.split(' - ')[0][1:])
                    client_data = clients_upd[clients_upd['idCliente']==id_client_selected]

                    st_upd_activity, ms_upd_activity = bd.actualizar_actividad(name_upd_activity, type_upd_activity, description_upd_activity, actions_upd_activity, state_upd_activity,id_support_selected, id_client_selected, support_selected_first, id_activity_selected)
                
                    if st_upd_activity:
                        st.success(ms_upd_activity)
                        st.info(f"{name_upd_activity} -- {type_upd_activity} -- {description_upd_activity} -- {type_upd_activity} -- {description_upd_activity} -- {actions_upd_activity} -- {state_upd_activity} -- {clients_upd_activity} -- {support_upd_activity}")

                    else:
                        st.error(ms_upd_activity)
                    time.sleep(3)
                    message_container.empty()
                    st.rerun()
        else:
            st.warning("No hay datos para mostrar")
    
    elif any(role in ["user"] for role in st.session_state["roles"]):
        state_email, id_support_selected = bd.consultar_id_email(st.session_state['email'])
        activities_available = bd.consultar_actividades_dispo(1,id_support_selected)
        clients_upd = bd.consultar_todos_clientes()

        if activities_available is not None and not activities_available.empty:
            combined_activities = [f"#{row['idActividad']} - {row['nombre']}" for index, row in activities_available.iterrows()]
            activity_selected = st.selectbox("Selecciona un Actividad", combined_activities, key="update_activities_sb")
            id_activity_selected = int (activity_selected.split(' - ')[0][1:])
            activity_data = activities_available[activities_available['idActividad']==id_activity_selected]

            # Vamos a dar las posibilidades para los miembros
            combined_clients = [f"#{row['idCliente']} - {row['nombre']}" for index, row in clients_upd.iterrows()]

            index_type, index_status = ut.dict_activity_upd(activity_data['tipo'].iloc[0], activity_data['estado'].iloc[0])

            client_data_tmp = clients_upd[clients_upd['idCliente']== activity_data['idCliente'].iloc[0]]
            with st.container(border=True):
                st.markdown(f"**Cliente Actual: #{client_data_tmp['idCliente'].iloc[0]} - {client_data_tmp['nombre'].iloc[0]}**")

            with st.form("update_activity_indie", clear_on_submit= True):
                name_upd_activity = st.text_input("Nombre*: ", value=f"{activity_data['nombre'].iloc[0]}", key="name_upd_activity")
                type_upd_activity = st.selectbox("Tipo*: ", ["Matenimiento", "Incidencia"], index=index_type)
                description_upd_activity = st.text_area("Descripción*: ", value=f"{activity_data['descripcion'].iloc[0]}")
                actions_upd_activity = st.text_area("Accciones: ", value=f"{activity_data['acciones_realizadas'].iloc[0]}")
                state_upd_activity = st.selectbox("Estado", ["Abierto", "En Curso", "Pendiente"], index=index_status)
                clients_upd_activity = st.selectbox("Cliente: ", combined_clients, key="update_activities_client")
                
                st.write("*Campos Obligatorios")
                submit_upd_activity = st.form_submit_button("Actualizar")
            

            message_container = st.empty()

            if submit_upd_activity:
                if not name_upd_activity.strip() or not description_upd_activity.strip() or not actions_upd_activity.strip():
                    st.error("Actividad No Actualizada")
                    st.info("Llene todos los campos obligatorios")
                else:
                    #Parte en la que obtenemos el cliente y el miembro...
                    support_selected_first = activity_data['idMiembro'].iloc[0]
                
                    id_client_selected = int (clients_upd_activity.split(' - ')[0][1:])
                    client_data = clients_upd[clients_upd['idCliente']==id_client_selected]

                    st_upd_activity, ms_upd_activity = bd.actualizar_actividad(name_upd_activity, type_upd_activity, description_upd_activity, actions_upd_activity, state_upd_activity,id_support_selected, id_client_selected, support_selected_first, id_activity_selected)
                
                    if st_upd_activity:
                        st.success(ms_upd_activity)
                        st.info(f"{name_upd_activity} -- {type_upd_activity} -- {description_upd_activity} -- {type_upd_activity} -- {description_upd_activity} -- {actions_upd_activity} -- {state_upd_activity} -- {clients_upd_activity}")

                    else:
                        st.error(ms_upd_activity)
                    time.sleep(3)
                    message_container.empty()
                    st.rerun()
        else: 
            st.warning("No hay datos para mostrar")
    else: 
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")

with tab_del_activity:
    if any(role in ["admin"] for role in st.session_state["roles"]):
        st.info("Un actividad terminada no podrá modificarse.")
        st.info("Si cierra una actividad se cerrarán todas las facturas asociadas, en caso de estar abiertas")

        activities_delete_available = bd.consultar_actividades_eliminacion()
        if activities_delete_available is not None:
            combined_activities_delete = [f"#{row['idActividad']} - {row['nombre']}" for index, row in activities_delete_available.iterrows()]
            activity_selected_delete = st.selectbox("Selecciona una Actividad", combined_activities_delete, key="delete_activities_sb")
            id_activity_selected_delete = int (activity_selected_delete.split(' - ')[0][1:])
            activity_data_delete = activities_delete_available[activities_delete_available['idActividad']==id_activity_selected_delete]

            with st.container(border = True):
                st.markdown(f"## 💼 #{activity_data_delete["idActividad"].iloc[0]} - {activity_data_delete["nombre"].iloc[0]}")
                st.markdown(f"📆 Fecha Inicio: {activity_data_delete["fecha_inicio"].iloc[0]}")
                st.markdown(f"🔠 Descripcion: {activity_data_delete["descripcion"].iloc[0]}")
                st.markdown(f"🏢 Cliente: #{activity_data_delete["idCliente"].iloc[0]} - {activity_data_delete["nombre_c"].iloc[0]}")
                st.markdown(f"👤 Miembro: #{activity_data_delete["idMiembro"].iloc[0]} - {activity_data_delete["nombre_m"].iloc[0]}")

            with st.popover(f"Eliminar", use_container_width=True):
                    st.write(f"¿Seguro que quieres eliminar a {activity_data_delete["nombre"].iloc[0]}?")
                    if st.button("Si. Estoy Seguro"):
                        # Generados automaticamente
                        date_today = datetime.now()
                        datemodified_del_activity= date_today.strftime("%Y-%m-%d")
                        modifyby_del_activity = st.session_state['name']

                        state_close_activity, msj_close_activity = bd.cerrar_actividad(id_activity_selected_delete, datemodified_del_activity, datemodified_del_activity, modifyby_del_activity)

                        if state_close_activity == 1:
                            st.success("Actividad Cerrada")
                            st.info(msj_close_activity)
                        else:
                            st.error("Actividad No Cerrada")
                            st.info(msj_close_activity)
                        
                        message_container.empty()
                        time.sleep(3)
                        st.rerun()
    else: 
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")