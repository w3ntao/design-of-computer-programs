from functools import update_wrapper

def n_ary(f):
	def n_ary_f(x, *args):
		if not args:
			return x
		else:
			return f(x, n_ary_f(*args))
	update_wrapper(n_ary, f)
	return n_ary_f

@n_ary
def add(x, y): return x+y

def seq(x, y): return ("seq", x, y)

#seq = n_ary(seq)

#add = n_ary(add)

print add(4, 10, 10)