import json
import random
from kafka import KafkaProducer
import pandas as pd

class AirportInfo:
    def __init__(self, airport_seq_id, airport_id, airport, display_airport_name,
                 display_airport_city_name_full, airport_wac, airport_country_name,
                 airport_country_code_iso, airport_state_name, airport_state_code, latitude, longitude):
        self.airport_seq_id = airport_seq_id
        self.airport_id = airport_id
        self.airport = airport
        self.display_airport_name = display_airport_name
        self.display_airport_city_name_full = display_airport_city_name_full
        self.airport_wac = airport_wac
        self.airport_country_name = airport_country_name
        self.airport_country_code_iso = airport_country_code_iso
        self.airport_state_name = airport_state_name
        self.airport_state_code = airport_state_code
        self.latitude = latitude
        self.longitude = longitude

    def to_json(self):
        return json.dumps({
            "AIRPORT_SEQ_ID": self.airport_seq_id,
            "AIRPORT_ID": self.airport_id,
            "AIRPORT": self.airport,
            "DISPLAY_AIRPORT_NAME": self.display_airport_name,
            "DISPLAY_AIRPORT_CITY_NAME_FULL": self.display_airport_city_name_full,
            "AIRPORT_WAC": self.airport_wac,
            "AIRPORT_COUNTRY_NAME": self.airport_country_name,
            "AIRPORT_COUNTRY_CODE_ISO": self.airport_country_code_iso,
            "AIRPORT_STATE_NAME": self.airport_state_name,
            "AIRPORT_STATE_CODE": self.airport_state_code,
            "LATITUDE": self.latitude,
            "LONGITUDE": self.longitude
        })

class AirportInfoKafkaLogger:
    def __init__(self, broker: str = 'localhost:9092'):
        self.producer = KafkaProducer(bootstrap_servers=broker)

    def produce(self, airport_info: AirportInfo):
        try:
            future = self.producer.send(topic='airport_data_topic', key=f"{random.randrange(999999)}".encode(), value=airport_info.to_json().encode())
            record_metadata = future.get(timeout=10)
            print("Message sent:", airport_info.to_json())
        except Exception as e:
            print("Failed to send message:", e)

if __name__ == "__main__":
    producer = AirportInfoKafkaLogger()
    data = pd.read_csv('T_MASTER_CORD 2.csv')
    for index, row in data.iterrows():
        print(row['AIRPORT_SEQ_ID'])
    # Creating an instance of AirportInfo with predefined data
        airport_info = AirportInfo(
            airport_seq_id=row['AIRPORT_SEQ_ID'],
            airport_id=row['AIRPORT_ID'],
            airport=row['AIRPORT'],
            display_airport_name=row['DISPLAY_AIRPORT_NAME'],
            display_airport_city_name_full=row['DISPLAY_AIRPORT_CITY_NAME_FULL'],
            airport_wac=row['AIRPORT_WAC'],
            airport_country_name=row['AIRPORT_COUNTRY_NAME'],
            airport_country_code_iso=row['AIRPORT_COUNTRY_CODE_ISO'],
            airport_state_name=row['AIRPORT_STATE_NAME'],
            airport_state_code=row['AIRPORT_STATE_CODE'],
            latitude=row['LATITUDE'],
            longitude=row['LONGITUDE']
        )
        producer.produce(airport_info)


