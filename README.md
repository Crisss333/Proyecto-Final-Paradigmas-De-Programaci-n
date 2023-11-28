# Proyecto de Visualización de Datos del Titanic

Este proyecto presenta una visualización interactiva de los datos de los pasajeros del Titanic. Utiliza Flask como backend para servir los datos y Chart.js en el frontend para las representaciones gráficas.

# Estructura del Proyecto
Backend: Contiene el código de Flask que procesa y sirve los datos del Titanic.
Frontend: Contiene los archivos HTML y JavaScript para visualizar los datos utilizando Chart.js.
Base de datos: Archivo CSV con los datos del Titanic.

# Preparación del Proyecto
Antes de ejecutar el proyecto, es importante preparar y organizar los archivos correctamente.

# Organización de Archivos
Descarga o clona el repositorio a tu máquina local.
Asegúrate de tener las siguientes carpetas y archivos:
Una carpeta Backend que contiene el código de Flask (app.py y otras dependencias).
Una carpeta Frontend que contiene los archivos HTML y JavaScript.
El archivo de base de datos del Titanic (usualmente un archivo .csv).

# Configuración del Entorno
Es recomendable usar un entorno virtual para instalar las dependencias. Puedes crear uno con los siguientes comandos:

bash
Copy code

# Crear un entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate

# En Unix o MacOS:
source venv/bin/activate

# Instalación de Dependencias
Instala las dependencias necesarias utilizando pip:

bash
Copy code

pip install flask pandas

# Ejecución del Servidor Flask
Para ejecutar el servidor Flask, sigue estos pasos:

Navega a la carpeta Backend.

Asegúrate de que el archivo .csv con los datos del Titanic esté accesible por el script de Flask, ajusta la ruta en el código si es necesario.

Ejecuta el siguiente comando:

bash
Copy code
python app.py
Esto iniciará el servidor en localhost en el puerto 5000.

# Acceso a la Interfaz Web
Una vez que el servidor esté corriendo, sigue estos pasos:

Abre tu navegador.
Navega a http://localhost:5000.
Aquí podrás ver la interfaz web y los gráficos generados con los datos del Titanic.
