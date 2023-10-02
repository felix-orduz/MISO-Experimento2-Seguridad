#!/bin/bash

# Variables
GITHUB_USERNAME="felix-orduz"
GITHUB_REPO_NAME="experimento2-arquitectura"
IMAGE_NAME_USERS="ms_users_image"
IMAGE_NAME_PAGOS="ms_pagos_image"
VERSION="latest"  # Puedes cambiar esto por el número de versión que desees.

# 1. Autenticarse en GitHub Container Registry
echo "Introduce tu token de acceso personal de GitHub:"
read -s GITHUB_TOKEN
echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USERNAME --password-stdin

# 2 y 3. Construir y etiquetar la imagen Docker para ms_users
docker build -t ghcr.io/$GITHUB_USERNAME/$IMAGE_NAME_USERS:$VERSION ./ms_users

# 4. Publicar la imagen Docker para ms_users
docker push ghcr.io/$GITHUB_USERNAME/$IMAGE_NAME_USERS:$VERSION

# 2 y 3. Construir y etiquetar la imagen Docker para ms_pagos
docker build -t ghcr.io/$GITHUB_USERNAME/$IMAGE_NAME_PAGOS:$VERSION ./ms_pagos

# 4. Publicar la imagen Docker para ms_pagos
docker push ghcr.io/$GITHUB_USERNAME/$IMAGE_NAME_PAGOS:$VERSION

echo "Imágenes publicadas exitosamente en GitHub Container Registry."
