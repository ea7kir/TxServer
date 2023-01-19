import asyncio
import websockets
from time import sleep

PORT = 8765

print(f'Server listening on port {PORT}')

# NOTE: the server will close the connection after 20 seconds - after the client disconnects

# NOTE: https://codedamn.com/news/python/how-to-build-a-websocket-server-in-python

class RoofData:
    connected = False

roof_data = RoofData()

async def server(websocket): #, path):
    print('A client just connected')
    roof_data.connected = True
    i = 0
    try:
        while True:
            await websocket.send(f'{i}')
            i += 1
            sleep(1.0)
    # Handle disconnecting clients 
    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")
        roof_data.connected = False
    finally:
        roof_data.connected = False

start_server = websockets.serve(server, "0.0.0.0", PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

##async def echo(websocket):
##    async for message in websocket:
##        await websocket.send(message)
##
##async def main():
##    async with websockets.serve(echo, "localhost", 8765):
##        await asyncio.Future()  # run forever
##
##asyncio.run(main())
