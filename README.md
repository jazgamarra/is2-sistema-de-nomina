# is2-sistema-de-nomina
Sistema de nominas y pago de salarios para la asignatura Ingenieria de Software II. 

## Para crear el proyecto: 
**1. Crear y activar un entorno virtual**
En windows, la creacion se realiza con el comando python -m venv venv. Para activarlo, ingresar a la carpeta venv\Scripts y ejecutar el comando activate

**2. Instalar los requerimientos**

Para este paso se necesita tener pip para manejar los paquetes. Los requerimientos se instalan una vez activado el entorno virtual, con el comando pip install -r requirements.txt

**3. Conectar la base de datos**

Es necesario tener una base de datos PostgreSQL vacia llamada `Nomina` para el siguiente paso.
Ejecutar el comando `python manage.py makemigrations` para crear las migraciones y `python manage.py migrate` para aplicarlas a la base de datos. 

**4. Correr el proyecto**

Ejecutar el comando `python manage.py runserver` y visitar `/login`