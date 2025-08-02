# This code is heavily based on the introduction to ZeroMQ PDF provided on Canvas
import zmq

# get a message from the user to send to the server
changes_json = {
                    "action": "update_plan",
                    "remove": "Wash car",
                    "add": {
                            "id": "laundry",
                            "duration": 40
                            },
                    "plan": [
                                {"id": "Wash car", "duration": 30},
                                {"id": "Study", "duration": 50}
                            ],
                    "allocated_time": 120
                }

message = changes_json
print("Message sent: '" + str(message) + "'")

# establish the context, set up a request socket, and connect to the server
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# send the user-supplied message
socket.send_json(message)

# get the reply from the server
reply = socket.recv_json()
print("Server replied: ", str(reply))

print(type(reply))
print(reply["plan"][1])
