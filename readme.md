# Django App

This is a Django app that provides [brief description of the app].

## Installation and Setup

### Manual Installation

1. Clone the repository:

   git clone <repository_url>

2. Change to the project directory:

   cd <project_directory>

3. Create a virtual environment:

   python -m venv env

4. Activate the virtual environment:

   - For Windows:

     .\env\Scripts\activate

   - For Unix or Linux:

     source env/bin/activate

5. Install the dependencies:

   pip install -r requirements.txt

6. Apply database migrations:

   python manage.py migrate

7. Create a superuser (optional):

   python manage.py createsuperuser

8. Start the development server:

   python manage.py runserver

9. Access the app at http://localhost:8000/.

### Docker Installation

1. Install Docker on your machine following the official Docker documentation: https://docs.docker.com/get-docker/

2. Clone the repository:

   git clone <repository_url>

3. Change to the project directory:

   cd <project_directory>

4. Build the Docker image:

   docker build -t django-app .

5. Run the Docker container:

   docker run -d -p 8000:8000 django-app

6. Access the app at http://localhost:8000/.

## Running Tests

1. Manual Testing:

   - Activate the virtual environment (if not already activated):

     - For Windows:

       .\env\Scripts\activate

     - For Unix or Linux:

       source env/bin/activate

   - Run the tests:

     python manage.py test

2. Docker Testing:

   - Run the tests inside the Docker container:

     docker exec -it <container_id> python manage.py test

## URLS

- /admin/ 
    - for Administrators and super users managment
- /auth/login/
    - method: POST
    - receives: email: str, password: str
    - return access_token and refresh_token
- /auth/register
    - method: POST
    - receives: name: str, email: str, password: str
    - return user
- /auth/refresh/  
    - method: POST
    - receives jwt
    - returns access_token
- /api/task/     - need jwt on headers
    - method: POST
    - receives: title: str, description: str
    - returns task
    -
    - method: GET
    - accepts: query params: title, description, created_at
    - return list of task
- /api/task/<id:int> - need jwt on headers
    - method: GET
    - returns task
    - 
    - method PUT
    - receives: title:str, description:str
    - returns task
    - 
    - method DELETE
    - returns message
- /api/task/<id:int>/complete - need jwt on headers
    - method: PUT
    - returns task

## CONDICIONES
# Invera ToDo-List Challenge (Python/Django Jr-SSr)

El propósito de esta prueba es conocer tu capacidad para crear una pequeña aplicación funcional en un límite de tiempo. A continuación, encontrarás las funciones, los requisitos y los puntos clave que debés tener en cuenta durante el desarrollo.

## Qué queremos que hagas:

- El Challenge consiste en crear una aplicación web sencilla que permita a los usuarios crear y mantener una lista de tareas.
- La entrega del resultado será en un nuevo fork de este repo y deberás hacer una pequeña demo del funcionamiento y desarrollo del proyecto ante un super comité de las más grandes mentes maestras de Invera, o a un par de devs, lo que sea más fácil de conseguir.
- Podes contactarnos en caso que tengas alguna consulta.

## Objetivos:

El usuario de la aplicación tiene que ser capaz de:

- Autenticarse
- Crear una tarea
- Eliminar una tarea
- Marcar tareas como completadas
- Poder ver una lista de todas las tareas existentes
- Filtrar/buscar tareas por fecha de creación y/o por el contenido de la misma

## Qué evaluamos:

- Desarrollo utilizando Python, Django. No es necesario crear un Front-End, pero sí es necesario tener una API que permita cumplir con los objetivos de arriba.
- Uso de librerías y paquetes estandares que reduzcan la cantidad de código propio añadido.
- Calidad y arquitectura de código. Facilidad de lectura y mantenimiento del código. Estándares seguidos.
- [Bonus] Manejo de logs.
- [Bonus] Creación de tests (unitarias y de integración)
- [Bonus] Unificar la solución propuesta en una imagen de Docker por repositorio para poder ser ejecutada en cualquier ambiente (si aplica para full stack).

## Requerimientos de entrega:

- Hacer un fork del proyecto y pushearlo en github. Puede ser privado.
- La solución debe correr correctamente.
- El Readme debe contener todas las instrucciones para poder levantar la aplicación, en caso de ser necesario, y explicar cómo se usa.
- Disponibilidad para realizar una pequeña demo del proyecto al finalizar el challenge.
- Tiempo para la entrega: Aproximadamente 7 días.