from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import random
# Generieren und schreiben Sie zufällige Datenpunkte
import time

# Ihre vorhandenen Daten
username = 'admin'
password = 'Administrator1'
token = '2toOHIzhKsi51grUHQ4TUZbarf5z7ig69HfhjcCfthBhj4Am4Tf36TDMHPCLcvl1kyH8DCI9fN6JDUVAIYrNAg'
bucket = "Flight Logs"
org = "LEVITUM"

# Erstellen Sie den InfluxDB-Client
client = InfluxDBClient(url="http://localhost:8086", token=token, username=username, password=password)

# Erstellen Sie eine Write-API, die Punkt-Daten schreibt
write_api = client.write_api(write_options=SYNCHRONOUS)

# Erzeugen Sie zufällige Datenpunkte
def generate_random_data():
    measurement = 'your_measurement'
    tags = {'tag1': 'value1', 'tag2': 'value2'}
    fields = {'field1': random.randint(0, 100), 'field2': random.uniform(0.0, 1.0)}

    # Erzeugen Sie einen Zeitstempel für die aktuelle Zeit
    timestamp = datetime.utcnow()

    # Erstellen Sie einen Datenpunkt
    point = Point(measurement)\
        .tag("tag1", tags['tag1'])\
        .tag("tag2", tags['tag2'])\
        .field("field1", fields['field1'])\
        .field("field2", fields['field2'])\
        .time(timestamp, WritePrecision.NS)

    # Schreiben Sie den Datenpunkt in InfluxDB
    write_api.write(bucket, org, point)


def write_realtime_data():
    while True:
        # Generieren und schreiben Sie zufällige Datenpunkte
        generate_random_data()

        # Warten Sie eine Sekunde, bevor Sie die nächste Datenreihe generieren
        time.sleep(0.1)

# Starten Sie die Datenerfassung und -schreibung
write_realtime_data()