# DominionAI学習用クラス

import os
import random
import datetime
import numpy as np
import torch
import torch.optim as optim
import torch.nn.functional as F
from collections import namedtuple

from Dominion import dominion_forTrain as d
from Dominion import player as p
from Dominion import strategy
from DQN import DQN
from DQN import DQN_Memory as DQN_M
from Utils import myFunction as myF


# 固定パラメータ
MEMORY_SIZE = 50000  # 記録用メモリサイズ
MAX_PRICE = 8  # プール内最大価格
VERSION = "standard"  # サプライのバージョン
COMMON_CARD_NUM = 7  # 共通サプライ種類数
MAX_STATE = 20  # 同一カード保持上限枚数
ADJUST = 96  # SUPPLY_NUM, MAX_STATEに依存
MAX_TURN = 30  # ターン上限
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
TRANSITION = namedtuple('Transition', ('state', 'action', 'next_state', 'reward'))


# ハイパーパラメータ
NUM_EPISODES = 5000  # 学習回数
BATCH_SIZE = 80  # バッチサイズ
GAMMA = 0.99  # 割引率
EPS_START = 0.8  # e-greedy法
EPS_END = 0.1  # e-greedy法
EPS_DECAY = 10000  # e-greedy法
TARGET_UPDATE = 10  # 学習結果反映タイミング 
TARGET_SAVE = 100  # 学習結果記録タイミング


# ログ用設定
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9), 'JST'))
ymd = format(now,"%m%d")
hm = format(now,"%H%M")
dirname = ymd+"/"+hm+"pre"
log1 = dirname+'/buy.log'
log2 = dirname+'/train.log'
log3 = dirname+'/param.csv'
os.makedirs(dirname)


# Dominion準備
dominion = d.Dominion_forTrain(VERSION)
all_list = dominion.all_cardlist
version_card_num = dominion.version_card_num
all_card_num = COMMON_CARD_NUM + version_card_num
random_supply = dominion.generate_random_supply(VERSION, version_card_num)
dominion.setup(random_supply)

# DQN準備
memory = DQN_M.DQN_Memory(MEMORY_SIZE, TRANSITION)
policy_net = DQN.DQN(all_card_num, MAX_STATE, ADJUST, all_card_num+1).to(DEVICE)
target_net = DQN.DQN(all_card_num, MAX_STATE, ADJUST, all_card_num+1).to(DEVICE)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()
optimizer = optim.RMSprop(policy_net.parameters())
steps_done = 0


# 購入カード選択メソッド
def select_action(state, money):
    # e-greedy法を満たした場合、DQNに従う
    if myF.eps_greedy(EPS_START, EPS_END, EPS_DECAY, steps_done):
        save_log(log1, '<AI'+str(money)+'>')
        with torch.no_grad():
            result = policy_net(state)


            # money, supplyで絞り込み
            numlist = dominion.get_numlist_for_just_money(money)
            tmplist = []
            if money <= 2:
                tmplist.append(float(result[0, 0]))  # 2金以下の場合Noneを選択肢に入れる
            for i in numlist:
                tmplist.append(float(result[0, i+1]))

            # 絞り込み後のリストから最大値を探索
            if money <= 2 & tmplist.index(max(tmplist)) == 0:
                return None
            else:
                return dominion.int2allcard(numlist[tmplist.index(max(tmplist))-1])
    # e-greedy法を満たさなかった場合、コインプレイに従う
    else:
        return strategy.coin_method(money)

        
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
        

# ネットワーク最適化処理
def optimize_model():
    if (len(memory) < BATCH_SIZE):
        return
    
    transitions = memory.pop_memory(BATCH_SIZE)
    batch = TRANSITION(*zip(*transitions))

    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                      batch.next_state)), device=DEVICE, dtype=torch.bool)
    non_final_next_states = torch.cat([s for s in batch.next_state
                                            if s is not None])
    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)
    
    state_action_values = policy_net(state_batch).gather(1, action_batch)

    next_state_values = torch.zeros(BATCH_SIZE, device=DEVICE)

    result = target_net(non_final_next_states)
    numlist = dominion.get_numlist_for_just_money(money)
    tmplist = []
    tmplist.append(result[0, 0])
    for i in numlist:
        tmplist.append(result[0, i+1])
    next_state_values[non_final_mask] = max(tmplist).detach()

    expected_state_action_values = (next_state_values * GAMMA) + reward_batch
    
    loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1))

    optimizer.zero_grad()
    loss.backward()
    for param in policy_net.parameters():
        param.grad.data.clamp_(-1, 1)
    optimizer.step()
    

# ログ出力        
def save_log(fileName, word):
    with open(fileName, 'a', encoding='utf-8') as f:
        f.write(word)

# 記録用
save_log(log3, 'None, ')
for log3_card in all_list:
    save_log(log3, log3_card.japanese + ', ')
save_log(log3, '\n')
# 勝率計算用
total_reward = 0
for i_episode in range(1, NUM_EPISODES+1):

    dominion.setup(dominion.generate_random_supply(VERSION, version_card_num))
    players = []
    
    # 順番決め
    x = random.randint(0,3)
    for i in range(4):
        if i==x:
            target = p.Player()
            target.setup(i)
            players.append(target)
        else:
            player = p.Player()
            player.setup(i)
            players.append(player)
            
    done = False
    print(i_episode)
    
    for t in range(MAX_TURN):
        for n in range(4):
            # ターゲットプレイヤーのターン
            if n == x:
                # 確認用
                # 初期状態のパラメータをログに出力する
                if (i_episode % TARGET_SAVE == 0) and (t == 0):
                    for rep_money in range(9):
                        rep_state = shape_state(dominion.get_state(target.get_allcard()), MAX_STATE, rep_money, DEVICE)
                        rep_result = policy_net(rep_state)
                        for rep_num in range(all_card_num+1):
                            save_log(log3, format(float(rep_result[0, rep_num]), '.1f') + ', ')
                        save_log(log3, '\n')
                    save_log(log3, '\n')

                # アクションフェイズ
                target, players = dominion.execute_action(target, players)
        
                # 購入直前の状態を取得
                money = target.count_money()
                limit_money = min(money, MAX_PRICE)
                state = shape_state(dominion.get_state(target.get_allcard()), MAX_STATE, limit_money, DEVICE)
                steps_done += 1
                
                # 購入カードの選択
                action = select_action(state, limit_money)
                if action==None:
                    save_log(log1, 'なし, ')
                else:
                    save_log(log1, action.japanese + ', ')
                
                # 購入フェイズ
                target = dominion.execute_buy(target, action)
                
                # クリーンアップ
                target = dominion.execute_cleanup(target)
                
                # 購入直後の状態を取得
                next_state = shape_state(dominion.get_state(target.get_allcard()), MAX_STATE, limit_money, DEVICE)
                
                # ゲーム終了判定
                if dominion.check_gameset():
                    done = True
                    next_state = None
                    if dominion.is_win(target, players):
                        reward = 1
                    else:
                        reward = -1
                else: 
                    done = False
                    reward = 0
                    
            else:
                other = players[n]
            
                # アクションフェイズ
                other, players = dominion.execute_action(other, players)
                # 購入フェイズ
                other = dominion.execute_buy(other, strategy.coin_method(other.count_money()))
                # クリーンアップ
                other = dominion.execute_cleanup(other)
                
                # ゲーム終了判定
                if dominion.check_gameset():
                    done = True
                    next_state = None
                    if dominion.is_win(target, players):
                        reward = 1
                    else:
                        reward = -1
                else: 
                    done = False
                    reward = 0

        # ターンごとに結果をメモリに記録
        action = dominion.allcard2int(action)
        action = myF.int2tensor([action], DEVICE)
        reward = myF.int2tensor(reward, DEVICE)
        memory.push_memory(state, action, next_state, reward)
        
        optimize_model()
        
        # ゲーム終了時
        if done:
            
            total_reward += reward[0].item()
            save_log(log1, str(reward[0].item()) + '\n')
            break
        
    if i_episode % TARGET_UPDATE == 0:
        target_net.load_state_dict(policy_net.state_dict())
            
    if i_episode % TARGET_SAVE == 0:
        epidir = dirname+'/'+str(i_episode)
        os.makedirs(epidir)
        model_name = epidir+'/param.dat'
        torch.save(policy_net.state_dict(), model_name)
            
        win = (TARGET_SAVE + total_reward) / 2
        winrate = win/TARGET_SAVE
        save_log(log2, str(winrate) + '\n')
        total_reward = 0

print('Complete')