# CS 212, hw1-2: Jokers Wild
#
# -----------------
# User Instructions
#
# Write a function best_wild_hand(hand) that takes as
# input a 7-card hand and returns the best 5 card hand.
# In this problem, it is possible for a hand to include
# jokers. Jokers will be treated as 'wild cards' which
# can take any rank or suit of the same color. The
# black joker, '?B', can be used as any spade or club
# and the red joker, '?R', can be used as any heart
# or diamond.
#
# The itertools library may be helpful. Feel free to
# define multiple functions if it helps you solve the
# problem.
#
# -----------------
# Grading Notes
#
# Muliple correct answers will be accepted in cases
# where the best hand is ambiguous (for example, if
# you have 4 kings and 3 queens, there are three best
# hands: 4 kings along with any of the three queens).

import itertools

all_ranks = "23456789TJQKA"
red_cards   = [rank+suit for rank in all_ranks for suit in "DH"]
black_cards = [rank+suit for rank in all_ranks for suit in "SC"]

def get_best_5_from_7(hands):
	best_hands = [best_hand(hand) for hand in hands]
	return best_hands


# official one
def best_wild_hand(hand):
	"Try all values for jokers in all 5-card selections."
	hands = set(best_hand(h) for h in itertools.product(*map(replacements, hand)))
	return max(hands, key=hand_rank)

'''
# my approach
def best_wild_hand(hand):
	"Try all values for jokers in all 5-card selections."
	return max(get_best_5_from_7(replace_joker(hand)), key=hand_rank)
'''
def replacements(card):
	if   card == "?B": return black_cards
	elif card == "?R": return red_cards
	else:
		return [card]


def replace_joker(hand):
	joker     = [card for card in hand if card in ["?B", "?R"]]
	non_joker = [card for card in hand if card not in joker]

	number     = "2 3 4 5 6 7 8 9 T J Q K A".split()
	red_suit   = "D H".split()
	black_suit = "C S".split()

	red_card   = [num+suit for num,suit in list(itertools.product(number, red_suit))]
	black_card = [num+suit for num,suit in list(itertools.product(number, black_suit))]

	replaced_card = [non_joker]

	for i in range(joker.count("?R")):
		replaced_card = [(lambda x: x[0]+[x[1]])(item) for item in list(itertools.product(replaced_card, red_card))]

	for i in range(joker.count("?B")):
		replaced_card = [(lambda x: x[0]+[x[1]])(item) for item in list(itertools.product(replaced_card, black_card))]

	return replaced_card

def test_best_wild_hand():
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    return 'test_best_wild_hand passes'

# ------------------
# Provided Functions
#
# You may want to use some of the functions which
# you have already defined in the unit to write
# your best_hand function.

def best_hand(hand):
    "From a 7-card hand, return the best 5 card hand."
    return max(itertools.combinations(hand, 5), key=hand_rank)

def hand_rank(hand):
    "Return a value indicating the ranking of a hand."
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)

def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse = True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks

def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r,s in hand]
    return len(set(suits)) == 1

def straight(ranks):
    """Return True if the ordered
    ranks form a 5-card straight."""
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5

def kind(n, ranks):
    """Return the first rank that this hand has
    exactly n-of-a-kind of. Return None if there
    is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n: return r
    return None

def two_pair(ranks):
    """If there are two pair here, return the two
    ranks of the two pairs, else None."""
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))
    if pair and lowpair != pair:
        return (pair, lowpair)
    else:
        return None

hand_0 = "6C 7C 8C 9C TC 5C ?B".split()
hand_1 = "TD TC 5H 5C 7C ?R ?B".split()
hand_2 = "JD TC TH 7C 7D 7S 7H".split()

#print(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))

#print(sorted(best_wild_hand(hand_1)))

#print(best_wild_hand(hand_2))


print(test_best_wild_hand())