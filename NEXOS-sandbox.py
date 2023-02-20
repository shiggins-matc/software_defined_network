## Written by: Sean Higgins
## the purpose of this code is to get information from the cisco sandbox devices using an API
## and then returning the information and printing it out in a pleasing format
## majority of code was obtained from the sandbox itself

## imports required modules for lab
import requests
import json

"""
Modify these please
"""
## log in credentials for the device we are accessing
switchuser='cisco'
switchpassword='cisco'
## address of device we are calling and payload is information we need for our call to succeed
url='https://10.10.20.177/ins'
myheaders={'content-type':'application/json-rpc'}
payload=[
  {
    "jsonrpc": "2.0",
    "method": "cli",
    "params": {
      "cmd": "show version",
      "version": 1
    },
    "id": 1
  }
]
## the verify = False is important becasue it lets us get around the inital rejection when tring to access devices in the sandbox
##the rest of the response variable is storing the information we recieve from the switch
response = requests.post(url,data=json.dumps(payload), verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json()
## stores device name into an easier accessed variable
host_name = response["result"]["body"]["host_name"]
## mem_size variable stores the interget returned from our dictionary into a string so we can concatinate it
mem_size = str(response["result"]["body"]["memory"])
## mem_type is actually what was stored in the switch so this makes it an easier to access value
mem_type = response["result"]["body"]["mem_type"]

## the printout shows our created variable and descriptive text so we can clearly read what we are seeing
print("Your hostname is: " + host_name)
print("Your memory size is: " + mem_size + " " + mem_type)
