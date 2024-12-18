import streamlit as st
import pandas as pd
import time
from menu import menu_with_redirect
import logic.bd as bd
from datetime import datetime



# Primero hacemos las comprobacion
menu_with_redirect()

#Creamos un titulo
st.markdown("# 🔧 Recursos")

# Mostrar las disintas actividades a realizar
tab_lst_resource, tab_asign_resource,tab_ins_resource, tab_upd_resource, tab_del_resource, tab_new_resource = \
      st.tabs(["Listar Recursos","Asignar Recursos","Agregar Recurso", "Actualizar Recurso", "Eliminar Recurso", "Petición Recurso"])


with tab_asign_resource: 
    resources_to_asign = bd.consultar("SELECT * FROM recurso WHERE estado_recurso = 'En Stock'")
    activities_to_assign = bd.consultar("SELECT * FROM actividad;")

    if resources_to_asign is not None and not resources_to_asign.empty and activities_to_assign is not None and not activities_to_assign.empty:
        # Crear listas con recursos y actividades
        combined_resources_toasign = [f"#{row['idRecurso']} - {row['nombre']}" for index, row in resources_to_asign.iterrows()]
        combined_activities_toasign = [f"#{row['idActividad']} - {row['nombre']}" for index, row in activities_to_assign.iterrows()]

        # Selección de actividad
        activity_selected = st.selectbox("Elija una Actividad: ", combined_activities_toasign, key="asign_resources")
        id_activity_selected = int(activity_selected.split(' - ')[0][1:])

        # Veremos que recursos estan asginados a que actividad
        resources_asigned_to_activity = bd.consultar(f"""
            SELECT r.idRecurso, r.nombre 
            FROM actividad_has_recurso ahr
            INNER JOIN recurso r ON r.idRecurso = ahr.idRecurso
            INNER JOIN actividad a ON a.idActividad = ahr.idActividad
            WHERE ahr.idActividad = '{id_activity_selected}'
        """)
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
                        for asigned in assigned_resources:
                            # Obtener el id del recurso
                            id_resource_asigned = int(asigned.split(' - ')[0][1:])
                            
                            # Eliminar la relación de la tabla de vinculación
                            bd.eliminar(f"DELETE FROM actividad_has_recurso WHERE idActividad='{id_activity_selected}' AND idRecurso='{id_resource_asigned}';")
                            
                            # Actualizar el estado del recurso a "En Stock"
                            state_asigned, msj_asigned = bd.actualizar(f"UPDATE recurso SET estado_recurso = 'En Stock' WHERE idRecurso='{id_resource_asigned}'")
                            
                            # Verificar si la operación de eliminación y actualización fue exitosa
                            if state_asigned:
                                st.success(f"Recurso #{id_resource_asigned} desvinculado correctamente.")
                            else:
                                st.error(f"Hubo un error al desvincular el recurso #{id_resource_asigned}.")
                        # Después de la asignación, actualizar la página
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
                        insert_result= bd.insertar(f"INSERT INTO actividad_has_recurso (idActividad, idRecurso) VALUES('{id_activity_selected}', '{id_resource_selected}')")
                        
                        # Actualizar el estado del recurso a "En Uso"
                        update_result = bd.actualizar(f"UPDATE recurso SET estado_recurso = 'En Uso' WHERE idRecurso={id_resource_selected}")

                        # Validar si las operaciones fueron exitosas
                        if insert_result and update_result:
                            st.success(f"Recurso #{id_resource_selected} asignado correctamente a la actividad #{id_activity_selected}.")
                        else:
                            st.error(f"Hubo un error al asignar el recurso #{id_resource_selected}.")
                    
                    # Después de la asignación, actualizar la página
                    time.sleep(3)
                    st.rerun()
                else:
                    st.warning("No hay recursos seleccionados.")
    else:
        st.warning("No hay recursos o actividades para mostrar.")

with tab_lst_resource:
    resources = bd.consultar("SELECT nombre, tipo, descripcion, categoria, no_serie, estado_recurso, vida_util, fecha_ingreso, notas FROM recurso;")

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
                        if resource['vida_util'] == "10 Años":
                            dias_totales = 3650
                        elif resource['vida_util'] == "5 Años":
                            dias_totales = 1825
                        elif resource['vida_util'] == "1 Año":
                            dias_totales = 365
                            
                        dias_vida = (datetime.now().date() - resource['fecha_ingreso']).days
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


with tab_ins_resource:
    with st.form("insert_resource", clear_on_submit=True):
        # Entradas del formulario
        name_ins_resource = st.text_input("Nombre*: ", placeholder="Llave")
        type_ins_resource = st.selectbox("Tipo*: ", ["Herramienta", "Material"])
        description_ins_resource = st.text_input("Descripción*: ", placeholder="Llave Allen 3/4")
        category_ins_resource = st.text_input("Categoria*: ", placeholder="Mecánica")
        serialnumber_ins_resource = st.text_input("No. Serie", placeholder="ALL15313")
        life_ins_resource = st.selectbox("Vida Útil", ["1 Vez", "1 Año", "5 Años","10 Años"])
        comments_ins_resource = st.text_area("Notas Adicionales: ", placeholder="Agrega tus comentarios")
        
        # Indicador de campos obligatorios
        st.markdown("*Campos Obligatorios")
        
        # Botón de envío
        submit_insert_resource = st.form_submit_button("Agregar")

        message_container = st.empty()

        # Generacion de campos automaticos: 
        datetoday = datetime.now()
        dates_ins_resource = datetoday.strftime("%Y-%m-%d")


        if submit_insert_resource:
            if not name_ins_resource.strip() or not type_ins_resource.strip() or not description_ins_resource.strip()\
            or not category_ins_resource.strip() or not serialnumber_ins_resource.strip():
                st.error("Recurso No Agregado")
                st.info("Llene todos los campos obligatorios")
            else:
                query_insert_resource = f"INSERT INTO recurso (nombre, tipo, descripcion, categoria, no_serie, estado_recurso, vida_util, fecha_ingreso, notas ) VALUES ('{name_ins_resource}', '{type_ins_resource}', '{description_ins_resource}', '{category_ins_resource}', '{serialnumber_ins_resource}', 'En Stock', '{life_ins_resource}', '{dates_ins_resource}' ,'{comments_ins_resource}');"
                bd.insertar(query_insert_resource)
                st.success("Recurso Agregado")
                st.info(f"{name_ins_resource} -- {type_ins_resource} -- {description_ins_resource} -- {category_ins_resource} -- {serialnumber_ins_resource} -- {life_ins_resource} -- En Stock -- {comments_ins_resource}")
                
            # Para que se limpien los mensajes
            time.sleep(3)
            message_container.empty()
            st.rerun()

with tab_upd_resource:
    resources_available = bd.consultar("SELECT * FROM recurso;")
    
    if resources_available is not None:
        combined_resources = [f"#{row['idRecurso']} - {row['nombre']}" for index, row in resources_available.iterrows()]
        resource_selected = st.selectbox("Selecciona un Recurso", combined_resources, key="update_resources_sb")
        id_resource_selected = int (resource_selected.split(' - ')[0][1:])
        resource_data = resources_available[resources_available['idRecurso']==id_resource_selected]
        
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

        index_type = type_dict[resource_data['tipo'].iloc[0]]
        index_life = life_dict[resource_data['vida_util'].iloc[0]]
        index_status = status_dict[resource_data['estado_recurso'].iloc[0]]



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
            state_update_resource, msj_update_resource = bd.actualizar(f"UPDATE recurso SET nombre='{name_upd_resource}', tipo='{type_upd_resource}', descripcion='{description_upd_resource}', categoria='{category_upd_resource}', no_serie='{serialnumber_upd_resource}', vida_util='{life_upd_resource}', estado_recurso='{state_upd_resource}', notas='{comments_upd_resource}' WHERE idRecurso = '{id_resource_selected}';")
            if state_update_resource == 1:
                    st.success("Recurso Actualizado")
                    st.info(f"{name_upd_resource} -- {type_upd_resource} -- {description_upd_resource} -- {category_upd_resource} -- {serialnumber_upd_resource} -- {comments_upd_resource}")
            else:
                st.error("Recurso No Actualizado")
                st.info(msj_update_resource)
            
        # Para que se limpien los mensajes
        time.sleep(3)
        message_container.empty()
        st.rerun()


with tab_del_resource:
    resources_avaliable = bd.consultar("SELECT * FROM recurso")
    if resources_avaliable is not None:
        combined_resources = [f"#{row['idRecurso']} - {row['nombre']}" for index, row in resources_avaliable.iterrows()]
        resource_selected = st.selectbox("Selecciona un Recurso", combined_resources)
        id_resource_selected = int(resource_selected.split(' - ')[0][1:])
        resource_data = resources_avaliable[resources_avaliable['idRecurso'] == id_resource_selected]

        # Hagamos la notifiación de que no se puede eliminar si tiene actividades abiertas
        resource_with_activities = bd.consultar(f"SELECT r.idRecurso, count(*) as act_abiertas FROM actividad_has_recurso a INNER JOIN recurso r ON a.idRecurso=r.idRecurso WHERE a.idRecurso={id_resource_selected} GROUP BY a.idRecurso;")

        with st.container(border = True):
            st.markdown(f"## 🔧 {resource_data["nombre"].iloc[0]}")
            st.markdown(f"🔠 Descripción: {resource_data["descripcion"].iloc[0]}")
            st.markdown(f"#️⃣ No. Serie: {resource_data["no_serie"].iloc[0]}")
        
        with st.container():
            with st.popover(f"Eliminar", use_container_width=True):
                st.write(f"¿Seguro que quieres eliminar a {resource_data["nombre"].iloc[0]}?")
                if st.button("Si. Estoy Seguro"):
                    if resource_with_activities.empty:
                        state_del, ms_del= bd.eliminar(f"DELETE FROM recurso WHERE idRecurso='{id_resource_selected}'")
                        st.success("Recurso Eliminado")
                        time.sleep(3)
                        message_container.empty()
                        st.rerun()
                    else: 
                        st.error("Recurso No Eliminado")
                        st.info("Este recurso esta asociado a actividades, no puede ser eliminado.")
                        time.sleep(3)
                        message_container.empty()
                        st.rerun()
    else:
        st.warning("No hay datos para mostrar...")


with tab_new_resource:
    st.markdown("### Listado")

    new_resources = bd.consultar("SELECT pnr.*, m.nombre as nombre_m FROM peticion_nuevo_recurso pnr INNER JOIN miembro m ON m.idMiembro=pnr.idMiembro;")

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
                    st.markdown(f"## 🔧 {resource['nombre']}")
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
                    
                    if resource['estado_peticion'] == "Listo":
                        st.markdown(f'''### :green[{resource['estado_peticion']}]''')
                    elif resource['estado_peticion'] == "En Proceso":
                        st.markdown(f'''### :orange[{resource['estado_peticion']}]''')
                    else:
                        st.markdown(f'''### :red[{resource['estado_peticion']}]''')
                    
            # Actualizar el índice para alternar entre las columnas
            index += 1
    else:
        st.warning("No existen peticiones")

    
    st.markdown("---")
    st.markdown("### Petición")
    # Parte de la petición

    supports_new_resource = bd.consultar("SELECT idMiembro, nombre FROM miembro;")
    combined_supports = [f"#{row['idMiembro']} - {row['nombre']}" for index, row in supports_new_resource.iterrows()] 
    
    with st.form("new_resource", clear_on_submit=True):
        # Entradas del formulario
        name_new_resource = st.text_input("Nombre*: ", placeholder="Llave")
        type_new_resource = st.selectbox("Tipo*: ", ["Herramienta", "Material"])
        description_new_resource = st.text_input("Descripción*: ", placeholder="Llave Allen 3/4")
        date_new_resource = datetime.now().strftime("%Y-%m-%d")
        quantity_new_resource = st.selectbox("Cantidad de Pieza*: ", ["1","2","3","4","5","6","7","8","9","10"])
        state_new_resource = "Recibido"
        support_new_resource = st.selectbox("Miembro Asociado:", combined_supports)
        comments_new_resource = st.text_area("Notas Adicionales: ", placeholder="Agrega tus comentarios")
        st.markdown("*Campos Obligatorios")
        submit_new_resource = st.form_submit_button("Pedir")

        #Extraccion id de los selectbox
        id_support_ins = int (support_new_resource.split(' - ')[0][1:])

        if submit_new_resource:
            if not name_new_resource.strip() or not type_new_resource.strip() or not description_new_resource.strip():
                st.error("Petición No Agregada")
                st.info("Llene todos los campos obligatorios")
            else:
                query_new_resource = f"INSERT INTO peticion_nuevo_recurso (nombre, tipo, descripcion, fecha_peticion, cantidad, estado_peticion, notas, idMiembro) VALUES ('{name_new_resource}', '{type_new_resource}', '{description_new_resource}', '{date_new_resource}', '{quantity_new_resource}', '{state_new_resource}', '{comments_ins_resource}', '{id_support_ins}');"
                bd.insertar(query_new_resource)
                st.success("Petición Agregada")

    st.markdown("---")
    st.markdown("### Eliminar")

    new_resources_avaliable = bd.consultar("SELECT * FROM peticion_nuevo_recurso;")
    if new_resources_avaliable is not None and not new_resources_avaliable.empty:
        new_combined_resources = [f"#{row['idNuevoRecurso']} - {row['nombre']}" for index, row in new_resources_avaliable.iterrows()]
        new_resource_selected = st.selectbox("Selecciona un Recurso", new_combined_resources)
        new_id_resource_selected = int(new_resource_selected.split(' - ')[0][1:])
        new_resource_data = new_resources_avaliable[new_resources_avaliable['idNuevoRecurso'] == new_id_resource_selected]

        with st.container():
            with st.popover(f"Eliminar", use_container_width=True):
                st.write(f"¿Seguro que quieres eliminar a {new_resource_data["nombre"].iloc[0]}?")
                if st.button("Si. Estoy Seguro", key="delete_new_resource"):
                    if resource_with_activities.empty:
                        state_del, ms_del= bd.eliminar(f"DELETE FROM peticion_nuevo_recurso WHERE idNuevoRecurso='{new_id_resource_selected}'")
                        st.success("Petición Eliminada")
                        time.sleep(3)
                        message_container.empty()
                        st.rerun()
                    else: 
                        st.error("Petición No Eliminada")
                        time.sleep(3)
                        message_container.empty()
                        st.rerun()
    else:
        st.warning("No hay datos para mostrar")

    