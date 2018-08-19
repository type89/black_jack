import tkinter as tk
import pandas as pd
import random
import sys
from time import sleep
from tkinter import messagebox

#カードのリスト取得
df = pd.read_csv('/home/soen/source_code/python/BJ/card.csv')
df_i = df.set_index('マーク')

#カードのラベル（本当はcsvから取得すべき）
label_list =['A','2','3','4','5','6','7','8','9','10','J','Q','K']
#ディーラー、プレイヤーの持ち金、レベル、ターン回数、名前を保存する変数を辞書で持つ。
dealer = {"turn":"ディーラー", "hit":1, "point":0}
player = {"turn":"あなた","hit":1, "point":0}


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        master.title("The Black Jack")
        master.geometry("900x480")
        #self.pack()
        self.create_widgets(master)

    def create_widgets(self,master):
        super().__init__(master)
        frame = tk.LabelFrame(master,bd=2,relief="ridge",text="menu")
        frame.pack(fill="x")

        self.Start_button = tk.Button(frame,text="Start Game", command=self.Start_Game)
        #self.Start_button = tk.Button(frame,text="Start Game", command=TurnProcess())
        self.Start_button.pack(anchor="nw",side="left")

        self.Quit_button = tk.Button(frame,text="Leave Game", command=master.destroy)
        self.Quit_button.pack(anchor="ne")

        self.text_area = tk.Text(master,font=16)
        self.text_area.pack(fill="x")

        return

    def Start_Game(self):
        #txt ='MMMMMMM22222222222M'
        #self.text_area.insert('end', txt + '\n')
        self.text_area.insert('end', 'ゲームを始めます' + '\n')
        dealer["hit"], dealer["point"] = self.choice_card(dealer["turn"], dealer["hit"], dealer["point"])
        player["hit"], player["point"] = self.choice_card(player["turn"], player["hit"], player["point"])
        dealer["hit"], dealer["point"] = self.choice_card(dealer["turn"], dealer["hit"], dealer["point"])

        i = 0
        while(i == 0):
            player["hit"], player["point"] = self.choice_card(player["turn"], player["hit"], player["point"])
            #self.text_area.insert('end','もう一枚引きますか？続けるには y を入力してください。\n')
            result = messagebox.askokcancel("ディーラーより","もう一枚引きますか？")
            if result is False:
                self.text_area.insert('end', 'カードは引きません' + '\n')
                i = 1
        i = 0
        while(i == 0):
            i = self.decide_dealer(dealer["turn"], dealer["hit"], dealer["point"])

        self.V_Check(player["point"],dealer["point"])

        return

    def choice_card(self, turn, hit, point):
        #print(turn + 'の番です')
        self.text_area.insert('end', turn + 'の番です\n')

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
            #print(turn + 'は' + 'カードを引きました')
            self.text_area.insert('end', turn + 'は' + 'カードを引きました\n')
        else:
            #print(turn + 'は' + suit + 'の' + str(suit_df[rank].name) + 'を引きました')
            self.text_area.insert('end', turn + 'は' + suit + 'の' + str(suit_df[rank].name) + 'を引きました\n')

        hit += 1
        point += int(suit_df[rank])
        df_i.at[suit,rank] = None

        return hit, point

    def decide_dealer(self,turn,hit,point):
        if(point < 17):
            dealer["hit"], dealer["point"] = self.choice_card(dealer["turn"], dealer["hit"], dealer["point"])
            #print("dealer_hit ==>" + str(dealer["hit"]) + " dealer_point ==>" + str(dealer["point"]))
            return 0
        else:
            pass
            return 1

    def V_Check(self,player_point,dealer_point):
        self.text_area.insert('end', "player_point ==>" + str(player["point"]) + " dealer_point ==>" + str(dealer["point"]) +'\n')
        if(player_point > 21 and dealer_point > 21):
            self.text_area.insert('end', '引き分けです' + '\n')
        if(player_point > 21 and dealer_point <= 21):
            self.text_area.insert('end', 'あなたの負けです' + '\n')
        if(player_point <= 21 and dealer_point > 21):
            self.text_area.insert('end', 'あなたの勝ちです' + '\n')
        if(player_point <= 21 and dealer_point <= 21 and player_point > dealer_point):
            self.text_area.insert('end', 'あなたの勝ちです' + '\n')
        if(player_point <= 21 and dealer_point <= 21 and player_point == dealer_point):
            self.text_area.insert('end', '引き分けです' + '\n')
        if(player_point <= 21 and dealer_point <= 21 and player_point < dealer_point):
            self.text_area.insert('end', 'あなたの負けです' + '\n')
        return


def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
