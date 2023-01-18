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

connected = set()

async def server(websocket): #, path):
    print('A client just connected')
    roof_data.connected = True
    # Store a copy of the connected client
    connected.add(websocket)
    # Handle incoming messages
    try:
        async for message in websocket:
            print("Received message from client: " + message)
            # Send a response to all connected clients except sender
            for conn in connected:
                if conn != websocket:
                    await conn.send("Someone said: " + message)
    # Handle disconnecting clients 
    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")
        roof_data.connected = False
    finally:
        connected.remove(websocket)
        roof_data.connected = False

start_server = websockets.serve(server, "0.0.0.0", PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()