"""TxServer"""

import asyncio
import json
from time import sleep

from device_manager import congifure_devices, shutdown_devices, read_server_data
from device_manager import switch_28v_On, switch_28v_Off
from device_manager import switch_12v_On, switch_12v_Off
from device_manager import switch_5v_On, switch_5v_Off

PORT = 8765

class ServerData:
    preamp_temp = '-'
    pa_temp = '-'
    pa_current = '-'
    fans = '-'

def arm_for_tx():
    switch_5v_On()
    sleep(1)
    switch_28v_On()
    sleep(1)
    switch_12v_On()

def disarm_for_tx():
    switch_28v_Off()
    sleep(1)
    switch_5v_Off()
    sleep(1)
    switch_12v_Off()

def run_server():
    # developed from "TCP echo server using streams"
    # https://docs.python.org/3/library/asyncio-stream.html#tcp-echo-server-using-streams
    async def handle(reader, writer):
        print('CLIENT CONNECTED')
        arm_for_tx()
        while True:
            server_data = read_server_data()
            data_dict = server_data.__dict__
            json_dict = json.dumps(data_dict)
            #print(f'{json_dict}')
            json_dict_raw = json_dict.encode()
            try:
                writer.write(json_dict_raw)
                await writer.drain()
            #except IOError as e:
            #    print(f'EXCEPTION {e}')
            #    break
            except ConnectionResetError:
                print(f'CONNECTION LOST')
                disarm_for_tx()
                break
        writer.close()

    async def main():
        server = await asyncio.start_server(handle, '0.0.0.0', PORT)
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')
        async with server:
            await server.serve_forever()

    asyncio.run(main())

# TODO: intecept sigint for gracefull shutodown
# TODO: pi = pigpio.pi() # TODO: also need to close ?
if __name__ == '__main__':

    congifure_devices()

    run_server()  # TODO: https://github.com/wbenny/python-graceful-shutdown

    shutdown_devices()

    # shutdown
    print('about to shut down')
    #import subprocess
    #subprocess.check_call(['sudo', 'poweroff'])






