# by: Sean Higgins created: 4/11/2023
#the function of this script is to access a nxapi device and get a printout of show ip int brief

#needed imports
import requests
import json, urllib3, re

urllib3.disable_warnings()

#function to get cookie
def getCookie(url) :

    payload= {"aaaUser" :
              {"attributes" :
                   {"name" : "cisco",
                    "pwd" : "cisco"}
               }
          }

    response = requests.post(url, json=payload, verify = False)

    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]
#function that uses cookie to get interface inforamtion
def show_int():
    
    switchuser='cisco'
    switchpassword='cisco'

    url='https://10.10.20.177/ins'
    myheaders={'content-type':'application/json-rpc'}
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
    response = requests.post(url,data=json.dumps(payload),verify=False, headers=myheaders,auth=(switchuser,switchpassword)).json()
    return response
##static address since script is just for one device
cookie = getCookie("https://10.10.20.177/api/aaaLogin.json")
#calls the int function and stores result
new_dict = show_int()
## function to store information into dictionary for access
def int_list():
    switchuser='cisco'
    switchpassword='cisco'

    url ='https://10.10.20.177/api/node/mo/sys/ipv4/inst/dom-default.json?query-target=children'
    myheaders={'content-type':'application/json-rpc'}
    payload = []

    # Define a cookie dictionary
    cookie = getCookie("https://10.10.20.177/api/aaaLogin.json")
    cookie_dict = {'APIC-cookie': cookie}

    # Add the cookie to the request
    response = requests.get(url,
                            data=json.dumps(payload),
                            verify=False,
                            headers=myheaders,
                            auth=(switchuser, switchpassword),
                            cookies=cookie_dict).json()

    return response
# calls function above stores result in variable
ints=int_list()
# printout in desired table format
for item in ints['imdata']:
    print(item['ipv4If']['attributes']['dn'], item['ipv4If']['attributes']['id'])

