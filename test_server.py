import asyncio
import websockets
from time import sleep

PORT = 8765

print(f'Server listening on port {PORT}')

# NOTE: the server will close the connection after 20 seconds - after the client disconnects

# NOTE: https://codedamn.com/news/python/how-to-build-a-websocket-server-in-python

class RoofData:
    counter = 0
    connected = False

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

                await websocket.send(f'{roof_data.counter}') # TODO: needs JSON
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
    pass

OLD_process_run_server(999)