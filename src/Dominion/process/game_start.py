import random
from Dominion.operation import deck_operation
from Dominion.card import card_factory as CF



# 共通サプライ
def set_common_supply(supply):
    bronze = CF.make_card('bronze')
    silver = CF.make_card('silver')
    gold = CF.make_card('gold')
    house = CF.make_card('house')
    territory = CF.make_card('territory')
    province = CF.make_card('province')
    curse = CF.make_card('curse')
    
    supply.append(bronze)
    supply.append(silver)
    supply.append(gold)
    supply.append(house)
    supply.append(territory)
    supply.append(province)
    supply.append(curse)
    
    return supply

# ランダム生成
def set_random_supply(version, max):
    supply = []
    # 乱数10個作る
    randlist = random.sample(range(max), 10)

    if version == "standard":
        for n in randlist:
            supply.append(CF.make_card_standard(n))
    
    return supply
    
def sort_by_cost(supply):
    for i in range(len(supply)):
        for j in range(len(supply) - i -1):
            if supply[j].cost > supply[j+1].cost:
                supply[j], supply[j+1] = supply[j+1], supply[j]
    return supply
    
def setup_personal_info():
    
    bronze = CF.make_card('bronze')
    house = CF.make_card('house')
    
    deck = []
    hand = []
    discard = []
        
    for i in range(7):
        deck.append(bronze)
        
    for i in range(3):
        deck.append(house)
        
    deck = deck_operation.shuffle(deck)
    
    for i in range(5):
        deck, hand, discard = deck_operation.draw(deck, hand, discard)
        
    return deck, hand, discard