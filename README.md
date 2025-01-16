# Challenge: Docs en Drive Públicos

Esta aplicación permite inventariar los archivos de Google Drive de un usuario en una base de datos SQLite. Además, detecta archivos públicos, modifica su visibilidad a privada, y notifica al propietario por correo electrónico.

### Funcionalidades

- Inventariar archivos de Google Drive en una base de datos SQLite.
- Identificar archivos públicos y cambiar su visibilidad a privada.
- Notificar por correo electrónico al propietario cuando un archivo cambia de visibilidad.
- Actualizar la base de datos con cambios realizados en archivos ya inventariados.
- Mantener un registro histórico de archivos que fueron públicos en algún momento.

### Requisitos Previos
- Python 3.8 o superior
- Cuenta de Google
- Cuenta de correo electrónico para enviar notificaciones

### 🔧 Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tatlopez/Challenge-Drive.git
   cd app

2. Instalar las dependencias:
    ```bash
    pip install -r requirements.txt

3. Obtener credenciales:
   - Ir a [Google Cloud Console](https://console.cloud.google.com)
   - Crear un nuevo proyecto
   - Habilitar la Google Drive API
   - Crear credenciales OAuth 2.0
   - Configura la pantalla de consentimiento OAuth:
      - Seleccionando "External"
      - Añadir los scopes necesarios:
        - `.../auth/drive.metadata.readonly`
        - `.../auth/drive.file`
   - Descargar el archivo de credenciales para luego completar el .env

4. Configurar las variables de entorno con un archivo .env en el directorio raíz con el siguiente formato:

    ```bash
    CLIENT_ID=<client_id>
    PROJECT_ID=<project_id>
    CLIENT_SECRET=<client_secret>
    EMAIL_ADDRESS=<email_address> #el mail que envia la notificación
    EMAIL_PASSWORD=<email_password> #la contraseña de aplicación del mail

### 💻 Uso

1. Ejecutar la aplicación:
   ```bash
   python app/main.py


### 📂 Estructura del Proyecto

    app/
    │
    ├── db.py           # Gestión de la base de datos SQLite.
    ├── drive.py        # Funciones para interactuar con la API de Google Drive.
    ├── emailer.py      # Funciones para enviar correos electrónicos.
    ├── main.py         # Script principal de la aplicación.
    ├── utils.py        # Funciones auxiliares.
    ├── token.json      # Token de autenticación de Google (autogenerado).
    ├── drive_inventory.db # Base de datos SQLite (autogenerada).

### 📏 Estructura de la Base de Datos
La aplicación utiliza SQLite con las siguientes tablas:
- `drive_files`: Almacena la información actual de los archivos
  - `id`: ID único del archivo
  - `name`: Nombre del archivo
  - `extension`: Extensión del archivo
  - `owner`: Propietario del archivo
  - `visibility`: Estado de visibilidad
  - `last_modified`: Fecha de última modificación

- `public_file_history`: Registro histórico de archivos públicos
  - `id`: ID único del archivo
  - `name`: Nombre del archivo
  - `owner`: Propietario del archivo
  - `changed_at`: Fecha en la que la visibilidad del archivo fue modificado.

### API de Google Drive - Documentación

#### Scope
- `https://www.googleapis.com/auth/drive`: Acceso completo a los archivos y carpetas en Google Drive.

#### Autenticación y Autorización
La aplicación utiliza OAuth 2.0 para la autenticación, implementando el flujo de autorización para aplicaciones instaladas:

1. `get_credentials()`: 
   - Maneja el proceso de autenticación OAuth 2.0
   - Almacena el token en 'token.json' para usos posteriores
   - Refresca automáticamente el token cuando expira

#### Endpoints utilizados

1. `files().list()`:
   - Lista los archivos del usuario
   - Parámetros utilizados:
     - `pageSize`: 1000 archivos por página
     - `fields`: Campos solicitados:
       - `id`: Identificador único del archivo
       - `name`: Nombre del archivo
       - `mimeType`: Tipo de archivo
       - `owners.emailAddress`: Email del propietario
       - `shared`: Estado de compartición
       - `modifiedTime`: Última modificación

2. `permissions().delete()`:
   - Utilizado para remover el acceso público (`anyoneWithLink`)
   - Parámetros:
     - `fileId`: ID del archivo
     - `permissionId`: 'anyoneWithLink' para acceso público

3. `about().get()`:
   - Obtiene información sobre el usuario autenticado
   - Campo solicitado: `user` para obtener el email

### 🧪 Tests de la aplicación

    tests/
    │
    ├── conftest.py   #Configuracion de pytest  
    ├── test_db.py    #Pruebas de la base de datos
    ├── test_drive.py   #Pruebas de manejos de archivos de Drive e interaccion con la API
    ├── test_email.py   #Pruebas para el envio de correos     
 
1. Ejecutar los tests:
   ```bash
   pytest tests/ --disable-warnings -v

### ⚠️ Nota Importante
La aplicación está actualmente en estado de desarrollo/testing, por lo cual no ha pasado el proceso de verificación de Google. Esto implica que: 
- Solo puede ser utilizada con hasta 100 usuarios de prueba
- Al autenticarse, el usuario va a ver una advertencia de "App no verificada"
- Se deberá usar una cuenta que esté registrada como usuario de prueba en el proyecto de Google Cloud

Para testing, se debe:
1. Agregar la cuenta de Google como usuario de prueba en Google Cloud Console
2. Al ver la pantalla de advertencia durante la autenticación, hacer clic en "Continuar" 

### 📝 Autor
Desarrollado por Tatiana Lopez.