import json
from kafka import KafkaConsumer

class PageViewKafkaConsumer:
    def __init__(self, broker: str = 'localhost:9092'):
        self.consumer = KafkaConsumer(
            'test-topic1',
            bootstrap_servers=broker,
            auto_offset_reset='earliest',  # start reading at the earliest message
            group_id='my-group',  # consumer group id
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # deserialize JSON messages
        )

    def consume(self):
        try:
            for message in self.consumer:
                # Since we set up the deserializer, `message.value` is already a dictionary
                print(f"Received message: {message.value}")
                if 'test-topic1' in message.value:  # Adjust key to match your actual message structure
                    print(f"URL: {message.value['test-topic1']['url']}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    consumer = PageViewKafkaConsumer()
    consumer.consume()
