## By Sean Higgins on 2/27/2023
##the basic code structure was provided by denny wright
## the purpose on this code is to make calls to our sandbox switches, return data and print it out in a nice format


import requests
import json

def getVersion(mgmtIPAddress):
#This code is mostly generated by the NXOSAPI and gets a dictionary of OSPF neighbors.
#The dictionary (response) should be returned from this function to be used by the print function.
#mgmtIPaddress is received and used to ,modify the URL so that the code can be run on whatever device’s IP is received
    
    switchuser='cisco'
    switchpassword='cisco'

    url='https://' + mgmtIP +'/ins'
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
    response = requests.post(url,data=json.dumps(payload), verify = False,headers=myheaders,auth=(switchuser,switchpassword)).json()
    return response
 
#Below is the dictionary we pull from to get information for our functions

devices = {
    "dist-sw01" : {
        "hostname" : "dist-sw01",
        "deviceType" : "switch",
        "mgmtIP" : "10.10.20.177"
        },
    "dist-sw02" : {
        "hostname" : "dist-sw02",
        "deviceType" : "switch",
        "mgmtIP" : "10.10.20.178"
        }
}

## basic easy to read printout that pulls from dictionary
print("Host "+ '\t' + "Type" + '\t' + "Mgmt IP")
print("-" * 70)
print(devices["dist-sw01"]["hostname"] + '\t' + devices["dist-sw01"]["deviceType"] + '\t' + devices["dist-sw01"]["mgmtIP"])
print(devices["dist-sw02"]["hostname"] + '\t' + devices["dist-sw02"]["deviceType"] + '\t' + devices["dist-sw02"]["mgmtIP"])

## this function prints out information from our getVersion function above displaying various info

def showprinter(devices):
        print("Name"+ '\t'+ '\t' + "Memory" + '\t' + "Type" +'\t' + "Chassis" + '\t' + '\t' + "Boot File")
        print("-" * 70)
        print(response["result"]["body"]["host_name"] + '\t' + str(response["result"]["body"]["memory"]) + response["result"]["body"]["mem_type"] + '\t' + response["result"]["body"]["chassis_id"] + '\t' + response["result"]["body"]["kick_file_name"])

## the for loop takes the different ip addresses to run through our other functions
## response stores the first functions result so we can manipulate it
## for this loop it prints out my responses twice and i am curious how to fix that       
for device in devices:
    count = 0
    while count == 0:
        mgmtIP = devices["dist-sw01"]["mgmtIP"]
        response = getVersion(mgmtIP)
        showprinter(response)
        count += 1
    else:
        mgmtIP = devices["dist-sw02"]["mgmtIP"]
        response = getVersion(mgmtIP)
        showprinter(response)
            

