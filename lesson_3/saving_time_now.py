from functools import update_wrapper

def decorator(d):
	def _d(fn):
		return update_wrapper(d(fn), fn)
	update_wrapper(_d, d)
	return _d

callcounts = {}

@decorator
def countcalls(f):
	def _f(*args):
		callcounts[_f] += 1
		return f(*args)
	callcounts[_f] = 0
	return _f

@decorator
def memo(f):
	cache = {}
	def _f(*args):
		try:
			return cache[args]
		except KeyError:
			cache[args] = result = f(*args)
			return result
		except TypeError:
			return f(args)
	return _f

@countcalls
@memo
def fib_memo(n):
	if n <= 1:
		return 1
	return fib_memo(n-1) + fib_memo(n-2)

@countcalls
def fib(n):
	if n <= 1:
		return 1
	return fib(n-1) + fib(n-2)

fib(20)
fib_memo(20)
print callcounts
