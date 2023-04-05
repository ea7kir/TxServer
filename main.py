"""TxServer"""

import asyncio
import json

import socketserver
import logging

from device_constants import SERVER_PORT
from device_manager import congifure_devices, shutdown_devices, read_server_data
from device_manager import power_up, power_down, read_server_data_string

class ServerData:
    preamp_temp = '-'
    pa_temp = '-'
    pa_current = '-'
    fans = '-'

def run_server_original():
    # developed from "TCP echo server using streams"
    # https://docs.python.org/3/library/asyncio-stream.html#tcp-echo-server-using-streams
    async def handle(reader, writer):
        logging.info('Client connected')
        power_up()
        while True:

            server_status_msg = read_server_data_string()
            # TODO: send one line

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

# developed from
# https://docs.python.org/3/library/socketserver.html?highlight=server#socketserver.TCPServer

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        #print(f'CONNECTED to {self.client_address[0]}', flush=True)
        logging.info(f'Client {self.client_address[0]} Connected')
        power_up()
        #   # self.request is the TCP socket connected to the client
        #   self.data = self.request.recv(1024).strip()
        #   print("{} wrote:".format(self.client_address[0]))
        #   print(self.data)
        #   # just send back the same data, but upper-cased
        #   self.request.sendall(self.data.upper())
        while True:
            try:
                self.server_status_msg = read_server_data_string()
                self.request.sendall(bytes(self.server_status_msg, "utf-8"))
                #print(self.server_status_msg, flush=True)
            except:
                #print('DISCONNECTED', flush=True)
                logging.info('Connection lost')
                logging.info(f'Client {self.client_address[0]} Disconnected')
                power_down()
                break

def run_server():
    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer(('0.0.0.0', SERVER_PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()


logging.basicConfig(filename='/home/pi/txserver.log', format='%(asctime)s %(message)s', encoding='utf-8', level=logging.DEBUG)
logging.info('---------- TxServer Starting ----------')

# TODO: intecept sigint for gracefull shutodown

if __name__ == '__main__':

    congifure_devices()

    #run_server_original()  # TODO: https://github.com/wbenny/python-graceful-shutdown

    run_server()  # TODO: https://github.com/wbenny/python-graceful-shutdown

    shutdown_devices()

    # shutdown
    logging.info('About to shutdown')
    #import subprocess
    #subprocess.check_call(['sudo', 'poweroff'])
