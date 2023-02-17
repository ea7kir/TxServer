import signal
import time

run = True

def handler_stop_signals(signum, frame):
    global run
    run = False

signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)

while run:
    print('running')
    time.sleep(1)

print('stopped')
time.sleep(5)
