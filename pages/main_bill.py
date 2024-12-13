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
tab_lst_resource, tab_ins_resource, tab_upd_resource, tab_del_resource = \
      st.tabs(["Listar Facturas","Agregar Factura", "Actualizar Factura", "Eliminar Factura"])


with tab_lst_resource:
    resources = bd.consultar("SELECT nombre, tipo, descripcion, categoria, no_serie, estado_recurso, vida_util, notas FROM recurso;")

    if resources is not None and not resources.empty:

        # Definir el número de columnas
        num_cols = 2
        cols = st.columns(num_cols)
        
        # Inicializar el índice para repartir a las columnas
        index = 0

        # Iterar sobre los resources en el DataFrame
        for _, resource in resources.iterrows():
            col = cols[index % num_cols]  # Alterna entre las columnas (0 y 1)
            
            # Mostrar la información del resource en la columna correspondiente
            with col:
                with st.container(border=True):
                    st.markdown(f"## 🔧 {resource['nombre']}")
                    if resource['tipo'] == "Herramienta":
                        st.markdown(f"⚒️ Tipo: {resource['tipo']}")
                    else:
                        st.markdown(f"🖥️ Tipo: {resource['tipo']}")
                    st.markdown(f"🔠 Descripción: {resource['descripcion']}")
                    st.markdown(f"♟️ Categoria: {resource['categoria']}")
                    st.markdown(f"#️⃣ No. Serie: {resource['no_serie']}")
                    st.markdown(f"⏲️ Vida Útil: {resource['vida_util']}")
                    if resource['notas'] !="":
                        st.markdown(f"🗒️ Notas: {resource['notas']}")
                    
                    if resource['estado_recurso'] == "En Stock":
                        st.markdown(f'''### ✅ :green[{resource['estado_recurso']}]''')
                    else:
                        st.markdown(f'''### ❌ :orange[{resource['estado_recurso']}]''')
                    
            
            # Actualizar el índice para alternar entre las columnas
            index += 1

    else:
        st.warning("No existen datos")


with tab_ins_resource:
    with st.form("insert_resource", clear_on_submit=True):
        # Entradas del formulario
        name_ins_resource = st.text_input("Nombre*: ", placeholder="Llave")
        type_ins_resource = st.selectbox("Tipo*: ", ["Herramienta", "Material"])
        description_ins_resource = st.text_input("Descripción*: ", placeholder="Llave Allen 3/4")
        category_ins_resource = st.text_input("Categoria*: ", placeholder="Mecánica")
        serialnumber_ins_resource = st.text_input("No. Serie", placeholder="ALL15313")
        life_ins_resource = st.selectbox("Vida Útil", ["1 Vez", "1 Año", "5 Años","10 Años"])
        comments_ins_resource = st.text_area("Notas Adicionales: ", placeholder="Agrega tus comentarios")
        
        # Indicador de campos obligatorios
        st.markdown("*Campos Obligatorios")
        
        # Botón de envío
        submit_insert_resource = st.form_submit_button("Agregar")

        message_container = st.empty()

        if submit_insert_resource:
            if not name_ins_resource.strip() or not type_ins_resource.strip() or not description_ins_resource.strip()\
            or not category_ins_resource.strip() or not serialnumber_ins_resource.strip():
                st.error("Recurso No Agregado")
                st.info("Llene todos los campos obligatorios")
            else:
                query_insert_resource = f"INSERT INTO recurso (nombre, tipo, descripcion, categoria, no_serie, estado_recurso, vida_util, notas ) VALUES ('{name_ins_resource}', '{type_ins_resource}', '{description_ins_resource}', '{category_ins_resource}', '{serialnumber_ins_resource}', 'En Stock', '{life_ins_resource}', '{comments_ins_resource}');"
                bd.insertar(query_insert_resource)
                st.success("Recurso Agregado")
                st.info(f"{name_ins_resource} -- {type_ins_resource} -- {type_ins_resource} -- {description_ins_resource} -- {category_ins_resource} -- {serialnumber_ins_resource} -- {life_ins_resource} -- En Stock -- {comments_ins_resource}")
                
            # Para que se limpien los mensajes
            time.sleep(3)
            message_container.empty()
            st.rerun()

with tab_upd_resource:
    resources_available = bd.consultar("SELECT * FROM recurso;")
    
    if resources_available is not None:
        combined_resources = [f"#{row['idRecurso']} - {row['nombre']}" for index, row in resources_available.iterrows()]
        resource_selected = st.selectbox("Selecciona un Recurso", combined_resources, key="update_resources_sb")
        id_resource_selected = int (resource_selected.split(' - ')[0][1:])
        resource_data = resources_available[resources_available['idRecurso']==id_resource_selected]
        
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

        index_type = type_dict[resource_data['tipo'].iloc[0]]
        index_life = life_dict[resource_data['vida_util'].iloc[0]]
        index_status = status_dict[resource_data['estado_recurso'].iloc[0]]


        with st.form("update_resource", clear_on_submit= True):
            name_upd_resource = st.text_input("Nombre*: ", value=f"{resource_data['nombre'].iloc[0]}", key="name_upd_resource")
            type_upd_resource = st.selectbox("Tipo*: ", ["Herramienta", "Material"], index=index_type)
            description_upd_resource = st.text_input("Descripción*: ", value=f"{resource_data['descripcion'].iloc[0]}")
            category_upd_resource = st.text_input("Categoria*: ", value=f"{resource_data['categoria'].iloc[0]}")
            serialnumber_upd_resource = st.text_input("No. Serie", value=f"{resource_data['no_serie'].iloc[0]}")
            life_upd_resource = st.selectbox("Vida Útil", ["1 Vez", "1 Año", "5 Años","10 Años"], index=index_life)
            state_upd_resource = st.selectbox("Estado", ["En Stock", "En Uso"], index=index_status)
            comments_upd_resource = st.text_area("Notas Adicionales: ", value=f"{resource_data['notas'].iloc[0]}")
            st.write("*Campos Obligatorios")
            submit_upd_resource = st.form_submit_button("Actualizar")
        

    message_container = st.empty()

    if submit_upd_resource:
        if not name_upd_resource.strip() or not description_upd_resource.strip() or not serialnumber_upd_resource.strip():
            st.error("Recurso No Actualizado")
            st.info("Llene todos los campos obligatorios")
        else:
            state_update_resource, msj_update_resource = bd.actualizar(f"UPDATE recurso SET nombre='{name_upd_resource}', tipo='{type_upd_resource}', descripcion='{description_upd_resource}', categoria='{category_upd_resource}', no_serie='{serialnumber_upd_resource}', vida_util='{life_upd_resource}', estado_recurso='{state_upd_resource}', notas='{comments_upd_resource}' WHERE idRecurso = '{id_resource_selected}';")
            if state_update_resource == 1:
                    st.success("Recurso Actualizado")
                    st.info(f"{name_upd_resource} -- {type_upd_resource} -- {description_upd_resource} -- {category_upd_resource} -- {serialnumber_upd_resource} -- {comments_upd_resource}")
            else:
                st.error("Recurso No Actualizado")
                st.info(msj_update_resource)
            
        # Para que se limpien los mensajes
        time.sleep(3)
        message_container.empty()
        st.rerun()
