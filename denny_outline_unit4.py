import requests
#Receives a string that is a number from 1 -3 which will be used to get that number of decks from the API
#Return a deck_id from the API

def getNewDeck(num_decks):   

    url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=" + num_decks
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)


    deck_id = response.json()["deck_id"]

    return deck_id

## function that takes input for how many decks to use in our game
def getNumberofDecks():

    isValidNumber = False

    while isValidNumber == False:
        num_chosen = input("Enter the number of decks (1 - 3): ")
        if num_chosen == "1" or num_chosen == "2" or num_chosen == "3":
            isValidNumber = True

        else:

            print("Invalid entry")

    return num_chosen

## function that prints the rules, once when the game starts then can be repeated if desired
def printRules():
    print("Hello, and welcome to Sean's card game.")
    print("In this game you will decide how many cards both you and a computer will draw,")
    print("Points are earned = to the number on the card and highest score will win")
    print("Also Jack = 11, Queen = 12, King =13 and Ace = 1")

## function that takes input for how many cards with which to war, only takes 1-5 to confirm valid inputs 
def getNumberOfCards():
    isValidNumber = False
    while isValidNumber == False:
        num_cards = input("How many cards would you like each player to draw? (1-5): ")
        if num_cards == "1" or num_cards == "2" or num_cards == "3" or num_cards =="4" or num_cards == "5":
            
            isValidNumber = True

        else:
            print("Invalid entry")

    return num_cards #string

def drawCards(deck_id, num_of_cards_to_draw):  #API call to get cards
    url = "https://deckofcardsapi.com/api/deck/" +deck_id + "/draw/?count=" + num_of_cards_to_draw
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)


    card_list = response.json()["cards"]
    return card_list

##function that prints the value and suit of cards drawn
def printCards(cardsList):
    

    for card in cardsList:
        print(card["value"] + " of " + card["suit"])

## function that hard codes the values of cards drawn then reiterates and adds the cards togeather for total score
def calculateScore(cardsList):
    score = 0 
    for var in cardsList:
        if var["value"] == "2":
            score = score + 2
        elif var["value"] == "3":
            score = score + 3
        elif var["value"] == "4":
            score = score + 4
        elif var["value"] == "5":
            score = score + 5
        elif var["value"] == "6":
            score = score + 6
        elif var["value"] == "7":
            score = score + 7
        elif var["value"] == "8":
            score = score + 8
        elif var["value"] == "9":
            score = score + 9
        elif var["value"] == "10":
            score = score + 10
        elif var["value"] == "JACK":
            score = score + 11
        elif var["value"] == "QUEEN":
            score = score + 12
        elif var["value"] == "KING":
            score = score + 13
        elif var["value"] == "ACE":
            score = score + 1
    return score #integer
#####Main

printRules()

#ask a user for the number of decks returns string that is 1-3, then stores that in a variable
number_of_decks = getNumberofDecks()

##takes the result of previous function and puts that into our API call for a deck ID
deck_id = getNewDeck(number_of_decks)

## function takes 1-5 input for cards drawn and stores it as a variable
num_of_cards_to_draw = getNumberOfCards()


#if num_of_cards_to_draw == 0 quit else do the stuff below

## sets the cards the computer draws with a deck id and how many cards drawn
cardsList_Computer = drawCards(deck_id, num_of_cards_to_draw)


## same as above but for the user
cardsList_User = drawCards(deck_id, num_of_cards_to_draw)

print("You drew the following cards: " ) #Users cards
## uses print cards function to display what was drawn for user
printCards(cardsList_User)

print("The computer drew the following cards: ")
## same but for computer
printCards(cardsList_Computer)
## uses calulate score to total up cards and stores it under user score
user_score = calculateScore(cardsList_User)

print("You scored: " , user_score)
## same as user_score but for computer
computer_score = calculateScore(cardsList_Computer)

### compares the scores and declares a winner
print("The computer scored: ", computer_score)
if computer_score > user_score:
    print("Mankind is bested by machines yet again")
elif computer_score == user_score:
    print("A tie has been drawn!")
elif computer_score < user_score:
    print("You bested the machines! yay")



