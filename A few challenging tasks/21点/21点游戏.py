import numpy as np
class Blackjack:
    my_list = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
    def __init__(self):
        self.player_cards = []
        self.computer_cards = []

    def fa_pai(self):
        return np.random.choice(self.my_list)
    def pai_dian(self,x):
        if x in ["J","Q","K"]:
            return 10
        elif x == "A":
            return 11
        else:
            return int(x)
    def pai_total(self,X):
        total = 0
        pin_count = X.count("A")
        for x in X:
            total += self.pai_dian(x)

        while total > 21 and pin_count >0 :
            total -= 10
            pin_count -= 1
        return total

    def pai_begin(self):
        for i in range(2):
            self.player_cards.append(self.fa_pai())
        for _ in range(2):
            self.computer_cards.append(self.fa_pai())

    def win_or_lost(self):
        player_total = self.pai_total(self.player_cards)
        computer_total = self.pai_total(self.computer_cards)
        if player_total == 21:
            return "你赢了"
        elif computer_total == 21:
            return "电脑赢了"


    def busted(self,X):
        return self.pai_total(X) > 21

    def player_round(self,choice):
        if choice == "Hit":
            self.player_cards.append(self.fa_pai())
            if self.busted(self.player_cards):
                return f"你的牌爆了，你的点数为{self.pai_total(self.player_cards)}"
            else:
                return f"你选择继续抽牌，你的手牌为{self.player_cards},总点数为{self.pai_total(self.player_cards)}"
        elif choice == "stand":
            return f"你选择了停止抽牌，总点数为{self.pai_total(self.player_cards)}"
        else:
            return "无效选择，请输入 Hit 或 stand"

    def computer_round(self):
        computer_total = self.pai_total(self.computer_cards)
        while computer_total < 17:
            self.computer_cards.append(self.fa_pai())
            computer_total = self.pai_total(self.computer_cards)
        if self.busted(self.computer_cards):
            return f"电脑爆牌了,总点数为{self.pai_total(self.computer_cards)},你赢了"
        else:
            return f"电脑最终点数为{self.pai_total(self.computer_cards)}"

    def last_score(self):
        player_total = self.pai_total(self.player_cards)
        computer_total = self.pai_total(self.computer_cards)
        if player_total > computer_total:
            return "你赢了"
        elif player_total < computer_total:
            return "电脑赢了"
        else:
            return "平局"



if __name__ == "__main__":
        game = Blackjack()
        game.pai_begin()
        blackjack_result = game.win_or_lost()
        if blackjack_result:
            print(blackjack_result)
        else:
            print(f"你的初始手牌：{game.player_cards}，总点数：{game.pai_total(game.player_cards)}")
            player_choice = input("请选择 Hit（要牌）或 Stand（停牌）：")
            player_result = game.player_round(player_choice)
            print(player_result)

            current_player_total = game.pai_total(game.player_cards)
            if current_player_total < 21:
                computer_result = game.computer_round()
                print(computer_result)


                current_computer_total = game.pai_total(game.computer_cards)
                if current_computer_total <= 21:
                    final_result = game.last_score()
                    print(final_result)












