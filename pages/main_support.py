import streamlit as st
import pandas as pd
import time
from menu import menu_with_redirect
import logic.bd as bd



# Primero hacemos las comprobacion
menu_with_redirect()

#Creamos un titulo
st.markdown("# 👤 Miembros")

# Mostrar las disintas actividades a realizar
tab_lst_support, tab_ins_support, tab_upd_support, tab_del_support = \
      st.tabs(["Listar Miembro","Agregar Miembro", "Actualizar Miembro", "Eliminar Miembro"])


with tab_lst_support:
    supports = bd.consultar("SELECT * FROM miembro;")

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
                    activities_by_support = bd.consultar(f"SELECT idMiembro, count(*) as no_actividades FROM actividad WHERE idMiembro = '{support['idMiembro']}';")
                    activities_by_support_hist = bd.consultar(f"SELECT idMiembro, count(*) as no_actividades FROM actividad_hist WHERE idMiembro='{support['idMiembro']}' GROUP BY idMiembro")
                    avg_time_support = bd.consultar(f"SELECT AVG(fecha_fin_a - fecha_inicio_a) AS promTiempo FROM actividad_hist WHERE idMiembro={support['idMiembro']};")

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


with tab_ins_support:
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
                query_insert_support = f"INSERT INTO miembro (nombre, telefono, email, direccion, disponibilidad, estatus, notas) VALUES ('{name_ins_support}', '{phone_ins_support}', '{email_ins_support}', '{address_ins_support}', '{disponibility_ins_support}', '{status_ins_support}', '{comments_ins_support}');"
                bd.insertar(query_insert_support)
                st.success("Miembro de Soporte Agregado")
                st.info(f"{name_ins_support} -- {phone_ins_support} -- {email_ins_support} -- {address_ins_support}")
                
            # Para que se limpien los mensajes
            time.sleep(3)
            message_container.empty()
            st.rerun()

with tab_upd_support:
    supports_available = bd.consultar("SELECT * FROM miembro;")
    
    if supports_available is not None:
        combined_supports = [f"#{row['idMiembro']} - {row['nombre']}" for index, row in supports_available.iterrows()]
        support_selected = st.selectbox("Selecciona un Miembro", combined_supports, key="update_supports_sb")
        id_support_selected = int (support_selected.split(' - ')[0][1:])
        support_data = supports_available[supports_available['idMiembro']==id_support_selected]
        
        #Necesitamos ademas saber el index del estatus
        status_dict = {
            "Libre": 0,
            "Vacaciones": 1,
            "En Actividad": 2,
            "Incapacidad": 3
        }

        index_status = status_dict[support_data['estatus'].iloc[0]]


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
        if not name_upd_support.strip() or not phone_upd_support.strip() or not email_upd_support.strip()\
        or not address_upd_support.strip():
            st.error("Miembro de Soporte Actualizado")
            st.info("Llene todos los campos obligatorios")
        else:
            if status_upd_support in ["Vacaciones", "Baja", "En Actividad", "Incapacidad"]:
                    disponibility_upd_support = "No Disponible"
                    print(disponibility_upd_support)
            else: 
                disponibility_upd_support = "Disponible"
            state_update_support, msj_update_support = bd.actualizar(f"UPDATE miembro SET nombre='{name_upd_support}', telefono='{phone_upd_support}', email='{email_upd_support}', direccion='{address_upd_support}', disponibilidad='{disponibility_upd_support}', estatus='{status_upd_support}', notas='{comments_upd_support}' WHERE idMiembro = '{id_support_selected}';")
            if state_update_support == 1:
                    st.success("Miembro Actualizado")
                    st.info(f"{name_upd_support} -- {phone_upd_support} -- {email_upd_support} -- {address_upd_support} -- {comments_upd_support}")
            else:
                st.error("Miembro No Actualizado")
                st.info(msj_update_support)
            
        # Para que se limpien los mensajes
        time.sleep(3)
        message_container.empty()
        st.rerun()


with tab_del_support:
    st.warning("Si eliminamos un miembro, se eliminará de igual manera sus peticiones")
    supports_avaliable = bd.consultar("SELECT * FROM miembro")
    if supports_avaliable is not None:
        combined_supports = [f"#{row['idMiembro']} - {row['nombre']}" for index, row in supports_avaliable.iterrows()]
        support_selected = st.selectbox("Selecciona un Miembro", combined_supports)
        id_support_selected = int(support_selected.split(' - ')[0][1:])
        support_data = supports_avaliable[supports_avaliable['idMiembro'] == id_support_selected]

        # Hagamos la notifiación de que no se puede eliminar si tiene actividades abiertas
        support_with_activities = bd.consultar(f"SELECT a.idMiembro, count(*) as act_abiertas FROM actividad a INNER JOIN miembro m ON a.idMiembro=m.idMiembro WHERE a.idMiembro={id_support_selected} GROUP BY a.idMiembro;")

        with st.container(border = True):
            st.markdown(f"## 👤 {support_data["nombre"].iloc[0]}")
            st.markdown(f"☎️ Telefono: {support_data["telefono"].iloc[0]}")
            st.markdown(f"📧 Email: {support_data["email"].iloc[0]}")
            st.markdown(f"🔤 Direccion: {support_data["direccion"].iloc[0]}")
        
        with st.container():
            with st.popover(f"Eliminar", use_container_width=True):
                st.write(f"¿Seguro que quieres eliminar a {support_data["nombre"].iloc[0]}?")
                if st.button("Si. Estoy Seguro"):
                    if support_with_activities.empty:
                        state_del, ms_del= bd.eliminar(f"DELETE FROM miembro WHERE idMiembro='{id_support_selected}'")
                        state_del_reques, ms_del_request= bd.eliminar(f"DELETE FROM peticion_nuevo_recurso WHERE idMiembro='{id_support_selected}'")
                        st.success("Miembro Eliminado")
                        time.sleep(3)
                        message_container.empty()
                        st.rerun()
                    else: 
                        st.error("Miembro No Eliminado")
                        st.info(f"El miembro: #{support_data['idMiembro'].iloc[0]} - {support_data['nombre'].iloc[0]} tiene asociadas actividades.")
                        st.info("Primero intenta cerrar las actividades")
                        time.sleep(3)
                        message_container.empty()
                        st.rerun()
    else:
        st.warning("No hay datos para mostrar...")