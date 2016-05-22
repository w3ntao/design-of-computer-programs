# -----------------
# User Instructions
#
# Write a function, shortest_path_search, that generalizes the search algorithm
# that we have been using. This function should have three inputs, a start state,
# a successors function, and an is_goal function.
#
# You can use the solution to mc_problem as a template for constructing your
# shortest_path_search. You can also see the example is_goal and successors
# functions for a simple test problem below.

def shortest_path_search(start, successors, is_goal):
	"""Find the shortest path from start state to a state
	such that is_goal(state) is true."""
	if is_goal(start):
		return [start]

	explored = set() # set of states we have visited
	frontier = [ [start] ] # ordered list of paths we have blazed
	while frontier:
		path = frontier.pop(0)
		s = path[-1]
		for (state, action) in successors(s).items():
			if state not in explored:
				explored.add(state)
				path2 = path + [action, state]
				if is_goal(state):
					return path2
				else:
					frontier.append(path2)
	return Fail


def mc_problem1(start=(3, 3, 1, 0, 0, 0), goal=None):
	"""Solve the missionaries and cannibals problem.
	State is 6 ints: (M1, C1, B1, M2, C2, B2) on the start (1) and other (2) sides.
	Find a path that goes from the initial state to the goal state (which, if
	not specified, is the state with no people or boats on the start side."""
	if goal is None:
		goal = (0, 0, 0) + start[:3]
	if start == goal:
		return [start]
	explored = set() # set of states we have visited
	frontier = [ [start] ] # ordered list of paths we have blazed
	while frontier:
		path = frontier.pop(0)
		s = path[-1]
		for (state, action) in csuccessors(s).items():
			if state not in explored:
				explored.add(state)
				path2 = path + [action, state]
				if state == goal:
					return path2
				else:
					frontier.append(path2)
	return Fail

Fail = []

def csuccessors(state):
	"""Find successors (including those that result in dining) to this
	state. But a state where the cannibals can dine has no successors."""
	M1, C1, B1, M2, C2, B2 = state
	## Check for state with no successors
	if C1 > M1 > 0 or C2 > M2 > 0:
		return {}
	items = []
	if B1 > 0:
		items += [(sub(state, delta), a + '->')
				  for delta, a in deltas.items()]

	if B2 > 0:
		items += [(add(state, delta), '<-' + a)
				  for delta, a in deltas.items()]
	return dict(items)

def add(X, Y):
	"add two vectors, X and Y."
	return tuple(x+y for x,y in zip(X, Y))

def sub(X, Y):
	"subtract vector Y from X."
	return tuple(x-y for x,y in zip(X, Y))

deltas = {(2, 0, 1,    -2,  0, -1): 'MM',
		  (0, 2, 1,     0, -2, -1): 'CC',
		  (1, 1, 1,    -1, -1, -1): 'MC',
		  (1, 0, 1,    -1,  0, -1): 'M',
		  (0, 1, 1,     0, -1, -1): 'C'}
Fail = []


# --------------
# Example problem
#
# Let's say the states in an optimization problem are given by integers.
# From a state, i, the only possible successors are i+1 and i-1. Given
# a starting integer, find the shortest path to the integer 8.
#
# This is an overly simple example of when we can use the
# shortest_path_search function. We just need to define the appropriate
# is_goal and successors functions.

def is_goal(state):
	if state == 8:
		return True
	else:
		return False

def successors(state):
	successors = {state + 1: '->',
				  state - 1: '<-'}
	return successors
if __name__ == '__main__':
	#test
	assert shortest_path_search(5, successors, is_goal) == [5, '->', 6, '->', 7, '->', 8]
	print "test passes"