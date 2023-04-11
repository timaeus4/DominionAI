# DominionAI動作テスト用

import math
import random
import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
if 'inline' in matplotlib.get_backend():
    from IPython import display
from collections import namedtuple, deque
from itertools import count
from PIL import Image

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T

from Dominion import dominion as d
from Dominion import player as p
from Dominion import strategy
from Dominion.card import card_factory as CF
from DQN import DQN
from DQN import DQN_Memory as DQN_M
from Utils import myFunction as myF


MAX_PRICE = 8
SUPPLY_NUM = 16
MAX_STATE = 20
ADJUST = 192
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
TRANSITION = namedtuple('Transition', ('state', 'action', 'next_state', 'reward'))


def select_action(state, money):
    if(money > MAX_PRICE):
        money = MAX_PRICE

    with torch.no_grad():
        t = policy_net(state)[0, 0:dominion.count_supply(money)].unsqueeze(0).max(1)[1].view(1, 1)
        return dominion.int2card(t[0,0].item())


# dominionから得たstateをDQN入力用に整形
def shape_state(state, size, money, device):
    a = myF.expand_line2plane(state, size)
    b = np.zeros((len(a), size))
    for i in range(dominion.count_supply(money)-1):
        for j in range(size):
            b[i][j] = 1
    c = np.zeros(((2, len(a), size)))
    c[0,:,:] = a
    c[1,:,:] = b
    return myF.convert_to_tensor(c, device)
        
        
allcard = []
for i in range(7):
    allcard.append(CF.make_card("bronze"))
for i in range(3):
    allcard.append(CF.make_card("house"))


dominion = d.Dominion()
random_supply = dominion.generate_random_supply()
# c = 0 
# while c < 10:
#     random_cardname = input("supply?: ")
#     try:
#         random_card = card_factory.make_card(random_cardname)
#         random_supply.append(random_card)
#         c += 1
#     except Exception:
#         print("Invalid cardname")
#         continue
dominion.setup(random_supply)
s = dominion.get_state(allcard)


policy_net = DQN.DQN(SUPPLY_NUM, MAX_STATE, ADJUST, SUPPLY_NUM+1).to(DEVICE)
policy_net.load_state_dict(torch.load('model/param.dat'))
    
while True:
    money = input("money?: ")
    if(money=="q"):
        break
    else:
        try:
            money = int(money)
            if money < 0:
                raise Exception("Invalid number")
        except Exception:
            print("Invalid number")
            continue
    
    state = shape_state(dominion.get_state(allcard), MAX_STATE, money, DEVICE)
    action = select_action(state, money)
    if action == None:
        print("Best Practice: None")
    else:
        print("Best Practice: "+action.name)
    
    while True:
        cardname = input("cardname?: ")
        if(cardname=="q"):
            break
        elif(cardname==""):
            card = action
            break
        else:
            try:
                card = CF.make_card(cardname)
                break
            except Exception:
                print("Invalid cardname")
            continue
    if card != None:
        allcard.append(card)