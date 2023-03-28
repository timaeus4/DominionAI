import random
from Dominion.card import card_factory as CF

def coin_method(money):
    if(money >= 8):
        card = CF.make_card('province')
    elif(money >= 6):
        card = CF.make_card('gold')
    elif(money >= 3):
        card = CF.make_card('silver')
    else:
        card = None
        
    return card
    
def random_method(money, cardlist):
    
    while(True):
        rand = random.randint(0, len(cardlist)-1)
        card = cardlist[rand]
        
        if(card.cost <= money):
            break
    
    return card