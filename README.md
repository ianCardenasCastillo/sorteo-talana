# Sorteo Talana

Sorteo Talana en conjunto con Incoludidos Papel desarrollaron una Servicio para el sorteo de abastecimiento de papel higenico de por vida para el ganador.

## Endpoints

### Registrar Participante
Este endpoint permite registrar a un participante para el sorteo, en este paso se solicitara el rut, nombre y correo electronico que se debe enviar de la siguiente manera

Metodo: POST
Endpoint: /api/usuario
Cuerpo:
```
{
  "rut": "11111111-2",
  "nombre": "Pedro Sanchez",
  "correo": "uncorreo@deundominio.algo"
}
```
El resultado es:
```
200 HTTP OK
{
  "id": 27,
  "rut": "11111111-2",
  "nombre": "Pedro Sanchez",
  "correo": "uncorreo@deundominio.algo",
  "password": null,
  "validado": false
}
```

Cuando el correo ya se encuentra registrado el resultado es:
```
500 INTERNAL SERVER ERROR
{
  "correo": [
    "usuario with this correo already exists."
  ]
}
```

Cuando falta un dato:
```
500 INTERNAL SERVER ERROR
{
  "correo": [
    "This field is required."
  ]
}
```

Al finalizar la inscripción del proceso le llegara un correo al participante. En el log del envio del correo debera aparecer algo similar a esto:
```
celery_1  | [2021-05-19 04:11:34,412: INFO/MainProcess] Received task: sorteo.tasks.send_email[9b3e66cb-4c7d-441d-8460-8f4d68af8c1a]
celery_1  | [2021-05-19 04:11:37,541: INFO/ForkPoolWorker-2] Task sorteo.tasks.send_email[9b3e66cb-4c7d-441d-8460-8f4d68af8c1a] succeeded in 3.12683190000007s: 'Email Sended'
```

_Para los fines de desarrollo se habilito una cuenta en [Ethereal](https://ethereal.email) donde se tiene una cuenta y este servicio intercepta los correos enviados_
_El usuario es: maymie82@ethereal.email y la password: YwT9Xxz8ypzyg2c96j_
_Y pueden ver en la sección de [Mensajes](https://ethereal.email/messages) los correos interceptados_

#### Configuración Correo

```
# Setting for Sending Emails
EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.ethereal.email'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'maymie82@ethereal.email'
EMAIL_HOST_PASSWORD = 'YwT9Xxz8ypzyg2c96j'
```

### Confirmar Correo

Luego de que el participante se registre en el sorteo, le llegara el correo donde encontrara un enlace para confirmar su correo

Metodo: GET
Endpoint: /api/confirm-email/{id-usuario}

Al ingresar obtendra el mensaje "Confirmado Correctamente"
En caso de que se vuelva a ingresar al enlace obtendra el mensaje "Correo ya se encuentra validado"

### Crear Password

Cuando el participante confirma su correo, ya podra estar habilitado para generar su contraseña. 

Metodo: POST
Endpoint: /api/create-password
Cuerpo:
```
{
  "id": 27,
  "rut": "11111111-2",
  "nombre": "Pedro Sanchez",
  "correo": "uncorreo@deundominio.algo",
  "password": "1111"
}
```

Si el participante no tiene creada la password obtendra la siguiente respuesta:
```
200 HTTP OK
{
  "msg": "Contraseña Creada"
}
```

Caso contrario, si ya tenia la contraseña creada obtendra la siguiente respuesta:
```
200 HTTP OK
{
  "msg" : "Ya cuenta con una contraseña"
}
```

Si el participante no a confirmado su correo obtendra la siguiente respuesta:
```
200 HTTP OK
{
  "msg" : "Primero debe confirmar su correo"
}
```

### Generar Ganador del Sorteo

Para obtener el ganador del sorteo se dispone del siguiente endpoint:

Metodo: GET
Endpoint: /api/get-winner

El cual si existe al menos 1 participante con su correo confirmado y su password creada obtendra la siguiente respuesta:
```
{
  "ganador": {
    "rut": "11111111-2",
    "nombre": "Pedro Sanchez",
    "correo": "uncorreo@deundominio.algo"
  }
}
```
En caso de que no exista ningun participante con las condiciones de correo confirmado ni password creada obtendra la siguiente respuesta:
```
{
  "msg": "No existen usuarios validos en el sorteo"
}
```

## Base de Datos

La base de datos ocupada es sqlite3 para el almacenamiento de la información que esta ubicada en la carpeta raiz del proyecto

## Despliegue

Para desplegar el servicio de forma local debe realizar un git pull `git pull` cambiar de directorio `cd ./sorteo-talana` y ejecutar `docker-compose up --build`

El despliegue consta de 3 servicios llamados `redis`, `celery` y `api`

Cuando ejecute el comando `docker-compose up --build` debe obtener un resultado similar a:
```
Starting prueba-tecnica-talana_redis_1 ... done
Recreating talana-sorteo               ... done
Recreating prueba-tecnica-talana_celery_1 ... done
Attaching to prueba-tecnica-talana_redis_1, talana-sorteo, prueba-tecnica-talana_celery_1
redis_1   | 1:C 19 May 2021 04:44:04.369 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis_1   | 1:C 19 May 2021 04:44:04.369 # Redis version=6.2.3, bits=64, commit=00000000, modified=0, pid=1, just started
redis_1   | 1:C 19 May 2021 04:44:04.369 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
redis_1   | 1:M 19 May 2021 04:44:04.370 * monotonic clock: POSIX clock_gettime
redis_1   | 1:M 19 May 2021 04:44:04.370 * Running mode=standalone, port=6379.
redis_1   | 1:M 19 May 2021 04:44:04.370 # Server initialized
redis_1   | 1:M 19 May 2021 04:44:04.370 * Loading RDB produced by version 6.2.3
redis_1   | 1:M 19 May 2021 04:44:04.371 * RDB age 2178 seconds
redis_1   | 1:M 19 May 2021 04:44:04.371 * RDB memory usage when created 0.77 Mb
redis_1   | 1:M 19 May 2021 04:44:04.371 * DB loaded from disk: 0.000 seconds
redis_1   | 1:M 19 May 2021 04:44:04.371 * Ready to accept connections
talana-sorteo | Watching for file changes with StatReloader
talana-sorteo | Performing system checks...
talana-sorteo |
talana-sorteo | System check identified no issues (0 silenced).
talana-sorteo |
talana-sorteo | You have 26 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, django_celery_results, sessions.
talana-sorteo | Run 'python manage.py migrate' to apply them.
talana-sorteo | May 19, 2021 - 04:44:07
talana-sorteo | Django version 3.2.3, using settings 'talana.settings'
talana-sorteo | Starting development server at http://0.0.0.0:8000/
talana-sorteo | Quit the server with CONTROL-C.
celery_1  | /usr/local/lib/python3.8/site-packages/celery/platforms.py:796: RuntimeWarning: You're running the worker with superuser privileges: this is
celery_1  | absolutely not recommended!
celery_1  |
celery_1  | Please specify a different user using the --uid option.
celery_1  |
celery_1  | User information: uid=0 euid=0 gid=0 egid=0
celery_1  |
celery_1  |   warnings.warn(RuntimeWarning(ROOT_DISCOURAGED.format(
celery_1  |  
celery_1  |  -------------- celery@6cb4b030c235 v5.0.5 (singularity)
celery_1  | --- ***** -----
celery_1  | -- ******* ---- Linux-5.10.25-linuxkit-x86_64-with-glibc2.2.5 2021-05-19 04:44:10
celery_1  | - *** --- * ---
celery_1  | - ** ---------- [config]
celery_1  | - ** ---------- .> app:         talana:0x7f9738191400
celery_1  | - ** ---------- .> transport:   redis://redis:6379/0
celery_1  | - ** ---------- .> results:
celery_1  | - *** --- * --- .> concurrency: 2 (prefork)
celery_1  | -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
celery_1  | --- ***** -----
celery_1  |  -------------- [queues]
celery_1  |                 .> celery           exchange=celery(direct) key=celery
celery_1  |
celery_1  |
celery_1  | [tasks]
celery_1  |   . sorteo.tasks.add
celery_1  |   . sorteo.tasks.mul
celery_1  |   . sorteo.tasks.send_email
celery_1  |   . sorteo.tasks.xsum
celery_1  |   . talana.celery.debug_task
celery_1  |
celery_1  | [2021-05-19 04:44:10,697: INFO/MainProcess] Connected to redis://redis:6379/0
celery_1  | [2021-05-19 04:44:10,705: INFO/MainProcess] mingle: searching for neighbors
celery_1  | [2021-05-19 04:44:11,723: INFO/MainProcess] mingle: all alone
celery_1  | [2021-05-19 04:44:11,738: WARNING/MainProcess] /usr/local/lib/python3.8/site-packages/celery/fixups/django.py:203: UserWarning: Using settings.DEBUG leads to a memory
celery_1  |             leak, never use this setting in production environments!
celery_1  |   warnings.warn('''Using settings.DEBUG leads to a memory
celery_1  |
celery_1  | [2021-05-19 04:44:11,738: INFO/MainProcess] celery@6cb4b030c235 ready.
```

### Docker Compose

```
version: '3.8'

services:
  redis:
    image: redis:alpine
  celery:
    restart: always
    build:
      context: .
    command: celery -A talana worker -l info
    volumes:
      - ./:/src
    environment:
      - DEBUG=1
      - DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
      - CELERY_BROKER=redis://redis:6379/0
      - CELERY_BACKEND=redis://redis:6379/0
    depends_on:
      - redis
      - api
  api:
    container_name: talana-sorteo
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ./:/src
    command: python manage.py runserver 0.0.0.0:8000
``` 

### Dockerfile

```
#Usamos la imagen de python en su versión 3.7.
FROM python:3.8.5

#Seteamos la variable de entorno
ENV PYTHONUNBUFFERED 1

# Dentro del contenedor creamos una carpeta que contendra la app
RUN mkdir /src

# Definimos que la carpeta de trabajo sera el src de nuestro contenedor
WORKDIR /src

# Copía los recursos desde el src local al contenedor en su primera ejecución
COPY ./ /src/

# Instalamos los requerimientos mediante pip install leyendo los requerimientos del txt
RUN pip install -r requirements.txt

RUN python manage.py makemigrations sorteo
RUN python manage.py migrate sorteo
# Al final de esto se debera generar una imagen
```

Luego utilizando [Postman](https://www.postman.com/downloads/) podra testear el servicio.

* **Ian Cárdenas C.** - *Desarrollo* - [ianCardenasCastillo](https://github.com/ianCardenasCastillo)
* **Ian Cárdenas C.** - *Documentación* - [ianCardenasCastillo](https://github.com/ianCardenasCastillo)

---
⌨️ con ❤️ por [Ian Cárdenas C](https://github.com/ianCardenasCastillo) 😊