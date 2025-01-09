import streamlit as st
import pandas as pd
import time
from menu import menu_with_redirect
import logic.bd as bd
from datetime import datetime
import logic.utilities as ut

# Primero hacemos las comprobacion
menu_with_redirect()

#Creamos un titulo
st.markdown("# 🔧 Recursos")

# Mostrar las disintas actividades a realizar
tab_lst_resource, tab_asign_resource,tab_ins_resource, tab_upd_resource, tab_del_resource, tab_new_resource = \
      st.tabs(["Listar Recursos","Asignar Recursos","Agregar Recurso", "Actualizar Recurso", "Eliminar Recurso", "Petición Recurso"])

with tab_lst_resource:
    col1, col2 = st.columns([95,1])
    with col2: 
        if st.button("🔄", key="ref_resources"):
            st.rerun()
    if any(role in ["admin", "user"] for role in st.session_state["roles"]):
        resources = bd.consultar_recursos()
        if resources is not None and not resources.empty:

            # Definir el número de columnas
            num_cols = 2
            cols = st.columns(num_cols)
            
            # Inicializar el índice para repartir a las columnas
            index = 0

            # Iterar sobre los resources en el DataFrame
            for _, resource in resources.iterrows():
                col = cols[index % num_cols]  # Alterna entre las columnas (0 y 1)
                
                # Mostrar la información del resource en la columna correspondiente
                with col:
                    with st.container(border=True):
                        st.markdown(f"## 🔧 {resource['nombre']}")
                        if resource['tipo'] == "Herramienta":
                            st.markdown(f"⚒️ Tipo: {resource['tipo']}")
                        else:
                            st.markdown(f"🖥️ Tipo: {resource['tipo']}")
                        st.markdown(f"🔠 Descripción: {resource['descripcion']}")
                        st.markdown(f"♟️ Categoria: {resource['categoria']}")
                        st.markdown(f"#️⃣ No. Serie: {resource['no_serie']}")
                        

                        if resource['vida_util'] in ["1 Año", "5 Años","10 Años"]:
                            dias_vida, dias_totales = ut.get_total_days_life(resource['vida_util'], resource['fecha_ingreso'])    
                            st.markdown(f" ⏲️ Vida: **{dias_vida}/{dias_totales}**")

                            if dias_vida > dias_totales:
                                st.markdown(f'''#### :red[Resurtir en Inventario]''')
                        else:
                            st.markdown(f"⏲️ Vida Útil: {resource['vida_util']}")

                        if resource['notas'] !="":
                            st.markdown(f"🗒️ Notas: {resource['notas']}")
                        
                        if resource['estado_recurso'] == "En Stock":
                            st.markdown(f'''### ✅ :green[{resource['estado_recurso']}]''')
                        else:
                            st.markdown(f'''### ❌ :orange[{resource['estado_recurso']}]''')
                        
                
                # Actualizar el índice para alternar entre las columnas
                index += 1

        else:
            st.warning("No existen datos")
    else:
        st.info("No tienes permisos para realizar esta acción, Contacta al administrador")

with tab_asign_resource: 
    if any(role in ["admin"] for role in st.session_state["roles"]):
        resources_to_asign = bd.consultar_recursos_disponible()
        activities_to_assign = bd.consultar_actividades()

        if activities_to_assign is not None and not activities_to_assign.empty:
            # Crear listas con recursos y actividades
            combined_resources_toasign = [f"#{row['idRecurso']} - {row['nombre']}" for index, row in resources_to_asign.iterrows()]
            combined_activities_toasign = [f"#{row['idActividad']} - {row['nombre']}" for index, row in activities_to_assign.iterrows()]
            activity_selected = st.selectbox("Elija una Actividad: ", combined_activities_toasign, key="asign_resources")
            id_activity_selected = int(activity_selected.split(' - ')[0][1:])

            # Veremos que recursos estan asginados a que actividad
            resources_asigned_to_activity = bd.recursos_asginados_a_actividad(id_activity_selected)
            st.markdown("### Asignados a la actividad:")

            # Verificar si hay recursos asignados a la actividad
            if resources_asigned_to_activity is not None and not resources_asigned_to_activity.empty:
                combined_resources_assigned = [f"#{row['idRecurso']} - {row['nombre']}" for index, row in resources_asigned_to_activity.iterrows()]
                
                # Crear un contenedor para los recursos asignados con checkboxes
                with st.container(border=True):
                    assigned_resources = []
                    
                    for resource_a in combined_resources_assigned:
                        # Crear un checkbox para cada recurso asignado
                        if st.checkbox(resource_a, value=True):
                            assigned_resources.append(resource_a)

                    # Botón para desvincular los recursos seleccionados
                    if st.button("Desvincular"):
                        if assigned_resources:
                            # Iterar sobre los recursos seleccionados
                            for assigned in assigned_resources:
                                id_resource_assigned = int(assigned.split(' - ')[0][1:])
                                                                
                                # Actualizar el estado del recurso a "En Stock"
                                state_assigned, msj_assigned = bd.desvincular_recurso(id_activity_selected, id_resource_assigned)
                                
                                if state_assigned:
                                    st.success(msj_assigned)
                                else:
                                    st.error("Recurso No Desvinculado")
                                    st.info(msj_assigned)
                            time.sleep(3)
                            st.rerun()
                        else:
                            st.warning("No se seleccionaron recursos para desvincular.")
            else:
                # Si no hay recursos asignados a la actividad
                st.info("No hay recursos asignados a esta actividad.")

            
            # Muestra los checkboxes para los recursos
            st.markdown("### Asignar a la actividad")
            with st.container(border=True):
                selected_resources = []
                for resource in combined_resources_toasign:
                    # Usar st.checkbox para cada recurso
                    if st.checkbox(resource):
                        selected_resources.append(resource)

                # Al presionar el botón "Asignar"
                if st.button("Asignar"):
                    if selected_resources:
                        # Asignar los recursos seleccionados a la actividad
                        for selected in selected_resources:
                            id_resource_selected = int(selected.split(' - ')[0][1:])
                            
                            state_unsaggnied, msj_unsaggnied = bd.vincular_recurso(id_activity_selected, id_resource_selected)
                            
                            # Validar si las operaciones fueron exitosas
                            if state_unsaggnied:
                                st.success(msj_unsaggnied)
                            else:
                                st.error("Recurso No Vinculado")
                                st.info(msj_unsaggnied)
                        
                        time.sleep(3)
                        st.rerun()
                    else:
                        st.warning("No hay recursos seleccionados.")
        else:
            st.warning("No hay recursos o actividades para mostrar.")
    else:
        st.info("No tienes permisos para realizar esta acción, Contacta al administrador")

with tab_ins_resource:
    if any(role in ["admin"] for role in st.session_state["roles"]):
        with st.form("insert_resource", clear_on_submit=True):
            # Entradas del formulario
            name_ins_resource = st.text_input("Nombre*: ", placeholder="Llave")
            type_ins_resource = st.selectbox("Tipo*: ", ["Herramienta", "Material"])
            description_ins_resource = st.text_input("Descripción*: ", placeholder="Llave Allen 3/4")
            category_ins_resource = st.text_input("Categoria*: ", placeholder="Mecánica")
            serialnumber_ins_resource = st.text_input("No. Serie", placeholder="ALL15313")
            life_ins_resource = st.selectbox("Vida Útil", ["1 Vez", "1 Año", "5 Años","10 Años"])
            comments_ins_resource = st.text_area("Notas Adicionales: ", placeholder="Agrega tus comentarios")
            st.markdown("*Campos Obligatorios")
            
            # Botón de envío
            submit_insert_resource = st.form_submit_button("Agregar")

            message_container = st.empty()

            if submit_insert_resource:
                if not name_ins_resource.strip() or not type_ins_resource.strip() or not description_ins_resource.strip() or not category_ins_resource.strip() or not serialnumber_ins_resource.strip():
                    st.error("Recurso No Agregado")
                    st.info("Llene todos los campos obligatorios")
                else:
                    state_ins_resource, msj_ins_resource = bd.insertar_recurso(serialnumber_ins_resource, name_ins_resource ,description_ins_resource, category_ins_resource , life_ins_resource, comments_ins_resource, type_ins_resource)
                    if state_ins_resource:
                        st.success(msj_ins_resource)
                        st.info(f"{name_ins_resource} -- {type_ins_resource} -- {description_ins_resource} -- {category_ins_resource} -- {serialnumber_ins_resource} -- {life_ins_resource} -- En Stock -- {comments_ins_resource}")
                    else:
                        st.error(msj_ins_resource)
                time.sleep(3)
                message_container.empty()
                st.rerun()
    else:
        st.info("No tienes permisos para realizar esta acción, Contacta al administrador")
    
with tab_upd_resource:
    
    if any(role in ["admin"] for role in st.session_state["roles"]):
        resources_available = bd.consultar_recursos()
        
        if resources_available is not None and not resources_available.empty:
            combined_resources = [f"#{row['idRecurso']} - {row['nombre']}" for index, row in resources_available.iterrows()]
            resource_selected = st.selectbox("Selecciona un Recurso", combined_resources, key="update_resources_sb")
            id_resource_selected = int (resource_selected.split(' - ')[0][1:])
            resource_data = resources_available[resources_available['idRecurso']==id_resource_selected]
            
            #Necesitamos ademas saber el index del tipo, vida_util, estado
            index_type, index_life, index_status = ut.dict_resource_upd(resource_data['tipo'].iloc[0], resource_data['vida_util'].iloc[0], resource_data['estado_recurso'].iloc[0])

            with st.form("update_resource", clear_on_submit= True):
                name_upd_resource = st.text_input("Nombre*: ", value=f"{resource_data['nombre'].iloc[0]}", key="name_upd_resource")
                type_upd_resource = st.selectbox("Tipo*: ", ["Herramienta", "Material"], index=index_type)
                description_upd_resource = st.text_input("Descripción*: ", value=f"{resource_data['descripcion'].iloc[0]}")
                category_upd_resource = st.text_input("Categoria*: ", value=f"{resource_data['categoria'].iloc[0]}")
                serialnumber_upd_resource = st.text_input("No. Serie", value=f"{resource_data['no_serie'].iloc[0]}")
                life_upd_resource = st.selectbox("Vida Útil", ["1 Vez", "1 Año", "5 Años","10 Años"], index=index_life)
                state_upd_resource = st.selectbox("Estado", ["En Stock", "En Uso"], index=index_status)
                comments_upd_resource = st.text_area("Notas Adicionales: ", value=f"{resource_data['notas'].iloc[0]}")
                st.write("*Campos Obligatorios")
                submit_upd_resource = st.form_submit_button("Actualizar")
            

                message_container = st.empty()

                if submit_upd_resource:
                    if not name_upd_resource.strip() or not description_upd_resource.strip() or not serialnumber_upd_resource.strip():
                        st.error("Recurso No Actualizado")
                        st.info("Llene todos los campos obligatorios")
                    else:
                        state_update_resource, msj_update_resource = bd.actualizar_recurso(name_upd_resource, type_upd_resource, description_upd_resource, category_upd_resource, serialnumber_upd_resource, life_upd_resource, state_upd_resource, comments_upd_resource, id_resource_selected)
                        if state_update_resource:
                                st.success("Recurso Actualizado")
                                st.info(f"{name_upd_resource} -- {type_upd_resource} -- {description_upd_resource} -- {category_upd_resource} -- {serialnumber_upd_resource} -- {comments_upd_resource}")
                        else:
                            st.error("Recurso No Actualizado")
                            st.info(msj_update_resource)
                        
                    time.sleep(3)
                    message_container.empty()
                    st.rerun()
    else:
        st.info("No tienes permisos para realizar esta acción, Contacta al administrador")

with tab_del_resource:
    if any(role in ["admin"] for role in st.session_state["roles"]):
        resources_avaliable = bd.consultar_recursos()
        if resources_avaliable is not None and not resources_available.empty:
            combined_resources = [f"#{row['idRecurso']} - {row['nombre']}" for index, row in resources_avaliable.iterrows()]
            resource_selected = st.selectbox("Selecciona un Recurso", combined_resources)
            id_resource_selected = int(resource_selected.split(' - ')[0][1:])
            resource_data = resources_avaliable[resources_avaliable['idRecurso'] == id_resource_selected]


            with st.container(border = True):
                st.markdown(f"## 🔧 {resource_data["nombre"].iloc[0]}")
                st.markdown(f"🔠 Descripción: {resource_data["descripcion"].iloc[0]}")
                st.markdown(f"#️⃣ No. Serie: {resource_data["no_serie"].iloc[0]}")
            
            with st.container():
                with st.popover(f"Eliminar", use_container_width=True):
                    st.write(f"¿Seguro que quieres eliminar a {resource_data["nombre"].iloc[0]}?")
                    if st.button("Si. Estoy Seguro"):
                        state_del_resouce, msj_del_resource= bd.eliminar_recurso(id_resource_selected)
                        if state_del_resouce:
                            st.success(msj_del_resource)
                        else:
                            st.error("Recurso No Eliminado")
                            st.info(msj_del_resource)
                        time.sleep(3)
                        message_container.empty()
                        st.rerun()
        else:
            st.warning("No hay datos para mostrar...")
    else:
        st.info("No tienes permisos para realizar esta acción, Contacta al administrador")

with tab_new_resource:
    col1, col2 = st.columns([95,1])
    with col2: 
        if st.button("🔄", key="ref_new_resource"):
            st.rerun()
    if any(role in ["admin", "user"] for role in st.session_state["roles"]):
        ################################# LISTADO ################################# 
        # El listado es para todos, para saber que se dice 
        st.markdown("### Listado")
        new_resources = bd.consultar_peticiones_recursos(0)

        if new_resources is not None and not new_resources.empty:
            #Definir el número de columnas
            num_cols = 2
            cols = st.columns(num_cols)
            
            # Inicializar el índice para repartir a las columnas
            index = 0

            # Iterar sobre los new_resources en el DataFrame
            for _, resource in new_resources.iterrows():
                col = cols[index % num_cols]  # Alterna entre las columnas (0 y 1)
                
                # Mostrar la información del resource en la columna correspondiente
                with col:
                    with st.container(border=True):
                        st.markdown(f"## 🔧 #{resource['idNuevoRecurso']} - {resource['nombre']}")
                        if resource['tipo'] == "Herramienta":
                            st.markdown(f"⚒️ Tipo: {resource['tipo']}")
                        else:
                            st.markdown(f"🖥️ Tipo: {resource['tipo']}")

                        st.markdown(f"🔠 Descripción: {resource['descripcion']}")
                        st.markdown(f"📆 Recibido: {resource['fecha_peticion']}")
                        st.markdown(f"👤 Pedido Por: {resource['nombre_m']}")

                        st.markdown(f"#️⃣ Cantidad: {resource['descripcion']}")

                        if resource['notas'] !="":
                            st.markdown(f"🗒️ Notas: {resource['notas']}")
                        
                       # if resource['estado_peticion'] == "Listo":
                       #     st.markdown(f'''### :green[{resource['estado_peticion']}]''')
                       # elif resource['estado_peticion'] == "En Proceso":
                       #     st.markdown(f'''### :orange[{resource['estado_peticion']}]''')
                       # else:
                       #     st.markdown(f'''### :red[{resource['estado_peticion']}]''')
                        
                # Actualizar el índice para alternar entre las columnas
                index += 1
        else:
            st.warning("No existen peticiones")

        ################################# PETICION #################################
        # Para el caso de una petición, solo cuando sea admin tendrá que desplegar la opcion de escoger un miembro 
        st.markdown("---")
        st.markdown("### Petición")

        supports_new_resource = bd.consultar_miembros(1)
        combined_supports = [f"#{row['idMiembro']} - {row['nombre']}" for index, row in supports_new_resource.iterrows()] 
        
        with st.form("new_resource", clear_on_submit=True):
            # Entradas del formulario
            name_new_resource = st.text_input("Nombre*: ", placeholder="Llave")
            type_new_resource = st.selectbox("Tipo*: ", ["Herramienta", "Material"])
            description_new_resource = st.text_input("Descripción*: ", placeholder="Llave Allen 3/4")
            date_new_resource = datetime.now().strftime("%Y-%m-%d")
            quantity_new_resource = st.selectbox("Cantidad de Piezas*: ", ["1","2","3","4","5","6","7","8","9","10"])
            state_new_resource = "Recibido"

            if any(role in ["admin"] for role in st.session_state["roles"]):
                if combined_supports:
                    support_new_resource = st.selectbox("Miembro Asociado:", combined_supports)
                    id_support_ins = int (support_new_resource.split(' - ')[0][1:])
            else:
                # Nos dira si tenenos permiso, basandose en el corrreo
                state_consultar_email, msj_consultar_email = bd.consultar_id_email(st.session_state['email'])
                if state_consultar_email: 
                    id_support_ins = msj_consultar_email


            comments_new_resource = st.text_area("Notas Adicionales: ", placeholder="Agrega tus comentarios")
            st.markdown("*Campos Obligatorios")
            submit_new_resource = st.form_submit_button("Pedir")

            if submit_new_resource:
                if not name_new_resource.strip() or not type_new_resource.strip() or not description_new_resource.strip():
                    st.error("Petición No Agregada")
                    st.info("Llene todos los campos obligatorios")
                else:
                    if id_support_ins > 0:
                        state_ins_new_resource, msj_ins_new_resource = bd.insertar_peticion_nuevo_recurso(name_new_resource, type_new_resource, description_new_resource, date_new_resource, quantity_new_resource, state_new_resource, comments_new_resource, id_support_ins)
                        if state_ins_new_resource:
                            st.success("Petición Agregada")
                            st.info(msj_ins_new_resource)
                        else:
                            st.error(msj_ins_new_resource)
                        
                        time.sleep(3)
                        st.rerun()
                    # En caso contrario 
                    else:
                        st.warning("No tiene permiso para hacer peticiones. Contacte a soporte.")
        ################################# ELIMINACION #################################
        st.markdown("---")
        st.markdown("### Eliminar")

        if any(role in ["admin"] for role in st.session_state["roles"]):
            new_resources_avaliable = bd.consultar_peticiones_recursos(1)
        else: 
            state_id_email, id_sesion = bd.consultar_id_email(st.session_state['email'])
            if state_id_email:
                new_resources_avaliable = bd.consultar_peticiones_por_id(id_sesion)
            
        if new_resources_avaliable is not None and not new_resources_avaliable.empty:
            new_combined_resources = [f"#{row['idNuevoRecurso']} - {row['nombre']}" for index, row in new_resources_avaliable.iterrows()]
            new_resource_selected = st.selectbox("Selecciona un Recurso", new_combined_resources)
            new_id_resource_selected = int(new_resource_selected.split(' - ')[0][1:])
            new_resource_data = new_resources_avaliable[new_resources_avaliable['idNuevoRecurso'] == new_id_resource_selected]
            
            with st.container():
                with st.popover(f"Eliminar", use_container_width=True):
                    st.write(f"¿Seguro que quieres eliminar a {new_resource_data["nombre"].iloc[0]}?")
                    if st.button("Si. Estoy Seguro", key="delete_new_resource"):
                        state_del, ms_del= bd.eliminar_peticion_nuevo_recurso(new_id_resource_selected)
                        if state_del: 
                            st.success("Petición Eliminada")
                            st.info(ms_del)
                        else: 
                            st.error("Petición No Eliminada")
                            st.info(ms_del)
                        time.sleep(3)
                        st.rerun()
        else:
            st.warning("No hay datos para mostrar")

    else:
        st.info("No tienes permisos para realizar esta acción, Contacta al administrador")