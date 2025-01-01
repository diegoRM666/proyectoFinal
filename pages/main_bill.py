import streamlit as st
import pandas as pd
import time
from menu import menu_with_redirect
import logic.bd as bd
import logic.utilities as ut
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px


# Primero hacemos las comprobacion
menu_with_redirect()

#Creamos un titulo
st.markdown("# 💵 Facturas")

# Mostrar las disintas actividades a realizar
tab_lst_bill, tab_ins_bill, tab_upd_bill, tab_del_bill, tab_metric_bill= st.tabs(["Listar Facturas","Agregar Factura", "Actualizar Factura", "Cerrar Factura", "Ver Métricas"])


with tab_lst_bill:
    col1, col2 = st.columns([95,1])
    with col2: 
        if st.button("🔄", key="ref_resources"):
            st.rerun()
    if any(role in ["admin", "user"] for role in st.session_state["roles"]):
        if any(role in ["admin"] for role in st.session_state["roles"]):
            bills = bd.consultar_facturas(0,0)
        else: 
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
                    with st.container(border=True):
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
                        
                        if bill['estatus'] == "Abierta":
                            st.markdown(f'''### 🔴 :red[{bill['estatus']}]''')
                        elif bill['estatus'] == "En Proceso":
                            st.markdown(f'''### 🟡 :yellow[{bill['estatus']}]''')
                        else:
                            st.markdown(f'''### 🟢 :green[{bill['estatus']}]''')
                        
                
                # Actualizar el índice para alternar entre las columnas
                index += 1

        else:
            st.warning("No existen datos")


        st.markdown("---")
        st.markdown("### Facturas Completadas")

        if any(role in ["admin"] for role in st.session_state["roles"]):
            activities_closed = bd.consultar_actividades_listado(1,0)
        else:
            st_tmp, id_support= bd.consultar_id_email(st.session_state['email'])
            activities_closed = bd.consultar_actividades_listado(3, id_support)

        if activities_closed is not None and not activities_closed.empty:
            combined_activities_closed = [f"#{row['idActividad']} - {row['nombre_a']}" for index, row in activities_closed.iterrows()]
            activity_closed = st.selectbox("Actividad: ", combined_activities_closed)
            id_activity_closed = int (activity_closed.split(' - ')[0][1:])

            bills_closed =bd.consultar_facturas_hist(id_activity_closed)


            if bills_closed is not None and not bills_closed.empty:
                col1, col2, col3 = st.columns(3)
                
                # Iterar sobre los activities en el DataFrame
                for _, bill in bills_closed.iterrows():
                    
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
            st.warning("No existen datos")
    else: 
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")

with tab_metric_bill:
    if any(role in ["admin"] for role in st.session_state["roles"]):
        state_metrics, activities_metrics_bill, client_metrics_bill = bd.obtener_metricas_facturacion()
        
        if state_metrics:

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


            fig_pie_1.update_layout(title_text="Costo por Actividad",
                                paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo del papel transparente
                                plot_bgcolor='rgba(0, 0, 0, 0)',  # Fondo del gráfico transparente
                                height = 700,
                                width = 700)
            

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


            fig_pie_2.update_layout(title_text="Costo por Cliente",
                                paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo del papel transparente
                                plot_bgcolor='rgba(0, 0, 0, 0)',  # Fondo del gráfico transparente
                                height = 700,
                                width = 700)
            
            col1, col2 = st.columns(2)

            with col1:
                st.plotly_chart(fig_pie_1, use_container_width=True)
            with col2:
                st.plotly_chart(fig_pie_2, use_container_width=True)
        else:
            st.error("No hay datos")
    else: 
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")

with tab_ins_bill:
    id_support_ins=0
    if any(role in ["admin", "user"] for role in st.session_state["roles"]):
        if any(role in ["admin"] for role in st.session_state["roles"]):
            supports_ins_bills = bd.consultar_miembros(1)
            if supports_ins_bills is not None and not supports_ins_bills.empty:
                combined_supports = [f"#{row['idMiembro']} - {row['nombre']}" for index, row in supports_ins_bills.iterrows()]
                support_ins_bill = st.selectbox("Miembro: ", combined_supports)
                id_support_ins = int (support_ins_bill.split(' - ')[0][1:])
        else:
            state_ins_mail, id_support_ins = bd.consultar_id_email(st.session_state['email'])

        activities_ins_bills = bd.consultar_actividades_id(id_support_ins)
        if activities_ins_bills is not None and not activities_ins_bills.empty:
            combined_activities = [f"#{row['idActividad']} - {row['nombre']}" for index, row in activities_ins_bills.iterrows()]    
            activity_ins_bill = st.selectbox("Actvidad: ", combined_activities)
            id_activity_ins = int (activity_ins_bill.split(' - ')[0][1:])
        
            with st.form("insert_bill", clear_on_submit=True):
                # Entradas del formulario
                name_ins_bill = st.text_input("Nombre*: ", placeholder="Taxi a Sitio")
                cost_ins_bill = st.text_input("Costo*: ", placeholder="300.00")
                type_ins_bill = st.selectbox("Tipo: ",["Viaje", "Comida", "Hospedaje"])
                tax_ins_bill = st.text_input("Impuesto*: ", placeholder="45.00")
                
                # Indicador de campos obligatorios
                st.markdown("*Campos Obligatorios")
                
                # Valores por default
                dateemission_ins_bill = ut.get_today_date()
                createby_ins_bill = st.session_state['name']

                # Botón de envío
                submit_insert_bill = st.form_submit_button("Agregar", use_container_width=True)

                message_container = st.empty()

                if submit_insert_bill:
                    if not name_ins_bill.strip() or not cost_ins_bill.strip() or not tax_ins_bill.strip():
                        st.error("Factura No Agregada")
                        st.info("Llene todos los campos obligatorios")
                    else:
                        state_insert_bill, msj_insert_bill = bd.insertar_factura(name_ins_bill, dateemission_ins_bill, cost_ins_bill, type_ins_bill, tax_ins_bill, createby_ins_bill, id_activity_ins, id_support_ins)
                        if state_insert_bill:
                            st.success(msj_insert_bill)
                            st.info(f"{name_ins_bill} -- {dateemission_ins_bill} -- {cost_ins_bill} -- {type_ins_bill} -- Abierta -- {createby_ins_bill} -- {activities_ins_bills} -- {id_support_ins}")
                        else:
                            st.error(msj_insert_bill)
                    # Para que se limpien los mensajes
                    time.sleep(3)
                    message_container.empty()
                    st.rerun()
        else: 
            st.warning("No hay activiades abiertas")
    else: 
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")

with tab_upd_bill:
    if any(role in ["admin"] for role in st.session_state["roles"]):
        bills_available = bd.consultar_factura_actualizar()

        if bills_available is not None and not bills_available.empty:
            combined_bills = [f"#{row['idFactura']} - {row['nombre']}" for index, row in bills_available.iterrows()]
            bill_selected = st.selectbox("Selecciona una Factura", combined_bills, key="update_bills_sb")
            id_bill_selected = int (bill_selected.split(' - ')[0][1:])
            bill_data = bills_available[bills_available['idFactura']==id_bill_selected]

            index_type, index_status = ut.dict_bill_upd(bill_data['tipo'].iloc[0], bill_data['estatus'].iloc[0])

            with st.container(border=True):
                st.markdown(f"**Miembro: #{bill_data['idMiembro'].iloc[0]} - {bill_data['nombre_m'].iloc[0]}**")
                st.markdown(f"**Actividad: #{bill_data['idActividad'].iloc[0]} - {bill_data['nombre_a'].iloc[0]}**")
            with st.form("update_bill", clear_on_submit= True):
                name_upd_bill = st.text_input("Nombre*: ", value=f"{bill_data['nombre'].iloc[0]}")
                cost_upd_bill = st.text_input("Costo*: ", value=f"{bill_data['costo'].iloc[0]}")
                type_upd_bill = st.selectbox("Tipo: ",["Viaje", "Comida", "Hospedaje"], index = index_type)
                tax_upd_bill = st.text_input("Impuesto*: ", value=f"{bill_data['impuesto'].iloc[0]}")
                status_upd_bill = st.selectbox("Estatus: ", ["Abierta", "Pendiente"], index=index_status)
                support_upd_bill = st.selectbox("Miembro: ", combined_supports)
                activity_upd_bill = st.selectbox("Actvidad: ", combined_activities)

                submit_upd_bill = st.form_submit_button("Actualizar", use_container_width=True)
            

            # Generados automaticamente
            datemodified_upd_bill = ut.get_today_date()
            modifyby_upd_bill = st.session_state['name']

            id_supportbill_selected = int (support_upd_bill.split(' - ')[0][1:])
            id_activitytbill_selected = int (activity_upd_bill.split(' - ')[0][1:])


            message_container = st.empty()

            if submit_upd_bill:
                if not name_upd_bill.strip() or not cost_upd_bill.strip() or not tax_upd_bill.strip():
                    st.error("Factura No Actualizada")
                    st.info("Llene todos los campos obligatorios")
                else:
                    state_update_bill, msj_update_bill = bd.actualizar_factura(id_bill_selected, name_upd_bill, cost_upd_bill, type_upd_bill, tax_upd_bill, status_upd_bill, datemodified_upd_bill, modifyby_upd_bill, id_supportbill_selected, id_activitytbill_selected)
                    if state_update_bill:
                            st.success(msj_update_bill)
                            st.info(f"{name_upd_bill} -- {cost_upd_bill} -- {type_upd_bill} -- {tax_upd_bill} -- {status_upd_bill} -- {datemodified_upd_bill} -- {modifyby_upd_bill} -- {support_upd_bill} -- {activity_upd_bill}")
                    else:
                        st.error("Factura Actualizada")
                        st.info(msj_update_bill)
                time.sleep(3)
                message_container.empty()
                st.rerun()
    else: 
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")

with tab_del_bill:
    if any(role in ["admin"] for role in st.session_state["roles"]):
        st.markdown("## Cerrar Factura")
        st.warning("Una factura cerrada no podrá modificarse.")
        st.warning("Esta la podrá consultar en el listado de facturas. En cuanto la actividad a la que está asociada sea cerrada se generará un histórico")

        bills_delete_available = bd.consultar_factura_actualizar()
        
        if bills_delete_available is not None and not bills_delete_available.empty:
            combined_bills_delete = [f"#{row['idFactura']} - {row['nombre']}" for index, row in bills_delete_available.iterrows()]
            bill_selected_delete = st.selectbox("Selecciona una Factura", combined_bills_delete, key="delete_bills_sb")
            id_bill_selected_delete = int (bill_selected_delete.split(' - ')[0][1:])
            bill_data_delete = bills_delete_available[bills_delete_available['idFactura']==id_bill_selected_delete]

            col1, col2, col3 = st.columns([1,4,1])

            with col2:
                with st.container(border=True):
                    st.markdown(f"## 💵 #{bill_data_delete['idFactura'].iloc[0]} - {bill_data_delete['nombre'].iloc[0]}")
                    st.markdown(f"📆 Fecha Emision: {bill_data_delete['fecha_emision'].iloc[0]}")
                    st.markdown(f"🪙 Costo: {bill_data_delete['costo'].iloc[0]}")
                    st.markdown(f"📖 Tipo: {bill_data_delete['tipo'].iloc[0]}")
                    st.markdown(f"📈 Impuesto: {bill_data_delete['impuesto'].iloc[0]}")
                    st.markdown(f"👤 Creado Por: {bill_data_delete['creado_por'].iloc[0]}")
                    st.markdown(f"📅 Ultima Modificación: {bill_data_delete['fecha_modificacion'].iloc[0]}")
                    st.markdown(f"👤 Modificado Por: {bill_data_delete['modificado_por'].iloc[0]}")
                    st.write(f"💼 Actividad: #{bill_data_delete['idA'].iloc[0]}-{bill_data_delete['nombre_a'].iloc[0]}")
                    st.write(f"👤 Miembro: #{bill_data_delete['idM'].iloc[0]}-{bill_data_delete['nombre_m'].iloc[0]}")
                    
                    if bill_data_delete['estatus'].iloc[0] == "Abierta":
                        st.markdown(f'''### 🔴 :red[{bill_data_delete['estatus'].iloc[0]}]''')
                    elif bill_data_delete['estatus'].iloc[0] == "En Proceso":
                        st.markdown(f'''### 🟡 :yellow[{bill_data_delete['estatus'].iloc[0]}]''')
                    else:
                        st.markdown(f'''### 🟢 :green[{bill_data_delete['estatus'].iloc[0]}]''')
                    
                    
            with col2:
                    if st.button("Cerrar Factura", use_container_width=True):
                        datemodified_del_bill = ut.get_today_date()
                        modifyby_del_bill = st.session_state['name']

                        # La parte interesante surge aquí. 
                        state_del_bill, msj_del_bill = bd.cerrar_factura(id_bill_selected_delete, datemodified_del_bill, modifyby_del_bill)
                        if state_del_bill:
                            st.success(msj_del_bill)
                            st.info(f"{bill_data_delete['nombre'].iloc[0]}")
                        else: 
                            st.error("Factura No Eliminada")
                            st.info(msj_del_bill)
                        time.sleep(3)
                        message_container.empty()
                        st.rerun()
    else: 
        st.info("No tienes permisos para realizar esta accion. Contacta al administrador")