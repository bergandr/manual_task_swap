# run the microservice

# This code is heavily based on the introduction to ZeroMQ PDF provided on Canvas
import zmq
from swap_functions import apply_changes, validate_plan

# establish the context and set up the socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
print("Listening for messages ...")

# listen for messages
try:
    while True:
        raw_message = socket.recv_json()
        if len(raw_message) > 0:
            socket.send_json(raw_message)
except KeyboardInterrupt:
    print("\nShutting down the server ...\n")

# Clear the context and exit
context.destroy()
