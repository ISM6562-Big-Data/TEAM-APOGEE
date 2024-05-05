import json
import random
from kafka import KafkaProducer
import pandas as pd

class FlightInfo:
    def __init__(self, op_unique_carrier, carrier_name, origin_airport_id, service_class,
                 rev_acrft_dep_perf_510, rev_pax_enp_110):
        self.op_unique_carrier = op_unique_carrier
        self.carrier_name = carrier_name
        self.origin_airport_id = origin_airport_id
        self.service_class = service_class
        self.rev_acrft_dep_perf_510 = rev_acrft_dep_perf_510
        self.rev_pax_enp_110 = rev_pax_enp_110

    def to_json(self):
        return json.dumps({
            "OP_UNIQUE_CARRIER": self.op_unique_carrier,
            "CARRIER_NAME": self.carrier_name,
            "ORIGIN_AIRPORT_ID": self.origin_airport_id,
            "SERVICE_CLASS": self.service_class,
            "REV_ACRFT_DEP_PERF_510": self.rev_acrft_dep_perf_510,
            "REV_PAX_ENP_110": self.rev_pax_enp_110
        })

class FlightInfoKafkaLogger:
    def __init__(self, broker: str = 'localhost:9092'):
        self.producer = KafkaProducer(bootstrap_servers=broker)

    def produce(self, flight_info: FlightInfo):
        try:
            future = self.producer.send(topic='passengers_topic', key=f"{random.randrange(999999)}".encode(), value=flight_info.to_json().encode())
            record_metadata = future.get(timeout=10)
            print("Message sent:", flight_info.to_json())
        except Exception as e:
            print("Failed to send message:", e)

if __name__ == "__main__":
    producer = FlightInfoKafkaLogger()
    data = pd.read_csv('T3_AIR_CARRIER_SUMMARY_AIRPORT_ACTIVITY_2019.csv')
    for index, row in data.iterrows():
        # Creating an instance of FlightInfo with data from the row
        flight_info = FlightInfo(
            op_unique_carrier=row['OP_UNIQUE_CARRIER'],
            carrier_name=row['CARRIER_NAME'],
            origin_airport_id=row['ORIGIN_AIRPORT_ID'],
            service_class=row['SERVICE_CLASS'],
            rev_acrft_dep_perf_510=row['REV_ACRFT_DEP_PERF_510'],
            rev_pax_enp_110=row['REV_PAX_ENP_110']
        )
        producer.produce(flight_info)
