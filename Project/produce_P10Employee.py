import json
import random
import pandas as pd
from kafka import KafkaProducer

def send_airline_data_to_kafka(data_file, broker='localhost:9092', topic='employees'):
    producer = KafkaProducer(bootstrap_servers=broker)

    def produce(airline_data):
        try:
            message = json.dumps(airline_data)
            key = f"{random.randrange(999999)}".encode()
            future = producer.send(topic, key=key, value=message.encode())
            future.get(timeout=10)  # Wait for send confirmation
            print("Message sent:", message)
        except Exception as e:
            print("Failed to send message:", e)

    data = pd.read_csv(data_file)
    for _, row in data.iterrows():
        airline_data = {
            "YEAR": row['YEAR'],
            "AIRLINE_ID": row['AIRLINE_ID'],
            "OP_UNIQUE_CARRIER": row['OP_UNIQUE_CARRIER'],
            "UNIQUE_CARRIER_NAME": row['UNIQUE_CARRIER_NAME'],
            "CARRIER": row['CARRIER'],
            "CARRIER_NAME": row['CARRIER_NAME'],
            "ENTITY": row['ENTITY'],
            "GENERAL_MANAGE": row['GENERAL_MANAGE'],
            "PILOTS_COPILOTS": row['PILOTS_COPILOTS'],
            "OTHER_FLT_PERS": row['OTHER_FLT_PERS'],
            "PASS_GEN_SVC_ADMIN": row['PASS_GEN_SVC_ADMIN'],
            "MAINTENANCE": row['MAINTENANCE'],
            "ARCFT_TRAF_HANDLING_GRP1": row['ARCFT_TRAF_HANDLING_GRP1'],
            "GEN_ARCFT_TRAF_HANDLING": row['GEN_ARCFT_TRAF_HANDLING'],
            "AIRCRAFT_CONTROL": row['AIRCRAFT_CONTROL'],
            "PASSENGER_HANDLING": row['PASSENGER_HANDLING'],
            "CARGO_HANDLING": row['CARGO_HANDLING'],
            "TRAINEES_INTRUCTOR": row['TRAINEES_INTRUCTOR'],
            "STATISTICAL": row['STATISTICAL'],
            "TRAFFIC_SOLICITERS": row['TRAFFIC_SOLICITERS'],
            "OTHER": row['OTHER'],
            "TRANSPORT_RELATED": row['TRANSPORT_RELATED'],
            "TOTAL": row['TOTAL']
        }
        produce(airline_data)

if __name__ == "__main__":
    send_airline_data_to_kafka('data/P10_EMPLOYEES.csv')
