# Используем официальный образ Go
FROM golang:1.21-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем Air для hot-reload
RUN go install github.com/cosmtrek/air@v1.41.0


# Устанавливаем gcc и другие необходимые инструменты для компиляции
RUN apk add --no-cache build-base


# Включаем CGo, чтобы поддерживать go-sqlite3
ENV CGO_ENABLED=1

# Копируем go.mod и go.sum для установки зависимостей
COPY go.mod go.sum ./

# Устанавливаем зависимости
RUN go mod download

# Копируем исходный код
COPY . .

# Открываем порт, на котором будет работать приложение
EXPOSE 8080

# Запускаем приложение с использованием Air
CMD ["air", "-c", "air.toml"]