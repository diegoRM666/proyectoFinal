import streamlit as st
import pandas as pd
import time
from menu import menu_with_redirect
import logic.bd as bd
from datetime import datetime


# Primero hacemos las comprobacion
menu_with_redirect()

#Creamos un titulo
st.markdown("# 💵 Facturas")

# Mostrar las disintas actividades a realizar
tab_lst_bill, tab_ins_bill, tab_upd_bill, tab_del_bill = \
      st.tabs(["Listar Facturas","Agregar Factura", "Actualizar Factura", "Eliminar Factura"])


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


with tab_ins_bill:
    with st.form("insert_bill", clear_on_submit=True):
        #Obtenemos las actividades y los miembros disponibles
        supports_ins_bills = bd.consultar("SELECT idMiembro, nombre FROM miembro;")
        activities_ins_bills = bd.consultar("SELECT idActividad, nombre FROM actividad;")
        combined_supports = [f"#{row['idMiembro']} - {row['nombre']}" for index, row in supports_ins_bills.iterrows()]
        combined_activities = [f"#{row['idActividad']} - {row['nombre']}" for index, row in activities_ins_bills.iterrows()]    

        # Entradas del formulario
        name_ins_bill = st.text_input("Nombre*: ", placeholder="Taxi a Sitio")
        cost_ins_bill = st.text_input("Costo*: ", placeholder="300.00")
        type_ins_bill = st.selectbox("Tipo: ",["Viaje", "Comida", "Hospedaje"])
        tax_ins_bill = st.text_input("Impuesto*: ", placeholder="45.00")
        support_ins_bill = st.selectbox("Miembro: ", combined_supports)
        activity_ins_bill = st.selectbox("Actvidad: ", combined_activities)

        
        # Indicador de campos obligatorios
        st.markdown("*Campos Obligatorios")
        
        # Valores por default
        date_today = datetime.now()
        dateemission_ins_bill = date_today.strftime("%Y-%m-%d")
        createby_ins_bill = st.session_state['name']

        #Extraccion id de los selectbox
        id_support_ins = int (support_ins_bill.split(' - ')[0][1:])
        id_activity_ins = int (activity_ins_bill.split(' - ')[0][1:])

        # Botón de envío
        submit_insert_bill = st.form_submit_button("Agregar")

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
    bills_available = bd.consultar("SELECT f.*, m.nombre as nombre_m, a.nombre as nombre_a FROM factura f INNER JOIN miembro m ON f.idMiembro=m.idMiembro INNER JOIN actividad a ON a.idActividad=f.idActividad;")
    
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

            submit_upd_bill = st.form_submit_button("Actualizar")
        

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
