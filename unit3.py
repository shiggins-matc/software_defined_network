router1 = {
    "hostname": "R1",
    "brand": "Cisco",
    "mgmtIP": "10.0.0.1",
    "interfaces": {
        "G0/0": "10.1.1.1",
        "G0/1": "10.1.2.1"
        }
    }
# dictionary block for print out below
print("router1 keys\n",router1.keys())
print("router1 [interfaces] keys\n", router1["interfaces"].keys())
print("router1 values\n",router1.values())
print("router1 [interfaces] values \n",router1["interfaces"].values())
print("router1 items\n",router1.items())
print("router1 [interfaces] items\n",router1["interfaces"].items())
for interface in router1["interfaces"]:
    print(interface + " " * 5 +router1["interfaces"][interface])
# Prints pairs of items and what they are
devices = {
    "R1": {
        "type": "router",
        "hostname": "R1",
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
#Nested dictionary we will be pulling from
for dog in devices:
    print("Ping" + " " * 5 +devices[dog]["mgmtIP"])
#print command for ping and a mgmt IP    

