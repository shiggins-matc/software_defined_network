## This script is the first part of the final project. this script reads a json dictionary file loads it in and lets you add, remove, modify, save and quit when done.
## Written by Isaac Powers, Cole Gnatzig, Will Loper and Sean Higgins




import json
import requests

def load_inventory(): #Loads the inventory.json file to be used when altering the device dictionary

    """Loads the inventory file as a dictionary.""" 

    with open("inventory.json", "r") as f: #Opens inventory.json to read using the imported json package

        inventory = json.load(f) #Assigns the contents of the json file to the variable 'inventory'

        return inventory #Returns the inventory from the json file back to the main Function

def print_dict(device_dict): #Prints the device_dict in a table format

    print(f"Hostname\tType\tIp Address") #Prints the heading to the columns

    for device in device_dict: #Runs the for loop for each device in the dictionary

        print(device_dict[device]['hostname'], end='' + '\t') #Prints the hostname for the device

        print(device_dict[device]['device type'], end='' + '\t') #Prints the device type for the device

        print(device_dict[device]['mgmtIp']) #Prints the mgmtIP for the device
 
	
def add_device(device_dict): #Adds a device to the dictionary

	var = False #Sets var to False so it iterates through the while loop until the condition is met

	while var == False: #Runs the loop until the condition is met

		new_ip = input("What would you like the new IP address to be? ") #Asks for user input on what the IP address should be

		if check_ip(new_ip) == True and validate_IP_in_dict(new_ip, device_dict) == True: #Runs two functions to ensure the IP is a valid IP as well as it doesn't currently exist within the dictionary
		
			var = True #Set var to True to exit the while loop

		else: #If either the conditions are not met in the previous if statement then it informs the user the IP is invalid and reruns the loop

			print("Invalid IP.") 
	
	var = False #Sets var to False so it iterates through the while loop until the condition is met
	
	while var == False: #Runs the loop until the condition is met
	
		new_hostname =  input("What would you like the new hostname to be? ") #Asks for user input on what the hostname should be
	
		if validate_hostname_in_dict(new_hostname, device_dict) == True: #Runs the function to ensure the hostname is not currently in use within the dictionary
		
			var = True #Set var to True to exit the while loop
		
		else: #If the hostname is currently in use then it informs the user and reruns the loop
		
			print("Hostname already in use")
			
	var = False #Sets var to False so it iterates through the while loop until the condition is met
	
	while var == False: #Runs the loop until the condition is met
		
		userInput = input("What device type would you like to change this device to?\n1) NXOS\n2) IOS XE\n") #Asks for user input on what the device type should be
		if userInput == "1": #If the user inputs 1 it will set the new device type to a NXOS device
			new_device_type = "NXOS"
			var = True #Set var to True to exit the while loop
		elif userInput == "2": #If the user inputs 2 it will set the new device type to a IOS XE device
			new_device_type = "IOS XE"
			var = True #Set var to True to exit the while loop
		else: #If neither 1 or 2 is input then it informs the user that the input was invalid and reruns the loop
			print("Invalid selection")
				
	device_dict.update({new_hostname: {"hostname":new_hostname,"device type":new_device_type,"mgmtIp":new_ip}}) #Updates the device_dict with the new items asked by the user
	
	return device_dict #Returns the dictionary back to the main function
	
def modify_device(device_dict): #Function to reroute to a different modification function based on user input
	
	userInput = input("What device would you like to modify? ")  #Asks the user which device they would like to modify
	if userInput in device_dict.keys(): #Confirms that the device the user entered is located in the device dictionary
		userInput_Mod = input("What would you like to modify about " + userInput + "?\n1) IP Address\n2) Hostname\n3) Device Type\n") #Asks for user input on what they would like to modify about the device
		if userInput_Mod == "1": #If the user inputs 1 it reroutes them to the IP modification function
			modify_IP(device_dict,userInput)	
		elif userInput_Mod == "2": #If the user inputs 2 it reroutes them to the hostname modification function
			modify_hostname(device_dict,userInput)	
		elif userInput_Mod == "3": #If the user inputs 3 it reroutes them to the device type modification function
			modify_device_type(device_dict,userInput)	
		else: #If the user inputs an invalid selection then it alerts them and exits the function
			print("Invalid selection")		
	else: #If the user inputs an invalid device then it alerts them and exits the function
		print("Invalid device")
		
	return device_dict #Returns the device dictionary back to the main function
	
def modify_IP(device_dict,device_name): #Function to modify the IP address of a device

	var = False #Sets var to False so it iterates through the while loop until the condition is met

	while var == False: #Runs the loop until the condition is met

		new_ip = input("What would you like the new IP address to be? ") #Asks for user input on what the IP address should be

		if check_ip(new_ip) == True and validate_IP_in_dict(new_ip, device_dict) == True: #Runs two functions to ensure the IP is a valid IP as well as it doesn't currently exist within the dictionary

			device_dict[device_name]['mgmtIp'] = new_ip #Sets the new IP inputted by the user

			var = True #Set var to True to exit the while loop

		else: #If either the conditions are not met in the previous if statement then it informs the user the IP is invalid and reruns the loop

			print("Invalid IP.") 

	return device_dict #Returns the device dictionary back to the main function
    
def modify_hostname(device_dict,device_name): #Function to modify the hostname of a device
	
	var = False #Sets var to False so it iterates through the while loop until the condition is met
	
	while var == False: #Runs the loop until the condition is met
	
		new_hostname =  input("What would you like the new hostname to be? ") #Asks for user input on what the hostname should be
	
		if validate_hostname_in_dict(new_hostname, device_dict) == True: #Runs the function to ensure the hostname is not currently in use within the dictionary
		
			device_dict[device_name]["hostname"] = new_hostname #Sets the new hostname inputted by the user
		
			var = True #Set var to True to exit the while loop
		
		else: #If the hostname is already present in the dictionary it alerts the user
		
			print("Hostname already in use")
		
	return device_dict #Returns the device dictionary back to the main function
	
def modify_device_type(device_dict,device_name):
	
	userInput = input("What device type would you like to change this device to?\n1) NXOS\n2) IOS XE\n") #Asks for user input on what the device type should be
	if userInput == "1":#If the user inputs 1 it will set the new device type to a NXOS device
		device_dict[device_name]["device type"] = "NXOS"
	elif userInput == "2":#If the user inputs 2 it will set the new device type to a IOS XE device
		device_dict[device_name]["device type"] = "IOS XE"
	else: #If neither 1 or 2 is input then it informs the user that the input was invalid
		print("Invalid selection")
		
	return device_dict #Returns the device dictionary back to the main function
	
def del_device(device_dict): #Deletes a device from the dictionary

	userInput = input("What device would you like to delete? ") #Asks the user which device they would like to delete
	if userInput in device_dict.keys(): #Checks to see if the device the user input is located within the dictionary
		device_dict.pop(userInput) #If the device is located it deletes it from the dictionary
	else: #If the device is not found in the dictionary it alerts the user
		print("Invalid device")
		
	return device_dict #Returns the device dictionary back to the main function
	

def save_dict(device_dict): #Saves the dictionary back to the inventory.json file

    """ Saves the inventory to the file. """ 

    with open('inventory.json', "w") as f: #Writes to the inventory.json file

        json.dump(device_dict, f) 
        
    print("Inventory updated") #Lets the user know that the file was updated with their changes
	
	
def validate_IP_in_dict(ipAddr, device_dict): #Validates that an IP input is not already located in the dictionary

	return_val = True #Default returns true that the IP input is unique

	for device in device_dict.values(): #Runs through every device located in the dictionary

		if ipAddr in device["mgmtIp"]: #If the IP address is already in use this if statement is ran

			print("That IP already exists. Please enter again.") 

			return_val = False #Sets the value to false


	return return_val #Returns the boolean value if the value was found or not
            
def validate_hostname_in_dict(hostname, device_dict): #Validates that a hostname input is not already located in the dictionary

	return_val = True #Default returns true that the IP input is unique
	
	for device in device_dict.values(): #Runs through every device located in the dictionary
	
		if hostname in device['hostname']: #If the hostname is already in use this if statement is ran
		
			print("That hostname already exists. Please enter again.")
			
			return_val = False #Sets the value to false
				
	return return_val #Returns the boolean value if the value was found or not
	
# This function will check if the entered IP address is valid 

def check_ip(ip_address): 

    valid_ip = True 

# take the input and make a list, with the "." as the separator 

    list_ip = ip_address.split(".") 

# check that length of the list is 4 

    if len(list_ip) != 4: 

        valid_ip = False 

# loop through items in list_ip 

    if len(list_ip) == 4: 

        for n in list_ip: 

# check each item is numeric 

            if not n.isdigit(): 

                valid_ip = False 

# check if integer is between 0 and 255 

            if n.isdigit(): 

                if not (0 <= int(n) <= 255): 

                    valid_ip = False 

    return valid_ip 

def is_valid_cisco_hostname(hostname): 

    """ 

    Verify if a given hostname is valid according to Cisco's naming conventions. 

    Args: 

        hostname (str): The hostname to be verified. 

    Returns: 

        bool: True if the hostname is valid, False otherwise. 

    """ 

    validReturn = True 

    # Check if hostname is longer than 63 characters 

    if len(hostname) > 63: 

        validReturn = False 

    # Check if hostname starts with an alphabetic character 

    elif not hostname[0].isalpha(): 

        validReturn = False 

    # Check if hostname ends with an alphanumeric character 

    elif not hostname[-1].isalnum(): 

        validReturn = False 

    # Check if hostname contains only valid characters (letters, numbers, hyphen, or underscore) 

    for char in hostname[1:-1]: 

        if not char.isalnum() and char != '-' and char != '_': 

            validReturn = False 

    return validReturn 

  


# set a control variable to false 

device_inventory = load_inventory() #Loads the inventory from the inventory.json file
print(device_inventory)

var = False #Set the variable to False to keep the while loop running until the user prompts to quit and the value changes

while var == False: #Runs the while loop until the variable is set to true within the quit elif statement

    user_input = input("What would you like to do? Enter a to add device, m to modify, d to delete, s to save, or q for quit: ") #Asks the user for a character input to decide what they would like to change about the devices

    if user_input == "a": #Runs if the user inputs an 'a' to add a device
        device_inventory = add_device(device_inventory) 
    elif user_input == "m": #Runs if the user inputs an 'm' to modify a device
        device_inventory = modify_device(device_inventory)
    elif user_input == "d": #Runs if the user inputs an 'd' to delete a device
        device_inventory = del_device(device_inventory) 
    elif user_input == "s": #Runs if the user inputs an 's' to save the changes
        save_dict(device_inventory) 
    elif user_input == "q": #Runs if the user inputs an 'q' to quit the script
        var = True #Set the variable to true to exit the while loop
    else: #Informs the user that their entry was invalid and to try again
        print("That is not a valid entry. Try again.") 
    print_dict(device_inventory)
        

