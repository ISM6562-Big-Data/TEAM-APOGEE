import json
import random
import pandas as pd
from kafka import KafkaProducer
 
def send_flight_info_to_kafka(data_file, broker='localhost:9092', topic='weather_topic'):
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
            "STATION": row['STATION'],
            "NAME": row['NAME'],
            "DATE": row['DATE'],
            "AWND": row['AWND'],
            "PGTM": row['PGTM'],
            "PRCP": row['PRCP'],
            "SNOW": row['SNOW'],
            "SNWD": row['SNWD'],
            "TAVG": row['TAVG'],
            "TMAX": row['TMAX'],
            "TMIN": row['TMIN'],
            "WDF2": row['WDF2'],
            "WDF5": row['WDF5'],
            "WSF2": row['WSF2'],
            "WSF5": row['WSF5'],
            "WT01": row['WT01'],
            "WT02": row['WT02'],
            "WT03": row['WT03'],
            "WT04": row['WT04'],
            "WT05": row['WT05'],
            "WT06": row['WT06'],
            "WT07": row['WT07'],
            "WT08": row['WT08'],
            "WT09": row['WT09'],
            "WESD": row['WESD'],
            "WT10": row['WT10'],
            "PSUN": row['PSUN'],
            "TSUN": row['TSUN'],
            "SN32": row['SN32'],
            "SX32": row['SX32'],
            "TOBS": row['TOBS'],
            "WT11": row['WT11']
        }
        produce(flight_info)
 
if __name__ == "__main__":
    send_flight_info_to_kafka('data/airport_weather_2019.csv')