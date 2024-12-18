import streamlit as st
import pandas as pd
import time
from menu import menu_with_redirect
import logic.bd as bd
import random as random
from datetime import datetime


# Primero hacemos las comprobacion
menu_with_redirect()

#Creamos un titulo
st.markdown("# 💼 Actividad")

# Mostrar las disintas actividades a realizar
tab_lst_activity, tab_ins_activity, tab_upd_activity, tab_del_activity= \
      st.tabs(["Listar Actividades","Crear Actividad", "Actualizar Actividad", "Terminar Actividad"])


with tab_lst_activity:
    activities = bd.consultar("SELECT a.*, m.nombre as miembro_n, c.nombre as cliente_n FROM actividad a INNER JOIN miembro m ON a.idMiembro = m.idMiembro INNER JOIN cliente c ON a.idCliente = c.idCliente;")

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
                        st.markdown(f'''### 🟡 :yellow[{activity['estado']}]''')
                    else: 
                        st.markdown(f'''### 🟢 :green[{activity['estado']}]''')
                    
            
            # Actualizar el índice para alternar entre las columnas
            index += 1

    else:
        st.warning("No existen datos")


with tab_ins_activity:    
    # Aqui va el formulario
    with st.form("insert_activity", clear_on_submit=True):
        # Obtenemos los clientes disponibles
        clients_available = bd.consultar("SELECT idCliente, nombre FROM cliente;")
        combined_clients = [f"#{row['idCliente']} - {row['nombre']}" for index, row in clients_available.iterrows()]
        # Entradas del formulario
        name_ins_activity = st.text_input("Nombre*: ", placeholder="Reemplazo Inyector Tinta")
        description_ins_activity = st.text_area("Descripción*: ", placeholder="Se requiere el reemplazo de...")
        type_ins_activity = st.selectbox("Tipo*: ", ["Matenimiento", "Incidencia"])
        client_ins_activity = st.selectbox("Cliente*: ", combined_clients)

        id_client_ins = int (client_ins_activity.split(' - ')[0][1:])

        # Generación automatica del resto de campos necesarios para la inserción
        datestart_ins_activity_prev = datetime.now()
        datestart_ins_activity = datestart_ins_activity_prev.strftime("%Y-%m-%d")
        state_ins_activity = "Abierto"

        # Esta parte asigna de manera automatica. 
        supports_available_activity = bd.consultar("SELECT idMiembro as id, nombre FROM miembro WHERE disponibilidad='Disponible';")  # tiene a los miembros
        if supports_available_activity is not None and not supports_available_activity.empty: 
            support_ins_activity = random.choice(supports_available_activity['id'].tolist())
            support_random_selected = supports_available_activity[supports_available_activity['id'] == support_ins_activity ]
        else:
            st.warning("No hay Miembros Disponibles. Se asignará al Miembro con menos actividades")
            occupability_support = bd.consultar("SELECT idMiembro as id, count(*) as no_actividades FROM actividad GROUP BY idMiembro;")
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
                query_insert_activity = f"INSERT INTO actividad (nombre, fecha_inicio, descripcion, acciones_realizadas, tipo, estado, idCliente, idMiembro ) VALUES ('{name_ins_activity}', '{datestart_ins_activity}', '{description_ins_activity}', 'None','{type_ins_activity}', '{state_ins_activity}', '{id_client_ins}', '{support_ins_activity}');"
                bd.insertar(query_insert_activity)
                st.write("")

                st.success("Recurso Agregado")
                st.info(f"{name_ins_activity} -- {description_ins_activity} -- {type_ins_activity} -- #{support_ins_activity}:{support_random_selected['nombre'].iloc[0]} -- {datestart_ins_activity}")
                
            # Para que se limpien los mensajes
            time.sleep(5)
            message_container.empty()
            st.rerun()

with tab_upd_activity:
    activities_available = bd.consultar("SELECT * FROM actividad WHERE estado='Abierto' OR estado='En Curso' OR estado='Pendiente';")
    supports_upd = bd.consultar("SELECT idMiembro, nombre FROM miembro;")
    clients_upd = bd.consultar("SELECT idCliente, nombre FROM cliente;")

    if activities_available is not None and supports_upd is not None:
        combined_activities = [f"#{row['idActividad']} - {row['nombre']}" for index, row in activities_available.iterrows()]
        activity_selected = st.selectbox("Selecciona un Actividad", combined_activities, key="update_activities_sb")
        id_activity_selected = int (activity_selected.split(' - ')[0][1:])
        activity_data = activities_available[activities_available['idActividad']==id_activity_selected]
        
        # Vamos a dar las posibilidades para los miembros
        combined_supports = [f"#{row['idMiembro']} - {row['nombre']}" for index, row in supports_upd.iterrows()]
        combined_clients = [f"#{row['idCliente']} - {row['nombre']}" for index, row in clients_upd.iterrows()]

        # Necesitamos ademas saber el index del tipo, vida_util, estado
        type_dict = {
            "Matenimiento": 0,
            "Incidencia": 1
        }

        status_dict = {
            "Abierto": 0,
            "En Curso": 1,
            "Pendiente": 2,
        }

        index_type = type_dict[activity_data['tipo'].iloc[0]]
        index_status = status_dict[activity_data['estado'].iloc[0]]

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
            
        
            state_update_activity, msj_update_activity = bd.actualizar(f"UPDATE actividad SET nombre='{name_upd_activity}', tipo='{type_upd_activity}', descripcion='{description_upd_activity}', acciones_realizadas='{actions_upd_activity}', estado='{state_upd_activity}', idMiembro={id_support_selected}, idCliente={id_client_selected}  WHERE idActividad = '{id_activity_selected}';")
            if state_update_activity == 1:      
                # Comprobamos que no tenga mas actividades
                support_upd_dispo = bd.consultar(f"SELECT idMiembro, count(*) as no_actividades FROM actividad WHERE idMiembro={support_selected_first} GROUP BY idMiembro;")

                if support_upd_dispo.empty:
                    state_update_activity2, msj_update_activity2 = bd.actualizar(f"UPDATE miembro SET disponibilidad= 'Disponible', estatus='Libre' WHERE idMiembro={support_selected_first}")
                    st.write("Cambia a Disponible Anterior") 
                
                state_update_activity3, msj_update_activity3 =bd.actualizar(f"UPDATE miembro SET disponibilidad = 'No Disponible', estatus='En Actividad' WHERE idMiembro={id_client_selected}")   
                        
                if state_update_activity == 1:
                    st.success("Recurso Actualizado")
                    st.info(f"{name_upd_activity} -- {type_upd_activity} -- {description_upd_activity} -- {type_upd_activity} -- {description_upd_activity} -- {actions_upd_activity} -- {state_upd_activity} -- {clients_upd_activity} -- {support_upd_activity}")
            
            ###########################
            # Piensa en un ROLLBACK
            ##########################
            
            else:

                st.error("Recurso No Actualizado")
                st.info(msj_update_activity)
            
        # Para que se limpien los mensajes
        time.sleep(3)
        message_container.empty()
        st.rerun()


with tab_del_activity:
    st.info("Un actividad terminada no podrá modificarse.")
    st.info("Si cierra una actividad se cerrarán todas las facturas asociadas, en caso de estar abiertas")

    activities_delete_available = bd.consultar("SELECT a.*, c.nombre as nombre_c, m.nombre as nombre_m  FROM actividad a INNER JOIN cliente c ON a.idCliente=c.idCliente INNER JOIN miembro m ON a.idMiembro=m.idMiembro;")
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

