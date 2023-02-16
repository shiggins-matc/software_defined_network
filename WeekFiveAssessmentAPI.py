### By: Sean Higgins
## written: 2/13/2023 with the base code taken from denny wright, changes made by me

## imports the required modules for script to execute
import requests
import json

"""
Be sure to run feature nxapi first on Nexus Switch
## this is done so we can get the information from the switch
"""
##login credentials for the device we are accessing and getting data from
switchuser='cisco'
switchpassword='cisco'
## the address we are accessing is the url
url='https://10.10.20.178/ins'
myheaders={'content-type':'application/json-rpc'}
## payload is needed for our API call
payload=[
  {
    "jsonrpc": "2.0",
    "method": "cli",
    "params": {
      "cmd": "show ip interface brief",
      "version": 1
    },
    "id": 1
  }
]

'''

verify=False below is to accept untrusted certificate

'''
##stores the data from the switch into the response variable
response = requests.post(url,data=json.dumps(payload), verify=False,headers=myheaders,auth=(switchuser,switchpassword)).json()
## switch_list stores the response in an easier to acccess varialbe
switch_list = response["result"]["body"]["TABLE_intf"]["ROW_intf"]
##function that runs through input, in this case switch_list, and prints out the data in a nice format
def printout2(dicts):
    print("Name"+ '\t'+ "Proto" + '\t' + "Link" +'\t' + "Address")
    print("-" * 70)
    for item in dicts:
        print(item["intf-name"]+ '\t' + item["proto-state"] + '\t' + item["link-state"]+ '\t' + item["prefix"])
##the call to run switch_list through our printout function
printout2(switch_list)
