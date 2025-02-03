# Используем образ с Node.js для стадии разработки
FROM node:18 AS development-stage
WORKDIR /app

# Копируем package.json и устанавливаем зависимости
COPY package*.json ./
RUN npm install

# Копируем все исходники в контейнер
COPY . .

# Запускаем сервер Vue в режиме разработки
CMD ["npm", "run", "serve"]
