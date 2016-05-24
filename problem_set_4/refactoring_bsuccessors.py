# -----------------
# User Instructions
#
# In this problem you will be refactoring the bsuccessors function.
# Your new function, bsuccessors3, will take a state as an input
# and return a dict of {state:action} pairs.
#
# A state is a (here, there, light) tuple. Here and there are
# frozensets of people (each person is represented by an integer
# which corresponds to their travel time), and light is 0 if
# it is on the `here` side and 1 if it is on the `there` side.
#
# An action is a tuple of (travelers, arrow), where the arrow is
# '->' or '<-'. See the test() function below for some examples
# of what your function's input and output should look like.

def bsuccessors3(state):
	"""Return a dict of {state:action} pairs.  State is (here, there, light)
	where here and there are frozen sets of people, light is 0 if the light is
	on the here side and 1 if it is on the there side.
	Action is a tuple (travelers, arrow) where arrow is '->' or '<-'"""
	_, _, light = state

	def _bsuccessors3(travelers):
		start = state[light]   - travelers
		dest  = state[1-light] | travelers
		if light == 0:
			return (start, dest,  1), (travelers, "->")
		else:
			return (dest,  start, 0), (travelers, "<-")

	return dict(_bsuccessors3(set([a, b]))
				for a in state[light]
				for b in state[light])

def test():
	assert bsuccessors3((frozenset([1]), frozenset([]), 0)) == {
			(frozenset([]), frozenset([1]), 1)  :  (set([1]), '->')}

	assert bsuccessors3((frozenset([1, 2]), frozenset([]), 0)) == {
			(frozenset([1]), frozenset([2]), 1)    :  (set([2]), '->'),
			(frozenset([]), frozenset([1, 2]), 1)  :  (set([1, 2]), '->'),
			(frozenset([2]), frozenset([1]), 1)    :  (set([1]), '->')}

	assert bsuccessors3((frozenset([2, 4]), frozenset([3, 5]), 1)) == {
			(frozenset([2, 4, 5]), frozenset([3]), 0)   :  (set([5]), '<-'),
			(frozenset([2, 3, 4, 5]), frozenset([]), 0) :  (set([3, 5]), '<-'),
			(frozenset([2, 3, 4]), frozenset([5]), 0)   :  (set([3]), '<-')}
	return 'tests pass'


if __name__ == '__main__':
	print test()