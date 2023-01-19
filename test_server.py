import asyncio
import websockets
import json
from json import JSONEncoder
from time import sleep

PORT = 8765

print(f'Server listening on port {PORT}')

# NOTE: the server will close the connection after 20 seconds - after the client disconnects

# NOTE: https://codedamn.com/news/python/how-to-build-a-websocket-server-in-python

class RoofData:
    counter = 0
    connected = False

class RoofDataEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


roof_data = RoofData()

###############################################################
def OLD_process_run_server(connection):
    async def server(websocket): #, path):
        print('A client just connected', flush=True)
        roof_data.connected = True
        try:
            while True:
                command = await websocket.recv()
                print(command, flush=True)

                data = RoofDataEncoder().encode(roof_data)
                print(data, flush=True)
                await websocket.send(data)
                roof_data.counter += 1
                sleep(1.0)
        # Handle disconnecting clients 
        except websockets.exceptions.ConnectionClosed as e:
            print("A client just disconnected", flush=True)
            roof_data.connected = False
        finally:
            roof_data.connected = False

    start_server = websockets.serve(server, "0.0.0.0", PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
###############################################################

def NEW_process_run_server(connection):
    async def handler(websocket):
        print('A client just connected', flush=True)
        roof_data.connected = True
        while True:
            message = await websocket.recv()
            print(message, flush=True)
    async def main():
        async with websockets.serve(handler, "0.0.0.0", PORT):
            await asyncio.Future()  # run forever
    asyncio.run(main()) 

OLD_process_run_server(999)
#NEW_process_run_server(999)