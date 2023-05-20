# DominionAI動作テスト用

import math
import random
import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, ttk
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
VERSION = "standard"
COMMON_CARD_NUM = 7  # 共通サプライ種類数
MAX_STATE = 20
ADJUST = 96
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
TRANSITION = namedtuple('Transition', ('state', 'action', 'next_state', 'reward'))

# 購入カード選択メソッド
def select_action(state, money):
    with torch.no_grad():
        result = policy_net(state)

        # money, supplyで絞り込み
        numlist = dominion.get_numlist_for_money(money)
        tmplist = []
        tmplist.append(result[0, 0])  # Noneは毎回選択肢に入る
        for i in numlist:
            tmplist.append(result[0, i+1])

        # 絞り込み後のリストから最大値を探索
        if tmplist.index(max(tmplist)) == 0:
            return None
        else:
            return dominion.int2allcard(numlist[tmplist.index(max(tmplist))-1])


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

def setup_root(root):
    # ラベルを作成する
    message_label = tk.Label(root, text="サプライを選択してください")
    message_label.place(x=0, y=0)

    #チェックボックスの設置
    list_check = []
    count=[0,0,0,0,0,0,0,0,0]
    for i in range(len(cardlist)):
        bln=tk.BooleanVar()		
        bln.set(False) 
        c = tk.Checkbutton(root, variable = bln, text=cardlist[i].japanese, background='white')
        list_check.append(bln) #チェックボックスの初期値
        cost = cardlist[i].cost
        c.place(x=100*(cost-2), y=50+(30*(count[cost])))
        count[cost]+=1

    def decidion():
        # プルダウンメニューに表示する項目を作成する
        random_supply = []
        for i in range(len(cardlist)):
            bln = list_check[i].get()   #checkbuttonの値
            if bln == True:  #チェック済みの行
                random_supply.append(cardlist[i])

        if len(random_supply) == 10:
            clear()
            supply = random_supply
            for common_card in CF.make_cardlist_common():
                supply.append(common_card)
            
            dominion.setup(random_supply)

            # メインウィンドウを設定
            main_window = tk.Tk()
            main_window.geometry("300x100")
            setup_main(main_window, supply)
            main_window.mainloop
        else:
            random_supply = []
            messagebox.showwarning(title="Warning", message="サプライの数が不正です")

    def clear():
        for widget in root.winfo_children():
            widget.destroy()
        root.destroy()

    button = tk.Button(root, text='決定', command=decidion)
    button.place(x=200, y=350)


def setup_main(main_window, supply):
    def search():
        money = int(money_var.get())
        state = shape_state(dominion.get_state(allcard), MAX_STATE, money, DEVICE)
        action = select_action(state, money)
        if action == None:
            money_label["text"]="Best Practice: None"
        else:
            money_label["text"]="Best Practice: "+action.japanese

    def get():
        cardname = card_var.get()
        for card in supply:
            if card.japanese == cardname:
                allcard.append(card)
        card_label["text"]="Append: "+cardname

    supply_namelist = []
    for card in supply:
        supply_namelist.append(card.japanese)

    # ラベルを作成する
    message_label = tk.Label(main_window, text="財宝")
    message_label.place(x=0, y=0)
    # ラベルを作成する
    message_label2 = tk.Label(main_window, text="カードリスト")
    message_label2.place(x=150, y=0)
    

    # コンボボックスの選択肢のリスト
    moneylist = []
    for i in range(9):
        moneylist.append(i)
    money_var = tk.StringVar()
    money_cb = ttk.Combobox(
        main_window, 
        textvariable=money_var, 
        values=moneylist, 
        width=5,
    )
    money_cb.set(moneylist[0])
    money_cb.bind('<<ComboboxSelected>>')
    money_cb.place(x=0, y=20)

    button = tk.Button(main_window, text='購入カード探索', command=search)
    button.place(x=0, y=40)

    money_label = tk.Label(main_window, text="")
    money_label.place(x=0, y=60)

    # コンボボックスの選択肢のリスト
    card_var = tk.StringVar()
    card_cb = ttk.Combobox(
        main_window, 
        textvariable=card_var, 
        values=supply_namelist, 
        width=10,
    )
    card_cb.set(supply_namelist[0])
    card_cb.bind('<<ComboboxSelected>>')
    card_cb.place(x=150, y=20)

    button2 = tk.Button(main_window, text='獲得', command=get)
    button2.place(x=150, y=40)

    card_label = tk.Label(main_window, text="")
    card_label.place(x=150, y=60)

dominion = d.Dominion(VERSION)
version_card_num = dominion.version_card_num
all_card_num = COMMON_CARD_NUM + version_card_num
policy_net = DQN.DQN(all_card_num, MAX_STATE, ADJUST, all_card_num+1).to(DEVICE)
policy_net.load_state_dict(torch.load('model/param.dat'))

allcard = []
for i in range(7):
    allcard.append(CF.make_card("bronze"))
for i in range(3):
    allcard.append(CF.make_card("house"))

cardlist = CF.make_cardlist_for_version(VERSION, False)

# アプリケーションを作成する
root = tk.Tk()
root.geometry("500x400")
setup_root(root)

# アプリケーションを実行する
root.mainloop()