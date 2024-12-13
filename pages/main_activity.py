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
tab_lst_activity, tab_ins_activity, tab_upd_activity, tab_del_activity = \
      st.tabs(["Listar Actividades","Crear Actividad", "Actualizar Actividad", "Eliminar Actividad"])


with tab_lst_activity:
    activities = bd.consultar("SELECT nombre, fecha_inicio, descripcion, acciones_realizadas, tipo, estado FROM actividad;")

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
                    st.markdown(f"## 💼 {activity['nombre']}")
                    st.markdown(f"📆 Fecha Inicio: {activity['fecha_inicio']}")
                    st.markdown(f"🔠 Descripción: {activity['descripcion']}")
                    st.markdown(f"#️⃣ Tipo: {activity['tipo']}")
                    if activity['acciones_realizadas'] != "":
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
        # Entradas del formulario
        name_ins_activity = st.text_input("Nombre*: ", placeholder="Reemplazo Inyector Tinta")
        description_ins_activity = st.text_area("Descripción*: ", placeholder="Se requiere el reemplazo de...")
        type_ins_activity = st.selectbox("Tipo*: ", ["Matenimiento", "Incidencia"])

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
           st.warning("No hay Miembros Disponibles")
           #Aqui se hara el mecanismo ese  


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
                query_insert_activity = f"INSERT INTO actividad (nombre, fecha_inicio, descripcion, tipo, estado, idCliente ) VALUES ('{name_ins_activity}', '{datestart_ins_activity}', '{description_ins_activity}','{type_ins_activity}', '{state_ins_activity}', '{support_ins_activity}');"
                bd.insertar(query_insert_activity)

                st.success("Recurso Agregado")
                st.info(f"{name_ins_activity} -- {description_ins_activity} -- {type_ins_activity} -- #{support_ins_activity}:{support_random_selected['nombre'].iloc[0]} -- {datestart_ins_activity}")
                
            # Para que se limpien los mensajes
            time.sleep(5)
            message_container.empty()
            st.rerun()

with tab_upd_activity:
    activities_available = bd.consultar("SELECT * FROM recurso;")
    
    if activities_available is not None:
        combined_activities = [f"#{row['idRecurso']} - {row['nombre']}" for index, row in activities_available.iterrows()]
        activity_selected = st.selectbox("Selecciona un Recurso", combined_activities, key="update_activities_sb")
        id_activity_selected = int (activity_selected.split(' - ')[0][1:])
        activity_data = activities_available[activities_available['idRecurso']==id_activity_selected]
        
        #Necesitamos ademas saber el index del tipo, vida_util, estado
        type_dict = {
            "Herramienta": 0,
            "Material": 1
        }

        life_dict = {
            "1 Vez": 0,
            "1 Año": 1,
            "5 Años": 2,
            "10 Años": 3 
        }

        status_dict = {
            "En Stock": 0,
            "En Uso": 1
        }

        index_type = type_dict[activity_data['tipo'].iloc[0]]
        index_life = life_dict[activity_data['vida_util'].iloc[0]]
        index_status = status_dict[activity_data['estado_recurso'].iloc[0]]


        with st.form("update_activity", clear_on_submit= True):
            name_upd_activity = st.text_input("Nombre*: ", value=f"{activity_data['nombre'].iloc[0]}", key="name_upd_activity")
            type_upd_activity = st.selectbox("Tipo*: ", ["Herramienta", "Material"], index=index_type)
            description_upd_activity = st.text_input("Descripción*: ", value=f"{activity_data['descripcion'].iloc[0]}")
            category_upd_activity = st.text_input("Categoria*: ", value=f"{activity_data['categoria'].iloc[0]}")
            serialnumber_upd_activity = st.text_input("No. Serie", value=f"{activity_data['no_serie'].iloc[0]}")
            life_upd_activity = st.selectbox("Vida Útil", ["1 Vez", "1 Año", "5 Años","10 Años"], index=index_life)
            state_upd_activity = st.selectbox("Estado", ["En Stock", "En Uso"], index=index_status)
            comments_upd_activity = st.text_area("Notas Adicionales: ", value=f"{activity_data['notas'].iloc[0]}")
            st.write("*Campos Obligatorios")
            submit_upd_activity = st.form_submit_button("Actualizar")
        

    message_container = st.empty()

    if submit_upd_activity:
        if not name_upd_activity.strip() or not description_upd_activity.strip() or not serialnumber_upd_activity.strip():
            st.error("Recurso No Actualizado")
            st.info("Llene todos los campos obligatorios")
        else:
            state_update_activity, msj_update_activity = bd.actualizar(f"UPDATE recurso SET nombre='{name_upd_activity}', tipo='{type_upd_activity}', descripcion='{description_upd_activity}', categoria='{category_upd_activity}', no_serie='{serialnumber_upd_activity}', vida_util='{life_upd_activity}', estado_recurso='{state_upd_activity}', notas='{comments_upd_activity}' WHERE idRecurso = '{id_activity_selected}';")
            if state_update_activity == 1:
                    st.success("Recurso Actualizado")
                    st.info(f"{name_upd_activity} -- {type_upd_activity} -- {description_upd_activity} -- {category_upd_activity} -- {serialnumber_upd_activity} -- {comments_upd_activity}")
            else:
                st.error("Recurso No Actualizado")
                st.info(msj_update_activity)
            
        # Para que se limpien los mensajes
        time.sleep(3)
        message_container.empty()
        st.rerun()
