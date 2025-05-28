FROM node:18-alpine

WORKDIR /app
COPY . /app

RUN npm install
RUN npm run build

# Instala 'serve' para servir la app de producción
# RUN npnm install -g serve

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]
