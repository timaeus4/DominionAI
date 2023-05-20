from Dominion.card.cardlist import action_card
from Dominion.card.cardlist import money_card
from Dominion.card.cardlist import victory_card

def make_card(name):
    if(name=="house"):
        return victory_card.house()
    elif(name=="territory"):
        return victory_card.territory()
    elif(name=="province"):
        return victory_card.province()
    elif(name=="bronze"):
        return money_card.bronze()
    elif(name=="silver"):
        return money_card.silver()
    elif(name=="gold"):
        return money_card.gold()
    elif(name=="curse"):
        return victory_card.curse()
    elif(name=="cellar"):
        return action_card.cellar()
    elif(name=="chapel"):
        return action_card.chapel()
    elif(name=="moat"):
        return action_card.moat()
    elif(name=="vassal"):
        return action_card.vassal()
    elif(name=="workshop"):
        return action_card.workshop()
    elif(name=="merchant"):
        return action_card.merchant()
    elif(name=="herbinger"):
        return action_card.herbinger()
    elif(name=="village"):
        return action_card.village()
    elif(name=="remodel"):
        return action_card.remodel()
    elif(name=="blacksmith"):
        return action_card.blacksmith()
    elif(name=="money_lender"):
        return action_card.money_lender()
    elif(name=="throne_room"):
        return action_card.throne_room()
    elif(name=="poacher"):
        return action_card.poacher()
    elif(name=="militia"):
        return action_card.militia()
    elif(name=="bureaucrat"):
        return action_card.bureaucrat()
    elif(name=="gardens"):
        return victory_card.gardens()
    elif(name=="market"):
        return action_card.market()
    elif(name=="stentry"):
        return action_card.stentry()
    elif(name=="council_room"):
        return action_card.council_room()
    elif(name=="laboratory"):
        return action_card.laboratory()
    elif(name=="mine"):
        return action_card.mine()
    elif(name=="festival"):
        return action_card.festival()
    elif(name=="archive"):
        return action_card.archive()
    elif(name=="bandit"):
        return action_card.bandit()
    elif(name=="witch"):
        return action_card.witch()
    elif(name=="artisan"):
        return action_card.artisan()
    else:
        raise Exception("Invalid cardname")
    
def make_card_common(num):
    if(num==0):
        return victory_card.house()
    elif(num==1):
        return victory_card.territory()
    elif(num==2):
        return victory_card.province()
    elif(num==3):
        return money_card.bronze()
    elif(num==4):
        return money_card.silver()
    elif(num==5):
        return money_card.gold()
    elif(num==6):
        return victory_card.curse()
    else:
        raise Exception("Invalid number")

def make_card_standard(num):
    if(num==0):
        return action_card.cellar()
    elif(num==1):
        return action_card.chapel()
    elif(num==2):
        return action_card.moat()
    elif(num==3):
        return action_card.vassal()
    elif(num==4):
        return action_card.workshop()
    elif(num==5):
        return action_card.merchant()
    elif(num==6):
        return action_card.herbinger()
    elif(num==7):
        return action_card.village()
    elif(num==8):
        return action_card.remodel()
    elif(num==9):
        return action_card.blacksmith()
    elif(num==10):
        return action_card.money_lender()
    elif(num==11):
        return action_card.throne_room()
    elif(num==12):
        return action_card.poacher()
    elif(num==13):
        return action_card.militia()
    elif(num==14):
        return action_card.bureaucrat()
    elif(num==15):
        return victory_card.gardens()
    elif(num==16):
        return action_card.market()
    elif(num==17):
        return action_card.stentry()
    elif(num==18):
        return action_card.council_room()
    elif(num==19):
        return action_card.laboratory()
    elif(num==20):
        return action_card.mine()
    elif(num==21):
        return action_card.festival()
    elif(num==22):
        return action_card.archive()
    elif(num==23):
        return action_card.bandit()
    elif(num==24):
        return action_card.witch()
    elif(num==25):
        return action_card.artisan()
    else:
        raise Exception("Invalid number")
    
def make_cardlist_common():
    cardlist = []
    common_max = 7
    for i in range(common_max):
        cardlist.append(make_card_common(i))
    return cardlist

def make_cardlist_for_version(ver_name, common_flg):
    cardlist = []

    if common_flg:
        common_max = 7
        for i in range(common_max):
            cardlist.append(make_card_common(i))

    if(ver_name=="standard"):
        standard_max = 26
        for i in range(standard_max):
            cardlist.append(make_card_standard(i))
    else:
        raise Exception("Invalid name")

    return cardlist

def get_version_max(ver_name):
    if(ver_name=="standard"):
        return 26