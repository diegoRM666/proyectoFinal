"""
Script description: This script imports tests the Streamlit-Authenticator package. 

Libraries imported:
- yaml: Module implementing the data serialization used for human readable documents.
- streamlit: Framework used to build pure Python web applications.
"""

import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import (CredentialsError,
                                               ForgotError,
                                               Hasher,
                                               LoginError,
                                               RegisterError,
                                               ResetError,
                                               UpdateError)
from menu import authenticated_menu

# Loading config file
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

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
    authenticator.login()
except LoginError as e:
    st.error(e)


# Authenticating user
if st.session_state['authentication_status']:
    st.write(f'Welcome *{st.session_state["name"]}*, Role: {st.session_state["roles"]}')
    st.title('Some content')
    authenticator.logout()
elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')




# Creating a password reset widget
if st.session_state['authentication_status']:
    try:
        if authenticator.reset_password(st.session_state['username']):
            st.success('Password modified successfully')
    except (CredentialsError, ResetError) as e:
        st.error(e)



# Saving config file
with open('config.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(config, file, default_flow_style=False)

authenticated_menu()