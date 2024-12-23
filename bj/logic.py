import random

class Card:
    suits = ['heart','club','dia','spade']
    def __init__(self):
        self.cards = []
        for suit in self.suits:
            self.cards.append([f'{suit} {number}' for number in range(1,14)])

    def draw(self):
        suit_index = random.randrange(len(self.cards))
        num_index = random.randrange(len(self.cards[suit_index]))
        draw_card = self.cards[suit_index][num_index]
        self.cards[suit_index].remove(self.cards[suit_index][num_index])
        return draw_card

    @staticmethod
    def card_img(card):
        suit, number = card.split()
        return f'bj/img/{suit}-{number}.png'

class Game(Card):
    def __init__(self):
        super().__init__()
        self.player_hand = []
        self.dealer_hand = []
        self.bet = 0
        self.room = 1
        self.player_sum = 0
        self.dealer_sum = 0
        self.isChip = 1

    def to_dict(self):
        return {
            'bet' : self.bet,
            'room' : self.room,
            'player_hand' : self.player_hand,
            'dealer_hand' : self.dealer_hand,
            'cards' : self.cards,
        }

    @classmethod
    def from_dict(cls, data):
        if data is None:  # Noneの場合でもエラーを回避
            return cls()  # 新しいGameオブジェクトを生成
        game = cls()
        game.bet = data.get('bet', 0)
        game.room = data.get('room', 1)
        game.player_hand = data.get('player_hand', [])
        game.dealer_hand = data.get('dealer_hand', [])
        game.cards = data.get('cards', [])
        return game


    def hand_sum(self,hand_list):
        total = 0
        count_ace = 0
        for card in hand_list:
            split_card = card.split()
            num = int(split_card[1])
            if num == 1:
                count_ace += 1
                total += 11
            elif num > 10:
                total += 10
            else:
                total += num

        while count_ace > 0 and total > 21:
            total -= 10
            count_ace -= 1

        return total

    def bust_check(self,number):
        if number > 21:
            return True
        else:
            return False

    
    #勝った場合の得るチップの倍率
    def return_rate(self):
        if len(self.player_hand) == 2 and self.hand_sum(self.player_hand) == 21: #playerオブジェクトに「hand_sum」っていうインスタンス変数がある前提
            return 2.5
        else:
            return 2

    # playerとdealerのそれぞれのHand合計値
    #isBet変数は、ベットした結果得たチップ、失ったチップを持つためのもの
    def judge(self, room):
        if self.bust_check(self.player_sum):
            self.isBet = -self.bet
            result = 'lose'
        elif self.bust_check(self.dealer_sum):
            self.isChip = self.bet * self.return_rate()
            self.isBet = self.isChip - self.bet
            room.chip += self.isChip
            result = 'win'
        elif self.player_sum < self.dealer_sum:
            self.isBet = -self.bet
            result = 'lose'
        elif self.player_sum > self.dealer_sum:
            self.isChip = self.bet * self.return_rate()
            self.isBet = self.isChip - self.bet
            room.chip += self.isChip
            result = 'win'
        else:
            self.isBet = 0
            room.chip += self.bet
            result = 'draw'
            
        room.save()

        return result