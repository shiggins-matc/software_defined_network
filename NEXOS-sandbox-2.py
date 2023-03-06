## by Sean Higgins written 2/28/2023

import requests
import json

import re
### had to look on stack overflow to find the re import and comparison
user_f = input("Enter a hostname: ")

name_q = "Would you like to add a hostname? "
match_f = re.match(r'^[A-Za-z0-9-_]*$', user_f)
### matches input to make sure valid characters, taken from stack overflow
def name_f(arg_f):
    
    if match_f :
        
        print("valid hostname accepted");
    else:
    
        print("invalid name please try again")
        
##runs user input through validation
name_f(user_f)
##takes user input for ip address
user_l = input("Enter a valid ip address: ")
## ties new name to variable to insert later
newName = user_f
match_l = re.match(r'^[0-9.]*$', user_l)
      
## function that tests if entered ip is valid and adds 2 in the third occtet
def ip_test(test_ip):
    test = test_ip.split(".")
    intMaker = list(map(int, test))
        
    result = True
    if len(intMaker) != 4:
            result = False

    for addr in test:
        if int(addr) < 0 or int(addr) > 255:
            result = False
        if result == False:
            print("Ip address is in x.x.x.x format where x>=0 and x <=255")
        if result == True:
            modIP = test_ip.split(".")
            plus2 = int(modIP[2]) +2
            strplus2 = str(plus2)
            print(modIP[0] + "." + modIP[1] + "." + strplus2 + "." + modIP[3])
            return result

ip_test(user_l)
## standard API call stuff below other than taking input for new hostname
switchuser='cisco'
switchpassword='cisco'

url='https://10.10.20.177/ins'
myheaders={'content-type':'application/json-rpc'}
payload=[
  {
    "jsonrpc": "2.0",
    "method": "cli",
    "params": {
      "cmd": "configure terminal",
      "version": 1
    },
    "id": 1
  },
  {
    "jsonrpc": "2.0",
    "method": "cli",
    "params": {
      "cmd": "hostname "+ newName,
      "version": 1
    },
    "id": 2
  }
]
response = requests.post(url,data=json.dumps(payload),verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json()

