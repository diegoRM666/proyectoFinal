import streamlit as st
import pandas as pd
import time
from menu import menu_with_redirect
import logic.bd as bd
import logic.utilities as ut 



# Primero hacemos las comprobacion
menu_with_redirect()

#Creamos un titulo
st.markdown("# 👤 Miembros")

# Mostrar las disintas actividades a realizar
tab_lst_support, tab_ins_support, tab_upd_support, tab_del_support = \
      st.tabs(["Listar Miembro","Agregar Miembro", "Actualizar Miembro", "Eliminar Miembro"])


with tab_lst_support:
    col1, col2 = st.columns([95,1])
    with col2: 
        if st.button("🔄", key="ref_support"):
            st.rerun()
    if any(role in ["admin", "user"] for role in st.session_state["roles"]):
        supports = bd.consultar_miembros(0)
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
                        if activities_by_support is not None and not activities_by_support.empty:
                            st.markdown(f''' Atendiendo **:green[{activities_by_support['no_actividades'].iloc[0]}]** actividades''')
                        if activities_by_support_hist is not None and not activities_by_support_hist.empty:
                            st.markdown(f''' Ha atendido **:green[{activities_by_support_hist['no_actividades'].iloc[0]}]** actividades''')
                        if avg_time_support is not None and not avg_time_support.empty and not avg_time_support['promTiempo'].iloc[0] == None:
                            st.markdown(f'''Avg. Solución (Dias): :green[{avg_time_support['promTiempo'].iloc[0]}]''')
                        if support['notas'] !="":
                            st.markdown(f"🗒️ {support['notas']}")
                        if support['disponibilidad'] == "No Disponible":
                            st.markdown(f'''### :orange[{support['estatus']}]''')
                        else:
                            st.markdown(f'''### :green[{support['estatus']}]''')
                
                # Actualizar el índice para alternar entre las columnas
                index += 1

        else:
            st.warning("No existen datos")
    else:
        st.info("No tienes permisos para realizar esta acción, Contacta al administrador")

with tab_ins_support:
    if any(role in ["admin"] for role in st.session_state["roles"]):
        with st.form("insert_support", clear_on_submit=True):
            # Entradas del formulario
            name_ins_support = st.text_input("Nombre*: ", placeholder="Juan Montes")
            phone_ins_support = st.text_input("Teléfono de Contacto*: ", placeholder="5530104575")
            email_ins_support = st.text_input("Email*: ", placeholder="juanmontes@test.com")
            address_ins_support = st.text_input("Dirección*: ", placeholder="Calle Siempre Viva 62 Col. El Temazcal")
            status_ins_support = "Libre"
            comments_ins_support = st.text_area("Notas Adicionales: ", placeholder="Agrega tus comentarios")
            
            # Indicador de campos obligatorios
            st.markdown("*Campos Obligatorios")
            
            # Botón de envío
            submit_insert_support = st.form_submit_button("Agregar")

            message_container = st.empty()

            if submit_insert_support:
                if not name_ins_support.strip() or not phone_ins_support.strip() or not email_ins_support.strip()\
                or not address_ins_support.strip():
                    st.error("Miembro de Soporte No Agregado")
                    st.info("Llene todos los campos obligatorios")
                else:
                    if status_ins_support in ["Vacaciones", "En Actividad", "Incapacidad"]:
                        disponibility_ins_support = "No Disponible"
                    else: 
                        disponibility_ins_support = "Disponible"
                    
                    state_ins_support, msj_ins_support = bd.insertar_miembro(name_ins_support, phone_ins_support, email_ins_support, address_ins_support, disponibility_ins_support, status_ins_support, comments_ins_support)
                    if state_ins_support:
                        st.success(msj_ins_support)
                        st.info(f"{name_ins_support} -- {phone_ins_support} -- {email_ins_support} -- {address_ins_support}")
                    else: 
                        st.error(msj_ins_support)
                time.sleep(3)
                message_container.empty()
                st.rerun()
    else:
        st.info("No tienes permisos para realizar esta acción, Contacta al administrador")

with tab_upd_support:
    if any(role in ["admin", "user"] for role in st.session_state["roles"]):
        if any(role in ["admin"] for role in st.session_state["roles"]):
            st.info("Considere que el cambio en el estatus de un miembro no cambiará el estatus de las actividades a las que esta asociado. Esto se deberá realizar manualmente.")
            supports_available = bd.consultar_miembros(0)

            if supports_available is not None:
                combined_supports = [f"#{row['idMiembro']} - {row['nombre']}" for index, row in supports_available.iterrows()]
                support_selected = st.selectbox("Selecciona un Miembro", combined_supports, key="update_supports_sb")
                id_support_selected = int (support_selected.split(' - ')[0][1:])
                support_data = supports_available[supports_available['idMiembro']==id_support_selected]
                
                #Necesitamos ademas saber el index del estatus
                index_status = ut.dict_support_upd(support_data['estatus'].iloc[0])

                with st.form("update_support", clear_on_submit= True):
                    name_upd_support = st.text_input("Nombre*: ", value=f"{support_data['nombre'].iloc[0]}", key="name_ins_support")
                    phone_upd_support = st.text_input("Telefono de Contacto*: ", value=f"{support_data['telefono'].iloc[0]}")
                    email_upd_support = st.text_input("email*: ", value=f"{support_data['email'].iloc[0]}")
                    address_upd_support = st.text_input("Dirección*: ", value=f"{support_data['direccion'].iloc[0]}")
                    status_upd_support = st.selectbox("Estatus", ["Libre","Vacaciones", "En Actividad", "Incapacidad"], index=index_status)
                    comments_upd_support = st.text_area("Notas Adicionales: ", value=f"{support_data['notas'].iloc[0]}")
                    st.write("*Campos Obligatorios")
                    submit_upd_support = st.form_submit_button("Actualizar")


                    message_container = st.empty()

                if submit_upd_support:
                    if not name_upd_support.strip() or not phone_upd_support.strip() or not email_upd_support.strip() or not address_upd_support.strip():
                        st.error("Miembro de Soporte Actualizado")
                        st.info("Llene todos los campos obligatorios")
                    else:
                        if status_upd_support in ["Vacaciones", "Baja", "En Actividad", "Incapacidad"]:
                                disponibility_upd_support = "No Disponible"
                        else: 
                            disponibility_upd_support = "Disponible"
                        state_update_support, msj_update_support = bd.actualizar_miembro(id_support_selected, name_upd_support, phone_upd_support, email_upd_support, address_upd_support, disponibility_upd_support, status_upd_support, comments_upd_support)
                        if state_update_support:
                                st.success(msj_update_support)
                                st.info(f"{name_upd_support} -- {phone_upd_support} -- {email_upd_support} -- {address_upd_support} -- {comments_upd_support}")
                        else:
                            st.error(msj_update_support)
                        
                    # Para que se limpien los mensajes
                    time.sleep(3)
                    message_container.empty()
                    st.rerun()
            else: 
                st.warning("No hay datos para mostrar")

        else: 
            state_support_indie, id_support_selected = bd.consultar_id_email(st.session_state['email'])
            if state_support_indie:
                support_data = bd.consultar_miembro_id(id_support_selected)     

                with st.form("update_support_indie", clear_on_submit= True):
                    name_upd_support = st.text_input("Nombre*: ", value=f"{support_data['nombre'].iloc[0]}", key="name_ins_support")
                    phone_upd_support = st.text_input("Telefono de Contacto*: ", value=f"{support_data['telefono'].iloc[0]}")
                    address_upd_support = st.text_input("Dirección*: ", value=f"{support_data['direccion'].iloc[0]}")
                    comments_upd_support = st.text_area("Notas Adicionales: ", value=f"{support_data['notas'].iloc[0]}")
                    st.write("*Campos Obligatorios")
                    submit_upd_support = st.form_submit_button("Actualizar")

                    message_container = st.empty()
                
                if submit_upd_support:
                    if not name_upd_support.strip() or not phone_upd_support.strip() or not address_upd_support.strip():
                        st.error("Miembro de Soporte Actualizado")
                        st.info("Llene todos los campos obligatorios")
                    else:
                        state_update_support, msj_update_support = bd.actualizar_miembro_indie(id_support_selected, name_upd_support, phone_upd_support, address_upd_support, comments_upd_support)
                        if state_update_support:
                                st.success(msj_update_support)
                                st.info(f"{name_upd_support} -- {phone_upd_support} -- {address_upd_support} -- {comments_upd_support}")
                        else:
                            st.error(msj_update_support)
                        
                    # Para que se limpien los mensajes
                    time.sleep(3)
                    message_container.empty()
                    st.rerun()
            
    else:
        st.warning("No tienes permisos para realizar esta acción, Contacta al administrador")   

with tab_del_support:
    if any(role in ["admin"] for role in st.session_state["roles"]):
        st.info("Si eliminamos un miembro, se eliminará de igual manera sus peticiones")
        supports_avaliable = bd.consultar_miembros(0)
        if supports_avaliable is not None is not supports_available.empty:
            combined_supports = [f"#{row['idMiembro']} - {row['nombre']}" for index, row in supports_avaliable.iterrows()]
            support_selected = st.selectbox("Selecciona un Miembro", combined_supports)
            id_support_selected = int(support_selected.split(' - ')[0][1:])
            support_data = supports_avaliable[supports_avaliable['idMiembro'] == id_support_selected]

            with st.container(border = True):
                st.markdown(f"## 👤 {support_data["nombre"].iloc[0]}")
                st.markdown(f"☎️ Telefono: {support_data["telefono"].iloc[0]}")
                st.markdown(f"📧 Email: {support_data["email"].iloc[0]}")
                st.markdown(f"🔤 Direccion: {support_data["direccion"].iloc[0]}")
            
            with st.container():
                with st.popover(f"Eliminar", use_container_width=True):
                    st.write(f"¿Seguro que quieres eliminar a {support_data["nombre"].iloc[0]}?")
                    if st.button("Si. Estoy Seguro"):
                        state_del, ms_del= bd.eliminar_miembro(id_support_selected)
                        if state_del:
                            st.success(ms_del)
                        else:
                            st.error(ms_del)
                        time.sleep(3)
                        message_container.empty()
                        st.rerun()
        else:
            st.warning("No hay datos para mostrar...")
    else:
        st.info("No tienes permisos para realizar esta acción, Contacta al administrador")