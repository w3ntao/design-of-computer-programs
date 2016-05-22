from csuccessors import csuccessors

def mc_problem(start = (3, 3, 1, 0, 0, 0), goal=None):
	'''Solve the missionaries and cannibals problem.
	State is 6 ints: (M1, C1, B1, M2, C2, B2) on the start(1) and other (2) sides.
	Find a path that goes from the initial state to the goal state (which, if
	not specified, is the state with no people or boats on the start side).'''
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

if __name__ == '__main__':
	print mc_problem()