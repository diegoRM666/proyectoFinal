import streamlit as st
import pandas as pd
import time
from menu import menu_with_redirect
import logic.bd as bd



# Primero hacemos las comprobacion
menu_with_redirect()

#Creamos un titulo
st.markdown("# 🔧 Recursos")

# Mostrar las disintas actividades a realizar
tab_lst_resource, tab_ins_resource, tab_upd_resource, tab_del_resource = \
      st.tabs(["Listar Recursos","Agregar Recurso", "Actualizar Recurso", "Eliminar Recurso"])


with tab_lst_resource:
    resources = bd.consultar("SELECT nombre, tipo, descripcion, categoria, no_serie, estado_recurso, vida_util, notas FROM recurso;")

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
                    st.markdown(f"## 👤 {resource['nombre']}")
                    st.markdown(f"☎️ {resource['tipo']}")
                    st.markdown(f"📧 {resource['descripcion']}")
                    st.markdown(f"🔤 {resource['categoria']}")
                    st.markdown(f"🔤 {resource['no_serie']}")
                    st.markdown(f"🔤 {resource['vida_util']}")
                    if resource['estado_recurso'] == "En Stock":
                        st.markdown(f'''### :green[{resource['estado_recurso']}]''')
                    else:
                        st.markdown(f'''### :orange[{resource['estado_recurso']}]''')
                    if resource['notas'] !="":
                        st.markdown(f"🗒️ {resource['notas']}")
                    
            
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
        state_ins_resource = st.selectbox("Estado", ["En Uso", "En Stock"])
        comments_ins_resource = st.text_area("Notas Adicionales: ", placeholder="Agrega tus comentarios")
        
        # Indicador de campos obligatorios
        st.markdown("*Campos Obligatorios")
        
        # Botón de envío
        submit_insert_resource = st.form_submit_button("Agregar")

        message_container = st.empty()

        if submit_insert_resource:
            if not name_ins_resource.strip() or not phone_ins_resource.strip() or not email_ins_resource.strip()\
            or not address_ins_resource.strip():
                st.error("Miembro de Soporte No Agregado")
                st.info("Llene todos los campos obligatorios")
            else:
                if status_ins_resource in ["Vacaciones", "En Actividad", "Incapacidad"]:
                    disponibility_ins_resource = "No Disponible"
                else: 
                    disponibility_ins_resource = "Disponible"
                query_insert_resource = f"INSERT INTO miembro (nombre, telefono, email, direccion, disponibilidad, estatus, notas) VALUES ('{name_ins_resource}', '{phone_ins_resource}', '{email_ins_resource}', '{address_ins_resource}', '{disponibility_ins_resource}', '{status_ins_resource}', '{comments_ins_resource}');"
                bd.insertar(query_insert_resource)
                st.success("Miembro de Soporte Agregado")
                st.info(f"{name_ins_resource} -- {phone_ins_resource} -- {email_ins_resource} -- {address_ins_resource}")
                
            # Para que se limpien los mensajes
            time.sleep(3)
            message_container.empty()
            st.rerun()

with tab_upd_resource:
    resources_available = bd.consultar("SELECT * FROM miembro;")
    
    if resources_available is not None:
        combined_resources = [f"#{row['idMiembro']} - {row['nombre']}" for index, row in resources_available.iterrows()]
        resource_selected = st.selectbox("Selecciona un Miembro", combined_resources, key="update_resources_sb")
        id_resource_selected = int (resource_selected.split(' - ')[0][1:])
        resource_data = resources_available[resources_available['idMiembro']==id_resource_selected]
        
        #Necesitamos ademas saber el index del estatus
        status_dict = {
            "Libre": 0,
            "Vacaciones": 1,
            "En Actividad": 2,
            "Incapacidad": 3
        }

        index_status = status_dict[resource_data['estatus'].iloc[0]]


        with st.form("update_resource", clear_on_submit= True):
            name_upd_resource = st.text_input("Nombre*: ", value=f"{resource_data['nombre'].iloc[0]}", key="name_ins_resource")
            phone_upd_resource = st.text_input("Telefono de Contacto*: ", value=f"{resource_data['telefono'].iloc[0]}")
            email_upd_resource = st.text_input("email*: ", value=f"{resource_data['email'].iloc[0]}")
            address_upd_resource = st.text_input("Dirección*: ", value=f"{resource_data['direccion'].iloc[0]}")
            status_upd_resource = st.selectbox("Estatus", ["Libre","Vacaciones", "En Actividad", "Incapacidad"], index=index_status)
            comments_upd_resource = st.text_area("Notas Adicionales: ", value=f"{resource_data['notas'].iloc[0]}")
            st.write("*Campos Obligatorios")
            submit_upd_resource = st.form_submit_button("Actualizar")
        
        

    message_container = st.empty()

    if submit_upd_resource:
        if not name_upd_resource.strip() or not phone_upd_resource.strip() or not email_upd_resource.strip()\
        or not address_upd_resource.strip():
            st.error("Miembro de Soporte Actualizado")
            st.info("Llene todos los campos obligatorios")
        else:
            if status_upd_resource in ["Vacaciones", "Baja", "En Actividad", "Incapacidad"]:
                    disponibility_upd_resource = "No Disponible"
                    print(disponibility_upd_resource)
            else: 
                disponibility_upd_resource = "Disponible"
            state_update_resource, msj_update_resource = bd.actualizar(f"UPDATE miembro SET nombre='{name_upd_resource}', telefono='{phone_upd_resource}', email='{email_upd_resource}', direccion='{address_upd_resource}', disponibilidad='{disponibility_upd_resource}', estatus='{status_upd_resource}', notas='{comments_upd_resource}' WHERE idMiembro = '{id_resource_selected}';")
            if state_update_resource == 1:
                    st.success("Miembro Actualizado")
                    st.info(f"{name_upd_resource} -- {phone_upd_resource} -- {email_upd_resource} -- {address_upd_resource} -- {comments_upd_resource}")
            else:
                st.error("Miembro No Actualizado")
                st.info(msj_update_resource)
            
        # Para que se limpien los mensajes
        time.sleep(3)
        message_container.empty()
        st.rerun()
