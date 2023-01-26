import asyncio
import json

from read_temperature_sensors import read_pa_temperature, read_preamp_temperature
from read_fan_status import read_fan_status
from read_current_sensor import read_pa_current
from time import sleep

PORT = 8765

class ServerData:
    preamp_temp:str = ''
    pa_temp: str = ''
    pa_current: str = ''
    fans: str = ''

def produce():
    server_data = ServerData()
    server_data.preamp_temp = read_preamp_temperature()
    server_data.pa_temp:str = read_pa_temperature()
    server_data.pa_current:str = read_pa_current()
    server_data.fans = read_fan_status()
    sleep(1)
    return server_data

def arm_for_tx():
    print("SWITCH ON 5 AND 28 VOLTS", flush=True)

def disarm_for_tx():
    print("SWITCH OFF 5 AND 28 VOLTS", flush=True)

# developed from "TCP echo server using streams"
# https://docs.python.org/3/library/asyncio-stream.html#tcp-echo-server-using-streams

async def handle(reader, writer):
    arm_for_tx()
    while True:
        server_data = produce()
        jsonStr = json.dumps(server_data.__dict__)
        try:
            writer.write(jsonStr.encode())
            await writer.drain()
        except:
            break
    writer.close()
    disarm_for_tx()

async def main():
    server = await asyncio.start_server(handle, '0.0.0.0', PORT)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}', flush=True)
    async with server:
        await server.serve_forever()

import signal, sys
def sigint_handler(signal, frame):
    print ('KeyboardInterrupt error caught')
#sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)

asyncio.run(main())

#process_run_server(999)
