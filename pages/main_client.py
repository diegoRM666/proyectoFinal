import streamlit as st
import pandas as pd
import time
from menu import menu_with_redirect
import logic.bd as bd


# Comprueba que el usuario este loggeado.
menu_with_redirect()

# Titutlo en header 1 de la pagina
st.markdown("# 🏢 Clientes")

# Hacemos las pestañas para cada uno de las operaciones que se puede realizar. Donde no se tenga el rol necesario, mostrará un mensaje.
tab_lst_client, tab_ins_client, tab_upd_client, tab_del_client = st.tabs(["Listar Clientes","Agregar Cliente", "Actualizar Cliente", "Eliminar Cliente"])

# Pestaña de listado
with tab_lst_client:
    # Crea columnas que dan formato a los objetos
    col1, col2 = st.columns([95,1])
    with col2: 
        # Botón para refrescar la información
        if st.button("🔄", key="ref_resources"):
            st.rerun()

    # Validación del rol de la sesion, en este caso aplica para ambos roles
    if any(role in ["admin", "user"] for role in st.session_state["roles"]):
        # Consulta todos los clientes
        clientes = bd.consultar_todos_clientes()
        
        # Valida que el resultado no sea vacio
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
        
        # Mensaje en caso de no haber clientes
        else:
            st.warning("No existen clientes para mostrar")
            
# Pestaña para agregar un nuevo cliente
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
            # Botón de envio de información
            submit_insert_client = st.form_submit_button("Agregar")
        
        # Este message container nos ayudará a que podamos limpiar los mensajes que se despliegan en caso de exito o no. 
        message_container = st.empty()

        # Acciones en el momento que hagamos el submit.
        if submit_insert_client:
            # Validación de campos obligatorios llenos
            if not name_ins_client.strip() or not phone_ins_client.strip() or not email_ins_client.strip() or not address_ins_client.strip():
                # Despliega un mensaje en caso de que algo no este lleno.
                st.error("Cliente No Agregado")
                st.info("Llene todos los campos obligatorios")
            else:
                # Verifica si un cliente existe en la tabla, si no existe lo inserta, la verificacion la realiza mediante el nombre del cliente.
                state_ins_client, msj_ins_client = bd.insertar_cliente(name_ins_client, phone_ins_client, email_ins_client, address_ins_client, comments_ins_client)
                
                # Valida si la insercion fue correcta 
                if state_ins_client:
                    # Mensaje de exito, junto con la informacion del cliente insertado
                    st.success(msj_ins_client)
                    st.info(f"{name_ins_client} -- {phone_ins_client} -- {email_ins_client} -- {address_ins_client}")
                else:
                    # En caso de no lograr insertalo, se despliega el mensaje que nos dice porque razón no lo inserto
                    # Puede ser porque ya existe o hay un problema con la base de datos
                    st.warning(msj_ins_client)

            # Limpieza de mensajes
            time.sleep(3)
            message_container.empty()
            st.rerun()
    
    # En caso de no tener el rol user o admin.
    else: 
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")

# Pestaña para actualizar un cliente
with tab_upd_client:
    # Validamos el rol para ver si puede realizar inserciones o no, en este caso, solo lo puede hacer admin
    if any(role in ["admin"] for role in st.session_state["roles"]):
        # Obtenemos todos lo clientes disponibles
        clients_avaliable = bd.consultar_todos_clientes()

        # Verificamos que no este vacio el resultado
        if clients_avaliable is not None and not clients_avaliable.empty:
            # Se combinan las columnas de identiicador y nombre del cliente.
            combined_clients = [f"#{row['idCliente']} - {row['nombre']}" for index, row in clients_avaliable.iterrows()]
            # Desplegamos el objeto que nos permite seleccionar un cliente
            client_selected = st.selectbox("Selecciona un Cliente", combined_clients, key="update_cliente_sb")
            # Obtenemos el identificador del cliente seleccionado
            id_client_selected = int(client_selected.split(' - ')[0][1:])
            # Se obtiene la data del cliente seleccionad, tomando como referencia el identificador.
            client_data = clients_avaliable[clients_avaliable['idCliente'] == id_client_selected]

            # Renderizamos un formulario para la actualización
            with st.form("update_client", clear_on_submit= True):
                # Se le dan por default los valores actuales.
                name_upd_client = st.text_input("Nombre*: ", value=f"{client_data['nombre'].iloc[0]}", key="name_ins_client")
                phone_upd_client = st.text_input("Telefono de Contacto*: ", value=f"{client_data['telefono'].iloc[0]}")
                email_upd_client = st.text_input("email*: ", value=f"{client_data['email'].iloc[0]}")
                address_upd_client = st.text_input("Dirección*: ", value=f"{client_data['direccion'].iloc[0]}")
                comments_upd_client = st.text_area("Notas Adicionales: ", value=f"{client_data['notas'].iloc[0]}")
                st.write("*Campos Obligatorios")
                # Boton de envio
                submit_upd_client = st.form_submit_button("Actualizar")
            
            # Contenedor de los mensajes que se generaran
            message_container = st.empty()

            # Acciones a realizar al enviar la información
            if submit_upd_client:
                # Verifica que los campos obligatorios esten llenos
                if not name_upd_client.strip() or not phone_upd_client.strip() or not email_upd_client.strip() or not address_upd_client.strip():
                    # Notifica en caso de que no se haya llenado algun campo
                    st.error("Cliente No Actualizado")
                    st.info("Llene todos los campos obligatorios")
                else:
                    # Funcion que actualiza el cliente
                    state_update, msj_update = bd.actualizar_cliente(name_upd_client, phone_upd_client, email_upd_client, address_upd_client, comments_upd_client, id_client_selected)
                    # En caso de que la actualización sea correcta 
                    if state_update:
                        # Informa al cliente de la corecta insercion y presenta los datos del cliente insertado
                        st.success("Cliente Actualizado")
                        st.info(f"{name_upd_client} -- {phone_upd_client} -- {email_upd_client} -- {address_upd_client} -- {comments_upd_client}")
                    else:
                        # En caso de que no sea correcta, muestra la razon por la cual no se inserto.
                        st.error("Cliente No Actualizado")
                        st.info(msj_update)
                # Limpieza de mensajes
                time.sleep(3)
                message_container.empty()
                st.rerun()
        
        # Si el resultado de la consulta es vacio
        else:
            st.warning("No existen clientes para modificar")
    # Si el usuario tiene el rol de user, le notificara que no puede actualizar clientes
    else:
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")

# Pestaña para eliminar un cliente
with tab_del_client:
    # Validamos el rol, solo el rol admin puede eliminar clientes.
    if any(role in ["admin"] for role in st.session_state["roles"]):
        # Se realiza la misma consulta que recupera todos los clientes
        clients_avaliable = bd.consultar_todos_clientes()
        
        # Validamos si el resultado es no vacio 
        if clients_avaliable is not None and not clients_avaliable.empty:
            # Combinación de columnas de identificador y nombre del cliente
            combined_clients = [f"#{row['idCliente']} - {row['nombre']}" for index, row in clients_avaliable.iterrows()]
            # Renderiza el selector de clientes y recupera el cliente seleccionado
            client_selected = st.selectbox("Selecciona un Cliente", combined_clients)
            # Obtención del identificador del cliente seleccionado
            id_client_selected = int(client_selected.split(' - ')[0][1:])
            # Recuperacion de los datos del cliente seleccionado
            client_data = clients_avaliable[clients_avaliable['idCliente'] == id_client_selected]

            # Renderiza un contenedor para mostrar la informacion del cliente a eliminar
            with st.container(border = True):
                st.markdown(f"## 🏢 {client_data["nombre"].iloc[0]}")
                st.markdown(f"☎️ Telefono: {client_data["telefono"].iloc[0]}")
                st.markdown(f"📧 Email: {client_data["email"].iloc[0]}")
                st.markdown(f"🔤 Direccion: {client_data["direccion"].iloc[0]}")
            
            # Renderiza un contenedor para el botón de eliminar
            with st.container():
                # Doble confirmacion para eliminar un cliente
                with st.popover(f"Eliminar", use_container_width=True):
                    # Informa que si se quiere eliminar el cliente que seleccionamos
                    st.write(f"¿Seguro que quieres eliminar a {client_data["nombre"].iloc[0]}?")
                    # Renderiza el botón y recupera la accion de presionarlo
                    if st.button("Si. Estoy Seguro"):
                        # Funcion que elimina el cliente, tomando su id como parametro
                        state_del_client, msj_del_client = bd.eliminar_cliente(id_client_selected)
                        # Si la eliminacion fue correcta
                        if state_del_client:
                            st.success(msj_del_client)
                        # En caso de no eliminar el cliente
                        else: 
                            # Este mensaje nos dice que no se elimino el cliente porque tiene asociadas actividades
                            st.error(msj_del_client)
                            st.info(f"El cliente: #{client_data['idCliente'].iloc[0]} - {client_data['nombre'].iloc[0]} tiene asociadas actividades.")
                            st.info("Primero intenta cerrar las actividades")
                        # Limpieza de mensajes
                        time.sleep(3)
                        message_container.empty()
                        st.rerun()
        # Nos informa que no existen clientes
        else:
            st.warning("No hay datos para mostrar")
    # Nos informa que el usuario con rol user no puede eliminar clientes
    else: 
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")