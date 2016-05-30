million = 1000000

def quality(state, action, U):
	if action == "hold":
		return U(state + 1*million)
	if action == "gamble":
		return U(state + 3*million)*0.5 + U(state)*0.5

def actions(state): return ["hold", "gamble"]

def identity(x): return x

def best_action(state, actions, Q, U):
	def _EU(action):
		return Q(state, action, U)
	return max(actions(state), key=_EU)

if __name__ == '__main__':
	import math

	own = 100
	print "Identity  as utility:", best_action(own, actions, quality, identity), "when owning", own
	print "Logarithm as utility:", best_action(own, actions, quality, math.log), "when owning", own

	own = 10*million
	print "Logarithm as utility:", best_action(own, actions, quality, math.log), "when owning", own