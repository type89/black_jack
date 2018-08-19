# -*- coding: utf8 -*-
import pandas as pd
import random
import sys
import tkinter
from tkinter import font
#from pandas import Series, DataFrame
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed, may indicate binary incompatibility.")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

#カードのリスト取得
df = pd.read_csv('/home/soen/source_code/python/BJ/card.csv')
df_i = df.set_index('マーク')

#カードのラベル（本当はcsvから取得すべき）
label_list =['A','2','3','4','5','6','7','8','9','10','J','Q','K']
#label_list = df[1]
#print("label_list ==> " + str(label_list))
#ディーラー、プレイヤーの持ち金、レベル、ターン回数、名前を保存する変数を辞書で持つ。
dealer = {"turn":"ディーラー", "hit":1, "point":0}
player = {"turn":"あなた","hit":1, "point":0}


class TurnProcess:
    """docstring for T."""
    def __init__(self):
        print('ゲームを始めます')
        dealer["hit"], dealer["point"] = TurnProcess.choice_card(dealer["turn"], dealer["hit"], dealer["point"])
        player["hit"], player["point"] = TurnProcess.choice_card(player["turn"], player["hit"], player["point"])
        dealer["hit"], dealer["point"] = TurnProcess.choice_card(dealer["turn"], dealer["hit"], dealer["point"])
        return

    def choice_card(turn,hit,point):
        print(turn + 'の番です')

        i = 0
        while(i == 0):
            #ランダムにスイート（行）を選択
            suit_df = df_i.sample(n=1)
            #不要な文字列を削除してスイートのみにする。改善の余地あり
            suit = str(suit_df.index)
            suit = suit.replace("Index(['", "")
            suit = suit.replace("'], dtype='object', name='マーク')", "")
            #print('suit ==> ' + suit)

            #数字のリストの中から、ランダムに数字（列）を選択
            rank = random.choice(label_list)
            #print('rank ==> ' + str(rank))

            #カードがNULLでないかの判定
            if (str(df_i.loc[suit,rank]) != 'nan'):
                i = 1

        if(hit > 1 and turn == 'ディーラー'):
            print(turn + 'は' + 'カードを引きました')
        else:
            print(turn + 'は' + suit + 'の' + str(suit_df[rank].name) + 'を引きました')

        hit += 1
        point += int(suit_df[rank])
        df_i.at[suit,rank] = None

        return hit, point

    def decide_player():
        print('もう一枚引きますか？続けるには y を入力してください。')
        key = input()
        #print(key)
        if(key == 'y'):
            pass
            return 0
        else:
            print("カードは引きません")
            return 1

    def decide_dealer(turn,hit,point):
        if(point < 17):
            dealer["hit"], dealer["point"] = TurnProcess.choice_card(dealer["turn"], dealer["hit"], dealer["point"])
            #print("dealer_hit ==>" + str(dealer["hit"]) + " dealer_point ==>" + str(dealer["point"]))
            return 0
        else:
            pass
            return 1

def V_Check(player_point,dealer_point):
    print("player_point ==>" + str(player["point"]) + " dealer_point ==>" + str(dealer["point"]))
    if(player_point > 21 and dealer_point > 21):
        print('引き分けです')
    if(player_point > 21 and dealer_point <= 21):
        print('あなたの負けです')
    if(player_point <= 21 and dealer_point > 21):
        print('あなたの勝ちです')
    if(player_point <= 21 and dealer_point <= 21 and player_point > dealer_point):
        print('あなたの勝ちです')
    if(player_point <= 21 and dealer_point <= 21 and player_point == dealer_point):
        print('引き分けです')
    if(player_point <= 21 and dealer_point <= 21 and player_point < dealer_point):
        print('あなたの負けです')
        return

def main():
    TurnProcess()
    #print("player_hit ==>" + str(player["hit"]) + "player_point ==>" + str(player["point"]))
    i = 0
    while(i == 0):
        player["hit"], player["point"] = TurnProcess.choice_card(player["turn"], player["hit"], player["point"])
        i = TurnProcess.decide_player()

    i = 0
    while(i == 0):
        i = TurnProcess.decide_dealer(dealer["turn"], dealer["hit"], dealer["point"])
        
    V_Check(player["point"],dealer["point"])

if __name__ == '__main__':
    main()
