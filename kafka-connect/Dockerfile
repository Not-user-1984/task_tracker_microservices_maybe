FROM debezium/connect:2.7.3.Final

# Установка коннектора для PostgreSQL
RUN curl -L -o /kafka/connect/debezium-connector-postgres.tar.gz https://repo1.maven.org/maven2/io/debezium/debezium-connector-postgres/2.7.3.Final/debezium-connector-postgres-2.7.3.Final-plugin.tar.gz && \
    tar -xzf /kafka/connect/debezium-connector-postgres.tar.gz -C /kafka/connect && \
    rm /kafka/connect/debezium-connector-postgres.tar.gz

# Добавление JAR-файла для трансформации
RUN curl -L -o /kafka/libs/debezium-core-2.7.3.Final.jar \
    https://repo1.maven.org/maven2/io/debezium/debezium-core/2.7.3.Final/debezium-core-2.7.3.Final.jar