# Usa una immagine di base Node.js per costruire il frontend
FROM node:14 AS build

# Setta la directory di lavoro
WORKDIR /app

# Copia i file package.json e package-lock.json
COPY package*.json ./

# Installa le dipendenze
RUN npm install

# Copia il resto del codice sorgente
COPY . .

# Compila l'app
RUN npm run build

# Usa una immagine Nginx per servire l'app compilata
FROM nginx:alpine

# Copia i file compilati nella directory di Nginx
COPY --from=build /app/build /usr/share/nginx/html

# Copia il file di configurazione di Nginx (se ne hai uno)
# COPY nginx.conf /etc/nginx/nginx.conf

# Espone la porta 80
EXPOSE 80

# Avvia Nginx
CMD ["nginx", "-g", "daemon off;"]
