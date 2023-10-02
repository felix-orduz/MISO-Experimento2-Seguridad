# Usamos una imagen base de Python
FROM python:3.8-slim

# Establecer un directorio de trabajo
WORKDIR /app

ENV FLASK_ENV=development

# Copiamos el archivo de requerimientos para instalar las dependencias
COPY requirements.txt requirements.txt

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código de la aplicación al contenedor
COPY . .

# Exponemos el puerto 5000 para que podamos acceder a él
EXPOSE 5000

# Ejecutamos la aplicación
#CMD ["python", "app.py"]

CMD ["flask", "run", "--host=0.0.0.0"]