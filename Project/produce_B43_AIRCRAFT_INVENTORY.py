import json
import random
import pandas as pd
from kafka import KafkaProducer

def send_aircraft_info_to_kafka(data_file, broker='localhost:9092', topic='aircraft_topic'):
    producer = KafkaProducer(bootstrap_servers=broker)
    
    def produce(aircraft_info):
        try:
            message = json.dumps(aircraft_info)
            key = f"{random.randrange(999999)}".encode()
            future = producer.send(topic, key=key, value=message.encode())
            future.get(timeout=10)  # Wait for send confirmation
            print("Message sent:", message)
        except Exception as e:
            print("Failed to send message:", e)

    data = pd.read_csv(data_file, encoding='latin1')
    for _, row in data.iterrows():
        aircraft_info = {
            "MANUFACTURE_YEAR": row['MANUFACTURE_YEAR'],
            "TAIL_NUM": row['TAIL_NUM'],
            "NUMBER_OF_SEATS": row['NUMBER_OF_SEATS']
        }
        produce(aircraft_info)

if __name__ == "__main__":
    send_aircraft_info_to_kafka('data/B43_AIRCRAFT_INVENTORY.csv')
