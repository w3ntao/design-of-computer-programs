# -----------------
# User Instructions
#
# Modify the rolls variable in the test() function so that it
# contains the fewest number of valid rolls that will cause
# the hold_at(50) strategy to win. Enter your rolls at line 63

import random

goal = 50
possible_moves = ['roll', 'hold']
other = {1:0, 0:1}

def hold(state):
	"""Apply the hold action to a state to yield a new state:
	Reap the 'pending' points and it becomes the other player's turn."""
	(p, me, you, pending) = state
	return (other[p], you, me+pending, 0)

def roll(state, d):
	"""Apply the roll action to a state (and a die roll d) to yield a new state:
	If d is 1, get 1 point (losing any accumulated 'pending' points),
	and it is the other player's turn. If d > 1, add d to 'pending' points."""
	(p, me, you, pending) = state
	if d == 1:
		return (other[p], you, me+1, 0) # pig out; other player's turn
	else:
		return (p, me, you, pending+d)  # accumulate die roll in pending

def clueless(state):
	"A strategy that ignores the state and chooses at random from possible moves."
	return random.choice(possible_moves)

def hold_at(x):
	"""Return a strategy that holds if and only if 
	pending >= x or player reaches goal."""
	def strategy(state):
		(p, me, you, pending) = state
		return 'hold' if (pending >= x or me + pending >= goal) else 'roll'
	strategy.__name__ = 'hold_at(%d)' % x
	return strategy

def dierolls():
	"Generate die rolls."
	while True:
		yield random.randint(1, 6)

def play_pig(A, B, dierolls=dierolls()):
	"""Play a game of pig between two players, represented by their strategies.
	Each time through the main loop we ask the current player for one decision,
	which must be 'hold' or 'roll', and we update the state accordingly.
	When one player's score exceeds the goal, return that player."""
	strategies = [A, B]
	state = (0, 0, 0, 0)
	while True:
		(p, me, you, pending) = state
		if me >= goal:
			return strategies[p]
		elif you >= goal:
			return strategies[other[p]]
		elif strategies[p](state) == 'hold':
			state = hold(state)
		else:
			state = roll(state, next(dierolls))

def test():
	A, B = hold_at(50), clueless
	rolls = iter([6]*8 + [2]) # <-- Your rolls here
	assert play_pig(A, B, rolls) == A
	return 'test passes'

if __name__ == '__main__':
	print test()