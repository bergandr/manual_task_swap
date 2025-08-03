# run the microservice

# Main code to run the microservice as a zmq server
import zmq
from swap_functions import apply_changes, validate_plan  # task swap functions

# send if cause of error cannot be determined
generic_error_message = {"action": "error", "message": "There was an error processing the request."}

# this is basically boilerplate server setup code, based on the course-provided zmq documentation
# establish the context and set up the socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
print("Listening for messages ...")

# listen for messages
try:
    while True:
        request = socket.recv_json()
        if len(request) > 0:
            print("Received request to change a plan")
            # first, apply the changes requested to the plan
            modified_plan = apply_changes(request)

            # check if the changes resulted in an error
            if "error" in modified_plan:
                # only a 'remove' can result in an error
                print("Error: task to remove not found in plan")
                reply = {"action": "removal_error", "message": modified_plan["error"]}
            else:
                # if the changes were accepted, validate the new plan against the time allocation
                allocated_time = request["allocated_time"]
                time_check = validate_plan(allocated_time, modified_plan)
                if time_check:
                    reply = {"action": "modified_plan", "plan": modified_plan, "allocated_time": allocated_time}
                else:
                    print("Error: tasks exceed allocated time")
                    reply = {"action": "duration_error", "message": "New plan exceeds time allocation."}

            # reply with either a new plan or an error message
            print("Replying to request")
            socket.send_json(reply)

        else:
            # if the client somehow connected but the message was lost
            socket.send_json(generic_error_message)

# shutdown server when receiving ctrl-C
except KeyboardInterrupt:
    print("\nShutting down the server ...\n")

# Clear the context and exit
context.destroy()
