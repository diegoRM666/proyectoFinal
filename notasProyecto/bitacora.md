## Bitácora

### 14 Noviembre de 2024

Se realizó la implemetanción de #login para la aplicación, para tal se utiliza el repositorio de Github proporcionado en el siguiente link [Streamlit-Authenticator](https://github.com/mkhorasani/Streamlit-Authenticator) por el usuario [Mohammad Khorasani](https://github.com/mkhorasani).

Para ello necesitamos el siguiente documento YAML que nos permita generar la configuración de credenciales: 

``` YAML
cookie:
  expiry_days: 30
  key: some_signature_key # Must be a string
  name: some_cookie_name
credentials:
  usernames:
    jsmith:
      email: jsmith@gmail.com
      failed_login_attempts: 0 # Will be managed automatically
      first_name: John
      last_name: Smith
      logged_in: False # Will be managed automatically
      password: abc # Will be hashed automatically
      roles: # Optional
      - admin
      - editor
      - viewer
    rbriggs:
      email: rbriggs@gmail.com
      failed_login_attempts: 0 # Will be managed automatically
      first_name: Rebecca
      last_name: Briggs
      logged_in: False # Will be managed automatically
      password: def # Will be hashed automatically
      roles: # Optional
      - viewer
oauth2: # Optional
  google: # Follow instructions: https://developers.google.com/identity/protocols/oauth2

	client_id: # To be filled
    client_secret: # To be filled
    redirect_uri: # URL to redirect to after OAuth2 authentication
  microsoft: # Follow instructions: https://learn.microsoft.com/en-us/graph/auth-register-app-v2
    client_id: # To be filled
    client_secret: # To be filled
    redirect_uri: # URL to redirect to after OAuth2 authentication
    tenant_id: # To be filled
pre-authorized: # Optional
  emails:
  - melsby@gmail.com
```

Se guardará como `config.yaml`.

**NOTA**: No importa que las contraseñas las ingresemos de manera literal, la aplicación al correr por primera vez genera el hash de manera automática por primera vez, y luego se comenta esa línea. 

Y para agregar nuevos, no hay tanto tema, de hecho solamente podemos preautorizar el correo que nosotros queramos. 

Ahora para el código necesitamos lo siguiente: 

#### Imports de Librerias
``` python
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

```

#### Cargamos el archivo de configuración
``` python
# Loading config file
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)
```

La primera linea abre el archivo `config.yaml` en modo de lectura (`'r'`) y especifica que debe usar la codificación UTF-8. La sintaxis `with open(...) as file` asegura que el archivo se cierre automáticamente al terminar la lectura, incluso si ocurre algún error en el proceso.

#### Cambiar el texto plano de las contraseñas a cifrado
``` python
stauth.Hasher.hash_passwords(config['credentials'])
```

Este se comentará posterior a la primera vez de correrlo, ya que esto solamente corre una vez y lo cifra, en consecuencia no deberá volverse a tocar. 

#### Creación de un objeto autenticador

Este objeto nos permite recopilar justamente la información de las credenciales de los usuarios. 

``` python 
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
```

- `config['credentials']`: Las credenciales de los usuarios (como nombres de usuario y contraseñas).
- `config['cookie']['name']`, `config['cookie']['key']`, y `config['cookie']['expiry_days']`: Configuraciones para almacenar una cookie de autenticación en el navegador del usuario.
  
  Esto nos permite que una vez iniciado, podamos de manera más sencilla navegar por la página web, sin necesidad de volvernos a identificar con la aplicación.

#### Creación del widget de login

Esto nos soluciona mucho de la capa de generar el login, ya que no necesitamos implementar mucho. Solamente llamamos al método `login`, este directamente hace la renderización.

``` python
try:
    authenticator.login()
except LoginError as e:
    st.error(e)
```

En caso de que no se pueda validar a la persona, desplegará un mensaje de error. 

