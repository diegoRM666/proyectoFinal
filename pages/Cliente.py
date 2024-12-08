import streamlit as st
import pandas as pd
import time


# Mostrar las disintas actividades a realizar
tab_lst_client, tab_ins_client, tab_upd_client, tab_del_client = \
      st.tabs(["Listar Clientes","Agregar Cliente", "Actualizar Cliente", "Eliminar Cliente"])

# with tab_lst_client: 
with tab_ins_client: 
    with st.form("insert_client", clear_on_submit= True):
        name_ins_client = st.text_input("Nombre*: ", placeholder="Inbursa")
        phone_ins_client = st.text_input("Telefono de Contacto*: ", placeholder="5530104575")
        email_ins_client = st.text_input("email*: ", placeholder="inbursa@test.com")
        address_ins_client = st.text_input("Dirección*: ", placeholder="Calle Siempre Viva 62 Col. El Temazcal")
        comments_ins_client = st.text_area("Notas Adicionales: ", placeholder="Agrega tus comentarios")
        st.write("*Campos Obligatorios")
        submit_insert_client = st.form_submit_button("Agregar")
        

    message_container = st.empty()

    if submit_insert_client:
        if not name_ins_client.strip() or not phone_ins_client.strip() or not email_ins_client.strip()\
        or not address_ins_client.strip():
            st.error("Cliente no agregado")
            st.info("Llene todos los campos obligatorios")
        else:
            # aqui va la llamda al metodo de insercion
            st.success("Cliente Agregado")
            st.info(f"{name_ins_client} -- {phone_ins_client} -- {email_ins_client} -- {address_ins_client}")
            
        # Para que se limpien los mensajes
        time.sleep(3)
        message_container.empty()
        st.rerun()

with tab_upd_client:
    #Los clientes que tenemos 
    #clients_avalidable = consulta
    #client_selected = selectbox() 
    with st.form("update_client", clear_on_submit= True):
        name_upd_client = st.text_input("Nombre*: ", value="Inbursa", key="name_ins_client")
        phone_upd_client = st.text_input("Telefono de Contacto*: ", value="5530104575")
        email_upd_client = st.text_input("email*: ", value="inbursa@test.com")
        address_upd_client = st.text_input("Dirección*: ", value="Calle Siempre Viva 62 Col. El Temazcal")
        comments_upd_client = st.text_area("Notas Adicionales: ", value="Agrega tus comentarios")
        st.write("*Campos Obligatorios")
        submit_upd_client = st.form_submit_button("Agregar")
        

    message_container = st.empty()

    if submit_upd_client:
        if not name_upd_client.strip() or not phone_upd_client.strip() or not email_upd_client.strip()\
        or not address_upd_client.strip():
            st.error("Cliente Actualizado")
            st.info("Llene todos los campos obligatorios")
        else:
            # aqui va la llamda al metodo
            st.success("Cliente Actualizado")
            st.info(f"{name_upd_client} -- {phone_upd_client} -- {email_upd_client} -- {address_upd_client} -- {comments_upd_client}")
            
        # Para que se limpien los mensajes
        time.sleep(3)
        message_container.empty()
        st.rerun()