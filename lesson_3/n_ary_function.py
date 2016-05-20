# ---------------
# User Instructions
#
# Write a function, n_ary(f), that takes a binary function (a function
# that takes 2 inputs) as input and returns an n_ary function.

def n_ary(f):
	"""Given binary function f(x, y), return an n_ary function such
	that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x."""
	def n_ary_f(x, *args):
		if not args:
			return x
		else:
			return f(x, n_ary_f(*args))
	return n_ary_f


def func_add(x, y): return x+y
print n_ary(func_add)(1,3,5,8)