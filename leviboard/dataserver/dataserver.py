import asyncio
import json
import random
from quart import websocket, Quart
from pymavlink import mavutil

app = Quart(__name__)

@app.websocket("/random_data")
async def random_data():
    while True:
        output = json.dumps([random.random() for _ in range(10)])
        await websocket.send(output)
        await asyncio.sleep(1)

# Connect to the MAVLink vehicle (replace 'udp:127.0.0.1:14550' with your connection string)
connection_string = 'udp:127.0.0.1:14550'
master = mavutil.mavlink_connection(connection_string)


msg = master.recv_match(type='ATTITUDE', blocking=True)

if msg is not None:
    # Append pitch angle and timestamp to lists
    pitch_angle = msg.pitch * 180 / 3.14159


def start_datserver(port=5000):
    app.run(port=port)

if __name__ == "__main__":
    app.run(port=5000)