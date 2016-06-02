# -----------------
# User Instructions
#
# In this problem, we introduce doubling to the game of pig.
# At any point in the game, a player (let's say player A) can
# offer to 'double' the game. Player B then has to decide to
# 'accept', in which case the game is played through as normal,
# but it is now worth two points, or 'decline,' in which case
# player B immediately loses and player A wins one point.
#
# Your job is to write two functions. The first, pig_actions_d,
# takes a state (p, me, you, pending, double), as input and
# returns all of the legal actions.
#
# The second, strategy_d, is a strategy function which takes a
# state as input and returns one of the possible actions. This
# strategy needs to beat hold_20_d in order for you to be
# marked correct. Happy pigging!

import random

def pig_actions_d(state):
	"""The legal actions from a state. Usually, ["roll", "hold"].
	Exceptions: If double is "double", can only "accept" or "decline".
	Can't "hold" if pending is 0.
	If double is 1, can "double" (in addition to other moves).
	(If double > 1, cannot "double").
	"""
	# state is like before, but with one more component, double,
	# which is 1 or 2 to denote the value of the game, or 'double'
	# for the moment at which one player has doubled and is waiting
	# for the other to accept or decline
	(p, me, you, pending, double) = state
	if double == "double":
		return ['accept', 'decline']
	actions = ["roll"]
	if pending:
		actions += ["hold"]
	if double is 1:
		actions += ["double"]
	return actions

def strategy_d(state):
	(p, me, you, pending, double) = state
	if pending >= 30 or me + pending >= goal:
		return "hold"
	if me-you > max(pending/3, 5) and double is 1:
		return "double"
	return "roll"

## You can use the code below, but don't need to modify it.
def hold_20_d(state):
	"Hold at 20 pending.  Always accept; never double."
	(p, me, you, pending, double) = state
	return ('accept' if double == 'double' else
			'hold' if (pending >= 20 or me + pending >= goal) else
			'roll')

def clueless_d(state):
	return random.choice(pig_actions_d(state))

def dierolls():
	"Generate die rolls."
	while True:
		yield random.randint(1, 6)

def play_pig_d(A, B, dierolls=dierolls()):
	"""Play a game of pig between two players, represented by their strategies.
	Each time through the main loop we ask the current player for one decision,
	which must be 'hold' or 'roll', and we update the state accordingly.
	When one player's score exceeds the goal, return that player."""
	strategies = [A, B]
	state = (0, 0, 0, 0, 1)
	while True:
		(p, me, you, pending, double) = state
		if me >= goal:
			return strategies[p], double
		elif you >= goal:
			return strategies[other[p]], double
		else:
			action = strategies[p](state)
			state = do(action, state, dierolls)

## No more roll() and hold(); instead, do:
def do(action, state, dierolls):
	"""Return the state that results from doing action in state.
	 If action is not legal, return a state where the opponent wins.
	Can use dierolls if needed."""
	(p, me, you, pending, double) = state
	if action not in pig_actions_d(state):
		return (other[p], goal, 0, 0, double)
	elif action == 'roll':
		d = next(dierolls)
		if d == 1:
			return (other[p], you, me+1, 0, double) # pig out; other player's turn
		else:
			return (p, me, you, pending+d, double)  # accumulate die in pending
	elif action == 'hold':
		return (other[p], you, me+pending, 0, double)
	elif action == 'double':
		return (other[p], you, me, pending, 'double')
	elif action == 'decline':
		return (other[p], goal, 0, 0, 1)
	elif action == 'accept':
		return (other[p], you, me, pending, 2)

goal = 40
other = {1:0, 0:1}

def strategy_compare(A, B, N=1000):
	"""Takes two strategies, A and B, as input and returns the percentage
	of points won by strategy A."""
	A_points, B_points = 0, 0
	for i in range(N):
		if i % 2 == 0:  # take turns with who goes first
			winner, points = play_pig_d(A, B)
		else:
			winner, points = play_pig_d(B, A)
		if winner.__name__ == A.__name__:
			A_points += points
		else: B_points += points
	A_percent = 100*A_points / float(A_points + B_points)
	#print 'In %s games of pig, strategy %s took %s percent of the points against %s.' % (N, A.__name__, A_percent, B.__name__)
	return A_percent

def test():
	assert set(pig_actions_d((0, 2, 3, 0, 1)))          == set(['roll', 'double'])
	assert set(pig_actions_d((1, 20, 30, 5, 2)))        == set(['hold', 'roll'])
	assert set(pig_actions_d((0, 5, 5, 5, 1)))          == set(['roll', 'hold', 'double'])
	assert set(pig_actions_d((1, 10, 15, 6, 'double'))) == set(['accept', 'decline'])
	assert strategy_compare(strategy_d, hold_20_d) > 60 # must win 60% of the points
	return 'test passes'

if __name__ == '__main__':
	#for _ in range(3):
	#	print test()
	#exit()

	total_p = 0
	times   = 20
	for _ in range(times):
		total_p += strategy_compare(strategy_d, hold_20_d)
	print total_p*1.0/times