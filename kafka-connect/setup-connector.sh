#!/bin/bash

# Ожидание готовности Kafka Connect
echo "Waiting for Kafka Connect to start..."
while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' http://debezium-connector:8083/connectors)" != "200" ]]; do
  sleep 5
done
echo "Kafka Connect is ready!"

# Конфигурация коннектора
CONNECTOR_CONFIG=$(cat <<EOF
{
  "name": "teams-userassignment-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.user": "django_user",
    "database.dbname": "django_db",
    "transforms.extractKey.field": "id",
    "slot.name": "debezium_slot",
    "publication.name": "debezium_pub",
    "transforms": "unwrap,extractKey",
    "database.server.name": "db_django",
    "transforms.extractKey.type": "org.apache.kafka.connect.transforms.ExtractField\$Key",
    "database.port": "5432",
    "plugin.name": "pgoutput",
    "topic.prefix": "django_db",
    "database.hostname": "db_django",
    "database.password": "django_password",
    "transforms.unwrap.drop.tombstones": "false",
    "transforms.unwrap.add.fields": "op,ts_ms",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
    "table.include.list": "public.teams_userassignment"
  }
}
EOF
)

# Отправка конфигурации в Kafka Connect
echo "Setting up Debezium connector..."
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" \
  http://debezium-connector/connectors/ -d "$CONNECTOR_CONFIG"

echo "Debezium connector setup complete!"