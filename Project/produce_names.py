import json
import random
import pandas as pd
from kafka import KafkaProducer
 
def send_flight_info_to_kafka(data_file, broker='localhost:9092', topic='names_topic'):
 
    producer = KafkaProducer(bootstrap_servers=broker)
 
    def produce(flight_info):
        try:
            message = json.dumps(flight_info)
            key = f"{random.randrange(999999)}".encode()
            future = producer.send(topic, key=key, value=message.encode())
            future.get(timeout=10)  # Wait for send confirmation
            print("Message sent:", message)
        except Exception as e:
            print("Failed to send message:", e)
 
    data = pd.read_csv(data_file)
 
    for _, row in data.iterrows():
        flight_info = {
            "OP_UNIQUE_CARRIER": row['OP_UNIQUE_CARRIER'],
            "CARRIER_NAME": row['CARRIER_NAME'],
            "AIRLINE_ID": row['AIRLINE_ID']  # Added AIRLINE_ID
        }
        produce(flight_info)
 
if __name__ == "__main__":
    send_flight_info_to_kafka('data/CARRIER_DECODE.csv')