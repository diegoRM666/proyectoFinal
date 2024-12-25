import streamlit as st
import pandas as pd
import time
from menu import menu_with_redirect
import logic.bd as bd


# Mandamos a llamara a menu con redirección
menu_with_redirect()

# v----------------- Apartir de aquí tenemos la visualización de la página
st.markdown("# 🏢 Clientes")

# Hacemos las tabs para cada uno de las operaciones que se puede realizar. Donde no se tenga el rol necesario, mostrará un mensaje.
tab_lst_client, tab_ins_client, tab_upd_client, tab_del_client = st.tabs(["Listar Clientes","Agregar Cliente", "Actualizar Cliente", "Eliminar Cliente"])


#################################################### LISTADO ######################################################

with tab_lst_client:
    col1, col2 = st.columns([95,1])
    with col2: 
        if st.button("🔄", key="ref_resources"):
            st.rerun()
    if any(role in ["admin", "user"] for role in st.session_state["roles"]):
        clientes = bd.consultar_todos_clientes()
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
                        st.markdown(f"## 🏢 #{cliente['idCliente']} - {cliente['nombre']}")
                        st.markdown(f"☎️ {cliente['telefono']}")
                        st.markdown(f"📧 {cliente['email']}")
                        st.markdown(f"🔤 {cliente['direccion']}")
                        if cliente['notas'] != "":
                            st.markdown(f"🗒️ {cliente['notas']}")
                
                # Actualizar el índice para alternar entre las columnas
                index += 1

        else:
            st.warning("No existen clientes para mostrar")

###################################################################################################################



#################################################### INSERCIÓN ####################################################
with tab_ins_client: 
    # Validamos el rol para ver si puede realizar inserciones o no:
    if any(role in ["admin", "user"] for role in st.session_state["roles"]):
        # Hacemos un formulario para la inserción del cliente
        with st.form("insert_client", clear_on_submit= True):
            name_ins_client = st.text_input("Nombre*: ", placeholder="Inbursa")
            phone_ins_client = st.text_input("Telefono de Contacto*: ", placeholder="5530104575")
            email_ins_client = st.text_input("email*: ", placeholder="inbursa@test.com")
            address_ins_client = st.text_input("Dirección*: ", placeholder="Calle Siempre Viva 62 Col. El Temazcal")
            comments_ins_client = st.text_area("Notas Adicionales: ", placeholder="Agrega tus comentarios")
            st.write("*Campos Obligatorios")
            submit_insert_client = st.form_submit_button("Agregar")
        
        # Este message container nos ayudará a que podamos limpiar los mensajes que se despliegan en caso de exito o no. 
        message_container = st.empty()

        # Acciones en el momento que hagamos el submit.
        if submit_insert_client:
            if not name_ins_client.strip() or not phone_ins_client.strip() or not email_ins_client.strip() or not address_ins_client.strip():
                st.error("Cliente No Agregado")
                st.info("Llene todos los campos obligatorios")
            else:
                # Verifica si un cliente existe en la tabla, si no existe lo inserta.
                state_ins_client, msj_ins_client = bd.insertar_cliente(name_ins_client, phone_ins_client, email_ins_client, address_ins_client, comments_ins_client)

                if state_ins_client:
                    st.success(msj_ins_client)
                    st.info(f"{name_ins_client} -- {phone_ins_client} -- {email_ins_client} -- {address_ins_client}")
                else:
                    st.warning(msj_ins_client)

            time.sleep(3)
            message_container.empty()
            st.rerun()
    else: 
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")

###################################################################################################################




#################################################### ACTUALIZACIÓN ####################################################

with tab_upd_client:
    # Validamos el rol para ver si puede realizar inserciones o no:
    if any(role in ["admin"] for role in st.session_state["roles"]):
        # Obtenemos todos lo clientes disponibles
        clients_avaliable = bd.consultar_todos_clientes()

        # Verificamos que no este vacio
        if clients_avaliable is not None and not clients_avaliable.empty:
            # Este proceso es justamente para obtener el id del cliente
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
                if not name_upd_client.strip() or not phone_upd_client.strip() or not email_upd_client.strip() or not address_upd_client.strip():
                    st.error("Cliente No Actualizado")
                    st.info("Llene todos los campos obligatorios")
                else:
                    state_update, msj_update = bd.actualizar_cliente(name_upd_client, phone_upd_client, email_upd_client, address_upd_client, comments_upd_client, id_client_selected)
                    if state_update:
                        st.success("Cliente Actualizado")
                        st.info(f"{name_upd_client} -- {phone_upd_client} -- {email_upd_client} -- {address_upd_client} -- {comments_upd_client}")
                    else:
                        st.error("Cliente No Actualizado")
                        st.info(msj_update)
                # Para que se limpien los mensajes
                time.sleep(3)
                message_container.empty()
                st.rerun()

        else:
            st.warning("No existen clientes para modificar")
    else:
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")

#######################################################################################################################



#################################################### ELIMINACIÓN ####################################################

with tab_del_client:
    # Validamos el rol para ver si puede realizar inserciones o no:
    if any(role in ["admin"] for role in st.session_state["roles"]):
        clients_avaliable = bd.consultar_todos_clientes()
        if clients_avaliable is not None and not clients_avaliable.empty:
            combined_clients = [f"#{row['idCliente']} - {row['nombre']}" for index, row in clients_avaliable.iterrows()]
            client_selected = st.selectbox("Selecciona un Cliente", combined_clients)
            id_client_selected = int(client_selected.split(' - ')[0][1:])
            client_data = clients_avaliable[clients_avaliable['idCliente'] == id_client_selected]

            with st.container(border = True):
                st.markdown(f"## 🏢 {client_data["nombre"].iloc[0]}")
                st.markdown(f"☎️ Telefono: {client_data["telefono"].iloc[0]}")
                st.markdown(f"📧 Email: {client_data["email"].iloc[0]}")
                st.markdown(f"🔤 Direccion: {client_data["direccion"].iloc[0]}")
            
            with st.container():
                with st.popover(f"Eliminar", use_container_width=True):
                    st.write(f"¿Seguro que quieres eliminar a {client_data["nombre"].iloc[0]}?")
                    if st.button("Si. Estoy Seguro"):
                        state_del_client, msj_del_client = bd.eliminar_cliente(id_client_selected)
                        if state_del_client:
                            st.success(msj_del_client)
                        else: 
                            st.error(msj_del_client)
                            st.info(f"El cliente: #{client_data['idCliente'].iloc[0]} - {client_data['nombre'].iloc[0]} tiene asociadas actividades.")
                            st.info("Primero intenta cerrar las actividades")
                        time.sleep(3)
                        message_container.empty()
                        st.rerun()
        else:
            st.warning("No hay datos para mostrar...")

    else: 
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")