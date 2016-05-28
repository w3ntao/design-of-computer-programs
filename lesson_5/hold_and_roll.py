# -----------------
# User Instructions
#
# Write the two action functions, hold and roll. Each should take a
# state as input, apply the appropriate action, and return a new
# state.
#
# States are represented as a tuple of (p, me, you, pending) where
# p:       an int, 0 or 1, indicating which player's turn it is.
# me:      an int, the player-to-move's current score
# you:     an int, the other player's current score.
# pending: an int, the number of points accumulated on current turn, not yet scored

def other(p):
	return (p+1)%2

def hold(state):
	"""Apply the hold action to a state to yield a new state:
	Reap the 'pending' points and it becomes the other player's turn."""
	p, me, you, pending = state
	return other(p), you, me+pending, 0

def roll(state, d):
	"""Apply the roll action to a state (and a die roll d) to yield a new state:
	If d is 1, get 1 point (losing any accumulated 'pending' points),
	and it is the other player's turn. If d > 1, add d to 'pending' points."""
	p, me, you, pending = state
	if d is 1:
		return other(p), you, me+1, 0
	else:
		return p, me, you, pending+d

def test():
	assert hold((1, 10, 20, 7))    == (0, 20, 17, 0)
	assert hold((0, 5, 15, 10))    == (1, 15, 15, 0)
	assert roll((1, 10, 20, 7), 1) == (0, 20, 11, 0)
	assert roll((0, 5, 15, 10), 5) == (0, 5, 15, 15)
	return 'tests pass'

if __name__ == '__main__':
	print test()