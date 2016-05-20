# ----------------
# User Instructions
#
# Write two functions, path_states and path_actions. Each of these
# functions should take a path as input. Remember that a path is a
# list of [state, action, state, action, ... ]
#
# path_states should return a list of the states. in a path, and
# path_actions should return a list of the actions.

def path_states(path):
	"Return a list of states in this path."
	return path[0::2]

def path_actions(path):
	"Return a list of actions in this path."
	return path[1::2]

def test():
	testpath = [(frozenset([1, 10]), frozenset(['light', 2, 5]), 5), # state 1
				(5, 2, '->'),                                        # action 1
				(frozenset([10, 5]), frozenset([1, 2, 'light']), 2), # state 2
				(2, 1, '->'),                                        # action 2
				(frozenset([1, 2, 10]), frozenset(['light', 5]), 5),
				(5, 5, '->'),
				(frozenset([1, 2]), frozenset(['light', 10, 5]), 10),
				(5, 10, '->'),
				(frozenset([1, 10, 5]), frozenset(['light', 2]), 2),
				(2, 2, '->'),
				(frozenset([2, 5]), frozenset([1, 10, 'light']), 10),
				(10, 1, '->'),
				(frozenset([1, 2, 5]), frozenset(['light', 10]), 10),
				(10, 10, '->'),
				(frozenset([1, 5]), frozenset(['light', 2, 10]), 10),
				(10, 2, '->'),
				(frozenset([2, 10]), frozenset([1, 5, 'light']), 5),
				(5, 1, '->'),
				(frozenset([2, 10, 5]), frozenset([1, 'light']), 1),
				(1, 1, '->')]
	assert path_states(testpath) == [(frozenset([1, 10]), frozenset(['light', 2, 5]), 5), # state 1
				(frozenset([10, 5]), frozenset([1, 2, 'light']), 2), # state 2
				(frozenset([1, 2, 10]), frozenset(['light', 5]), 5),
				(frozenset([1, 2]), frozenset(['light', 10, 5]), 10),
				(frozenset([1, 10, 5]), frozenset(['light', 2]), 2),
				(frozenset([2, 5]), frozenset([1, 10, 'light']), 10),
				(frozenset([1, 2, 5]), frozenset(['light', 10]), 10),
				(frozenset([1, 5]), frozenset(['light', 2, 10]), 10),
				(frozenset([2, 10]), frozenset([1, 5, 'light']), 5),
				(frozenset([2, 10, 5]), frozenset([1, 'light']), 1)]
	assert path_actions(testpath) == [(5, 2, '->'), # action 1
									  (2, 1, '->'), # action 2
									  (5, 5, '->'),
									  (5, 10, '->'),
									  (2, 2, '->'),
									  (10, 1, '->'),
									  (10, 10, '->'),
									  (10, 2, '->'),
									  (5, 1, '->'),
									  (1, 1, '->')]
	return 'tests pass'

print test()