import numpy as np
import itertools

suits = ["s", "h", "d", "c"]
values = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
deck = [value + suit for suit in  suits for value in values]
num_hands = int(52*51/2)
poss_hands = [list(list(itertools.combinations(deck,2))[i]) for i in range(num_hands)]
hand_nums = np.array(range(num_hands))
num_to_hand = dict(zip(hand_nums, poss_hands))
hand_to_num = {tuple(poss_hand): num for poss_hand, num in zip(poss_hands, hand_nums)}

keys = list(hand_to_num.keys()).copy()

for (card1, card2) in keys:
    hand_to_num[(card2, card1)] = hand_to_num[(card1, card2)]