import streamlit as st
import pandas as pd
import time
from menu import menu_with_redirect
import logic.bd as bd
from datetime import datetime
import logic.utilities as ut

# Comprueba que el usuario este loggeado.
menu_with_redirect()

#Creamos un titulo
st.markdown("# 🔧 Recursos")

# Mostrar las disintas actividades a realizar
tab_lst_resource, tab_asign_resource,tab_ins_resource, tab_upd_resource, tab_del_resource, tab_new_resource = \
      st.tabs(["Listar Recursos","Asignar Recursos","Agregar Recurso", "Actualizar Recurso", "Eliminar Recurso", "Petición Recurso"])

# Pestaña para listar los recursos
with tab_lst_resource:
    # Genera columnas para darle formato al boton de refresco
    col1, col2 = st.columns([95,1])
    with col2: 
        # Rederizamos un boton de refresco
        if st.button("🔄", key="ref_resources"):
            st.rerun()
    # Validamos que el usuario posea un rol de admin o user
    if any(role in ["admin", "user"] for role in st.session_state["roles"]):
        # Consulta todos los recursos dados de alta en el sistema
        resources = bd.consultar_recursos()
        # Valida que el resultado no sea vacio
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
                        
                        # Da formato a la vida que le resta al recurso
                        if resource['vida_util'] in ["1 Año", "5 Años","10 Años"]:
                            # Calcula los dias que tiene de vida y cuantos son en total
                            dias_vida, dias_totales = ut.get_total_days_life(resource['vida_util'], resource['fecha_ingreso'])    
                            st.markdown(f" ⏲️ Vida: **{dias_vida}/{dias_totales}**")
                            # En caso de que el recurso ya haya pasado los dias de vida, pide resurtir en el inventario
                            if dias_vida > dias_totales:
                                st.markdown(f'''#### :red[Resurtir en Inventario]''')
                        # En caso de que sea un objeto que solamente se usa una vez, simplemente los despliega
                        else:
                            st.markdown(f"⏲️ Vida Útil: {resource['vida_util']}")

                        # Si el recurso tiene notas, las mostrara, en caso contrario, no
                        if resource['notas'] !="":
                            st.markdown(f"🗒️ Notas: {resource['notas']}")
                        
                        # Da formato al estado del recurso, para si esta En Stock o cualquier otro estado.
                        if resource['estado_recurso'] == "En Stock":
                            st.markdown(f'''### ✅ :green[{resource['estado_recurso']}]''')
                        else:
                            st.markdown(f'''### ❌ :orange[{resource['estado_recurso']}]''')
                        
                
                # Actualizar el índice para alternar entre las columnas
                index += 1
        # En caso de que el resultado es vacio
        else:
            st.warning("No existen datos")
    # Si no se tiene rol de admin o user
    else:
        st.info("No tienes permisos para realizar esta acción, Contacta al administrador")

# Pestaña para asignar recursos
with tab_asign_resource: 
    # Valida que el rol sea de admin, ya que esta accion solo es ejecutable por un admin
    if any(role in ["admin"] for role in st.session_state["roles"]):
        # Funcion para extraer las actividades que se encuentran en el sistema
        activities_to_assign = bd.consultar_actividades()

        # Valida el resultado de las actividades, para que no sea vacio
        if activities_to_assign is not None and not activities_to_assign.empty:
            # Combinar las columnas del identificador y el nombre para actividades
            combined_activities_toasign = [f"#{row['idActividad']} - {row['nombre']}" for index, row in activities_to_assign.iterrows()]
            # Renderiza un selector de actividad
            activity_selected = st.selectbox("Elija una Actividad: ", combined_activities_toasign, key="asign_resources")
            # Extrae el identificador de la actividad
            id_activity_selected = int(activity_selected.split(' - ')[0][1:])

            # Funcion que consulta las recursos asignados a la actividad que seleccionamos
            resources_asigned_to_activity = bd.recursos_asginados_a_actividad(id_activity_selected)
            st.markdown("### Asignados a la actividad:")

            # Verificar si hay recursos asignados a la actividad
            if resources_asigned_to_activity is not None and not resources_asigned_to_activity.empty:
                # Combina las columas de identificador y nombre para los recursos
                combined_resources_assigned = [f"#{row['idRecurso']} - {row['nombre']}" for index, row in resources_asigned_to_activity.iterrows()]
                
                # Crear un contenedor para los recursos asignados con checkboxes
                with st.container(border=True):
                    # Lista de los recursos asignados a la actividad
                    assigned_resources = []
                    
                    # Recorre uno a uno los recursos asignados
                    for resource_a in combined_resources_assigned:
                        # Crear un checkbox para cada recurso asignado
                        if st.checkbox(resource_a, value=True):
                            # Ademas lo agrega a la lista si se selecciona
                            assigned_resources.append(resource_a)

                    # Botón para desvincular los recursos seleccionados
                    if st.button("Desvincular"):
                        # Verifica que la lista no este vacia 
                        if assigned_resources:
                            # Iterar sobre los recursos seleccionados
                            for assigned in assigned_resources:
                                # Obtiene el identificador de cada uno de los recursos asignados
                                id_resource_assigned = int(assigned.split(' - ')[0][1:])
                                                                
                                # Actualizar el estado del recurso a "En Stock" y desasocia el recurso de la actividad 
                                state_assigned, msj_assigned = bd.desvincular_recurso(id_activity_selected, id_resource_assigned)
                                
                                # Si la desvinculacion es correcta
                                if state_assigned:
                                    st.success(msj_assigned)
                                # Si la desvinculacion no es correcta
                                else:
                                    st.error("Recurso No Desvinculado")
                                    st.info(msj_assigned)
                            # Limpia los mensajes producidos
                            time.sleep(3)
                            st.rerun()
                        # Si no hay recursos seleccionados para desvincular    
                        else:
                            st.warning("No se seleccionaron recursos para desvincular.")
            # Si no hay recursos asignados a la actividad
            else:
                st.info("No hay recursos asignados a esta actividad.")

            # Asignacion de actividades
            st.markdown("### Asignar a la actividad")

            # Funcion para extraer los recursos disponibles para asignar
            resources_to_asign = bd.consultar_recursos_disponible()

            # Verifica que el resultado no sea vacio
            if resources_to_asign is not None and not resources_to_asign.empty:
                # Combinar las columnas del identificador y el nombre, para recursos y actividades
                combined_resources_toasign = [f"#{row['idRecurso']} - {row['nombre']}" for index, row in resources_to_asign.iterrows()]

                # Genera un contenedor
                with st.container(border=True):
                    # Lista para guardar aquellos recursos seleccionados para asignar
                    selected_resources = []
                    
                    # Recorre cada uno de los recursos que pueden ser asignados
                    for resource in combined_resources_toasign:
                        # Genera un checkbox para cada uno de los recursos y verifica si esta seleccionado
                        if st.checkbox(resource):
                            # En caso de ser seleccionado, lo agrega a la lista de recursos
                            selected_resources.append(resource)

                    # Boton para vincular o asignar los recursos seleccionados
                    if st.button("Asignar"):
                        # Si la hay recursos seleccionados para vincular
                        if selected_resources:
                            # Asignar los recursos seleccionados a la actividad
                            for selected in selected_resources:
                                # Obtiene el identificador de los recursos seleccionados para asignar
                                id_resource_selected = int(selected.split(' - ')[0][1:])
                                
                                # Genera una consulta para vincular un recurso y ademas lo cambia a "En Uso"
                                state_unsaggnied, msj_unsaggnied = bd.vincular_recurso(id_activity_selected, id_resource_selected)
                                
                                # Validar si las operaciones fueron exitosas
                                if state_unsaggnied:
                                    st.success(msj_unsaggnied)
                                else:
                                    st.error("Recurso No Vinculado")
                                    st.info(msj_unsaggnied)
                            
                            # Limpiar mensajes
                            time.sleep(3)
                            st.rerun()
                        # Informa si no hay recursos seleccionados    
                        else:
                            st.warning("No hay recursos seleccionados.")
            # Informa si no se tienen recursos disponibles para asignar
            else:
                st.warning("No hay recursos para asignar")
        # Informa en caso de no haber actividades para asingar recursos
        else:
            st.warning("No hay actividades para mostrar.")
    # En caso de tener el rol de user, no se puede realizar esta actividad
    else:
        st.info("No tienes permisos para realizar esta acción, Contacta al administrador")

# Pestaña para insertar un recurso
with tab_ins_resource:
    # Esta operacion solo la puede realiar el usuario con rol admin
    if any(role in ["admin"] for role in st.session_state["roles"]):
        # Renderiza un formulario para insertar un nuevo recurso
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

            # Contenedor de mensajes, que nos servirá para limpiarlos
            message_container = st.empty()

            # Recupera la accion del botón de envio 
            if submit_insert_resource:
                # Verifica que los campos obligatorios esten llenos
                if not name_ins_resource.strip() or not type_ins_resource.strip() or not description_ins_resource.strip() or not category_ins_resource.strip() or not serialnumber_ins_resource.strip():
                    st.error("Recurso No Agregado")
                    st.info("Llene todos los campos obligatorios")
                else:
                    # Funcion que inserta un recurso
                    state_ins_resource, msj_ins_resource = bd.insertar_recurso(serialnumber_ins_resource, name_ins_resource ,description_ins_resource, category_ins_resource , life_ins_resource, comments_ins_resource, type_ins_resource)
                    # Verifica que la insercion se haya realizado de manera correcta
                    if state_ins_resource:
                        # Muestra el mensaje de exito y la informacion de recurso insertado
                        st.success(msj_ins_resource)
                        st.info(f"{name_ins_resource} -- {type_ins_resource} -- {description_ins_resource} -- {category_ins_resource} -- {serialnumber_ins_resource} -- {life_ins_resource} -- En Stock -- {comments_ins_resource}")
                    # En caso de que no, se muestran las razones
                    else:
                        st.error(msj_ins_resource)
                # Limpieza de mensajes
                time.sleep(3)
                message_container.empty()
                st.rerun()
    # Se informa al usuario con rol user que no puede realizar esta actividad
    else:
        st.info("No tienes permisos para realizar esta acción, Contacta al administrador")

# Pestaña para actualizar un recurso    
with tab_upd_resource:
    # Advertencia
    st.warning("Si cambia el estado de un recurso a 'En Stock', se desvinculará de las actividades que tenga asociadas.")
    st.warning("Cambiar el estado de un recuros a 'En Uso' no lo vinculará con ninguna actividad.")
    # Verifica que el rol del usuario sea admin, ya que solo este rol puede hacerlo
    if any(role in ["admin"] for role in st.session_state["roles"]):
        # Funcion que consulta todos los recursos disponibles para actualizar
        resources_available = bd.consultar_recursos()
        
        # Verifica que el resultado de la consulta sea no vacio
        if resources_available is not None and not resources_available.empty:
            # Combina las columnas de identificador y nombre para los recursos
            combined_resources = [f"#{row['idRecurso']} - {row['nombre']}" for index, row in resources_available.iterrows()]
            # Renderiza un objeto que permite seleccionar un recurso
            resource_selected = st.selectbox("Selecciona un Recurso", combined_resources, key="update_resources_sb")
            # Obtiene el identificador del recurso seleccionado
            id_resource_selected = int (resource_selected.split(' - ')[0][1:])
            # Obtiene la informacion del recurso seleccionado
            resource_data = resources_available[resources_available['idRecurso']==id_resource_selected]
            
            # Funcion que regresa los indices respectivos a los diccionarios de listas de tipo, vida util y estatus
            index_type, index_life, index_status = ut.dict_resource_upd(resource_data['tipo'].iloc[0], resource_data['vida_util'].iloc[0], resource_data['estado_recurso'].iloc[0])

            # Renderiza un formulario con los datos actuales del recurso
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
                # Boton de Envio
                submit_upd_resource = st.form_submit_button("Actualizar")

                # Contiene los mensajes, servira para limpiar los mismos, mas adelante
                message_container = st.empty()

                # Recupera la accion del boton de envio
                if submit_upd_resource:
                    # Verifica que no existan campos obligatorios vacios
                    if not name_upd_resource.strip() or not description_upd_resource.strip() or not serialnumber_upd_resource.strip():
                        st.error("Recurso No Actualizado")
                        st.info("Llene todos los campos obligatorios")
                    else:
                        # Funcion que realiza la actualizacion de un recurso
                        state_update_resource, msj_update_resource = bd.actualizar_recurso(name_upd_resource, type_upd_resource, description_upd_resource, category_upd_resource, serialnumber_upd_resource, life_upd_resource, state_upd_resource, comments_upd_resource, id_resource_selected)

                        # Valida que la operacion de actualizacion sea correcta
                        if state_update_resource:
                            # Muestra el mensaje de exito y los datos del recurso actualizado
                            st.success("Recurso Actualizado")
                            st.info(f"{name_upd_resource} -- {type_upd_resource} -- {description_upd_resource} -- {category_upd_resource} -- {serialnumber_upd_resource} -- {comments_upd_resource}")
                        else:
                            # Muestra el mensaje de fallo y la razon
                            st.error("Recurso No Actualizado")
                            st.info(msj_update_resource)
                    
                    # Limpia los mensajes  
                    time.sleep(3)
                    message_container.empty()
                    st.rerun()
    # Si se tiene el rol de user, le hace saber al usuario que no puede realizar esta operacion
    else:
        st.info("No tienes permisos para realizar esta acción, Contacta al administrador")

# Pestaña para eliminar un recurso
with tab_del_resource:
    # Advertencia
    st.warning("Si en recurso esta asociado a una actividad no podra eliminarse")
    # Valida que el rol del usuario sea admin
    if any(role in ["admin"] for role in st.session_state["roles"]):
        # Funcion para obtener todos los recursos
        resources_avaliable = bd.consultar_recursos()
        # Verifica que el resultado sea no vacio
        if resources_avaliable is not None and not resources_available.empty:
            # Combina las columnas de identicador y nombre de recursos
            combined_resources = [f"#{row['idRecurso']} - {row['nombre']}" for index, row in resources_avaliable.iterrows()]
            # Renderiza un objeto para seleccionar un objeto a eliminar
            resource_selected = st.selectbox("Selecciona un Recurso", combined_resources)
            # Obtiene el identificador del recursos seleccionado
            id_resource_selected = int(resource_selected.split(' - ')[0][1:])
            # Obtiene los datos del recurso seleccionado
            resource_data = resources_avaliable[resources_avaliable['idRecurso'] == id_resource_selected]

            # Genera un contenedor para darle formato a los datos del recurso a eliminar
            with st.container(border = True):
                st.markdown(f"## 🔧 {resource_data["nombre"].iloc[0]}")
                st.markdown(f"🔠 Descripción: {resource_data["descripcion"].iloc[0]}")
                st.markdown(f"#️⃣ No. Serie: {resource_data["no_serie"].iloc[0]}")
            
            # Genera un contenedor para el boton de eliminar
            with st.container():
                # Verificacion de dos pasos para elimianr
                with st.popover(f"Eliminar", use_container_width=True):
                    st.write(f"¿Seguro que quieres eliminar a {resource_data["nombre"].iloc[0]}?")
                    # Renderiza un boton y recupera la accion de presionarlo
                    if st.button("Si. Estoy Seguro"):
                        # Funcion que elimina el recurso
                        state_del_resouce, msj_del_resource= bd.eliminar_recurso(id_resource_selected)
                        # Verifica el exito de la eliminacion
                        if state_del_resouce:
                            st.success(msj_del_resource)
                        # Si no es exitosa la eliminacion
                        else:
                            st.error("Recurso No Eliminado")
                            st.info(msj_del_resource)
                        # Limpia los mensajes
                        time.sleep(3)
                        message_container.empty()
                        st.rerun()
        # En caso de que no existan recursos
        else:
            st.warning("No hay datos para mostrar.")
    # En caso de ser un usuario con rol user
    else:
        st.info("No tienes permisos para realizar esta acción, Contacta al administrador")

# Pestaña para nuevos recursos
with tab_new_resource:
    # Genera columnas para darle formato al boton de refresco
    col1, col2 = st.columns([95,1])
    with col2: 
        # Renderiza y recupera la accion de presionar el boton de refresco
        if st.button("🔄", key="ref_new_resource"):
            st.rerun()
    # Verifica que el rol del usuario sea user o admin
    if any(role in ["admin", "user"] for role in st.session_state["roles"]):
        ################################# LISTADO ################################# 
        st.markdown("### Listado")
        # Hace una consulta de todas las peticiones de recursos
        new_resources = bd.consultar_peticiones_recursos(0)

        # Verifica que el resultado no sea vacio
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
                index += 1
        # En caso de que el resultado sea vacio
        else:
            st.warning("No existen peticiones")

        ################################# PETICION #################################
        # Para el caso de una petición, solo cuando sea admin tendrá que desplegar la opcion de escoger un miembro 
        st.markdown("---")
        st.markdown("### Petición")

        # Funcion que extrae los miembros disponibles
        supports_new_resource = bd.consultar_miembros(1)
        # Combina las columnas de identificador y nombre
        combined_supports = [f"#{row['idMiembro']} - {row['nombre']}" for index, row in supports_new_resource.iterrows()] 
        
        # Renderizar un formulario para hacer una peticion de un nuevo recurso
        with st.form("new_resource", clear_on_submit=True):
            # Entradas del formulario
            name_new_resource = st.text_input("Nombre*: ", placeholder="Llave")
            type_new_resource = st.selectbox("Tipo*: ", ["Herramienta", "Material"])
            description_new_resource = st.text_input("Descripción*: ", placeholder="Llave Allen 3/4")
            date_new_resource = datetime.now().strftime("%Y-%m-%d")
            quantity_new_resource = st.selectbox("Cantidad de Piezas*: ", ["1","2","3","4","5","6","7","8","9","10"])

            # Esta seccion nos da el identificador de a quien se asignara la actividad
            if any(role in ["admin"] for role in st.session_state["roles"]):
                # Si el resultado no es vacio
                if combined_supports:
                    # Generamos un selector de miembros para saber a que miembro asignar la peticion de nuevo recurso
                    support_new_resource = st.selectbox("Miembro Asociado:", combined_supports)
                    # Obtenemos el miembro seleccionado para la peticion de nuevo recurso
                    id_support_ins = int (support_new_resource.split(' - ')[0][1:])
            else:
                # Busca al miembro por el correo del usuario
                state_consultar_email, msj_consultar_email = bd.consultar_id_email(st.session_state['email'])
                
                # En caso de que no encuentre al miembro
                if state_consultar_email: 
                    id_support_ins = msj_consultar_email
                else:
                    id_support_ins=0
            
            # Sigue siendo parte del formulario
            comments_new_resource = st.text_area("Notas Adicionales: ", placeholder="Agrega tus comentarios")
            st.markdown("*Campos Obligatorios")
            # Boton de envio
            submit_new_resource = st.form_submit_button("Pedir")

            # Recupera la accion del boton del envio
            if submit_new_resource:
                # Verifica que los campos obligatorios esten llenos
                if not name_new_resource.strip() or not type_new_resource.strip() or not description_new_resource.strip():
                    st.error("Petición No Agregada")
                    st.info("Llene todos los campos obligatorios")
                else:
                    # Verifica que el usuario con rol user tenga un miembro asociado.
                    if id_support_ins > 0:
                        # Funcion hace el requisito del nuevo recurso
                        state_ins_new_resource, msj_ins_new_resource = bd.insertar_peticion_nuevo_recurso(name_new_resource, type_new_resource, description_new_resource, date_new_resource, quantity_new_resource, comments_new_resource, id_support_ins)
                        # Verifica el estado del requisito
                        if state_ins_new_resource:
                            # En caso de exito, muestra el mensaje de insercion
                            st.success("Petición Agregada")
                            st.info(msj_ins_new_resource)
                        else:
                            # En caso contrario explica porque no se pudo realizar
                            st.error(msj_ins_new_resource)
                    # En caso que no tenga un miembro asociado
                    else:
                        st.warning("No tiene permiso para hacer peticiones. Contacte a soporte.")
                # Limpia los mensajes  
                time.sleep(3)
                st.rerun()
                    
        ################################# ELIMINACION #################################
        st.markdown("---")
        st.markdown("### Eliminar")

        # Verifica que el usuario tenga un rol de admin
        if any(role in ["admin"] for role in st.session_state["roles"]):
            # Funcion que consulta las peticiones de recursos
            new_resources_avaliable = bd.consultar_peticiones_recursos(1)
        # En caso de ser un usuario con rol user
        else: 
            # Funcion que trae el identificador del miembro de acuerdo con su email
            state_id_email, id_sesion = bd.consultar_id_email(st.session_state['email'])
            if state_id_email:
                # En caso de encontrar a un miembro asociado al usuario
                new_resources_avaliable = bd.consultar_peticiones_por_id(id_sesion)
            else:
                # En caso de no encontrar a un miembro asociado al usario
                new_resources_avaliable= None
        
        # Verifica que el resultado no sea vacio
        if new_resources_avaliable is not None and not new_resources_avaliable.empty:
            # Combinamos las columnas de identificador y nombre de las peticiones
            new_combined_resources = [f"#{row['idNuevoRecurso']} - {row['nombre']}" for index, row in new_resources_avaliable.iterrows()]
            # Crea un objeto para seleccionar el recurso
            new_resource_selected = st.selectbox("Selecciona un Recurso", new_combined_resources)
            # Obtiene el identificador de la peticion recurso seleccionado
            new_id_resource_selected = int(new_resource_selected.split(' - ')[0][1:])
            # Obtiene los datos de la peticion
            new_resource_data = new_resources_avaliable[new_resources_avaliable['idNuevoRecurso'] == new_id_resource_selected]
            
            # Crear un contenedor para desplegar el boton de eliminar
            with st.container():
                # Crea una doble confirmacion para eliminar la peticion de nuevo recurso
                with st.popover(f"Eliminar", use_container_width=True):
                    st.write(f"¿Seguro que quieres eliminar a {new_resource_data["nombre"].iloc[0]}?")
                    # Recupera la accion de elminar la peticion
                    if st.button("Si. Estoy Seguro", key="delete_new_resource"):
                        # Funcion para eliminar la peticion del nuevo recurso
                        state_del, ms_del= bd.eliminar_peticion_nuevo_recurso(new_id_resource_selected)
                        # Muestra mensajes en caso de exito
                        if state_del: 
                            st.success("Petición Eliminada")
                            st.info(ms_del)
                        # Muestra mensajes en caso de falla
                        else: 
                            st.error("Petición No Eliminada")
                            st.info(ms_del)

                        # Limpia los mensajes
                        time.sleep(3)
                        st.rerun()
        # En caso de que el resultado sea vacio, puede ser porque no encontro ninguna peticion o porque no se encontro el id de miembro
        else:
            # Si no tiene ninguna peticion
            if state_id_email:
                st.warning("No hay datos para mostrar")
            # Si no tiene miembro asociado al usuario
            else: 
                st.warning("El usuario con el que iniciaste sesion no tiene un miembro asociado. Contacte con Soporte")
    # En caso de no tener permisos. Para roles futuros
    else:
        st.info("No tienes permisos para realizar esta acción, Contacta con Soporte")