import streamlit as st

def authenticated_menu():
    # Muestra el menu de navegacion para usuarios autenticados
    st.sidebar.page_link("login.py", label="Cuenta")
    
    # Discrimina de acuerdo al rol que tenemos asignado
    if any(role in ["admin", "user"] for role in st.session_state["roles"]):
        st.sidebar.page_link("pages/main_client.py", label="Clientes")
        st.sidebar.page_link("pages/main_support.py", label="Miembros")
        st.sidebar.page_link("pages/main_resource.py", label="Recursos")
        st.sidebar.page_link("pages/main_bill.py", label="Factura")
        st.sidebar.page_link("pages/main_activity.py", label="Actividad")

        if any(role in ["admin"] for role in st.session_state["roles"]):
            st.sidebar.page_link("pages/main_report.py", label="Reportes")

def unauthenticated_menu():
    # Muestra el menu de navegacion para usuarios no autenticados
    st.sidebar.page_link("login.py", label="Log in")

def menu():
    # Determina si un usuario esta acreditado o no, luego muestra el menu de navegacion correcto
    if not st.session_state.get("roles") or not st.session_state["roles"]:
        unauthenticated_menu()
        return
    authenticated_menu()

def menu_with_redirect():
    # Redirecciona a los usuarios no acreditados a la página de loggeo, de otra forma renderiza el menu de navegacion
    if not st.session_state.get("roles") or not st.session_state["roles"]:
        st.switch_page("login.py")
    else:
        menu()
