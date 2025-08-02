# This code is heavily based on the introduction to ZeroMQ PDF provided on Canvas
import zmq

# Set up the sample data for requests

# this is a valid request with an add and remove
valid_request = {
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

# this request attempts to remove a task that isn't in the original plan
removal_error = {
    "action": "update_plan",
    "remove": "Wash car",
    "add": {
        "id": "laundry",
        "duration": 40
    },
    "plan": [
        {"id": "Fix car", "duration": 30},
        {"id": "Study", "duration": 50}
    ],
    "allocated_time": 120
}

# this request creates changes that result in the tasks exceeding the allocated time limit
time_exceeded = {
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
    "allocated_time": 85
}

# put the samples in a list
samples = [valid_request, removal_error, time_exceeded, ""]


def main():
    # this is basically boilerplate request setup code, based on the course-provided zmq documentation
    # establish the context, set up a request socket, and connect to the server
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    # loop over the sample data
    for sample in samples:
        socket.send_json(sample)  # use send_json since all requests will be in JSON format

        # get the reply from the server
        reply = socket.recv_json()
        print("\nFull reply:", reply)
        if "plan" in reply:
            print("Just the plan: ", reply["plan"])
        else:
            print("Error message: ", reply["message"])


if __name__ == "__main__":
    main()
