"""Roof"""

import asyncio
import json
from multiprocessing import Process
from multiprocessing import Pipe
from process_roof_data import process_roof_data

PORT = 8765

from time import sleep
#
class RoofData:
    preamp_temp:str = '-'
    pa_temp: str = '-'
    pa_current: str = '-'
    fans: str = '-'

def run_server(connection):
    # developed from "TCP echo server using streams"
    # https://docs.python.org/3/library/asyncio-stream.html#tcp-echo-server-using-streams
    async def handle(reader, writer):
        print('CLIENT CONNECTED', flush=True)
        #arm_for_tx()
        while True:
            #print('handle will send ASK to conn1', flush=True)
            connection.send('ASK')
            #sleep(2)
            #print('handle will receive roof_data from conn2', flush=True)
            print('here 1', flush=True)
            #asyncio.sleep(1)
            roof_data = connection.recv()   ####### runs 1st time, but stops her on 2nd ####
            print('here 2', flush=True)
            #print('here 2', flush=True)
            #print(f' : {roof_data.pa_temp}', flush=True)
            #roof_data = RoofData()
            data_dict = roof_data.__dict__
            json_dict = json.dumps(data_dict)
            print(f'{json_dict}', flush=True)
            json_dict_raw = json_dict.encode()
            try:
                writer.write(json_dict_raw)
                await writer.drain()
            except IOError as e:
                print(f'EXCEPTION {e}', flush=True)
                break
        writer.close()

    async def main():
        server = await asyncio.start_server(handle, '0.0.0.0', PORT)
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}', flush=True)
        async with server:
            await server.serve_forever()

    asyncio.run(main())

if __name__ == '__main__':
    parent_connection, child_connection = Pipe()
    # create the process
    p_read_roof_data = Process(target=process_roof_data, args=(child_connection, ))
    # start the process
    p_read_roof_data.start()
    # main thread
    run_server(parent_connection)
    # kill 
    p_read_roof_data.kill()
    # shutdown
    print('about to shut down')
    #import subprocess
    #subprocess.check_call(['sudo', 'poweroff'])








