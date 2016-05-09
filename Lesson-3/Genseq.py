def lit(s):
	set_s = set([s])
	return lambda Ns: set_s if len(s) in Ns else null

def alt(x, y):
	return lambda Ns: x(Ns) | y(Ns)

def star(x):
	return lambda Ns: opt(plus(x))(Ns)

def plus(x):
	return lambda Ns: genseq(x, star(x), Ns, startx=1) #Tricky

def oneof(chars):
	set_chars = set(chars)
	return lambda Ns: set_chars if 1 in Ns else null

def seq(x, y):
	return lambda Ns: genseq(x, y, Ns)

def opt(x):
	return alt(epsilon, x)

dot = oneof('?')    # You could expand the alphabet to more chars.

epsilon = lit('')   # The pattern that matches the empty string.

def genseq(x, y, Ns, startx=0):
	if not Ns:
		return null
	xmatches = x(set(range(startx, max(Ns)+1)))
	Ns_x = set(len(m) for m in xmatches)
	Ns_y = set(n-m for n in Ns for m in Ns_x if n-m >= 0)
	ymatches = y(Ns_y)
	return set(m1+m2 for m1 in xmatches for m2 in ymatches if len(m1+m2) in Ns)

null = frozenset([])

f = star(seq(lit("R"), lit("a")))

print f(set([1,4,5,8,12]))