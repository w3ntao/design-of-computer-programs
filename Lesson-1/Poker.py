def poker(hands):
    "Return a list of winning hands: poker([hand,...]) => [hand,...]"
    return allmax(hands, key=hand_rank)

def allmax(iterable, key):
    "Return a list of all items equal to the max of the iterable."
    max_rank = hand_rank(max(iterable, key=hand_rank))
    result = []
    for hand in iterable:
    	if max_rank == hand_rank(hand):
    		result.append(hand)
    return result

count_rankings = {(4,1):7, (3,2):6, (3,1,1):3, (2,2,1):2, (2,1,1,1):1, (1,1,1,1,1):0}

def hand_rank(hand):
    "Return a value indicating the ranking of a hand."
    groups = group(["--23456789TJQKA".index(r) for r,s in hand])
    counts, ranks = unzip(groups)

    if ranks == (14, 5, 4, 3, 2):
    	ranks = (5, 4, 3, 2, 1)
    straight = len(ranks) == 5 and max(ranks)-min(ranks) == 4
    flush = len(set([s for r,s in hand])) == 1

    return max(count_rankings[counts], 4*straight + 5*flush), ranks

def group(items):
	groups = [(items.count(x), x) for x in set(items)]
	return sorted(groups, reverse=True)

def unzip(pairs):
	return zip(*pairs)

def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse = True)
    if ranks == [14, 5, 4, 3, 2]:
    	return [5, 4, 3, 2, 1]
    else:
    	return ranks

#print card_ranks(['AC', '3D', '4S', 'KH']) #should output [14, 13, 4, 3]

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    return (max(ranks)-min(ranks)==4) and len(set(ranks))==5

def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r,s in hand]
    return len(set(suits)) == 1

def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    for r in ranks:
    	if ranks.count(r) == n:
    		return r
    return None

def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    pair = kind(2, ranks)
    low_pair  = kind(2, list(reversed(ranks)))
    if pair and pair != low_pair:
    	return (pair, low_pair)
    else:
	    return None

import random

mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC']

def deal(numhands, n=5, deck=mydeck):
	random.shuffle(deck)
	return [deck[n*i:n*(i+1)] for i in range(numhands)]

for hand in deal(10):
	print hand_rank(hand)
