import yaml
import logic.bd as bd
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


# Importa la función del menú para gestionar la navegación
from menu import menu

# Configura la disposición de la página en formato ancho
st.set_page_config(layout="wide")

# Carga el archivo de configuración
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Guarda el archivo de configuración después de realizar cambios
def save_file_yaml():
    """Guarda el archivo de configuración en formato YAML."""
    with open('config.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(config, file, default_flow_style=False)

def deploy_information():
    """
    Despliega información de la cuenta y opciones de gestión basadas en el rol del usuario.

    - Para roles "admin" o "super-admin": permite ver información, actualizar contraseñas y crear nuevos usuarios.
    - Para otros roles: permite ver información y actualizar contraseñas.
    """
    if any(role in ["admin", "super-admin"] for role in st.session_state["roles"]):
        st.markdown("# ℹ️ Cuenta")
        tab_info_session, tab_update_session, tab_create_new = st.tabs(["Información", "Actualizar", "Crear Nuevo Usuario"])

        with tab_info_session:
            st.markdown("### Información")
            st.write(f"👤 Usuario:")
            st.info(f"{st.session_state['name']}")
            st.write(f"📧 Correo:")
            st.info(f"{st.session_state['email']}")
            st.write(f"📇 Roles: ")
            roles_assigned = " ".join(st.session_state["roles"])
            st.info(f"{roles_assigned}")

        with tab_update_session:
            # Widget para restablecer contraseña
            if st.session_state['authentication_status']:
                try:
                    if authenticator.reset_password(st.session_state['username'], fields={
                        'Form name': 'Cambiar Contraseña', 
                        'Current password': 'Contraseña Actual',
                        'New password': 'Nueva Contraseña',
                        'Repeat password': 'Repite la Contraseña',
                        'Reset': 'Cambiar Contraseña'}):
                        save_file_yaml()
                        st.success('Contraseña Actualizada Correctamente')
                except (CredentialsError, ResetError) as e:
                    st.error(e)

        with tab_create_new:
            # Widget para registrar un nuevo usuario
            try:
                email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
                    clear_on_submit=True, 
                    roles=['user'], 
                    fields={
                        'Form name': 'Crear Nuevo Usuario', 
                        'First name': 'Nombre', 
                        'Last name': 'Primer Apellido', 
                        'Username': 'Nombre de Usuario', 
                        'Password': 'Contraseña', 
                        'Repeat password': 'Repite Contraseña', 
                        'Password Hint': 'Sugerencia', 
                        'Register': 'Registrar'}
                )
                if email_of_registered_user:
                    # Se guarda la informacion en el YAML
                    save_file_yaml()
                    st.success('Usuario Registrado Correctamente')
            except RegisterError as e:
                st.error(e)
    else:
        tab_info_session, tab_update_session = st.tabs(["Información", "Actualizar"])

        with tab_info_session:
            st.markdown("### Información")
            st.write(f"👤 Usuario:")
            st.info(f"{st.session_state['name']}")
            st.write(f"📧 Correo:")
            st.info(f"{st.session_state['email']}")
            st.write(f"📇 Roles: ")
            roles_assigned = " ".join(st.session_state["roles"])
            st.info(f"{roles_assigned}")

            # Consulta el identificador con el correo del usuario
            state_email, result_email = bd.consultar_id_email(st.session_state['email'])
            if not state_email:
                st.warning("Este usuario no tiene asociado un miembro. Agregue un miembro")

        with tab_update_session:
            # Widget para restablecer contraseña
            if st.session_state['authentication_status']:
                try:
                    if authenticator.reset_password(st.session_state['username'], fields={
                        'Form name': 'Cambiar Contraseña', 
                        'Current password': 'Contraseña Actual',
                        'New password': 'Nueva Contraseña',
                        'Repeat password': 'Repite la Contraseña',
                        'Reset': 'Cambiar Contraseña'}):
                        save_file_yaml()
                        st.success('Contraseña Actualizada Correctamente')
                except (CredentialsError, ResetError) as e:
                    st.error(e)

# A partir de aqui continua el script
# Creación del objeto de autenticación
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Widget de inicio de sesión
try:
    authenticator.login(fields={
        'Form name': 'Iniciar Sesión', 
        'Username': 'Usuario',
        'Password': 'Contraseña',
        'Login': 'Iniciar Sesión'
    })
except LoginError as e:
    st.error(e)

# Autenticación del usuario
if st.session_state['authentication_status']:
    deploy_information()
    authenticator.logout("Salir Sesión")
elif st.session_state['authentication_status'] is False:
    st.error('Usuario/Contraseña Incorrecta')
elif st.session_state['authentication_status'] is None:
    st.warning('Por favor, ingresa tu Usuario y Contraseña')

# Llama a la función de menú para renderizar las opciones en la barra lateral
menu()


