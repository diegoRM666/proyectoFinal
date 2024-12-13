import streamlit as st
import pandas as pd
import time
from menu import menu_with_redirect
import logic.bd as bd



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
                    st.markdown(f"Fecha Emision: {bill['fecha_emision']}")
                    st.markdown(f"🔠 Costo: {bill['costo']}")
                    st.markdown(f"♟️ Tipo: {bill['tipo']}")
                    st.markdown(f"#️⃣ Impuesto: {bill['impuesto']}")
                    st.markdown(f"⏲️ Creado Por: {bill['creado_por']}")
                    st.markdown(f"⏲️ Ultima Modificación: {bill['fecha_modificacion']}")
                    st.markdown(f"⏲️ Modificado Por: {bill['modificado_por']}")
                    st.write(f"Actividad: #{bill['idA']}-{bill['nombre_a']}")
                    st.write(f"Miembro: #{bill['idM']}-{bill['nombre_m']}")
                    
                    if bill['estado'] == "Abierta":
                        st.markdown(f'''### 🔴 :red[{bill['estado']}]''')
                    elif bill['estado'] == "En Proceso":
                        st.markdown(f'''### 🟡 :yellow[{bill['estado']}]''')
                    else:
                        st.markdown(f'''### 🟢 :green[{bill['estado']}]''')
                    
            
            # Actualizar el índice para alternar entre las columnas
            index += 1

    else:
        st.warning("No existen datos")


with tab_ins_bill:
    with st.form("insert_bill", clear_on_submit=True):
        #Obtenemos las actividades y los miembros disponibles
        supports_ins_bills = bd.consultar("SELECT idMiembro, nombre FROM miembro;")
        activities_ins_bills = bd.consultar("SELECT idActividad, nombre FROM actividad;")
        
        # Entradas del formulario
        name_ins_bill = st.text_input("Nombre*: ", placeholder="Taxi a Sitio")
        cost_ins_bill = st.text_input("Costo*: ", placeholder="300.00")
        tipo_ins_bill = st.selectbox("Tipo: ",["Viaje", "Comida", "Hospedaje"])
        tax_ins_bill = st.text_input("Impuesto*: ", placeholder="45.00")



        life_ins_bill = st.selectbox("Vida Útil", ["1 Vez", "1 Año", "5 Años","10 Años"])
        comments_ins_bill = st.text_area("Notas Adicionales: ", placeholder="Agrega tus comentarios")
        
        # Indicador de campos obligatorios
        st.markdown("*Campos Obligatorios")
        
        # Botón de envío
        submit_insert_bill = st.form_submit_button("Agregar")

        message_container = st.empty()

        if submit_insert_bill:
            if not name_ins_bill.strip() or not type_ins_bill.strip() or not description_ins_bill.strip()\
            or not category_ins_bill.strip() or not serialnumber_ins_bill.strip():
                st.error("Recurso No Agregado")
                st.info("Llene todos los campos obligatorios")
            else:
                query_insert_bill = f"INSERT INTO recurso (nombre, tipo, descripcion, categoria, no_serie, estado_recurso, vida_util, notas ) VALUES ('{name_ins_bill}', '{type_ins_bill}', '{description_ins_bill}', '{category_ins_bill}', '{serialnumber_ins_bill}', 'En Stock', '{life_ins_bill}', '{comments_ins_bill}');"
                bd.insertar(query_insert_bill)
                st.success("Recurso Agregado")
                st.info(f"{name_ins_bill} -- {type_ins_bill} -- {type_ins_bill} -- {description_ins_bill} -- {category_ins_bill} -- {serialnumber_ins_bill} -- {life_ins_bill} -- En Stock -- {comments_ins_bill}")
                
            # Para que se limpien los mensajes
            time.sleep(3)
            message_container.empty()
            st.rerun()

with tab_upd_bill:
    bills_available = bd.consultar("SELECT * FROM recurso;")
    
    if bills_available is not None:
        combined_bills = [f"#{row['idRecurso']} - {row['nombre']}" for index, row in bills_available.iterrows()]
        bill_selected = st.selectbox("Selecciona un Recurso", combined_bills, key="update_bills_sb")
        id_bill_selected = int (bill_selected.split(' - ')[0][1:])
        bill_data = bills_available[bills_available['idRecurso']==id_bill_selected]
        
        #Necesitamos ademas saber el index del tipo, vida_util, estado
        type_dict = {
            "Herramienta": 0,
            "Material": 1
        }

        life_dict = {
            "1 Vez": 0,
            "1 Año": 1,
            "5 Años": 2,
            "10 Años": 3 
        }

        status_dict = {
            "En Stock": 0,
            "En Uso": 1
        }

        index_type = type_dict[bill_data['tipo'].iloc[0]]
        index_life = life_dict[bill_data['vida_util'].iloc[0]]
        index_status = status_dict[bill_data['estado_recurso'].iloc[0]]


        with st.form("update_bill", clear_on_submit= True):
            name_upd_bill = st.text_input("Nombre*: ", value=f"{bill_data['nombre'].iloc[0]}", key="name_upd_bill")
            type_upd_bill = st.selectbox("Tipo*: ", ["Herramienta", "Material"], index=index_type)
            description_upd_bill = st.text_input("Descripción*: ", value=f"{bill_data['descripcion'].iloc[0]}")
            category_upd_bill = st.text_input("Categoria*: ", value=f"{bill_data['categoria'].iloc[0]}")
            serialnumber_upd_bill = st.text_input("No. Serie", value=f"{bill_data['no_serie'].iloc[0]}")
            life_upd_bill = st.selectbox("Vida Útil", ["1 Vez", "1 Año", "5 Años","10 Años"], index=index_life)
            state_upd_bill = st.selectbox("Estado", ["En Stock", "En Uso"], index=index_status)
            comments_upd_bill = st.text_area("Notas Adicionales: ", value=f"{bill_data['notas'].iloc[0]}")
            st.write("*Campos Obligatorios")
            submit_upd_bill = st.form_submit_button("Actualizar")
        

    message_container = st.empty()

    if submit_upd_bill:
        if not name_upd_bill.strip() or not description_upd_bill.strip() or not serialnumber_upd_bill.strip():
            st.error("Recurso No Actualizado")
            st.info("Llene todos los campos obligatorios")
        else:
            state_update_bill, msj_update_bill = bd.actualizar(f"UPDATE recurso SET nombre='{name_upd_bill}', tipo='{type_upd_bill}', descripcion='{description_upd_bill}', categoria='{category_upd_bill}', no_serie='{serialnumber_upd_bill}', vida_util='{life_upd_bill}', estado_recurso='{state_upd_bill}', notas='{comments_upd_bill}' WHERE idRecurso = '{id_bill_selected}';")
            if state_update_bill == 1:
                    st.success("Recurso Actualizado")
                    st.info(f"{name_upd_bill} -- {type_upd_bill} -- {description_upd_bill} -- {category_upd_bill} -- {serialnumber_upd_bill} -- {comments_upd_bill}")
            else:
                st.error("Recurso No Actualizado")
                st.info(msj_update_bill)
            
        # Para que se limpien los mensajes
        time.sleep(3)
        message_container.empty()
        st.rerun()
