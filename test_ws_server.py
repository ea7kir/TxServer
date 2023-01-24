import asyncio
import websockets
import pickle
from time import sleep

from read_temperature_sensors import read_pa_temperature, read_preamp_temperature
from read_fan_status import read_fan_status
from read_current_sensor import read_pa_current

PORT = 8765

print(f'Server listening on port {PORT}')

# NOTE: the server will close the connection after 20 seconds - after the client disconnects

# NOTE: https://codedamn.com/news/python/how-to-build-a-websocket-server-in-python

class RoofData:
    preamp_temp:str = ''
    pa_temp: str = ''
    pa_current: str = ''
    fans: str = ''
    connected: bool = False

#roof_data = RoofData()

async def produce():
    roof_data = RoofData()
    roof_data.preamp_temp = read_preamp_temperature()
    roof_data.pa_temp:str = read_pa_temperature()
    roof_data.pa_current:str = read_pa_current()
    roof_data.fans = read_fan_status()
    roof_data.connected = True
    #roof2.send(roof_data)
    #asyncio.sleep(0.5)
    sleep(1)
    return roof_data

def process_run_server(connection):
    async def handler(websocket):
        print('A client just connected', flush=True)
        try:
            while True:
                roof_data = await produce()
                data = pickle.dumps(roof_data)
                await websocket.send(data)
        except websockets.exceptions.ConnectionClosedError as e:
            print('EXCEPTION: ConnectionClosedError', flush=True)
            print(e, flush=True)
        except websockets.exceptions.ConnectionClosed as e:
            print('EXCEPTION: ConnectionClosed', flush=True)
            print(e, flush=True)
        finally:
            print('FINALLY', flush=True)

    async def main():
        async with websockets.serve(handler, "0.0.0.0", PORT):
            await asyncio.Future()  # run forever
    asyncio.run(main()) 

process_run_server(999)