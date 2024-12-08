import streamlit as st
import pandas as pd

# Es imporante denotar que esto servirá un poco como una vista en un MVC

# Crea las tabs para distintas cosas. 
tab_select, tab_insert, tab_update, tab_delete = st.tabs(["Consultar", "Insertar", "Actualizar", "Eliminar"])

# with tab_select:
#   
#   dataframe = recuperacion()
#   st.dataframe()


with tab_insert: 
    with st.form("form_insert"):
        st.write("Ingresa un nuevo <var>.", value="Value 1")
        val_insert_module = st.text_input("Valor 1: ")
        submit_insert_module = st.form_submit_button("Ingresar")