"""Roof"""

from multiprocessing import Process
from multiprocessing import Pipe

from process_roof_data import process_roof_data

import asyncio
import websockets
from time import sleep

PORT = 8765

# NOTE: the server will close the connection after 20 seconds - after the client disconnects

# NOTE: https://codedamn.com/news/python/how-to-build-a-websocket-server-in-python

def main(connection):
    print(f'Server listening on port {PORT}')

    for i in range(1, 10):
        # only if client is connected
        roof_data = connection.recv()
        while connection.poll():
            _ = connection.recv()
        print(roof_data.pa_current)
        #sleep(1.0)



if __name__ == '__main__':
    conn1, conn2 = Pipe(duplex=True)
    # create the process
    p_read_roof_data = Process(target=process_roof_data, args=(conn2,))
    # start the process
    p_read_roof_data.start()
    # main ui
    main(conn1)
    # kill 
    p_read_roof_data.kill()
    # shutdown
    print('about to shut down')
    #import subprocess
    #subprocess.check_call(['sudo', 'poweroff'])








