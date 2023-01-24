import asyncio
import json

from read_temperature_sensors import read_pa_temperature, read_preamp_temperature
from read_fan_status import read_fan_status
from read_current_sensor import read_pa_current
from time import sleep

PORT = 8765

class RoofData:
    preamp_temp:str = ''
    pa_temp: str = ''
    pa_current: str = ''
    fans: str = ''
    connected: bool = False

def produce():
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

async def handle(reader, writer):
    while True:
        roof_data = produce()
        jsonStr = json.dumps(roof_data.__dict__)
        print(jsonStr, flush=True)
        writer.write(jsonStr.encode())
        await writer.drain()

    print("Close the connection")
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle, '0.0.0.0', PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}', flush=True)

    async with server:
        await server.serve_forever()

asyncio.run(main())

#process_run_server(999)
