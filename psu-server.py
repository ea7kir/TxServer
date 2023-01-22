# psu_server.py

import socket
import threading
import pigpio
#mport time

SERVER = '0.0.0.0' #socket.gethostbyname("txtouch.local")
PORT = 5050

ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = 'utf-8'

RELAY_0 = 17 # pin 11 # Relay 0 - AC to Psu12v Contactor
RELAY_1 = 27 # pin 13 # Relay 1 - AC to Psu28v Contactor
RELAY_2 = 22 # pin 15 # Relay 2 - 5v to RX Pi
RELAY_3 = 10 # pin 19 # Relay 3 - 12v to Pluto Fan, Driver Fan, PA LH Fan, PA RH Fan
RELAY_4 = 9  # pin 21 # Relay 4 - 5v to Pluto Vcc
RELAY_5 = 11 # pin 23 # Relay 5 - 5v to Driver Vcc (PTT)
RELAY_6 = 5  # pin 29 # Relay 6 - 28v to PA Bias (PTT)
RELAY_7 = 6  # pin 31 # Relay 7 - reserved

RELAY_OFF = 1 # note: the opto coupleers need reverse logic
RELAY_ON = 0

pi = pigpio.pi()

def config_gpio():
    print("config_gpio")
    def config(relay):
        pi.set_mode(relay, pigpio.OUTPUT)
        pi.write(relay, RELAY_OFF)
    
    config(RELAY_0)
    config(RELAY_1)
    config(RELAY_2)
    config(RELAY_3)
    config(RELAY_4)
    config(RELAY_5)
    config(RELAY_6)
    config(RELAY_7)


if __name__ == '__main__':
    config_gpio()


def reset_gpio():
    print("reset_gpio")
    def config(relay):
        pi.write(relay, RELAY_OFF)
        pi.set_mode(relay, pigpio.INPUT)
    
    config(RELAY_0)
    config(RELAY_1)
    config(RELAY_2)
    config(RELAY_3)
    config(RELAY_4)
    config(RELAY_5)
    config(RELAY_6)
    config(RELAY_7)
    pi.stop()


def relay_status():
    def strOnOff(relay):
        if pi.read(relay) == RELAY_ON:
            return "ON"
        return "OFF"

    relay_0 = strOnOff(RELAY_0)
    relay_1 = strOnOff(RELAY_1)
    relay_2 = strOnOff(RELAY_2)
    relay_3 = strOnOff(RELAY_3)
    relay_4 = strOnOff(RELAY_4)
    relay_5 = strOnOff(RELAY_5)
    relay_6 = strOnOff(RELAY_6)
    #relay_7 = strOnOff(RELAY_7)
    status = f"0={relay_0}, 1={relay_1}, 2={relay_2}, 3={relay_3}, 4={relay_4}, 5={relay_5}, 6={relay_6}"
    return status
 

def device_status():
    def isOnOff(level):
        if level == True:
            return "ON"
        return "OFF"

    rx = isOnOff(pi.read(RELAY_0) == RELAY_ON and pi.read(RELAY_2) == RELAY_ON)
    tx = isOnOff(pi.read(RELAY_1) == RELAY_ON and pi.read(RELAY_3) == RELAY_ON and pi.read(RELAY_4) == RELAY_ON)
    ptt = isOnOff(pi.read(RELAY_5) == RELAY_ON and pi.read(RELAY_6) == RELAY_ON)
    status = f"RX={rx} TX={tx} PTT={ptt}"
    return status


def toggle_rx(): # needs RELAY_0, RELAY_2
    print("toggle_rx")
    if pi.read(RELAY_0) == RELAY_OFF:
        pi.write(RELAY_0, RELAY_ON)
        pi.write(RELAY_2, RELAY_ON)
    else:
        pi.write(RELAY_2, RELAY_OFF)
        pi.write(RELAY_0, RELAY_OFF)


def toggle_tx(): #  RELAY_1, RELAY_3, RELAY_4
    print("toggle_tx")
    if pi.read(RELAY_1) == RELAY_OFF:
        pi.write(RELAY_1, RELAY_ON)
        pi.write(RELAY_3, RELAY_ON)
        pi.write(RELAY_4, RELAY_ON)
    else:
        # cancel ptt
        pi.write(RELAY_6, RELAY_OFF)
        pi.write(RELAY_5, RELAY_OFF)
        
        pi.write(RELAY_4, RELAY_OFF)
        pi.write(RELAY_3, RELAY_OFF)
        pi.write(RELAY_1, RELAY_OFF)


def toggle_ptt(): # needs RELAY_5, RELAY_6
    print("toggle_ptt(")
    if pi.read(RELAY_1) == RELAY_OFF:
        return
    if pi.read(RELAY_5) == RELAY_OFF:
        pi.write(RELAY_5, RELAY_ON)
        pi.write(RELAY_6, RELAY_ON)
    else:
        pi.write(RELAY_6, RELAY_OFF)
        pi.write(RELAY_5, RELAY_OFF)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # new - appears to prevent port in use
server.bind(ADDR)


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


def stop():
    print("************ need to close the server here *************")
    #server.shutdown(socket.SHUT_RDWR) # new
    #server.close() # new
    print ("********************closed ****************************")


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    will_stop = False
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == "q":
                connected = False
            elif msg == "r":
                toggle_rx()
            elif msg == "t":
                toggle_tx()
            elif msg == "p":
                toggle_ptt()
            elif msg == "s":
                pass
            elif msg == "k":
                conn.send("Server will stop".encode(FORMAT))
                connected = False
                will_stop = True
            else:
                conn.send("ILLEGAL COMMAND".encode(FORMAT))
 
            #print(f"[{addr}] {msg}")
            response = f"RELAYS: {relay_status()}\nDEVICES: {device_status()}\n"
            conn.send(response.encode(FORMAT))
    conn.close()
    if will_stop:
        stop()


print("[STARTING] server is starting...")
try:
    start()
except KeyboardInterrupt:
    stop()
except:
    stop()
finally:
    print("finally")
    reset_gpio()
