# Usa una imagen base de Python
FROM python:3.8.10

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el codigo de la aplicacion al contenedor
COPY . /app

# Instala las dependencias
RUN pip install -r requirements.txt

# Expone el puerto en el que se ejecuta la aplicacion (ajusta el puerto segun tus necesidades)
EXPOSE 8082

# Comando para ejecutar la aplicacion
# CMD ["flask", "run", "--port=8082"]

# Comando para ejecutar la aplicacion Flask
CMD ["flask", "run", "--host=0.0.0.0"]
