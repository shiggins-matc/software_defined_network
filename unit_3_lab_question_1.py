import re
### had to look on stack overflow to find this
user_f = input("Enter your first name: ")
#user_l = input("Enter your last name: ")
##def name_check(verify,prmpt):
##    valid_input = False
##    while valid_input == False:
##
##        input_value = input(prmpt)
##        if input_value == type(str):
##            valid_input = True
##            print(name_q + user_f + " " + user_l)
##        else:
##            print("Input must be a valid name")
##
##    return input_value
### whole section above was an attempt that did not work but i am curious to learn how to make it
name_q = "Welcome to the system: "
match_f = re.match(r'^[A-Za-z ]*$', user_f)
### matches input to make sure alphabeic characters, taken from stack overflow
def name_f(arg_f):
    
    if match_f :
        
        print("valid name accepted");
    else:
    
        print("invalid name please try again")
### function to test f name vs alphabet
name_f(user_f)
user_l = input("Enter your last name: ")
match_l = re.match(r'^[A-Za-z ]*$', user_l)
def name_l(arg_l):
    
    if match_l :
        print(name_q + user_f + " " + user_l + " ");
        
    else:
    
        print("invalid name please try again")
###same as f name function
name_f(user_f)
name_l(user_l)
