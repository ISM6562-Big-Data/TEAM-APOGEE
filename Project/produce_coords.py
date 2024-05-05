import json
import random
import pandas as pd
from kafka import KafkaProducer
 
def send_flight_info_to_kafka(data_file, broker='localhost:9092', topic='coords_topic'):
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
            "ORIGIN_AIRPORT_ID": row['ORIGIN_AIRPORT_ID'],
            "DISPLAY_AIRPORT_NAME": row['DISPLAY_AIRPORT_NAME'],
            "LATITUDE": row['LATITUDE'],
            "LONGITUDE": row['LONGITUDE']
        }
        produce(flight_info)
 
if __name__ == "__main__":
    send_flight_info_to_kafka('data/AIRPORT_COORDINATES.csv')