# -----------------
# User Instructions
#
# Update the play_pig function so that it looks at the result
# that comes from the strategy function and makes sure that
# it is either 'hold' or 'roll' and if it's not one of those
# then that strategy should immediately lose and the other
# strategy should be declared the winner.

import random

def roll(state, d):
	"""Apply the roll action to a state (and a die roll d) to yield a new state:
	If d is 1, get 1 point (losing any accumulated 'pending' points),
	and it is the other player's turn. If d > 1, add d to 'pending' points."""
	(p, me, you, pending) = state
	if d == 1:
		return (other[p], you, me+1, 0) # pig out; other player's turn
	else:
		return (p, me, you, pending+d)  # accumulate die roll in pending

def hold(state):
	"""Apply the hold action to a state to yield a new state:
	Reap the 'pending' points and it becomes the other player's turn."""
	(p, me, you, pending) = state
	return (other[p], you, me+pending, 0)

def dierolls():
	"Generate die rolls."
	while True:
		yield random.randint(1, 6)

other = {1:0, 0:1}
goal  = 40

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
		if you >= goal:
			return strategies[other[p]]

		if strategies[p](state) == "hold":
			state = hold(state)
		elif strategies[p](state) == "roll":
			state = roll(state, next(dierolls))
		else: # illegal action -> lose
			return strategies[other[p]]

def bad_strategy(state):
	"A strategy that could never win, unless a player makes an illegal move"
	return 'hold'

def illegal_strategy(state):
	return 'I want to win pig please.'

print play_pig(bad_strategy, illegal_strategy).__name__

def test():
	winner = play_pig(bad_strategy, illegal_strategy)
	assert winner.__name__ == 'bad_strategy'
	return 'tests pass'

if __name__ == '__main__':
	print test()
