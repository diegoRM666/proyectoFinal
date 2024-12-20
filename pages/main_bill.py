import streamlit as st
import pandas as pd
import time
from menu import menu_with_redirect
import logic.bd as bd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px


# Primero hacemos las comprobacion
menu_with_redirect()

#Creamos un titulo
st.markdown("# 💵 Facturas")

# Mostrar las disintas actividades a realizar
tab_lst_bill, tab_ins_bill, tab_upd_bill, tab_del_bill, tab_metric_bill= \
      st.tabs(["Listar Facturas","Agregar Factura", "Actualizar Factura", "Cerrar Factura", "Ver Métricas"])


with tab_lst_bill:
    bills = bd.consultar("SELECT f.*, a.idActividad as idA, a.nombre as nombre_a, m.idMiembro as idM, m.nombre as nombre_m FROM factura f INNER JOIN miembro m ON f.idMiembro=m.idMiembro INNER JOIN actividad a ON f.idActividad=a.idActividad;")

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

    activities_closed = bd.consultar("SELECT idActividad, nombre_a FROM actividad_hist;")
    combined_activities_closed = [f"#{row['idActividad']} - {row['nombre_a']}" for index, row in activities_closed.iterrows()]
    activity_closed = st.selectbox("Miembro: ", combined_activities_closed)
    id_activity_closed = int (activity_closed.split(' - ')[0][1:])

    bills_closed =bd.consultar(f"SELECT fh.*, ah.nombre_a, ah.nombre_m, ah.idMiembro as idM FROM factura_hist fh INNER JOIN actividad_hist ah ON fh.idActividad = ah.idActividad WHERE fh.idActividad='{id_activity_closed}';")

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


with tab_metric_bill:
    
    activities_metrics_bill = bd.consultar("SELECT fh.idActividad, ah.nombre_a, sum(fh.costo + fh.impuesto) AS total FROM factura_hist fh INNER JOIN actividad_hist ah ON fh.idActividad=ah.idActividad GROUP BY fh.idActividad;")
    client_metrics_bill = bd.consultar("SELECT ah.idCliente, ah.nombre_c, sum(fh.costo + fh.impuesto) AS total FROM factura_hist fh INNER JOIN actividad_hist ah ON fh.idActividad=ah.idActividad GROUP BY ah.idCliente, ah.nombre_c;")
    

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

with tab_ins_bill:
    supports_ins_bills = bd.consultar("SELECT idMiembro, nombre FROM miembro;")
    combined_supports = [f"#{row['idMiembro']} - {row['nombre']}" for index, row in supports_ins_bills.iterrows()]
    support_ins_bill = st.selectbox("Miembro: ", combined_supports)
    id_support_ins = int (support_ins_bill.split(' - ')[0][1:])
    
    #Esto actualizará lo siguiente:
    activities_ins_bills = bd.consultar(f"SELECT idActividad, nombre FROM actividad WHERE idMiembro='{id_support_ins}';")
    combined_activities = [f"#{row['idActividad']} - {row['nombre']}" for index, row in activities_ins_bills.iterrows()]    
    activity_ins_bill = st.selectbox("Actvidad: ", combined_activities)
    id_activity_ins = int (activity_ins_bill.split(' - ')[0][1:])
    
    with st.form("insert_bill", clear_on_submit=True):
        #Obtenemos las actividades y los miembros disponibles
        

        # Entradas del formulario
        name_ins_bill = st.text_input("Nombre*: ", placeholder="Taxi a Sitio")
        cost_ins_bill = st.text_input("Costo*: ", placeholder="300.00")
        type_ins_bill = st.selectbox("Tipo: ",["Viaje", "Comida", "Hospedaje"])
        tax_ins_bill = st.text_input("Impuesto*: ", placeholder="45.00")
        

        
        # Indicador de campos obligatorios
        st.markdown("*Campos Obligatorios")
        
        # Valores por default
        date_today = datetime.now()
        dateemission_ins_bill = date_today.strftime("%Y-%m-%d")
        createby_ins_bill = st.session_state['name']

        # Botón de envío
        submit_insert_bill = st.form_submit_button("Agregar", use_container_width=True)

        message_container = st.empty()

        if submit_insert_bill:
            if not name_ins_bill.strip() or not cost_ins_bill.strip() or not tax_ins_bill.strip():
                st.error("Factura No Agregada")
                st.info("Llene todos los campos obligatorios")
            else:
                query_insert_bill = f"INSERT INTO factura (nombre, fecha_emision, costo, tipo, impuesto, estatus, creado_por, fecha_modificacion, modificado_por, idActividad, idMiembro) VALUES ('{name_ins_bill}', '{dateemission_ins_bill}', '{cost_ins_bill}', '{type_ins_bill}', '{tax_ins_bill}', 'Abierta', '{createby_ins_bill}', '{dateemission_ins_bill}', '{createby_ins_bill}', '{id_activity_ins}', '{id_support_ins}'  );"
                bd.insertar(query_insert_bill)
                st.success("Factura Agregada")
                st.info(f"{name_ins_bill} -- {dateemission_ins_bill} -- {cost_ins_bill} -- {type_ins_bill} -- Abierta -- {createby_ins_bill} -- {activities_ins_bills} -- {support_ins_bill}")
                
            # Para que se limpien los mensajes
            time.sleep(3)
            message_container.empty()
            st.rerun()

with tab_upd_bill:
    bills_available = bd.consultar("SELECT f.*, m.nombre as nombre_m, a.nombre as nombre_a FROM factura f INNER JOIN miembro m ON f.idMiembro=m.idMiembro INNER JOIN actividad a ON a.idActividad=f.idActividad WHERE f.estatus != 'Cerrada';")
    
    if bills_available is not None:
        combined_bills = [f"#{row['idFactura']} - {row['nombre']}" for index, row in bills_available.iterrows()]
        bill_selected = st.selectbox("Selecciona una Factura", combined_bills, key="update_bills_sb")
        id_bill_selected = int (bill_selected.split(' - ')[0][1:])
        bill_data = bills_available[bills_available['idFactura']==id_bill_selected]
        
        #Necesitamos ademas saber el index del tipo, vida_util, estado
        type_dict = {
            "Viaje": 0,
            "Comida": 1,
            "Hospedaje": 2
        }

        status_dict = {
            "Abierta": 0,
            "Pendiente": 1
        }

        index_type = type_dict[bill_data['tipo'].iloc[0]]
        index_status = status_dict[bill_data['estatus'].iloc[0]]

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
        date_today = datetime.now()
        datemodified_upd_bill = date_today.strftime("%Y-%m-%d")
        modifyby_upd_bill = st.session_state['name']

        id_supportbill_selected = int (support_upd_bill.split(' - ')[0][1:])
        id_activitytbill_selected = int (activity_upd_bill.split(' - ')[0][1:])


    message_container = st.empty()

    if submit_upd_bill:
        if not name_upd_bill.strip() or not cost_upd_bill.strip() or not tax_upd_bill.strip():
            st.error("Factura No Actualizada")
            st.info("Llene todos los campos obligatorios")
        else:
            state_update_bill, msj_update_bill = bd.actualizar(f"UPDATE factura SET nombre='{name_upd_bill}', costo='{cost_upd_bill}', tipo='{type_upd_bill}', impuesto='{tax_upd_bill}', estatus='{status_upd_bill}', fecha_modificacion='{datemodified_upd_bill}', modificado_por='{modifyby_upd_bill}', idMiembro='{id_supportbill_selected}', idActividad='{id_activitytbill_selected}' WHERE idFactura = '{id_bill_selected}';")
            if state_update_bill == 1:
                    st.success("Factura Actualizada")
                    st.info(f"{name_upd_bill} -- {cost_upd_bill} -- {type_upd_bill} -- {tax_upd_bill} -- {status_upd_bill} -- {datemodified_upd_bill} -- {modifyby_upd_bill} -- {support_upd_bill} -- {activity_upd_bill}")
            else:
                st.error("Factura Actualizada")
                st.info(msj_update_bill)
        # Para que se limpien los mensajes
        time.sleep(3)
        message_container.empty()
        st.rerun()

with tab_del_bill:
    st.markdown("## Cerrar Factura")
    st.warning("Una factura cerrada no podrá modificarse.")
    st.warning("Esta la podrá consultar en el listado de facturas. En cuanto la actividad a la que está asociada sea cerrada se generará un histórico")

    bills_delete_available = bd.consultar("SELECT f.*, m.idMiembro as idM, a.idActividad as idA, m.nombre as nombre_m, a.nombre as nombre_a FROM factura f INNER JOIN miembro m ON f.idMiembro=m.idMiembro INNER JOIN actividad a ON a.idActividad=f.idActividad WHERE f.estatus!='Cerrada';")
    
    if bills_delete_available is not None:
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
                    date_today = datetime.today()
                    datemodified_del_bill = date_today.strftime("%Y-%m-%d")
                    modifyby_del_bill = st.session_state['name']

                    # La parte interesante surge aquí. 
                    state_del_bill, msj_del_bill = bd.actualizar(f"UPDATE factura SET fecha_modificacion =' {datemodified_del_bill}', modificado_por='{modifyby_del_bill}', estatus='Cerrada' WHERE idFactura={id_bill_selected_delete}")