import streamlit as st

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("login.py", label="Cuenta")
    
    # Check if the user's role is in the list of roles
    if any(role in ["admin", "user"] for role in st.session_state["roles"]):
        st.sidebar.page_link("pages/main_client.py", label="Clientes")
        st.sidebar.page_link("pages/main_support.py", label="Miembros")
        st.sidebar.page_link("pages/main_resource.py", label="Recursos")
        st.sidebar.page_link("pages/main_bill.py", label="Factura")
        st.sidebar.page_link("pages/main_activity.py", label="Actividad")

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("login.py", label="Log in")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if not st.session_state.get("roles") or not st.session_state["roles"]:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if not st.session_state.get("roles") or not st.session_state["roles"]:
        st.switch_page("login.py")
    else:
        menu()
