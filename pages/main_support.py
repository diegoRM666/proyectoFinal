import streamlit as st
import pandas as pd
import time
from menu import menu_with_redirect
import logic.bd as bd
import logic.utilities as ut 



# Comprueba que el usuario este loggeado.
menu_with_redirect()

#Creamos un titulo
st.markdown("# 👤 Miembros")

# Mostrar las disintas actividades a realizar
tab_lst_support, tab_ins_support, tab_upd_support, tab_del_support = \
      st.tabs(["Listar Miembros","Agregar Miembro", "Actualizar Miembro", "Eliminar Miembro"])

# Pestaña para listar los miembros de soporte
with tab_lst_support:
    # Genera columnas para distribuir mejor la informacion en la pagina
    col1, col2 = st.columns([95,1])
    with col2: 
        # Creación de botón para refrescar la página
        if st.button("🔄", key="ref_support"):
            st.rerun()
    # Determina si se tiene el rol admin o user 
    if any(role in ["admin", "user"] for role in st.session_state["roles"]):
        # Se realiza la consuta para obtener los miembros que se encuentran registrados en el sistema
        supports = bd.consultar_miembros(0)
        # Valida que el resultado no sea vacio
        if supports is not None and not supports.empty:
            # Definir el número de columnas
            num_cols = 2
            cols = st.columns(num_cols)
            
            # Inicializar el índice para repartir a las columnas
            index = 0

            # Iterar sobre los supports en el DataFrame
            for _, support in supports.iterrows():
                col = cols[index % num_cols]  # Alterna entre las columnas (0 y 1)
                
                # Mostrar la información del support en la columna correspondiente
                with col:
                    with st.container(border=True):
                        #Vamos a hacer el conteo de actividades realizadas actualmente e historicamente por usuario
                        state_metrics, activities_by_support, activities_by_support_hist, avg_time_support = bd.obtener_actividades_y_promedio(support['idMiembro'])

                        #Despliegue de información
                        st.markdown(f"## 👤 {support['nombre']}")
                        st.markdown(f"☎️ {support['telefono']}")
                        st.markdown(f"📧 {support['email']}")
                        st.markdown(f"🔤 {support['direccion']}")
                        # Metrica que informa si se esta realizando alguna actividad en el momento
                        if activities_by_support is not None and not activities_by_support.empty:
                            st.markdown(f''' Atendiendo **:green[{activities_by_support['no_actividades'].iloc[0]}]** actividades''')
                        # Metrica que informa cuantas actividades ha atendido el miembro
                        if activities_by_support_hist is not None and not activities_by_support_hist.empty:
                            st.markdown(f''' Ha atendido **:green[{activities_by_support_hist['no_actividades'].iloc[0]}]** actividades''')
                        # Metrica que muestra el tiempo promedio de solución de actividades para cada miembro 
                        if avg_time_support is not None and not avg_time_support.empty and not avg_time_support['promTiempo'].iloc[0] == None:
                            st.markdown(f'''Promedio de Solución (Dias): :green[{avg_time_support['promTiempo'].iloc[0]}]''')
                        # Si el miembro tiene notas lo muestra
                        if support['notas'] !="":
                            st.markdown(f"🗒️ {support['notas']}")
                        # Muestra un distinto color de texto de acuerdo a la disponibilidad
                        if support['disponibilidad'] == "No Disponible":
                            st.markdown(f'''### :orange[{support['estatus']}]''')
                        else:
                            st.markdown(f'''### :green[{support['estatus']}]''')
                
                # Actualizar el índice para alternar entre las columnas
                index += 1
        
        # En caso de que el resultado este vacio
        else:
            st.warning("No existen datos")
    
    # En caso de que no tengamos un rol asociado, se informa 
    else:
        st.info("No tienes permisos para realizar esta acción, Contacta al administrador")

# Pestañana para insetar un miembro de soporte
with tab_ins_support:
    # Verifica que el usuario tenga un rol de admin. Solo el admin puede insertar nuevos miembros
    if any(role in ["admin"] for role in st.session_state["roles"]):
        # Renderizamos un formulario para la insercion
        with st.form("insert_support", clear_on_submit=True):
            # Entradas del formulario
            name_ins_support = st.text_input("Nombre*: ", placeholder="Juan Montes")
            phone_ins_support = st.text_input("Teléfono de Contacto*: ", placeholder="5530104575")
            email_ins_support = st.text_input("Email*: ", placeholder="juanmontes@test.com")
            address_ins_support = st.text_input("Dirección*: ", placeholder="Calle Siempre Viva 62 Col. El Temazcal")
            status_ins_support = "Libre" # Por default se da el estatus de libre.
            comments_ins_support = st.text_area("Notas Adicionales: ", placeholder="Agrega tus comentarios")
            disponibility_ins_support = "Disponible"
            
            # Indicador de campos obligatorios
            st.markdown("*Campos Obligatorios")
            
            # Botón de envío
            submit_insert_support = st.form_submit_button("Agregar")

            # Contenedor de mensajes, que luego nos funcionara para limpiar los mismos
            message_container = st.empty()

            # Cuando se acciona el boton de envio de informacion
            if submit_insert_support:
                # Verifica si los campos obligatorios estan llenos
                if not name_ins_support.strip() or not phone_ins_support.strip() or not email_ins_support.strip() or not address_ins_support.strip():
                    # En caso de que no, entonces tenemos una advertencia
                    st.error("Miembro de Soporte No Agregado")
                    st.info("Llene todos los campos obligatorios")
                
                # Si estan llenos los campos obligatorios
                else:
                    # Se llama a la funcion que insertar el miembro de soporte
                    state_ins_support, msj_ins_support = bd.insertar_miembro(name_ins_support, phone_ins_support, email_ins_support, address_ins_support, disponibility_ins_support, status_ins_support, comments_ins_support)
                    # Basandonos en el estado despues de llamar a la función determinamos si se realizo de manera correcta o no
                    if state_ins_support:
                        # En caso de exito, se manda el mensaje y la informacion del miembro insertado
                        st.success(msj_ins_support)
                        st.info(f"{name_ins_support} -- {phone_ins_support} -- {email_ins_support} -- {address_ins_support}")
                    else: 
                        # En caso contrario se informa porque no fue posible eliminarlo
                        st.error(msj_ins_support)
                # Limpia los mensajes
                time.sleep(3)
                message_container.empty()
                st.rerun()
    
    # Si se tiene el rol de user, no se pueden ingresar miembros, entonces se le informa al usuario
    else:
        st.info("No tienes permisos para realizar esta acción, Contacta al administrador")

# Pestaña para actualizar un miembro de soporte
with tab_upd_support:
    # Valida si tiene uno de los roles que existen.
    if any(role in ["admin", "user"] for role in st.session_state["roles"]):
        
        # Si tenemos un rol de admin
        if any(role in ["admin"] for role in st.session_state["roles"]):
            # Genera una advertencia
            st.info("Considere que el cambio en el estatus de un miembro no cambiará el estatus de las actividades a las que esta asociado. Esto se deberá realizar manualmente.")
            
            # Llamado a la funcion que consulta a los miembros
            supports_available = bd.consultar_miembros(0)

            # Verifica que el resultado no es vacio
            if supports_available is not None and not supports_available.empty:
                # Combinamos las columnas del identificador y el nombre de los miembros que existen en el sistema
                combined_supports = [f"#{row['idMiembro']} - {row['nombre']}" for index, row in supports_available.iterrows()]
                # Desplegamos un objeto para seleccionar el miembro a seleccionar
                support_selected = st.selectbox("Selecciona un Miembro", combined_supports, key="update_supports_sb")
                # Obtenemos el identificador del miembro seleccionado
                id_support_selected = int (support_selected.split(' - ')[0][1:])
                # Obtencion de los datos de el miembro seleccionado para actualizar
                support_data = supports_available[supports_available['idMiembro']==id_support_selected]
                
                # Llamamos a una fucnion que nos permite obtener el indice de estatus de acuerdo a un diccionario.
                index_status = ut.dict_support_upd(support_data['estatus'].iloc[0])

                # Renderizamos el formulario para actualizar. Tendra los datos actuales del miembro
                with st.form("update_support", clear_on_submit= True):
                    name_upd_support = st.text_input("Nombre*: ", value=f"{support_data['nombre'].iloc[0]}", key="name_ins_support")
                    phone_upd_support = st.text_input("Telefono de Contacto*: ", value=f"{support_data['telefono'].iloc[0]}")
                    email_upd_support = st.text_input("email*: ", value=f"{support_data['email'].iloc[0]}")
                    address_upd_support = st.text_input("Dirección*: ", value=f"{support_data['direccion'].iloc[0]}")
                    status_upd_support = st.selectbox("Estatus", ["Libre","Vacaciones", "En Actividad", "Incapacidad"], index=index_status)
                    comments_upd_support = st.text_area("Notas Adicionales: ", value=f"{support_data['notas'].iloc[0]}")
                    st.write("*Campos Obligatorios")
                    # Botón de envio de la informacion
                    submit_upd_support = st.form_submit_button("Actualizar")

                    # Contenedor de mensajes, que posteriormente nos ayudara a limpiar
                    message_container = st.empty()

                # Recupera la acción del botón
                if submit_upd_support:
                    # Verifica que los campos obligatorios esten llenos
                    if not name_upd_support.strip() or not phone_upd_support.strip() or not email_upd_support.strip() or not address_upd_support.strip():
                        st.error("Miembro de Soporte Actualizado")
                        st.info("Llene todos los campos obligatorios")
                    else:
                        # Genera un cambio de estatus de acuerdo a la disponibilidad
                        if status_upd_support in ["Vacaciones", "Baja", "En Actividad", "Incapacidad"]:
                                disponibility_upd_support = "No Disponible"
                        # En caso de que no sea alguno de los estatus anteriores entonces esta disponible
                        else: 
                            disponibility_upd_support = "Disponible"
                        
                        # Funcion que permite actualizar el miembro  
                        state_update_support, msj_update_support = bd.actualizar_miembro(id_support_selected, name_upd_support, phone_upd_support, email_upd_support, address_upd_support, disponibility_upd_support, status_upd_support, comments_upd_support)
                        
                        # Verifica que la consulta se haya relizado de manera correcta
                        if state_update_support:
                                # Muestra el mensaje y la información actualizada
                                st.success(msj_update_support)
                                st.info(f"{name_upd_support} -- {phone_upd_support} -- {email_upd_support} -- {address_upd_support} -- {comments_upd_support}")
                        else:
                            # En caso de que la consulta no se ejecute de manera correcta
                            st.error(msj_update_support)
                        
                    # Limpieza de los mensajes
                    time.sleep(3)
                    message_container.empty()
                    st.rerun()
            
            # Si el resultado es vacio, se informa 
            else: 
                st.warning("No hay datos para mostrar")
        
        # Cuando tenemos el rol de user
        else: 
            # Se consulta el identificador del miembro de acuerdo al email del usuario
            state_support_indie, id_support_selected = bd.consultar_id_email(st.session_state['email'])
            
            # Verifica que exista el miembro asociado al usuario
            if state_support_indie and id_support_selected!=0:
                # Consulta los datos de un mimebro de acuerdo a su identificador.
                support_data = bd.consultar_miembro_id(id_support_selected)     

                # Renderiza un formulario para actualizar el miembro, con los valores actuales
                # No se pueden actualizar la misma cantidad de campos del miembro, por ejemplo, no actualiza el estatus del miembro
                with st.form("update_support_indie", clear_on_submit= True):
                    name_upd_support = st.text_input("Nombre*: ", value=f"{support_data['nombre'].iloc[0]}", key="name_ins_support")
                    phone_upd_support = st.text_input("Telefono de Contacto*: ", value=f"{support_data['telefono'].iloc[0]}")
                    address_upd_support = st.text_input("Dirección*: ", value=f"{support_data['direccion'].iloc[0]}")
                    comments_upd_support = st.text_area("Notas Adicionales: ", value=f"{support_data['notas'].iloc[0]}")
                    st.write("*Campos Obligatorios")
                    # Renderiza el boton de envio
                    submit_upd_support = st.form_submit_button("Actualizar")
                
                # Contenedor de mensajes, que servirá para ser limpiados
                message_container = st.empty()
                
                # Recupera la accion de presionar el boton
                if submit_upd_support:
                    # Verifica que los campos obligatorios esten llenos
                    if not name_upd_support.strip() or not phone_upd_support.strip() or not address_upd_support.strip():
                        st.error("Miembro de Soporte No Actualizado")
                        st.info("Llene todos los campos obligatorios")
                    # Si estan llenos los campos obligatorios
                    else:
                        # Funcion que realiza la actualizacion del miembro
                        state_update_support, msj_update_support = bd.actualizar_miembro_indie(id_support_selected, name_upd_support, phone_upd_support, address_upd_support, comments_upd_support)
                        # Verifica que la actualizacion fuera correcta
                        if state_update_support:
                                # Despliega mensajes en caso de exito, junto con la informacion actualizada
                                st.success(msj_update_support)
                                st.info(f"{name_upd_support} -- {phone_upd_support} -- {address_upd_support} -- {comments_upd_support}")
                        # Cuando no se pueda actualizar el miembro, lo notifica
                        else:
                            st.error(msj_update_support)
                        
                    # Limpieza de mensajes
                    time.sleep(3)
                    message_container.empty()
                    st.rerun()
            
            # Informa que el usuario no tiene un miembro asociado
            else: 
                st.warning("No hay un miembro asociado a tu correo electronico. Contacte a soporte")

    # En caso de que no tenga permisos, le informara al usuario.    
    else:
        st.warning("No tienes permisos para realizar esta acción, Contacta al administrador")   

# Pestaña para eliminar un miembro de soporte
with tab_del_support:
    # Esta accion solo puede ser realizada por un usuario admin, por lo cual verifica
    if any(role in ["admin"] for role in st.session_state["roles"]):
        # Informa que al eliminar un miembro, elimina de igual forma todos las peticiones asociadas al miembro
        st.info("Si eliminamos un miembro, se eliminará de igual manera sus peticiones")
        # Realiza una consulta de todos los miembros dentro del sistema.
        supports_avaliable = bd.consultar_miembros(0)

        # Valida que el resultado de la consulta no sea vacio
        if supports_avaliable is not None and not supports_available.empty:
            # Combina las columnas de identificador y nombre del miembro
            combined_supports = [f"#{row['idMiembro']} - {row['nombre']}" for index, row in supports_avaliable.iterrows()]
            # Despliega uin objeto que permite seleccionar el miembro de soporte
            support_selected = st.selectbox("Selecciona un Miembro", combined_supports)
            # Obtencion del identificador del miembro de soporte
            id_support_selected = int(support_selected.split(' - ')[0][1:])
            # Obtención de los datos del miembro de soporte seleccionado
            support_data = supports_avaliable[supports_avaliable['idMiembro'] == id_support_selected]

            # Genera un contenedor para mostrar la información del miembro a eliminar
            with st.container(border = True):
                st.markdown(f"## 👤 {support_data["nombre"].iloc[0]}")
                st.markdown(f"☎️ Telefono: {support_data["telefono"].iloc[0]}")
                st.markdown(f"📧 Email: {support_data["email"].iloc[0]}")
                st.markdown(f"🔤 Direccion: {support_data["direccion"].iloc[0]}")

            # Genera otro contenedor para desplegar el boton de eliminar
            with st.container():
                # Doble confirmacion del objeto a eliminar
                with st.popover(f"Eliminar", use_container_width=True):
                    st.write(f"¿Seguro que quieres eliminar a {support_data["nombre"].iloc[0]}?")
                    if st.button("Si. Estoy Seguro"):
                        # Funcion que elimina el miembro seleccionado junto con las peticiones asociadas al miembro
                        state_del, ms_del= bd.eliminar_miembro(id_support_selected)
                        # Determina si se elimino de manera correcta
                        if state_del:
                            st.success(ms_del)
                        else:
                            st.error(ms_del)
                        # Limpieza de mensajes
                        time.sleep(3)
                        message_container.empty()
                        st.rerun()
        # Si no se encuentra el miembro, informa que no hay datos para mostrar
        else: 
            st.warning("No hay datos para mostrar")
    # En caso de que no tengamos el rol de admin, nos dira que no tenemos permisos.
    else:
        st.info("No tienes permisos para realizar esta acción, Contacta al administrador")