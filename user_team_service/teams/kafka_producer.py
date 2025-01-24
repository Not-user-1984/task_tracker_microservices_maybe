from confluent_kafka import Producer

class KafkaProducer:
    def __init__(self, bootstrap_servers='kafka:9092'):
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})

    def send_message(self, topic, key, value):
        """
        Отправляет сообщение в Kafka.
        """
        self.producer.produce(topic, key=key, value=value)
        self.producer.flush()

kafka_producer = KafkaProducer()
