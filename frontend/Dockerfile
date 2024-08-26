# Dockerfile para nextjs-front
FROM node:22.7.0-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias de Node.js
RUN npm install

# Copiar el resto de los archivos de la aplicación
COPY . .

# Hacer ejecutable el script init.sh
RUN chmod +x init.sh

# Exponer el puerto 3000
EXPOSE 3000

# Comando por defecto para ejecutar el script init.sh
 CMD ["./init.sh"]

# CMD ["sh", "./init.sh"]