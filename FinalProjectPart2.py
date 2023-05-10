import requests 

import urllib3 

import json 

import ipaddress 

urllib3.disable_warnings() 

  

  

def load_inventory(): 

    """Loads the inventory file as a dictionary.""" 

    with open('inventory.json', 'r') as f: #Opens inventory.json to read using the imported json package

        inventory = json.load(f) #Assigns the contents of the json file to the variable 'inventory'

        return inventory #Returns the inventory from the json file back to the main Function

  

  

# Function gets a cookie. Receives an ip address as a string and returns the cookie json response. 

def get_cookie(addr): 

    url = f"https://{addr}/api/aaaLogin.json" #Creates the URL variable that stores the str in which the device can be accessed through

    payload = {"aaaUser": {"attributes": {"name": "cisco", "pwd": "cisco"}}} #Defines the payload to use when accessing the device to generate the cookie

    response = requests.post(url, json=payload, verify=False) #Stores the response generated from the device

    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"] #Returns the cookie from where it was called

  

  

# This function takes a str and returns a json response of interface info 

def get_ints(deviceIP): 

    url = "https://"+deviceIP+":443/restconf/data/ietf-interfaces:interfaces" #Creates the URL variable that stores the str in which the device can be accessed through

    username = 'cisco' #Sets the username to use when accessing the device

    password = 'cisco' #Sets the password to use when accessing the device

    payload = {} 

    headers = { 

        'Content-Type': 'application/yang-data+json', 

        'Accept': 'application/yang-data+json', 

        'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm' 

    } 

    response = requests.request("GET", url, auth=( 

        username, password), verify=False, headers=headers, data=payload) #Stores the response generated from the device

    return response.json()['ietf-interfaces:interfaces']['interface'] #Returns the list of interfaces on the Device using the IP passed into the function

  

  

# Function creates a vlan. Receives 3 str, and returns json response of POST. 

def create_vlan(deviceIp, vlanNum, vlanName): 

    cookie = get_cookie(deviceIp) #Calls the get_cookie function to generate the cookie to use within the header

    url = f"https://{deviceIp}/api/node/mo/sys/bd.json?query-target=children" #Creates the URL variable that stores the str in which the device can be accessed through

    payload = { 

        "l2BD": { 

            "attributes": { 

                "fabEncap": vlanNum, #Sets the VLAN number

                "name": vlanName #Sets the VLAN name

            } 

        } 

    } 

    headers = { 

        'Content-Type': 'text/plain', 

        'Cookie': f'APIC-cookie={cookie}' 

    } 

    response = requests.request( 

        "POST", url, verify=False, headers=headers, data=json.dumps(payload)) #Stores the response generated from the device

    return response #Returns back to the main function

  

  

# Function creates a SVI. Receives 3 str, and returns json response of POST. 

def create_SVI(deviceIp, sviName, sviIpAddr): 

    cookie = get_cookie(deviceIp) #Calls the get_cookie function to generate the cookie to use within the header

    url = f"https://{deviceIp}/api/node/mo/sys.json?query-target=self" #Creates the URL variable that stores the str in which the device can be accessed through

    payload = { 

        "topSystem": { 

            "children": [ 

                { 

                    "ipv4Entity": { 

                        "children": [ 

                            { 

                                "ipv4Inst": { 

                                    "children": [ 

                                        { 

                                            "ipv4Dom": { 

                                                "attributes": { 

                                                    "name": "default" 

                                                }, 

                                                "children": [ 

                                                    { 

                                                        "ipv4If": { 

                                                            "attributes": { 

                                                                "id": sviName #Sets the newly created SVIs name to the variable passed into the function

                                                            }, 

                                                            "children": [ 

                                                                { 

                                                                    "ipv4Addr": { 

                                                                        "attributes": { 

                                                                            "addr": sviIpAddr #Sets the newly created SVIs IP to the variable passed into the function

                                                                        }}}]}}]}}]}}]}},{ 

                    "interfaceEntity": { 

                        "children": [{ 

                                "sviIf": { 

                                    "attributes": { 

                                        "adminSt": "up", 

                                        "id": sviName #Sets the newly created SVIs name to the variable passed into the function

                                    }}}]}}]}} 

    headers = { 

        'Content-Type': 'text/plain', 

        'Cookie': f'APIC-cookie={cookie}' 

    } 

    response = requests.request( 

        "POST", url, verify=False, headers=headers, data=json.dumps(payload)) #Stores the response generated from the device

    return response #Returns the response back to the main function

  

# Function takes in an IP address and calculates the first usable IP address in the network and returns it as a string 

def calculate_hsrp_address(ip): 

# Convert the input IP address to an IPv4 network object 

# strict= False means the IP address can be a host address 

    ip_network = ipaddress.ip_network(ip, strict=False) 

# Get the first usable IP address in the network, use [1] so that the address is not the network address itself 

    hsrp_standby_address = str(ip_network[1]) 

    return hsrp_standby_address 

  


# This function passes in the IP address of a device and an interface and a HSRP group and address to configure them on the specified device and interface 

def create_hsrp(ip_addr, interface, hsrp_grp, hsrp_addr): 

    cookie = get_cookie(ip_addr) #Calls the get_cookie function to generate the cookie to use within the header

    url = "https://" + ip_addr + "/api/mo/sys.json" #Creates the URL variable that stores the str in which the device can be accessed through

    payload= { 

  "topSystem": { 

    "children": [ 

      { 

        "interfaceEntity": { 

          "children": [ 

            { 

              "sviIf": { 

                "attributes": { 

                  "id": interface #Defines which interface we are adding the HSRP on

                }}}]}}, 

      { 

        "hsrpEntity": { 

          "children": [ 

            { 

              "hsrpInst": { 

                "children": [ 

                  { 

                    "hsrpIf": { 

                      "attributes": { 

                        "id": interface #Defines which interface we are adding the HSRP on

                      }, 

                      "children": [ 

                        { 

                          "hsrpGroup": { 

                            "attributes": { 

                              "af": "ipv4", 

                              "id": hsrp_grp, #Sets the newly created HSRP group to the variable passed into the function

                              "ip": hsrp_addr, #Sets the newly created HSRP virtual IP to the variable passed into the function

                              "ipObtainMode": "admin" 

                            }}}]}}]}}]}}]}} 

    headers = { 

        'Content-Type': 'application/json', 

        'Cookie': 'APIC-cookie=' + cookie 

    } 

    response = requests.request("POST", url, headers=headers, verify = False, data=json.dumps(payload)) #Stores the response generated from the device

    return response.json() #Returns the response back to the main function

  

# Function creates an OSPF entry for an interface. Receives 4 str, and returns json response of POST. 

def add_int_to_process_area(deviceIp, intName, ospfProId, ospfArea): 

    cookie = get_cookie(deviceIp) #Calls the get_cookie function to generate the cookie to use within the header

    url = "https://"+deviceIp+"/api/node/mo/sys.json?query-target=self" #Creates the URL variable that stores the str in which the device can be accessed through

    payload = { 

        "topSystem": { 

            "children": [ 

                { 

                    "ospfEntity": { 

                        "children": [ 

                            { 

                                "ospfInst": { 

                                    "attributes": { 

                                        "name": ospfProId #Defines the process ID to use when adding new interfaces into the OSPF area

                                    }, 

                                    "children": [ 

                                        { 

                                            "ospfDom": { 

                                                "attributes": { 

                                                    "name": "default" 

                                                }, 

                                                "children": [ 

                                                    { 

                                                        "ospfIf": { 

                                                            "attributes": { 

                                                                "advertiseSecondaries": "yes", 

                                                                "area": ospfArea, #Sets which area the interface should be on for OSPF

                                                                "id": intName #Sets the name of the interface to use OSPF to the variable passed into the function

                                                            }}}]}}]}}]}}]}} 

    headers = { 

        'Content-Type': 'text/plain', 

        'Cookie': f'APIC-cookie={cookie}' 

    } 

    response = requests.request( 

        "POST", url, verify=False, headers=headers, data=json.dumps(payload)) #Stores the response generated from the device

    return response #Returns the response back to the main function

  

  

# Changes an IP address on a IOSXE device. Takes a str and returns json response. 

def change_ip(ipAddr, intName, intIp, netMask): 

    url = "https://"+ipAddr+":443/restconf/data/ietf-interfaces:interfaces/interface="+intName #Creates the URL variable that stores the str in which the device can be accessed through

    username = 'cisco' #Sets the username to use when accessing the device

    password = 'cisco' #Sets the password to use when accessing the device

    payload = {"ietf-interfaces:interface": { 

        "name": intName, #Defines the interface we are changing IP addresses on

        "description": "Configured by RESTCONF", 

        "type": "iana-if-type:ethernetCsmacd", 

        "enabled": "true", 

        "ietf-ip:ipv4": { 

            "address": [{ 

                "ip": intIp, #Sets the new IP for the interface based on the variable passed into the function

                "netmask": netMask #Set the subnet mask for the interface based on the variable passed into the function

            }]}}} 

     

    headers = { 

        'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm', 

        'Accept': 'application/yang-data+json', 

        'Content-Type': 'application/yang-data+json' 

    } 

  

    response = requests.request("PUT", url, auth=(username, password), headers=headers, verify=False, data=json.dumps(payload)) #Stores the response generated from the device

  



# Updates the IP address entered by delta amount in the octet entered into the function  

def update_address(ipAddress, octet, delta): 

    ipList = ipAddress.split(".") #Splits the IP address into its 4 octets

    ipList[octet-1] = str(int(ipList[octet-1]) + delta) #Updates the octet specified by the variable passed by delta amount

    ipAddress = ".".join(ipList) #Rejoins the list back into one string

    return ipAddress #Returns the new IP address

  

# Updates the SVI address to use within HSRP  

def update_svi_address(ipAddress, octet, delta): 

    ipList = ipAddress.split(".") #Splits the IP address into its 4 octets

    ipList[octet-1] = str(int(ipList[octet-1]) + delta[0]) #Updates the octet specified to be 0 (This will only work in increments of /8)

    ipAddress = ".".join(ipList) #Rejoins the list back into one string

    delta[0] += 1 #Updates the octet specified +1 to be the first usable address

    return ipAddress #Returns the new IP address

  

  

# This function takes a str and returns a json response of interface info 

def change_ip_NXOS(deviceIP, intName, addr): 

    cookie = get_cookie(deviceIP) #Calls the get_cookie function to generate the cookie to use within the header

    url = f"https://{deviceIP}/api/node/mo/sys.json?query-target=self" #Creates the URL variable that stores the str in which the device can be accessed through

    payload = { 

        "topSystem": { 

            "children": [ 

                {"ipv4Entity": { 

                    "children": [ 

                        { 

                            "ipv4Inst": { 

                                "children": [ 

                                    { 

                                        "ipv4Dom": { 

                                            "attributes": { 

                                                "name": "default" 

                                            }, 

                                            "children": [ 

                                                { 

                                                    "ipv4If": { 

                                                        "attributes": { 

                                                            "id": intName #Defines the interface that the IP is going to be updated on

                                                        }, 

                                                        "children": [ 

                                                            { 

                                                                "ipv4Addr": { 

                                                                    "attributes": { 

                                                                        "addr": f"{addr}" #Sets the IP address to be the variable passed into the function

                                                                    }}}]}}]}}]}}]}}]}} 

    headers = { 

        'Content-Type': 'text/plain', 

        'Cookie': f'APIC-cookie={cookie}' 

    } 

    response = requests.request( 

        "POST", url, verify=False, headers=headers, data=json.dumps(payload)) #Stores the response generated from the device

    return response #Returns the response back to the main function

  

  

def get_int_info(ipAddress): 

    cookie = get_cookie(ipAddress) #Calls the get_cookie function to generate the cookie to use within the header

    url = f"https://{ipAddress}/api/node/mo/sys/ipv4/inst/dom-default.json?query-target=children" #Creates the URL variable that stores the str in which the device can be accessed through

    payload = {} 

    headers = { 

        'Content-Type': 'text/plain', 

        'Cookie': f'APIC-cookie={cookie}' 

    } 

    response = requests.request( 

        "GET", url, verify=False, headers=headers, data=payload) #Stores the response generated from the device

    return response.json() #Returns the response back to the main function

  

  

def get_int_ip_info(ipAddress, intName): 

    cookie = get_cookie(ipAddress) #Calls the get_cookie function to generate the cookie to use within the header

    url = f"https://{ipAddress}/api/node/mo/sys/ipv4/inst/dom-default/if-{intName}.json?query-target=children" #Creates the URL variable that stores the str in which the device can be accessed through

    payload = {} 

    headers = { 

        'Content-Type': 'text/plain', 

        'Cookie': f'APIC-cookie={cookie}' 

    } 

    response = requests.request( 

        "GET", url, verify=False, headers=headers, data=payload) #Stores the response generated from the device

    return response.json()['imdata'][0]['ipv4Addr']['attributes']['addr'] #Returns the interface's IP info

  

  

def get_int_eth_ip_info(ipAddress, intName): 

    cookie = get_cookie(ipAddress) #Calls the get_cookie function to generate the cookie to use within the header

    url = f"https://{ipAddress}/api/node/mo/sys/ipv4/inst/dom-default/if-[{intName}].json?query-target=children" #Creates the URL variable that stores the str in which the device can be accessed through

    payload = {} 

    headers = { 

        'Content-Type': 'text/plain', 

        'Cookie': f'APIC-cookie={cookie}' 

    } 

    response = requests.request( 

        "GET", url, verify=False, headers=headers, data=payload) #Stores the response generated from the device

    return response.json()['imdata'][0]['ipv4Addr']['attributes']['addr'] #Returns the interface's IP info

  

  

### Main ### 

# Static values for the octet and octet_delta for the update_address() function. 

OCTET = 2 

OCTET_DELTA = 15 

  

# Static values for the octet and octet_delta for the update_svi_address() function. 

OCTET_SVI = 4 

OCTET_DELTA_SVI = [1] 

  

  

# All other static str values 

vlanNum = 'vlan-120' 

vlanNam = 'testNXOS' 

sviName = 'vlan120' 

networkAddr = '172.31.120.1' 

hsrpGroup = '10' 

ospfProId = '1' 

ospfArea = '0.0.0.0' 

  

device_dict = load_inventory() #Calls the load inventory function to pass the contents into device_dict

  

for device in device_dict: #Runs the for loop for each device located in the inventory.json file

    hostname = device_dict[device]['hostname'] #Sets the hostname based on the contents of the dictionary

    print(hostname) 

    deviceType = device_dict[device]['device type'] #Sets the device type based on the contents of the dictionary

    print(deviceType) 

    mgmtIP = device_dict[device]['mgmtIp'] #Sets the mgmtIP based on the contents of the dictionary

    if deviceType == 'NXOS': #Runs this if statement if the type of device is a NXOS switch

        intInfo = get_int_info(mgmtIP) #Calls the get_int_info function to get information about the switch to be used when updating values

        for interface in intInfo['imdata']: #Runs this for loop for each interface that is found on the device

            if 'vlan120' in interface['ipv4If']['attributes']['id']: #If VLAN 120 is not present yet we run this

                sviIpAddr = update_svi_address(networkAddr, OCTET_SVI, OCTET_DELTA_SVI) #Calls the update_svi_address

                print(sviIpAddr) 

                create_vlan(mgmtIP, vlanNum, vlanNam) #Calls the create_vlan function

                create_SVI(mgmtIP, sviName, f'{sviIpAddr}/24') #Calls the create_SVI function

                svi_addr = '172.31.120.1/24' #Sets the SVI address to be added to vlan 120

                hsrp_address_svi = calculate_hsrp_address(svi_addr) #Calculates the HSRP address for VLAN 120 to be the first usable

                print(hsrp_address_svi) 

                create_hsrp(mgmtIP, sviName, hsrpGroup, hsrp_address_svi) #Creates the HSRP on the VLAN 120

            elif 'vlan' in interface['ipv4If']['attributes']['id'] and not 'vlan120' in interface['ipv4If']['attributes']['id']: #If the interface is a VLAN and not VLAN 120 we run this

                interfaceName = interface['ipv4If']['attributes']['id'] #Pulls the name of the interface and stores it

                print(interfaceName) 

                interfaceIP = get_int_ip_info(mgmtIP, interfaceName) #Gets the IP info for the interface
    
                print(interfaceIP) 

                updatedIP = update_address(interfaceIP, OCTET, OCTET_DELTA) #Updates the IP to be incremented 15 in the second octet

                print(updatedIP) 

                change_ip_NXOS(mgmtIP, interfaceName, updatedIP) #Changes the IP on the NXOS switch

                hsrp_address = calculate_hsrp_address(updatedIP) #Calculates the HSRP to be the first usable address in the subnet

                print(hsrp_address) 

                create_hsrp(mgmtIP, interfaceName, hsrpGroup, hsrp_address) #Creates the HSRP for the VLAN interface

                #add_int_to_process_area(mgmtIP, interfaceName, ospfProId, ospfArea) 

            else: 

                interfaceName = interface['ipv4If']['attributes']['id'] #Pulls the name of the interface and stores it

                interfaceIP = get_int_eth_ip_info(mgmtIP, interfaceName) #Gets the IP of the mgmt interface

                updatedIP = update_address(interfaceIP, OCTET, OCTET_DELTA) #Updates the IP for the mgmt interface

                change_ip_NXOS(mgmtIP, interfaceName, updatedIP) #Changes the IP for the mgmt interface

                #add_int_to_process_area(mgmtIP, interfaceName, ospfProId, ospfArea) 
                
    if deviceType == 'IOS XE':  #Runs this if statement if the type of device is a IOS XE device

        intList = get_ints(mgmtIP) #Gets the list of interfaces on the IOS XE devices

        for interface in intList:  #Runs this for loop for each interface on the device

            interfaceName = interface['name']  #Pulls the interface name

            if interfaceName != 'GigabitEthernet1' and interfaceName != 'Loopback0':  #Checks to make sure the interface is not the G0/1 interface or the loopback interface as these shouldnt be altered

                interfaceIP = interface['ietf-ip:ipv4']['address'][0]['ip']  #Pulls the IP address for the interface

                netMask = interface['ietf-ip:ipv4']['address'][0]['netmask']  #Pulls the subnet mask for the IP on the interface

                updatedIP = update_address(interfaceIP, OCTET, OCTET_DELTA)  #Updates the IP to increment the second octet by 15

                change_ip(mgmtIP, interfaceName, updatedIP, netMask)  #Changes the IP address on the device to be updated with our values

                add_int_to_process_area(mgmtIP, interfaceName, ospfProId, ospfArea) #Adds the interface to the OSPF area
