from refactoring_paths import bsuccessors2
from calculating_costs import path_cost, bcost

def bridge_problem2(here):
	here = frozenset(here) | frozenset(["light"])
	explored = set() # set of states we have visited
	# State will be a (peoplelight_here, peoplelight_there) tuple
	# E.g. ({1, 2, 5, 10, "light"}, {})
	frontier = [ [(here, frozenset())] ] # ordered list of paths we have blazed
	while frontier:
		path = frontier.pop(0)
		here1, there1 = state1 = final_state(path)
		if not here1 or (len(here1)==1 and "light" in here1):
			return path
		explored.add(state1)
		pcost = path_cost(path)
		for (state, action) in bsuccessors2(state1).items():
			if state not in explored:
				total_cost = pcost + bcost(action)
				path2 = path + [(action, total_cost), state]
				add_to_frontier(frontier, path2)
	return Fail

Fail = []

def final_state(path):
	return path[-1]

def add_to_frontier(frontier, path):
	'''Add path to frontier, replacing costlier path if there is one.'''
	# (This could be done more efficiently.)
	# Find if there is an old path to the final state of this path.
	old = None
	for i, p in enumerate(frontier):
		if final_state(p) == final_state(path):
			old = i
			break
	if old is not None and path_cost(frontier[old]) < path_cost(path):
		return # Old path was better; do nothing
	elif old is not None:
		del frontier[old] # Old path was worse; delete it
	# Now add the new path and re-sort
	frontier.append(path)

if __name__ == '__main__':
	print bridge_problem2([1,2,4,8,16,32])
	print ""
	print bridge_problem2([1,2,5,10,15,20])