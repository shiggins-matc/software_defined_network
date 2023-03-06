### By: Sean Higgins
## written: 3/5/2023 with the outline taken from denny wright, changes made by me

## imports the required modules for script to execute
import requests
import json
import urllib3
## disables the annoying messages each time we make a call
urllib3.disable_warnings()
## since we are only accessing one device in this script i hard coded the mgmtIP for easier access throughout
## same for command

mgmtIP = "10.10.20.177"
command = "show ip interface brief"
## this is our API call that goes to mgmtIP and returns data for us to manipulate
def api_call(mgmtIP, command):
    switchuser='cisco'
    switchpassword='cisco'

    url='https://' +mgmtIP +'/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": command,
          "version": 1
        },
        "id": 2
      }
    ]
    response = requests.post(url,data=json.dumps(payload),verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json()
    switch_list = response["result"]["body"]["TABLE_intf"]["ROW_intf"]
    return switch_list


## this function checks the input from user about interface and compaires it versus the list of known interfaces below
def get_int_list(request_dict, interface):
    interf = interface.capitalize()

    if interf.capitalize() in request_dict:
        return True
    else:
        print("Not a valid interface please try again")
        return False


## our table printer function prints interfaces, status and ip address from our device
def table_print(int_list):
        print("Name"+ '\t'+ "Proto" + '\t' + "Link" +'\t' + "Address")
        print("-" * 70)
        for item in int_list:
            print(item["intf-name"]+ '\t' + item["proto-state"] + '\t' + item["link-state"]+ '\t' + item["prefix"])



## The culmination of the rest of the code, this takes the validated user input of interface and ip address and send it to our device
## to update it
def change_ip(mgmtIP,int_name,IP):
    switchuser='cisco'
    switchpassword='cisco'

    url='https://' +mgmtIP +'/ins'
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
          "cmd": "interface " + int_change,
          "version": 1
        },
        "id": 2
      },
      {
          "jsonrpc": "2.0",
          "method": "cli",
          "params": {
              "cmd": "ip address " + new_ip+"/24",
              "version": 1
              },
          "id" : 3
          }
    ]
    response = requests.post(url,data=json.dumps(payload),verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json()

    

    
## this function is our ip validator and will let us know if the ip we are attempting is invalid

def validIP(test_ip):
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

            return result

## below is the bones of the script, first thing is API call stored into new variable for access
new_dict = api_call(mgmtIP, command)
##then it is printed in our nice table
table_print(new_dict)
## asks the user which interface to update, stored in a variable for access
int_change = input("Which interface would you like to change? ")
interface = int_change
## im sure there are better ways but i hard coded the return from our api call into a dictionary to compare vs user input
int_dict =[
    {
        new_dict[0]['intf-name'],
        new_dict[1]['intf-name'],
        new_dict[2]['intf-name'],
        new_dict[3]['intf-name'],
        new_dict[4]['intf-name'],
        new_dict[5]['intf-name'],
        new_dict[6]['intf-name']
        }
    ]
## calls the function to compare input vs the dict
get_int_list(interface,int_change)
## takes input for the new address
new_ip = input("What would you like this interfaces IP to be? ")

## check the input is valid
validIP(new_ip)
## once interface and ip are valid sends the call to update device
change_ip(mgmtIP,int_change,new_ip)
## printout with new address assigned to input interface
changed_dict = api_call(mgmtIP, command)
table_print(changed_dict)
