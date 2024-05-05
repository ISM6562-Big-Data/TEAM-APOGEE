import json
import random
import pandas as pd
from kafka import KafkaProducer
 
def send_flight_info_to_kafka(data_file, broker='localhost:9092', topic='on6_topic'):
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
            "MONTH": row['MONTH'],
            "DAY_OF_MONTH": row['DAY_OF_MONTH'],
            "DAY_OF_WEEK": row['DAY_OF_WEEK'],
            "OP_UNIQUE_CARRIER": row['OP_UNIQUE_CARRIER'],
            "TAIL_NUM": row['TAIL_NUM'],
            "OP_CARRIER_FL_NUM": row['OP_CARRIER_FL_NUM'],
            "ORIGIN_AIRPORT_ID": row['ORIGIN_AIRPORT_ID'],
            "ORIGIN": row['ORIGIN'],
            "ORIGIN_CITY_NAME": row['ORIGIN_CITY_NAME'],
            "DEST_AIRPORT_ID": row['DEST_AIRPORT_ID'],
            "DEST": row['DEST'],
            "DEST_CITY_NAME": row['DEST_CITY_NAME'],
            "CRS_DEP_TIME": row['CRS_DEP_TIME'],
            "DEP_TIME": row['DEP_TIME'],
            "DEP_DELAY_NEW": row['DEP_DELAY_NEW'],
            "DEP_DEL15": row['DEP_DEL15'],
            "DEP_TIME_BLK": row['DEP_TIME_BLK'],
            "CRS_ARR_TIME": row['CRS_ARR_TIME'],
            "ARR_TIME": row['ARR_TIME'],
            "ARR_DELAY_NEW": row['ARR_DELAY_NEW'],
            "ARR_TIME_BLK": row['ARR_TIME_BLK'],
            "CANCELLED": row['CANCELLED'],
            "CANCELLATION_CODE": row['CANCELLATION_CODE'],
            "CRS_ELAPSED_TIME": row['CRS_ELAPSED_TIME'],
            "ACTUAL_ELAPSED_TIME": row['ACTUAL_ELAPSED_TIME'],
            "DISTANCE": row['DISTANCE'],
            "DISTANCE_GROUP": row['DISTANCE_GROUP'],
            "CARRIER_DELAY": row['CARRIER_DELAY'],
            "WEATHER_DELAY": row['WEATHER_DELAY'],
            "NAS_DELAY": row['NAS_DELAY'],
            "SECURITY_DELAY": row['SECURITY_DELAY'],
            "LATE_AIRCRAFT_DELAY": row['LATE_AIRCRAFT_DELAY']
        }
        produce(flight_info)
 
if __name__ == "__main__":
    send_flight_info_to_kafka('data/ONTIME_REPORTING_06.csv')