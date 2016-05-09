from functools import update_wrapper

def decorator(d):
	def _d(fn):
		return update_wrapper(d(fn), fn)
	update_wrapper(_d, d)
	return _d

def decorator(d):
	return lambda fn: update_wrapper(d(fn), fn)

decorator = decorator(decorator)