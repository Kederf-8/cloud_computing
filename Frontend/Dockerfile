# Usa una immagine Nginx per servire i file statici
FROM nginx:alpine

# Setta la directory di lavoro
WORKDIR /usr/share/nginx/html

# Copia i file statici (HTML, JS, CSS) nella directory di Nginx
COPY . .

# Espone la porta 80
EXPOSE 80

# Avvia Nginx
CMD ["nginx", "-g", "daemon off;"]
