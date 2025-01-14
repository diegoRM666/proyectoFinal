import streamlit as st
import pandas as pd
import time
from menu import menu_with_redirect
import logic.bd as bd
import logic.utilities as ut
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px


# Comprueba que el usuario este loggeado.
menu_with_redirect()

#Creamos un titulo
st.markdown("# 💵 Facturas")

# Mostrar las disintas actividades a realizar, genera pestañas
tab_lst_bill, tab_ins_bill, tab_upd_bill, tab_del_bill, tab_metric_bill= st.tabs(["Listar Facturas","Agregar Factura", "Actualizar Factura", "Cerrar Factura", "Ver Métricas"])

# Pestaña de para Lista Facturas
with tab_lst_bill:
    #Creación de columnas para localizar el botón
    col1, col2 = st.columns([95,1])
    with col2: 
        # Botón para refrescar la información
        if st.button("🔄", key="ref_resources"):
            st.rerun()

    # Validación del rol
    if any(role in ["admin", "user"] for role in st.session_state["roles"]):
        # Distintos resultados para distintos roles
        if any(role in ["admin"] for role in st.session_state["roles"]):
            # Consulta si es admin
            bills = bd.consultar_facturas(0,0)
        else: 
            # Consulta si es user, mandando el email para identificar al usuario.
            bills = bd.consultar_facturas(1,st.session_state['email'])
    
        if bills is not None and not bills.empty:
            # Definir el número de columnas
            num_cols = 2
            cols = st.columns(num_cols)

            # Inicializar el índice para repartir a las columnas
            index = 0

            # Iterar sobre los bills en el DataFrame
            for _, bill in bills.iterrows():
                col = cols[index % num_cols]  # Alterna entre las columnas (0 y 1)
                
                # Mostrar la información del bill en la columna correspondiente
                with col:
                    # Creación de contenedor para que se vea como un recuadro
                    with st.container(border=True):
                        # st.markdown sirve para escribir algo en la página en formato markdown
                        # La consula nos regresa un dataframe, podemos operarlo por columnas y renglones.
                        st.markdown(f"## 💵 #{bill['idFactura']} - {bill['nombre']}")
                        st.markdown(f"📆 Fecha Emision: {bill['fecha_emision']}")
                        st.markdown(f"🪙 Costo: {bill['costo']}")
                        st.markdown(f"📖 Tipo: {bill['tipo']}")
                        st.markdown(f"📈 Impuesto: {bill['impuesto']}")
                        st.markdown(f"👤 Creado Por: {bill['creado_por']}")
                        st.markdown(f"📅 Ultima Modificación: {bill['fecha_modificacion']}")
                        st.markdown(f"👤 Modificado Por: {bill['modificado_por']}")
                        st.write(f"💼 Actividad: #{bill['idA']}-{bill['nombre_a']}")
                        st.write(f"👤 Miembro: #{bill['idM']}-{bill['nombre_m']}")

                        # Verifica el estatus de la factura y le da un color de acuerdo al mismo.
                        if bill['estatus'] == "Abierta":
                            st.markdown(f'''### 🔴 :red[{bill['estatus']}]''')
                        elif bill['estatus'] == "En Proceso":
                            st.markdown(f'''### 🟡 :yellow[{bill['estatus']}]''')
                        else:
                            st.markdown(f'''### 🟢 :green[{bill['estatus']}]''')
                        
                # Actualizar el índice para alternar entre las columnas
                index += 1
        # En caso de que no encontremos datos
        else:
            st.warning("No existen datos")

        # Esta linea genera un divisor (linea) en la página.
        st.markdown("---")
        # Header 3 = '###'
        st.markdown("### Facturas Completadas")

        # Distintos resultados para distintos roles
        if any(role in ["admin"] for role in st.session_state["roles"]):
            # Consulta para admin
            activities_closed = bd.consultar_actividades_listado(1,0)
        else:
            # Consulta para user
            st_tmp, id_support= bd.consultar_id_email(st.session_state['email'])
            if st_tmp:
                # Si encuentra el usuario pide las actividades
                activities_closed = bd.consultar_actividades_listado(3, id_support)
            else: 
                # Si no lo encuentra es None el resultado
                activities_closed=None
        
        # Valida que tenga elementos el dataframe de la consulta
        if activities_closed is not None and not activities_closed.empty:
            # Crea un nuevo dataframe para combinar las columnas
            combined_activities_closed = [f"#{row['idActividad']} - {row['nombre_a']}" for index, row in activities_closed.iterrows()]
            # Genera un selectbox para seleccionar una actividad
            activity_closed = st.selectbox("Actividad: ", combined_activities_closed)
            # El resultado es un texto, hay que separarlo y castearlo en int para utilizar el id.
            id_activity_closed = int (activity_closed.split(' - ')[0][1:])

            # Consultamos el historico de las facturas de acuerdo a la factura seleccionada
            bills_closed =bd.consultar_facturas_hist(id_activity_closed)

            # Se valida que tengamos un resultado
            if bills_closed is not None and not bills_closed.empty:
                
                # Iterar sobre las facturas cerradas en el DataFrame
                for _, bill in bills_closed.iterrows():
                    # El container es para que se almacenen en un recuadro
                    with st.container(border=True):
                        st.markdown(f"## 💵 #{bill['idFactura']} - {bill['nombre']}")
                        st.markdown(f"📆 Fecha Emision: {bill['fecha_emision']}")
                        st.markdown(f"🪙 Costo: {bill['costo']}")
                        st.markdown(f"📖 Tipo: {bill['tipo']}")
                        st.markdown(f"📈 Impuesto: {bill['impuesto']}")
                        st.markdown(f"👤 Creado Por: {bill['creado_por']}")
                        st.markdown(f"📅 Ultima Modificación: {bill['fecha_modificacion']}")
                        st.markdown(f"👤 Modificado Por: {bill['modificado_por']}")
                        st.write(f"💼 Actividad: #{bill['idActividad']}-{bill['nombre_a']}")
                        st.write(f"👤 Miembro: #{bill['idM']}-{bill['nombre_m']}")         
        else:
            # En caso de que no hay datos, lo informa
            st.warning("No existen datos")
    else: 
        # Si no tiene un rol asociado
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")

# Pestaña de Metricas de Facturas
with tab_metric_bill:
    # Valida que el usuario tenga un rol 'admin'
    if any(role in ["admin"] for role in st.session_state["roles"]):
        # Obtiene los dataframes para realizas las metricas de costos por cliente y por actividad
        state_metrics, activities_metrics_bill, client_metrics_bill = bd.obtener_metricas_facturacion()
        
        # Valida que la consulta fuera correcta.
        if state_metrics:

            # Crea una figura del tipo pastel. 
            fig_pie_1 = go.Figure(
                go.Pie(
                    labels = activities_metrics_bill['nombre_a'] + ' #' + activities_metrics_bill['idActividad'].astype(str),
                    values=activities_metrics_bill['total'],
                    hole=0.4,  # Esto crea el efecto de dona
                    textinfo='label',
                    hoverinfo='label+value',
                    showlegend=False,
                    marker=dict(
                        colors=px.colors.sequential.RdBu
                    )
                )
            )

            # Actualiza anotaciones de la gráfica. 
            fig_pie_1.update_layout(title_text="Costo por Actividad",
                                paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo del papel transparente
                                plot_bgcolor='rgba(0, 0, 0, 0)',  # Fondo del gráfico transparente
                                height = 700,
                                width = 700)
            
            # Crea una figura del tipo pastel
            fig_pie_2 = go.Figure(
                go.Pie(
                    labels = client_metrics_bill['nombre_c'] + ' #' + client_metrics_bill['idCliente'].astype(str),
                    values=client_metrics_bill['total'],
                    hole=0.4,  # Esto crea el efecto de dona
                    textinfo='label',
                    hoverinfo='label+value',
                    showlegend=False,
                    marker=dict(
                        colors=px.colors.sequential.RdBu_r
                    )
                )
            )

            # Actualiza las anotaciones de la gráfica
            fig_pie_2.update_layout(title_text="Costo por Cliente",
                                paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo del papel transparente
                                plot_bgcolor='rgba(0, 0, 0, 0)',  # Fondo del gráfico transparente
                                height = 700,
                                width = 700)
            
            #  Generamos columnas para darle formato a la página
            col1, col2 = st.columns(2)

            with col1:
                # Desplegamos el primer gráfico
                st.plotly_chart(fig_pie_1, use_container_width=True)
            with col2:
                # Desplegamos el segundo gráfico
                st.plotly_chart(fig_pie_2, use_container_width=True)
        else:
            # En caso de que la consulta falle.
            st.error("No se puedo extraer los datos")
    else: 
        # En caso de que no estemos loggeados
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")

# Pestaña de inserción de Facturas
with tab_ins_bill:
    # En caso de que no tengamos nada en el sistema
    id_support_ins=0
    # Validamos si el usuario tiene un rol asignado, en este casos ambos
    if any(role in ["admin", "user"] for role in st.session_state["roles"]):
        # Validamos si es un admin
        if any(role in ["admin"] for role in st.session_state["roles"]):
            # Realizamos una consulta para obtener los miembros que tenemos en el sistema.
            supports_ins_bills = bd.consultar_miembros(1)
            # Validamos que la consulta tenga datos
            if supports_ins_bills is not None and not supports_ins_bills.empty:
                # Tratamos los datos para poder agrupar el identificador con el nombre
                combined_supports = [f"#{row['idMiembro']} - {row['nombre']}" for index, row in supports_ins_bills.iterrows()]
                # Desplegamos en un selectbox para seleccionar un miembro
                support_ins_bill = st.selectbox("Miembro: ", combined_supports)
                # Obtenemos el identificador del miembros
                id_support_ins = int (support_ins_bill.split(' - ')[0][1:])
        # Si no es un admin, es un user
        else:
            # Se valida que el usuario este dado de alta como miembro
            state_ins_mail, id_support_ins = bd.consultar_id_email(st.session_state['email'])
            if not state_ins_mail:
                # En caso de que no, asigna 0 como identificador, no hay miembro 0 en el sistema.
                id_support_ins = int (0)

        # Consulta que trae las actividades con el id de miembro
        activities_ins_bills = bd.consultar_actividades_id(id_support_ins)
        # Validación donde identifica si el resultado tiene filas
        if activities_ins_bills is not None and not activities_ins_bills.empty:
            # Combinacion de columnas de identificador y nombre de actividad
            combined_activities = [f"#{row['idActividad']} - {row['nombre']}" for index, row in activities_ins_bills.iterrows()]    
            # Despliegue para seleccionar la actividad a la que queremos asociar la factura.
            activity_ins_bill = st.selectbox("Actvidad: ", combined_activities, key='sbinsbill')
            # Obtencion del id de la actividad
            id_activity_ins = int (activity_ins_bill.split(' - ')[0][1:])
        
            # Renderizacion del formulario
            with st.form("insert_bill", clear_on_submit=True):
                # Entradas del formulario
                name_ins_bill = st.text_input("Nombre*: ", placeholder="Taxi a Sitio")
                cost_ins_bill = st.text_input("Costo*: ", placeholder="300.00")
                type_ins_bill = st.selectbox("Tipo: ",["Viaje", "Comida", "Hospedaje"])
                tax_ins_bill = st.text_input("Impuesto*: ", placeholder="45.00")
                
                # Indicador de campos obligatorios
                st.markdown("*Campos Obligatorios")
                
                # Valores por default, dia de emision y creacion por
                dateemission_ins_bill = ut.get_today_date()
                createby_ins_bill = st.session_state['name']

                # Botón de envío
                submit_insert_bill = st.form_submit_button("Agregar", use_container_width=True)

                # Contenedor de mensajes, para poder limpiarlo posteriora mandar el formulario
                message_container = st.empty()

                # Accion del boton de envió
                if submit_insert_bill:
                    # Validacion de campos obligatorios lleno.
                    if not name_ins_bill.strip() or not cost_ins_bill.strip() or not tax_ins_bill.strip():
                        # Si no estan llenos, notifica que no se agrego y que se llenen los campos
                        st.error("Factura No Agregada")
                        st.info("Llene todos los campos obligatorios")
                    else:
                        # Función que agrega la factura
                        state_insert_bill, msj_insert_bill = bd.insertar_factura(name_ins_bill, dateemission_ins_bill, cost_ins_bill, type_ins_bill, tax_ins_bill, createby_ins_bill, id_activity_ins, id_support_ins)
                        # Validación de la ejecución correcta
                        if state_insert_bill:
                            st.success(msj_insert_bill)
                            # Información de la factura insertada
                            st.info(f"{name_ins_bill} -- {dateemission_ins_bill} -- {cost_ins_bill} -- {type_ins_bill} -- Abierta -- {createby_ins_bill} -- Actividad #{id_activity_ins} -- Miembro #{id_support_ins}")
                        else:
                            # En caso de fallar, despliega el mensaje de la inserción fallida
                            st.error(msj_insert_bill)
                    # Limipieza de mensaje
                    time.sleep(3)
                    message_container.empty()
                    # Recarga la pagina
                    st.rerun()
        else:
            st.warning("No hay activiades abiertas")
    # En caso de no tener el rol de admin, se le informa al usuario.
    else: 
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")

# Pestaña de actualización de Facturas
with tab_upd_bill:
    # Valida si se tiene un rol de admin
    if any(role in ["admin"] for role in st.session_state["roles"]):
        # Consulta las facturas que se pueden actualizar
        bills_available = bd.consultar_factura_actualizar()

        # Consulta que trae las actividades con el id de miembro
        activities_ins_bills = bd.consultar_actividades()
        # Validación donde identifica si el resultado tiene filas
        if activities_ins_bills is not None and not activities_ins_bills.empty:
            # Combinacion de columnas de identificador y nombre de actividad
            combined_activities = [f"#{row['idActividad']} - {row['nombre']}" for index, row in activities_ins_bills.iterrows()]

        # Si el resultado no es vacio
        if bills_available is not None and not bills_available.empty:
            # Combinación de columnas de identificador y nombre de factura
            combined_bills = [f"#{row['idFactura']} - {row['nombre']}" for index, row in bills_available.iterrows()]
            # Despliegue de selector de factura
            bill_selected = st.selectbox("Selecciona una Factura", combined_bills, key="update_bills_sb")
            # Obtencion de identificador de factura
            id_bill_selected = int (bill_selected.split(' - ')[0][1:])
            # Extracción de los datos de la factura que seleccioamos
            bill_data = bills_available[bills_available['idFactura']==id_bill_selected]

            # Funcion de consulta a diccionarios, para establecer el indice de las selecciones de tipo y estatus
            index_type, index_status = ut.dict_bill_upd(bill_data['tipo'].iloc[0], bill_data['estatus'].iloc[0])

            # Contenedor que le da formato a los datos actuales de miembro y actividad
            # Se realiza este procedimiento ya que al rende
            with st.container(border=True):
                # Despliegue de datos de miembro y actividad, teniendo identificador y nombre
                st.markdown(f"**Miembro: #{bill_data['idMiembro'].iloc[0]} - {bill_data['nombre_m'].iloc[0]}**")
                st.markdown(f"**Actividad: #{bill_data['idActividad'].iloc[0]} - {bill_data['nombre_a'].iloc[0]}**")

            # Renderizacion del formulario
            with st.form("update_bill", clear_on_submit= True):
                # Se le dan los valore actuales
                name_upd_bill = st.text_input("Nombre*: ", value=f"{bill_data['nombre'].iloc[0]}")
                cost_upd_bill = st.text_input("Costo*: ", value=f"{bill_data['costo'].iloc[0]}")
                type_upd_bill = st.selectbox("Tipo: ",["Viaje", "Comida", "Hospedaje"], index = index_type)
                tax_upd_bill = st.text_input("Impuesto*: ", value=f"{bill_data['impuesto'].iloc[0]}")
                status_upd_bill = st.selectbox("Estatus: ", ["Abierta", "En Proceso"], index=index_status)
                support_upd_bill = st.selectbox("Miembro: ", combined_supports)
                activity_upd_bill = st.selectbox("Actvidad: ", combined_activities, key='sbupdbill')

                # Botón de envió de información
                submit_upd_bill = st.form_submit_button("Actualizar", use_container_width=True)
            

            # Generados automaticamente, obteniendo el dia de modificacion y el usuario que modifico
            datemodified_upd_bill = ut.get_today_date()
            modifyby_upd_bill = st.session_state['name']

            # Obtencion del identificador de la actividad y del mimebro de soporte
            id_supportbill_selected = int (support_upd_bill.split(' - ')[0][1:])
            id_activitytbill_selected = int (activity_upd_bill.split(' - ')[0][1:])

            # Contenedor de mensajes, que servira para limpiar los mismos
            message_container = st.empty()

            # Acción de botón de envió    
            if submit_upd_bill:
                # Validación de llenado de campos obligatorios
                if not name_upd_bill.strip() or not cost_upd_bill.strip() or not tax_upd_bill.strip():
                    # Mensaje de error en caso de no cumplir con el criterio
                    st.error("Factura No Actualizada")
                    st.info("Llene todos los campos obligatorios")
                else:
                    # Consulta para la actualización de la factura
                    state_update_bill, msj_update_bill = bd.actualizar_factura(id_bill_selected, name_upd_bill, cost_upd_bill, type_upd_bill, tax_upd_bill, status_upd_bill, datemodified_upd_bill, modifyby_upd_bill, id_supportbill_selected, id_activitytbill_selected)
                    # Si la consulta fue exitosa
                    if state_update_bill:
                            st.success(msj_update_bill)
                            st.info(f"{name_upd_bill} -- {cost_upd_bill} -- {type_upd_bill} -- {tax_upd_bill} -- {status_upd_bill} -- {datemodified_upd_bill} -- {modifyby_upd_bill} -- {support_upd_bill} -- {activity_upd_bill}")
                    # Si la consulta no fue exitosa
                    else:
                        st.error("Factura Actualizada")
                        st.info(msj_update_bill)
                # Limpieza de mensajes
                time.sleep(3)
                message_container.empty()
                st.rerun()
        else: 
            st.warning("No hay facturas")
    # En caso de no tener el rol admin, se le hara saber al usuario.
    else: 
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")

# Pestaña para cerrar Facturas
with tab_del_bill:
    # Valida que el usuario tenga el rol admin
    if any(role in ["admin"] for role in st.session_state["roles"]):
        st.markdown("## Cerrar Factura")
        # Mensajes de apoyo
        st.warning("Una factura cerrada no podrá modificarse.")
        st.warning("Esta la podrá consultar en el listado de facturas. En cuanto la actividad a la que está asociada sea cerrada se generará un histórico")

        # Consulta las facturas que se pueden actualizar, coinciden con las facturas que se pueden eliminar
        bills_delete_available = bd.consultar_factura_actualizar()
        
        # Validacion de elementos en el resultado
        if bills_delete_available is not None and not bills_delete_available.empty:
            # Transformacion de datos donde combinamos el id y el nombre de la factura
            combined_bills_delete = [f"#{row['idFactura']} - {row['nombre']}" for index, row in bills_delete_available.iterrows()]
            # Despliega el objeto que permitira seleccionar una factura
            bill_selected_delete = st.selectbox("Selecciona una Factura", combined_bills_delete, key="delete_bills_sb")
            # Obtencion del id de la factura seleccionada
            id_bill_selected_delete = int (bill_selected_delete.split(' - ')[0][1:])
            # Información de la factura que seleccionamos para cerrar.
            bill_data_delete = bills_delete_available[bills_delete_available['idFactura']==id_bill_selected_delete]

            # Creacion de columna para el formato en el despliegue
            col1, col2, col3 = st.columns([1,4,1])

            with col2:
                # Uso de container para el formato del despliegue
                with st.container(border=True):
                    st.markdown(f"## 💵 #{bill_data_delete['idFactura'].iloc[0]} - {bill_data_delete['nombre'].iloc[0]}")
                    st.markdown(f"📆 Fecha Emision: {bill_data_delete['fecha_emision'].iloc[0]}")
                    st.markdown(f"🪙 Costo: {bill_data_delete['costo'].iloc[0]}")
                    st.markdown(f"📖 Tipo: {bill_data_delete['tipo'].iloc[0]}")
                    st.markdown(f"📈 Impuesto: {bill_data_delete['impuesto'].iloc[0]}")
                    st.markdown(f"👤 Creado Por: {bill_data_delete['creado_por'].iloc[0]}")
                    st.markdown(f"📅 Ultima Modificación: {bill_data_delete['fecha_modificacion'].iloc[0]}")
                    st.markdown(f"👤 Modificado Por: {bill_data_delete['modificado_por'].iloc[0]}")
                    # Se conjuntan el id con el nombre de la actividad y del miembro de soporte
                    st.write(f"💼 Actividad: #{bill_data_delete['idA'].iloc[0]}-{bill_data_delete['nombre_a'].iloc[0]}")
                    st.write(f"👤 Miembro: #{bill_data_delete['idM'].iloc[0]}-{bill_data_delete['nombre_m'].iloc[0]}")
                    
                    
            with col2:
                    # Un objeto que funciona a forma de comprobacion al cerrar una factura.
                    with st.popover(f"Cerrar Factura", use_container_width=True):
                        # Mensaje de advertencia al cerrar factura
                        st.write(f"¿Seguro que quieres cerrar la factura?")
                        # Acción y renderización del botón para cerrar la factura.
                        if st.button("Si. Estoy Seguro"):
                            # Datos para actualizar la factura antes de cerrarla, estos son el dia y quien modifico por ultima vez la factura, obtenido de la sesion
                            datemodified_del_bill = ut.get_today_date()
                            modifyby_del_bill = st.session_state['name']

                            # Función que actualiza la factura y luego la cierra, es una transacción. 
                            state_del_bill, msj_del_bill = bd.cerrar_factura(id_bill_selected_delete, datemodified_del_bill, modifyby_del_bill)
                            
                            # Validacion de la ejecución
                            if state_del_bill:
                                st.success(msj_del_bill)
                                # Informa el nombre de la factura cerrada
                                st.info(f"{bill_data_delete['nombre'].iloc[0]}")
                            else: 
                                # Informa porque razón no se cerro la factura
                                st.error("Factura No Cerrada")
                                st.info(msj_del_bill)
                            
                            # Limpieza de mensajes
                            message_container.empty()
                            time.sleep(3)
                            st.rerun()
    
    # Advertencia de permisos para cerrar actividad
    else: 
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")
