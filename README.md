# Manual task swap microservice

This application adds and/or removes tasks from a task management plan. It's designed to run as a microservice connected to a task management application. This Readme outlines the requirements for:

- formatting the data for a request
- sending a request to the microservice
- receiving a reply from the microservice

# Communication contract

This service runs as a ZeroMQ server. After downloading this code from github, run `main.py`. The server will listen for requests continuously until killed with `Ctrl-C`.

By default, the server runs on port 5555. You may wish to change this if you are using that port for another service.
```
# boilerplate server setup code
# establish the context and set up the socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
```

## How to programmatically REQUEST data from the microservice

### Sample request

Sample JSON for a request. This will be used in the example calls below. 

```python
request = {
    "action": "update_plan",
    "remove": "Wash car",
    "add": {
            "id": "laundry",
            "duration": 40
            },
    "plan": [
                {"id": "Wash car", "duration": 30},
                {"id": "Study", "duration": 500}
            ],
    "allocated_time": 120
}
```
#### Field definitions

- action: the action to be taken (currently, updating a plan is the only supported action)
- remove: task to remove
- add: task to add
- plan: an existing plan, consisting of a list of tasks.
- allocated_time: the time allocated to complete all the tasks on the plan. It must be larger than the total duration of the tasks on the plan.

To request data from the microservice, run a ZeroMQ client formulate the request as JSON, as in the example `request` above.

### Sending a request
First, set up the connection:
```python
import zmq
# boilerplate request setup code
# establish the context, set up a request socket, and connect to the server
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")  # if you change the server port, change this port to match
```
Then use `zmq.send_json` to send the request:

```
socket.send_json(request)
```

## How to programmatically RECEIVE data from the microservice

The microservice responses are in JSON format. To receive requests, use `zmq.recv_json`. This will translate the response into a Python dictionary.

### Example call:
```
# get the reply from the server
reply = socket.recv_json()
if "plan" in reply:
    print("Server replied: ", reply["plan"])
else:
    print("Server replied: ", reply["message"])
```
Note that the response may be an error message rather than a plan. Check the parameter `reply["action"]` in the response to check for an error message.

Possible response `action`s:

- `{'action': 'modified_plan'}`: response includes a valid, updated plan
- `{'action': 'removal_error'}`: Task not found in original plan.
- `{'action': 'duration_error'}`: New plan exceeds time allocation.
- `{'action': 'error'}`: Generic error. For errors whose cause hasn't been determined programmatically.

Full example of a valid response:
```
{
    'action': 'modified_plan', 
    'plan': [
        {'id': 'Study', 'duration': 50}, 
        {'id': 'laundry', 'duration': 40}], 
    'allocated_time': 120}
}
```

## UML sequence diagram showing how requesting and receiving data works

 UML sequence diagram showing how requesting and receiving data works. Make it detailed enough that your teammate (and your grader) will understand.
