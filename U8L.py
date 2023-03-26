## By: Sean Higgins 03/26/2023
## the basic function of this code it to take user input on hostname and ip address, verify the inputs
## then send a call to the switches to actually change hostname


##required imports
import requests
import json, urllib3, re

urllib3.disable_warnings()

## our cookie getting function
def getCookie(url) :
#NX REST API Authen See REST API Reference for format of payload below

 
    payload= {"aaaUser" :
              {"attributes" :
                   {"name" : "cisco",
                    "pwd" : "cisco"}
               }
          }

    response = requests.post(url, json=payload, verify = False)

    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]

## function to change hostname, takes args of mgmt_ip to find device in url and hostname for new name
## Taken from chat GPT, specifics modified by me
def change_switch_hostname(hostname, mgmt_ip):
    url = f"https://{mgmt_ip}/ins"
    switch_username = "cisco"
    switch_password = "cisco"
    
    payload = [
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": f"hostname {hostname}",
                "version": 1
            },
            "id": 1
        }
    ]
    
    headers = {
        "content-type": "application/json-rpc"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, auth=(switch_username, switch_password), verify=False)
        response.raise_for_status()
        print(f"Successfully changed hostname to {hostname}")
        
        # update the dictionary with the new hostname and IP address
        for key, value in nx_switches.items():
            if value == mgmt_ip:
                del nx_switches[key]
                nx_switches[hostname] = mgmt_ip
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")


## dictionary to start off with our hostnames and mgmt ip
nx_switches= {
    "dist-sw01": "10.10.20.177",
    "dist-sw02": "10.10.20.178"
    }
## function that verifies user input is a valid hostname in our dict
def name_to_ip(dev_inpt):
    if dev_inpt in nx_switches:
        mgmtip = nx_switches[dev_inpt]
    else :
        print("Try again")
        return None
    
    return mgmtip

## ip validator function, i know we already made some of these but this is also from chat GPT
def is_valid_ip_address(ip_address: str) -> bool:
    """
    Returns True if the given string is a valid IP address, else False.
    """
    # Split the string into 4 parts using dot as the separator
    parts = ip_address.split('.')
    
    # Check if the length of the parts is 4
    if len(parts) != 4:
        print("Invalid IP")
        return False
    
    # Check if each part is a number between 0 and 255
    for part in parts:
        try:
            num = int(part)
            if num < 0 or num > 255:
                return False
            
        except ValueError:
            print("Invalid IP")
            return False
    
    return True

## function that verifies the attempted hostname is a valid one
## from chat GPT
def valid_switch_hostname(hostname):
    """
    Returns True if the given hostname is valid for a switch, False otherwise.
    """
    # A valid switch hostname can contain only letters (a-z, A-Z), digits (0-9), and hyphens (-).
    # It must also start and end with a letter or digit, and be no longer than 63 characters.
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]$'
    return bool(re.match(pattern, hostname))

## function that confirms user input on mgmt_ip is one in our dict
def confirm_mgmt_ip_in_dict(nx_switches, mgmt_ip):
    if mgmt_ip in nx_switches.values():
        return True
    else:
        return False
  

## prints dictionary with hostnames and addresses that can be adjusted
for hostname,ip in nx_switches.items():
    print(hostname + " at " + ip+" is an avalible device to modify" )

##takes input for which hostname
dev_inpt = input("Type in which device you would like to modify? ")
## verifies input is valid also binds the mgmt_ip
mgmt_ip = name_to_ip(dev_inpt)
## takes user input on which mgmt ip to work with
verify_ip = input("Type the mgmt IP listed above to verify device being modified ")
## confirms user input is a valid ip
is_valid_ip_address(verify_ip)

## a printout of if user input matches what we have in dictionary
if confirm_mgmt_ip_in_dict(nx_switches, mgmt_ip):
    print("mgmt_ip exists in nx_switches dictionary")
else:
    print("mgmt_ip does not exist in nx_switches dictionary")

## cookie getter
cookie = getCookie("https://"+ mgmt_ip +"/api/aaaLogin.json")
## takes user input for new hostname
hostname = input("What should the new hostname be? ")
## runs user input through function to determine if its a valid hostname
if valid_switch_hostname(hostname):
    print(f"{hostname} is a valid switch hostname.")
else:
    print(f"{hostname} is not a valid switch hostname.")

## calls function that actually changes hostname
change_switch_hostname(hostname, mgmt_ip)
