### nested dictionary to be manipilated
devices = {
    "R1": {
        "hostname": "R1",
        "type": "router",
        "mgmtIP": "10.0.0.1",

        },
    "R2": {
        "type": "router",
        "hostname": "R2",
        "mgmtIP": "10.0.0.2",

        },
    "S1": {
        "type": "switch",
        "hostname": "S1",
        "mgmtIP": "10.0.0.3",
        },
    "S2": {
        "type": "switch",
        "hostname": "S2",
        "mgmtIP": "10.0.0.4",
        }
    }
### function for ping
def ping_f(pingf):
    for device in devices:
        print("ping", '\t', devices[device]['mgmtIP'])

ping_f(devices)
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
            test_ip2 = input("Enter a valid x.x.x.x IP address  ")
            ip_test(test_ip2)
            devices["S3"] = {
                "mgmtIP": test_ip2
                }
        if result == True:
            return result
### I spent many hours trying to figure out how to get the result of this function to return into my dictionary
### I got the test to verify a valid ip but not to store the valid address in the table and if you could show
### what do change to get the actual desired results it would be appreciated
            
### function that asks if user wants to add S3 and prompts and stores input
def get_input(prmpt,value_list):
    valid_input = False
    while valid_input == False:
        input_value = input(prmpt)
        if input_value in value_list:
            valid_input = True
            new_ip = input("Enter the new devices mgmtIP: ")
            act_ret = ip_test(new_ip)
            #new line below
            
            new_host = input("Enter the new devices name: ")
            new_type = input("Enter the new device type: ")
            devices["S3"] = {
                "type": new_type,
                "hostname": new_host,
                "mgmtIP": new_ip,
                }
            print("you have added: ", devices["S3"])
        else:
            print("If you want to add a device you must use one of: ",value_list)
            break
### i know breaks are poor form but i got it to work this way
    return input_value

prompt = "Would you like to add another device?"
valid_values = ["Y","y"]

add_another=get_input(prompt,valid_values)


###begin ntp server problem
ntp_server = {
    "Server1": "221.100.250.75",
    "Server2": "201.0.113.22",
    "Server3": "58.23.191.6",
    }
###dictionary for question 2
ntps1 = list(ntp_server.keys())
ntps2 = list(ntp_server.values())
###make dict into lists for easier access
def printer(rtr):
    print("Server Name" + '\t' + "Address")
    print("-" * 90)
    values= ' '
    for key in rtr.keys():
        values = values +str(rtr[key])
        values = values + '\t'
    print(ntps1[0], '\t' , ntps2[0], '\n', ntps1[1], '\t', ntps2[1], '\n', ntps1[2], '\t', ntps2[2])
    return values
###function to print list
printer(ntp_server)
def ping_prep(ip_list):
    for x in ntp_server.values():
        print("ping", '\t', x)

ping_prep(ntp_server.values())
###ping prep function and call

        

