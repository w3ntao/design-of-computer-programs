from functools import update_wrapper

def decorator(d):
	def _d(fn):
		return update_wrapper(d(fn), fn)
	update_wrapper(_d, d)
	return _d

@decorator
def n_ary(f):
	def n_ary_f(x, *args):
		if not args:
			return x
		else:
			return f(x, n_ary_f(*args))
	return n_ary_f

@n_ary
def add(x, y): return x+y

print add(4, 10, 10)

print help(add)