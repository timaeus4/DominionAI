import random

def draw(deck, hand, discard):
    if(len(deck) == 0):
        deck, discard = refresh(deck, discard)
        
    if(len(deck) == 0):
        return deck, hand, discard
    
    card = deck.pop(0)
    hand.append(card)
    
    return deck, hand, discard
    
def check_top(deck, hand, discard):
    if(len(deck) == 0):
        deck, discard = refresh(deck, discard)
        
    if(len(deck) == 0):
        return deck, hand, discard
    
    card = deck[0]
    
    return card
    
def shuffle(deck):
    random.shuffle(deck)
    
    return deck

def refresh(deck, discard):
    deck.extend(discard)
    discard = []
    random.shuffle(deck)

    return deck, discard