import random
import itertools
import collections
import numpy as np

# suits = ["s", "h", "d", "c"]
# values = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
# deck = [value + suit for suit in  suits for value in values]
    
def check_quads(num_counts, numbers_to_values):

    score = 7
    score += numbers_to_values[num_counts.most_common()[0][0]]        
    score += numbers_to_values[num_counts.most_common()[1][0]]/100

    return score

def check_full_house(num_counts, numbers_to_values):

    score = 6
    score += numbers_to_values[num_counts.most_common()[0][0]]
    score += numbers_to_values[num_counts.most_common()[1][0]]/100

    return score

def check_three_kind(num_counts, numbers_to_values):

    score = 3
    score += numbers_to_values[num_counts.most_common()[0][0]]

    singles = sorted([num_counts.most_common()[1][0],num_counts.most_common()[2][0]], reverse=True)

    score += numbers_to_values[singles[0]]/100
    score += numbers_to_values[singles[1]]/100/100   
    
    return score

def check_two_pair(num_counts, numbers_to_values):
    
    score = 2

    doubles = sorted([num_counts.most_common()[0][0],num_counts.most_common()[1][0]], reverse=True)

    score += numbers_to_values[doubles[0]]
    score += numbers_to_values[doubles[1]]/100

    score += numbers_to_values[num_counts.most_common()[2][0]]/100/100
    
    return score

def check_one_pair(num_counts, numbers_to_values):
    
    score = 1
    score += numbers_to_values[num_counts.most_common()[0][0]]

    singles = sorted([num_counts.most_common()[1][0],num_counts.most_common()[2][0],num_counts.most_common()[3][0]], reverse=True)

    score += numbers_to_values[singles[0]]/100
    score += numbers_to_values[singles[1]]/100/100
    score += numbers_to_values[singles[2]]/100/100/100
    
    return score

def check_high_card(magnitude_num, numbers_to_values):

    score = 0

    singles = sorted(magnitude_num, reverse=True)
    
    score += numbers_to_values[singles[0]]
    score += numbers_to_values[singles[1]]/100
    score += numbers_to_values[singles[2]]/100/100
    score += numbers_to_values[singles[3]]/100/100/100
    score += numbers_to_values[singles[4]]/100/100/100/100 
    
    return score

def check_straight(magnitude_num, numbers_to_values):
    
    score = 0
    
    if (len(np.unique(magnitude_num))==5) & (max(magnitude_num)-min(magnitude_num) == 4):
        
        score = 4
        
        score += numbers_to_values[max(magnitude_num)]
        
    elif (len(np.unique(magnitude_num))==5) & (sorted(magnitude_num, reverse=True)==[14, 5, 4, 3, 2]):
        
        score = 4
        
        score += numbers_to_values[5]
        
    return score
    
def check_flush(suits, magnitude_num, numbers_to_values):
    
    if len(np.unique(suits)) == 1:
        
        score = 5
        
        singles = sorted(magnitude_num, reverse=True)
        
        score += numbers_to_values[singles[0]]
        score += numbers_to_values[singles[1]]/100
        score += numbers_to_values[singles[2]]/100/100
        score += numbers_to_values[singles[3]]/100/100/100
        score += numbers_to_values[singles[4]]/100/100/100/100 
        
    else:
        
        score = 0
        
    return score

def calc_five_card_strength(five_cards):
    
    #straight flush: 8
    #four of a kind: 7
    #full house: 6
    #flush: 5
    #straight: 4
    #trips: 3
    #two pair: 2
    #pair: 1
    #high card: 0
    
    #ones digit is hand type
    #tens-hundreds digits are most important card(s)
    #next two digits are second most imporatant card(s), and so one
    
    score = 0
    
    cards_to_numbers = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "T":10, "J":11, "Q":12, "K":13, "A":14}
    cards_to_values = {"2":.05, "3":.1, "4":.15, "5":.2, "6":.25, "7":.3, "8":.35, "9":.4, "T":.45, "J":.5, "Q":.55, "K":.6, "A":.65}
    numbers_to_values = dict(zip(cards_to_numbers.values(),cards_to_values.values()))
    
    magnitude = [five_cards[i][0] for i in range(len(five_cards))]
    magnitude_num = [cards_to_numbers[magnitude[i]] for i in range(len(magnitude))]
    
    suits = [five_cards[i][1] for i in range(len(five_cards))]
    
    num_counts = collections.Counter(magnitude_num)
    
    #check for quads
    if num_counts.most_common()[0][1] == 4:
        
        score = check_quads(num_counts, numbers_to_values)
    
    #check for full house
    elif (num_counts.most_common()[0][1] == 3) & (num_counts.most_common()[1][1] == 2):
        
        score = check_full_house(num_counts, numbers_to_values)
    
    #check for three of a kind
    elif (num_counts.most_common()[0][1] == 3):
        
        score = check_three_kind(num_counts, numbers_to_values)
    
    #check for two pair
    elif (num_counts.most_common()[0][1] == 2) & (num_counts.most_common()[1][1] == 2):
        
        score = check_two_pair(num_counts, numbers_to_values)
    
    #check for pair
    elif (num_counts.most_common()[0][1] == 2):
        
        score = check_one_pair(num_counts, numbers_to_values)
    
    #check for high card
    else:
        
        score = check_high_card(magnitude_num, numbers_to_values)
    
    straight = check_straight(magnitude_num, numbers_to_values)
    flush = check_flush(suits, magnitude_num, numbers_to_values)
    
    if (flush > 0) & (straight > 0):
        
        score = straight + 4
        
    else:
        
        score = max(score, flush, straight)
    
    return score

def calc_seven_card_strength(hand, board):
    
    all_scores = []
    
    for five_cards in list(itertools.combinations([*hand, *board],5)):
        
        all_scores.append(calc_five_card_strength(list(five_cards)))
        
    return max(all_scores)

class board_state:
    def __init__(self, phase, hand1, hand2, board, mod_deck):
        self.phase = phase
        self.hand1 = hand1
        self.hand2 = hand2
        self.board = board
        self.mod_deck = mod_deck
    
    def show_state(self):
        print('Player 1 hand: ' + str(self.hand1))
        print('Player 2 hand: ' + str(self.hand2))
        print('Board: ' + str(self.board))
    
    def flop(self):
        if self.phase != 0:
            print('error: phase not preflop, cannot execute flop.')
            #error
        elif self.phase == 0:
            self.phase = 1
            self.board = random.sample(self.mod_deck, 3)
            
            self.mod_deck = [self.mod_deck[i] for i in range(len(self.mod_deck)) if self.mod_deck[i] not in self.board]
            
    def turn(self):
        if self.phase != 1:
            print('error: phase not flop, cannot execute turn.')
            #error
        elif self.phase == 1:
            self.phase = 2
            turn = random.sample(self.mod_deck, 1)[0]
            self.board.append(turn)
            
            self.mod_deck.remove(turn)
            
    def river(self):
        if self.phase != 2:
            print('error: phase not turn, cannot execute river.')
            #error
        elif self.phase == 2:
            self.phase = 3
            river = random.sample(self.mod_deck, 1)[0]
            self.board.append(river)
            
            self.mod_deck.remove(river)
            
    def calculate_winner(self):
        
        if self.phase != 3:
            
            print('error: phase not river, cannot calculate winner.')
            
        elif self.phase == 3:
        
            hand1_strength = calc_seven_card_strength(self.board,self.hand1)
            hand2_strength = calc_seven_card_strength(self.board,self.hand2)
            
            if hand1_strength > hand2_strength:

                return 1

            elif hand2_strength > hand1_strength:

                return 2

            else:

                return 0
            
    def all_phases_calculate(self):
        
        self.flop()
        self.turn()
        self.river()
        
        return self.calculate_winner()
    
def start_game():
    
    hands = random.sample(deck, 4)
    
    hand1 = hands[0:2]
    hand2 = hands[2:4]
    
    mod_deck = [deck[i] for i in range(52) if deck[i] not in hands]
    
    X = board_state(0,hand1,hand2,[],mod_deck)
    
    return X

def start_game_with_hands(hand1, hand2):
    
    mod_deck = [deck[i] for i in range(52) if deck[i] not in [*hand1, *hand2]]
    
    X = board_state(0,hand1,hand2,[],mod_deck)
    
    return X

def simulate_hand_fight(hand1, hand2, iterations=1000, equity=True):
    
    results = [0,0,0]
    
    for trial in range(iterations):
        
        game_trial = start_game_with_hands(hand1, hand2)
        
        results[game_trial.all_phases_calculate()] += 1
        
    if equity==True:
        
        results = [results[1]+results[0]/2, results[2]+results[0]/2]
        
    return results
        
    