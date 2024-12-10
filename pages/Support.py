import streamlit as st
import pandas as pd
import time
from menu import menu_with_redirect



# Primero hacemos las comprobacion
menu_with_redirect()

#Creamos un titulo
st.markdown("# ")

# Mostrar las disintas actividades a realizar
tab_lst_support, tab_ins_support, tab_upd_support, tab_del_support = \
      st.tabs(["Listar Soporte","Agregar Soporte", "Actualizar Soporte", "Eliminar Soporte"])

# with tab_lst_support: 
with tab_ins_support: 
    with st.form("insert_support", clear_on_submit= True):
        name_ins_support = st.text_input("Nombre*: ", placeholder="Juan Montes")
        phone_ins_support = st.text_input("Telefono de Contacto*: ", placeholder="5530104575")
        email_ins_support = st.text_input("email*: ", placeholder="juanmontes@test.com")
        address_ins_support = st.text_input("Dirección*: ", placeholder="Calle Siempre Viva 62 Col. El Temazcal")
        comments_ins_support = st.text_area("Notas Adicionales: ", placeholder="Agrega tus comentarios")
        st.write("*Campos Obligatorios")
        submit_insert_support = st.form_submit_button("Agregar")
        

    message_container = st.empty()

    if submit_insert_support:
        if not name_ins_support.strip() or not phone_ins_support.strip() or not email_ins_support.strip()\
        or not address_ins_support.strip():
            st.error("Miembro de Soporte No Agregado")
            st.info("Llene todos los campos obligatorios")
        else:
            # aqui va la llamda al metodo de insercion
            st.success("Miembro de Soporte Agregado")
            st.info(f"{name_ins_support} -- {phone_ins_support} -- {email_ins_support} -- {address_ins_support}")
            
        # Para que se limpien los mensajes
        time.sleep(3)
        message_container.empty()
        st.rerun()

with tab_upd_support:
    #Los miembros de soporte que tenemos 
    #supports_avalidable = consulta
    #support_selected = selectbox() 
    with st.form("update_support", clear_on_submit= True):
        name_upd_support = st.text_input("Nombre*: ", value="Juan Montes", key="name_ins_support")
        phone_upd_support = st.text_input("Telefono de Contacto*: ", value="5530104575")
        email_upd_support = st.text_input("email*: ", value="juanmontes@test.com")
        address_upd_support = st.text_input("Dirección*: ", value="Calle Siempre Viva 62 Col. El Temazcal")
        comments_upd_support = st.text_area("Notas Adicionales: ", value="Agrega tus comentarios")
        st.write("*Campos Obligatorios")
        submit_upd_support = st.form_submit_button("Agregar")
        

    message_container = st.empty()

    if submit_upd_support:
        if not name_upd_support.strip() or not phone_upd_support.strip() or not email_upd_support.strip()\
        or not address_upd_support.strip():
            st.error("Miembro de Soporte Actualizado")
            st.info("Llene todos los campos obligatorios")
        else:
            # aqui va la llamda al metodo
            st.success("Miemrbo de Soporte Actualizado")
            st.info(f"{name_upd_support} -- {phone_upd_support} -- {email_upd_support} -- {address_upd_support} -- {comments_upd_support}")
            
        # Para que se limpien los mensajes
        time.sleep(3)
        message_container.empty()
        st.rerun()

    # Esta parte es para generar la actualización del soporte.
    st.write("---")
    st.write("### Estatus del Miembro")
    status_upd_support = st.selectbox("Elige un Estatus", ["Disponible", "De Vacaciones", "Incapacidad"])
    
    if st.button("Cambiar"):
        st.success("Estatus de Miembro Actualizado")
        st.info(f"➡️ {status_upd_support}")
        time.sleep(3)
        message_container.empty()
        st.rerun()


