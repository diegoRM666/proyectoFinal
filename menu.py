import streamlit as st

def authenticated_menu():
    """
    Muestra el menú de navegación para usuarios autenticados, permitiendo el acceso a diferentes páginas 
    según el rol asignado al usuario.

    - Los usuarios con roles "admin" o "user" tienen acceso a las páginas de Clientes, Miembros, Recursos, Factura y Actividad.
    - Los usuarios con el rol "admin" adicionalmente tienen acceso a la página de Reportes.
    """
    # Muestra el enlace a la cuenta del usuario
    st.sidebar.page_link("login.py", label="Cuenta")
    
    # Verifica si el usuario tiene roles de "admin" o "user"
    if any(role in ["admin", "user"] for role in st.session_state["roles"]):
        st.sidebar.page_link("pages/main_client.py", label="Clientes")
        st.sidebar.page_link("pages/main_support.py", label="Miembros")
        st.sidebar.page_link("pages/main_resource.py", label="Recursos")
        st.sidebar.page_link("pages/main_bill.py", label="Factura")
        st.sidebar.page_link("pages/main_activity.py", label="Actividad")

        # Verifica si el usuario tiene el rol de "admin"
        if any(role in ["admin"] for role in st.session_state["roles"]):
            st.sidebar.page_link("pages/main_report.py", label="Reportes")

def unauthenticated_menu():
    """
    Muestra el menú de navegación para usuarios no autenticados, permitiendo solo el acceso a la página de inicio de sesión.
    """
    # Muestra el enlace de inicio de sesión
    st.sidebar.page_link("login.py", label="Log in")

def menu():
    """
    Determina si un usuario está autenticado y muestra el menú de navegación correspondiente.
    
    - Si el usuario no está autenticado (no tiene roles), se muestra el menú de usuarios no autenticados.
    - Si el usuario está autenticado, se muestra el menú de usuarios autenticados.
    """
    # Verifica si el usuario tiene roles asignados
    if not st.session_state.get("roles") or not st.session_state["roles"]:
        unauthenticated_menu()
        return
    authenticated_menu()

def menu_with_redirect():
    """
    Redirecciona a los usuarios no autenticados a la página de inicio de sesión. 
    Si el usuario está autenticado, se renderiza el menú de navegación correspondiente.
    """
    # Verifica si el usuario tiene roles asignados y redirige o muestra el menú apropiado
    if not st.session_state.get("roles") or not st.session_state["roles"]:
        st.switch_page("login.py")
    else:
        menu()

