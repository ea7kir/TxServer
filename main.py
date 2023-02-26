"""TxServer"""

import asyncio
import json

import logging

from device_constants import SERVER_PORT
from device_manager import congifure_devices, shutdown_devices, read_server_data
from device_manager import power_up, power_down

class ServerData:
    preamp_temp = '-'
    pa_temp = '-'
    pa_current = '-'
    fans = '-'

def run_server():
    # developed from "TCP echo server using streams"
    # https://docs.python.org/3/library/asyncio-stream.html#tcp-echo-server-using-streams
    async def handle(reader, writer):
        logging.info('Client connected')
        power_up()
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
                logging.info('Connection lost')
                power_down()
                break
        writer.close()

    async def main():
        server = await asyncio.start_server(handle, '0.0.0.0', SERVER_PORT)
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        logging.info(f'Serving on {addrs}')
        async with server:
            await server.serve_forever()

    asyncio.run(main())

logging.basicConfig(filename='/home/pi/txserver.log', format='%(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)
logging.info('---------- TxServer Starting ----------')

# TODO: intecept sigint for gracefull shutodown

if __name__ == '__main__':

    congifure_devices()

    run_server()  # TODO: https://github.com/wbenny/python-graceful-shutdown

    shutdown_devices()

    # shutdown
    logging.info('About to shutdown')
    #import subprocess
    #subprocess.check_call(['sudo', 'poweroff'])






