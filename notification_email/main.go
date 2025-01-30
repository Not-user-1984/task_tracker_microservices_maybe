package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"sync"

	_ "github.com/mattn/go-sqlite3"
	"github.com/joho/godotenv"
	"github.com/segmentio/kafka-go"
	"gopkg.in/gomail.v2"
)

const AllowedEmail = "dmitri.pluzhnikov@yandex.ru"

type KafkaMessage struct {
	Schema  Schema  `json:"schema"`
	Payload Payload `json:"payload"`
}

type Schema struct {
	Type     string  `json:"type"`
	Fields   []Field `json:"fields"`
	Optional bool    `json:"optional"`
	Name     string  `json:"name"`
}

type Field struct {
	Type     string `json:"type"`
	Optional bool   `json:"optional"`
	Field    string `json:"field"`
	Name     string `json:"name"`
	Version  int    `json:"version"`
}

type Payload struct {
	ID          int64  `json:"id"`
	ProjectID   int64  `json:"project_id"`
	TeamID      int64  `json:"team_id"`
	UserID      int64  `json:"user_id"`
	ProjectName string `json:"project_name"`
	TeamName    string `json:"team_name"`
	UserOID     string `json:"user_oid"`
	UserEmail   string `json:"user_email"`
	UserName    string `json:"user_name"`
	UserRole    string `json:"user_role"`
	ProjectOID  string `json:"project_oid"`
	TeamOID     string `json:"team_oid"`
	Op          string `json:"__op"`
	TsMs        int64  `json:"__ts_ms"`
}

var (
	mu sync.Mutex
	db *sql.DB
)

func main() {
	// Загрузка переменных из .env
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Ошибка при загрузке .env файла")
	}

	// Получаем пароль из переменных окружения
	emailPassword := os.Getenv("EMAIL_PASSWORD")
	if emailPassword == "" {
		log.Fatal("EMAIL_PASSWORD не задан в .env файле")
	}

	// Инициализация базы данных
	db, err = initDB()
	if err != nil {
		log.Fatalf("Ошибка инициализации базы данных: %v", err)
	}
	defer db.Close()

	// Настройка Kafka consumer
	r := kafka.NewReader(kafka.ReaderConfig{
		Brokers:   []string{"kafka:9092"},
		Topic:     "django_db.public.teams_userassignment",
		Partition: 0,
		MinBytes:  10e3, // 10KB
		MaxBytes:  10e6, // 10MB
	})

	for {
		m, err := r.ReadMessage(context.Background())
		if err != nil {
			log.Fatalf("Ошибка при чтении сообщения: %v", err)
		}

		var msg KafkaMessage
		if err := json.Unmarshal(m.Value, &msg); err != nil {
			log.Printf("Ошибка при парсинге сообщения: %v", err)
			continue
		}

		email := msg.Payload.UserEmail
		userOID := msg.Payload.UserOID

		// Ограничение: отправляем только для "dmitri.pluzhnikov@yandex.ru"
		if email != AllowedEmail {
			fmt.Printf("Пропуск email: %s (не разрешен для отправки)\n", email)
			continue
		}

		// Проверяем, был ли уже обработан этот UserOID
		if isProcessed(userOID) {
			fmt.Printf("Пропуск UserOID: %s (уже обработан)\n", userOID)
			continue
		}

		// Передаем emailPassword в sendEmail
		status := sendEmail(email, userOID, emailPassword)

		// Запись email, userOID и статуса в SQLite
		saveEmailStatus(email, userOID, status)

		fmt.Printf("Email: %s, UserOID: %s, Status: %s\n", email, userOID, status)
	}
}

// Инициализация базы SQLite
func initDB() (*sql.DB, error) {
	db, err := sql.Open("sqlite3", "emails.db")
	if err != nil {
		return nil, err
	}

	// Создание таблицы, если её нет
	query := `CREATE TABLE IF NOT EXISTS email_status (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		email TEXT NOT NULL,
		user_oid TEXT NOT NULL UNIQUE,
		status TEXT NOT NULL
	);`
	_, err = db.Exec(query)
	if err != nil {
		return nil, err
	}

	return db, nil
}

// Функция отправки email
func sendEmail(email, userOID, emailPassword string) string {
	m := gomail.NewMessage()
	m.SetHeader("From", "deman.tmb.68@gmail.com")
	m.SetHeader("To", email)
	m.SetHeader("Subject", "Test Email")
	m.SetBody("text/plain", fmt.Sprintf("User OID: %s", userOID))

	d := gomail.NewDialer("smtp.gmail.com", 587, "deman.tmb.68@gmail.com", emailPassword)

	if err := d.DialAndSend(m); err != nil {
		log.Printf("Ошибка при отправке email: %v", err)
		return "Failed"
	}

	return "Success"
}

// Запись email, userOID и статуса в базу SQLite
func saveEmailStatus(email, userOID, status string) {
	mu.Lock()
	defer mu.Unlock()

	stmt, err := db.Prepare("INSERT INTO email_status (email, user_oid, status) VALUES (?, ?, ?)")
	if err != nil {
		log.Printf("Ошибка при подготовке запроса: %v", err)
		return
	}
	defer stmt.Close()

	_, err = stmt.Exec(email, userOID, status)
	if err != nil {
		log.Printf("Ошибка при записи в базу: %v", err)
	}
}

// Проверка, был ли уже обработан этот UserOID
func isProcessed(userOID string) bool {
	var count int
	err := db.QueryRow("SELECT COUNT(*) FROM email_status WHERE user_oid = ?", userOID).Scan(&count)
	if err != nil {
		log.Printf("Ошибка при проверке UserOID: %v", err)
		return false
	}
	return count > 0
}