#!/bin/bash

# Definir los nombres de las imágenes
IMAGE_NAME_USERS="ms_users_image"
IMAGE_NAME_PAGOS="ms_pagos_image"

# Navegar al directorio ms_users y construir la imagen
cd ms_users
docker build -t $IMAGE_NAME_USERS .

# Verificar si la construcción fue exitosa
if [ $? -ne 0 ]; then
    echo "Error construyendo la imagen $IMAGE_NAME_USERS"
    exit 1
fi

# Navegar al directorio ms_pagos y construir la imagen
cd ../ms_pagos
docker build -t $IMAGE_NAME_PAGOS .

# Verificar si la construcción fue exitosa
if [ $? -ne 0 ]; then
    echo "Error construyendo la imagen $IMAGE_NAME_PAGOS"
    exit 1
fi

echo "Ambas imágenes se construyeron exitosamente"
