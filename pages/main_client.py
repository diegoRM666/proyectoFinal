import streamlit as st
import pandas as pd
import time
from menu import menu_with_redirect
import logic.bd as bd




#Mandamos a llamara a menu con redirección
menu_with_redirect()


st.markdown("# 🏢 Clientes")


# Mostrar las disintas actividades a realizar
tab_lst_client, tab_ins_client, tab_upd_client, tab_del_client = \
      st.tabs(["Listar Clientes","Agregar Cliente", "Actualizar Cliente", "Eliminar Cliente"])
with tab_lst_client:
    clientes = bd.consultar("SELECT nombre, telefono, email, direccion, notas FROM cliente;")

    if clientes is not None and not clientes.empty:

        # Definir el número de columnas
        num_cols = 2
        cols = st.columns(num_cols)
        
        # Inicializar el índice para repartir a las columnas
        index = 0

        # Iterar sobre los clientes en el DataFrame
        for _, cliente in clientes.iterrows():
            col = cols[index % num_cols]  # Alterna entre las columnas (0 y 1)
            
            # Mostrar la información del cliente en la columna correspondiente
            with col:
                with st.container(border=True):
                    st.markdown(f"## 🏢 {cliente['nombre']}")
                    st.markdown(f"☎️ {cliente['telefono']}")
                    st.markdown(f"📧 {cliente['email']}")
                    st.markdown(f"🔤 {cliente['direccion']}")
                    st.markdown(f"🗒️ {cliente['notas']}")
            
            # Actualizar el índice para alternar entre las columnas
            index += 1

    else:
        st.warning("No existen datos")


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
            if not bd.consultar_nombre_insensible(name_ins_client):
                query = f"INSERT INTO cliente (nombre, telefono, email, direccion, notas) VALUES ('{name_ins_client}', '{phone_ins_client}', '{email_ins_client}', '{address_ins_client}', '{comments_ins_client}');"
                bd.insertar(query)
                st.success("Cliente Agregado")
                st.info(f"{name_ins_client} -- {phone_ins_client} -- {email_ins_client} -- {address_ins_client}")
            else: 
                st.error("Cliente no agregado")
                st.info("El Cliente ya existe. Revise la Lista")
        # Para que se limpien los mensajes
        time.sleep(3)
        message_container.empty()
        st.rerun()

with tab_upd_client:
    clients_avaliable = bd.consultar("SELECT * FROM cliente;")

    if clients_avaliable is not None:
        combined_clients = [f"#{row['idCliente']} - {row['nombre']}" for index, row in clients_avaliable.iterrows()]
        client_selected = st.selectbox("Selecciona un Cliente", combined_clients, key="update_cliente_sb")
        id_client_selected = int(client_selected.split(' - ')[0][1:])
        client_data = clients_avaliable[clients_avaliable['idCliente'] == id_client_selected]

        with st.form("update_client", clear_on_submit= True):
            name_upd_client = st.text_input("Nombre*: ", value=f"{client_data['nombre'].iloc[0]}", key="name_ins_client")
            phone_upd_client = st.text_input("Telefono de Contacto*: ", value=f"{client_data['telefono'].iloc[0]}")
            email_upd_client = st.text_input("email*: ", value=f"{client_data['email'].iloc[0]}")
            address_upd_client = st.text_input("Dirección*: ", value=f"{client_data['direccion'].iloc[0]}")
            comments_upd_client = st.text_area("Notas Adicionales: ", value=f"{client_data['notas'].iloc[0]}")
            st.write("*Campos Obligatorios")
            submit_upd_client = st.form_submit_button("Actualizar")
        

        message_container = st.empty()

        if submit_upd_client:
            if not name_upd_client.strip() or not phone_upd_client.strip() or not email_upd_client.strip()\
            or not address_upd_client.strip():
                st.error("Cliente No Actualizado")
                st.info("Llene todos los campos obligatorios")
            else:
                state_update, msj_update = bd.actualizar(f"UPDATE cliente SET nombre = '{name_upd_client}', telefono = '{phone_upd_client}', email = '{email_upd_client}', direccion = '{address_upd_client}', notas = '{comments_upd_client}' WHERE idCliente = '{id_client_selected}';")
                if state_update == 1:
                    st.success("Cliente Actualizado")
                    st.info(f"{name_upd_client} -- {phone_upd_client} -- {email_upd_client} -- {address_upd_client} -- {comments_upd_client}")
                else:
                    st.error("Cliente No Actualizado")
                    st.info(msj_update)
            # Para que se limpien los mensajes
            time.sleep(3)
            message_container.empty()
            st.rerun()
with tab_del_client:
    if clients_avaliable is not None:
        combined_clients = [f"#{row['idCliente']} - {row['nombre']}" for index, row in clients_avaliable.iterrows()]
        client_selected = st.selectbox("Selecciona un Cliente", combined_clients)
        id_client_selected = int(client_selected.split(' - ')[0][1:])
        client_data = clients_avaliable[clients_avaliable['idCliente'] == id_client_selected]

        with st.container(border = True):
            st.markdown(f"## 🏢 {client_data["nombre"].iloc[0]}")
            st.markdown(f"☎️ Telefono: {client_data["telefono"].iloc[0]}")
            st.markdown(f"📧 Email: {client_data["email"].iloc[0]}")
            st.markdown(f"🔤 Direccion: {client_data["direccion"].iloc[0]}")
        
        with st.popover(f"Eliminar"):
            st.write(f"¿Seguro que quieres eliminar a {client_data["nombre"].iloc[0]}?")
            if st.button("Si. Estoy Seguro"):
                #state_del, ms_del= bd.eliminar(f"DELETE FROM cliente WHERE idCliente='{id_client_selected}'")
                st.success("Cliente Eliminado")
    else:
        st.warning("No hay datos para mostrar...")