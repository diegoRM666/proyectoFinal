"""
Script description: This script imports tests the Streamlit-Authenticator package. 

Libraries imported:
- yaml: Module implementing the data serialization used for human readable documents.
- streamlit: Framework used to build pure Python web applications.
"""

import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import (CredentialsError,
                                               ForgotError,
                                               Hasher,
                                               LoginError,
                                               RegisterError,
                                               ResetError,
                                               UpdateError)
# Este es el que nos permitirá movernos al menu
from menu import menu

st.set_page_config(layout="wide")

# Loading config file
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

# Saving config file
def save_file_yaml():
    with open('config.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(config, file, default_flow_style=False)

        

def deploy_information():

    if any(role in ["admin", "super-admin"] for role in st.session_state["roles"]):
        st.markdown("# ℹ️ Cuenta")
        tab_info_session, tab_update_session, tab_create_new = st.tabs(["Información", "Actualizar", "Crear Nuevo Usuario"])

        with tab_info_session:
            st.markdown("### Información")
            st.write(f"👤 Usuario:")
            st.info(f"{st.session_state["name"]}")
            st.write(f"📧 Correo:")
            st.info(f"{st.session_state["email"]}")
            st.write(f"📇 Roles: ")
            roles_assigned = ""
            for role in st.session_state["roles"]:
                roles_assigned = roles_assigned+" "+role
            st.info(f"{roles_assigned}")

        with tab_update_session:
            # Creating a password reset widget
            if st.session_state['authentication_status']:
                try:
                    if authenticator.reset_password(st.session_state['username'], fields={'Form name':'Cambiar Contraseña', 
                                            'Current password':'Contraseña Actual',
                                            'New password':'Nueva Contraseña',
                                            'Repeat password':'Repite la Contraseña',
                                            'Reset': 'Cambiar Contraseña'}):
                        save_file_yaml()
                        st.success('Contraseña Actualiazada Correctamente')
                except (CredentialsError, ResetError) as e:
                    st.error(e)
        with tab_create_new:
            # Creating a new user registration widget
            try:
                (email_of_registered_user,
                    username_of_registered_user,
                 name_of_registered_user) = authenticator.register_user(clear_on_submit=True, roles=['user'], fields ={'Form name':'Crear Nuevo Usuario', 'First name':'Nombre', 'Last name': 'Primer Apellido', 'Username': 'Nombre de Usuario', 'Password': 'Contraseña', 'Repeat password': 'Repite Contraseña', 'Password Hint':'Sugerencia','Register': 'Registrar'})
                if email_of_registered_user:
                    save_file_yaml()
                    st.success('Usuario Registrado Correctamente')
            except RegisterError as e:
                st.error(e)


    else:
        tab_info_session, tab_update_session = st.tabs(["Información", "Actualizar"])

        with tab_info_session:
            st.markdown("### Información")
            st.write(f"👤 Usuario:")
            st.info(f"{st.session_state["name"]}")
            st.write(f"📧 Correo:")
            st.info(f"{st.session_state["email"]}")
            st.write(f"📇 Roles: ")
            roles_assigned = ""
            for role in st.session_state["roles"]:
                roles_assigned = roles_assigned+" "+role
            st.info(f"{roles_assigned}")

        with tab_update_session:
            # Creating a password reset widget
            if st.session_state['authentication_status']:
                try:
                    if authenticator.reset_password(st.session_state['username'], fields={'Form name':'Cambiar Contraseña', 
                                            'Current password':'Contraseña Actual',
                                            'New password':'Nueva Contraseña',
                                            'Repeat password':'Repite la Contraseña',
                                            'Reset': 'Cambiar Contraseña'}):
                        save_file_yaml()
                        st.success('Contraseña Actualiazada Correctamente')
                except (CredentialsError, ResetError) as e:
                    st.error(e)
    
# Creating the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

#authenticator = stauth.Authenticate(
#     '../config.yaml'
# )

# Creating a login widget
try:
    authenticator.login(fields={'Form name':'Iniciar Sesión', 
                                'Username':'Usuario',
                                'Password':'Contraseña',
                                'Login':'Iniciar Sesión'
                                })
except LoginError as e:
    st.error(e)


# Authenticating user
if st.session_state['authentication_status']:
    deploy_information()
    authenticator.logout("Salir Sesion")
elif st.session_state['authentication_status'] is False:
    st.error('Usuario/Contraseña Incorrecta')
elif st.session_state['authentication_status'] is None:
    st.warning('Porfavor, ingresa tu Usuario y Contraseña')


# We call the menu function to render the possibilities in the sidebar.
menu()

