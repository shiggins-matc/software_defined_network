### By: Sean Higgins
## written: 3/5/2023 with the outline taken from denny wright, changes made by me

## imports the required modules for script to execute
import requests
import json
import urllib3
## disables the annoying messages each time we make a call
urllib3.disable_warnings()

## command we will use frequently so its been made a variable
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






## our table printer function prints interfaces, status and ip address from our device
def table_print(int_list):
        print("Name"+ '\t'+ "Proto" + '\t' + "Link" +'\t' + "Address")
        print("-" * 70)
        for item in int_list:
            print(item["intf-name"]+ '\t' + item["proto-state"] + '\t' + item["link-state"]+ '\t' + item["prefix"])


## The culmination of the rest of the code, this takes the input of interface and ip address and send it to our device
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
          "cmd": "interface " + int_name,
          "version": 1
        },
        "id": 2
      },
      {
          "jsonrpc": "2.0",
          "method": "cli",
          "params": {
              "cmd": "ip address " + IP+"/24",
              "version": 1
              },
          "id" : 3
          }
    ]
    response = requests.post(url,data=json.dumps(payload),verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json()

## dictionary for accessing and changing more than one device if we so choose    
devices ={
    "dist-sw01" : "10.10.20.177",
    "dist-sw02" : "10.10.20.178"
    }
    
## the first for loop takes the management ip address from table above so we can alter more than one device at a time
for device, ip_address in devices.items():
    mgmtIP = ip_address
    
    old_dict = api_call(mgmtIP, command)
## it then prints the unaltered table for comparison
    print("The old addressing table: ")
    table_print(old_dict)
## this for loop takes the int names and addresses from the api call info stored in old_dict
    for items in old_dict:
        int_name = items["intf-name"]
        addr = items["prefix"]
## this if statement makes it so we only alter interfaces starting with a V thus our vlans, the split and add has been done before
## then we run the change ip function to update our vlan interfaces, finally it prints the updated table
        if int_name.startswith("V"):
            modIP = addr.split(".")
            plus2 = int(modIP[3]) +5
            strplus2 = str(plus2)
            result = modIP[0] + "." + modIP[1] + "." + modIP[2] + "." + strplus2
            change_ip(mgmtIP, int_name , result)
    print("Our new addressing table: ")    
    table_print(api_call(mgmtIP, command))




