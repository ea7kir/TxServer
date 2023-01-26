"""Roof"""

import asyncio
import json
from process_roof_data import read_roof_data

PORT = 8765

from time import sleep
#
class RoofData:
    preamp_temp:str = '-'
    pa_temp: str = '-'
    pa_current: str = '-'
    fans: str = '-'

def run_server():
    # developed from "TCP echo server using streams"
    # https://docs.python.org/3/library/asyncio-stream.html#tcp-echo-server-using-streams
    async def handle(reader, writer):
        print('CLIENT CONNECTED')
        #arm_for_tx()
        while True:
            roof_data = read_roof_data()
            data_dict = roof_data.__dict__
            json_dict = json.dumps(data_dict)
            print(f'{json_dict}')
            json_dict_raw = json_dict.encode()
            try:
                writer.write(json_dict_raw)
                await writer.drain()
            #except IOError as e:
            #    print(f'EXCEPTION {e}')
            #    break
            except ConnectionResetError:
                print(f'CONNECTION LOST')
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
    run_server()
    # shutdown
    print('about to shut down')
    #import subprocess
    #subprocess.check_call(['sudo', 'poweroff'])








