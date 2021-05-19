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