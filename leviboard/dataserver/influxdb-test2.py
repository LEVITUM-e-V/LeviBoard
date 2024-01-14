import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = '2toOHIzhKsi51grUHQ4TUZbarf5z7ig69HfhjcCfthBhj4Am4Tf36TDMHPCLcvl1kyH8DCI9fN6JDUVAIYrNAg' # os.environ.get("INFLUXDB_TOKEN")

print(token)
org = "LEVITUM"
url = "http://localhost:8086"
USER = 'admin'
PASSWORD = 'Administrator1'

write_client = influxdb_client.InfluxDBClient(url=url, username=USER, password=PASSWORD, token=token, org=org)

bucket="Flight Logs"

write_api = write_client.write_api(write_options=SYNCHRONOUS)
   
for value in range(5):
  point = (
    Point("measurement1")
    .tag("tagname1", "tagvalue1")
    .field("field1", value)
  )
  write_api.write(bucket=bucket, org="LEVITUM", record=point)
  time.sleep(1) # separate points by 1 second