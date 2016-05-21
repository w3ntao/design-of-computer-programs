# -----------------
# User Instructions
#
# Write a function, path_cost, which takes a path as input
# and returns the total cost associated with that path.
# Remember that paths will obey the convention
# path = (state, (action, total_cost), state, ...)
#
# If a path is less than length 3, your function should
# return a cost of 0.

def path_cost(path):
	"""The total cost of a path (which is stored in a tuple
	with the final action."""
	# path = (state, (action, total_cost), state, ... )
	if len(path) < 3:
		return 0
	else:
		action, total_cost = path[-2]
		return total_cost

def bcost(action):
	"""Returns the cost (a number) of an action in the
	bridge problem."""
	# An action is an (a, b, arrow) tuple; a and b are
	# times; arrow is a string.
	a, b, arrow = action
	return max(a, b)

def test():
	assert path_cost(('fake_state1', ((2, 5, '->'), 5), 'fake_state2')) == 5
	assert path_cost(('fs1', ((2, 1, '->'), 2), 'fs2', ((3, 4, '<-'), 6), 'fs3')) == 6
	assert bcost((4, 2, '->'),) == 4
	assert bcost((3, 10, '<-'),) == 10
	return 'tests pass'

print test()