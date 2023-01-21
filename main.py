"""Roof"""

from multiprocessing import Process
from multiprocessing import Pipe

import asyncio
import websockets
import pickle

from process_roof_data import process_roof_data

import asyncio
import websockets
from time import sleep

PORT = 8765

# NOTE: the server will close the connection after 20 seconds - after the client disconnects

# NOTE: https://codedamn.com/news/python/how-to-build-a-websocket-server-in-python

def run_server(connection):
    print(f'Server listening on port {PORT}')
    async def handler(websocket):
        print('A client just connected', flush=True)
        connected = True
        try:
            while True:
                #message = await websocket.recv()
                #print(message, flush=True)
                #async for message in websocket:
                #    consumer(message)
                roof_data = connection.recv()
                print('ready to send', flush=True)
                while connection.poll():
                    print('flush', flush=True)
                    _ = connection.recv()
                if connected :
                    data = pickle.dumps(roof_data)
                    await websocket.send(data)
                    print('sent', flush=True)
        except websockets.exceptions.ConnectionClosedError:
            print('EXCEPTION: ConnectionClosedError', flush=True)
        except websockets.exceptions.ConnectionClosed:
            print('EXCEPTION: ConnectionClosed', flush=True)
        finally:
            print('FINALLY', flush=True)

    async def main():
        async with websockets.serve(handler, "0.0.0.0", PORT):
            await asyncio.Future()  # run forever
    asyncio.run(main()) 

if __name__ == '__main__':
    conn1, conn2 = Pipe(duplex=True)
    # create the process
    p_read_roof_data = Process(target=process_roof_data, args=(conn2,))
    # start the process
    p_read_roof_data.start()
    # main ui
    run_server(conn1)
    # kill 
    p_read_roof_data.kill()
    # shutdown
    print('about to shut down')
    #import subprocess
    #subprocess.check_call(['sudo', 'poweroff'])








