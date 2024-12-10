import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("login.py", label="Sesión")
    
    # Check if the user's role is in the list of roles
    if any(role in ["admin", "super-admin"] for role in st.session_state["roles"]):
        st.sidebar.page_link("pages/Cliente.py", label="Cliente")


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
