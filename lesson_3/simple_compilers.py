# --------------
# User Instructions
#
# Fill out the function match(pattern, text), so that
# remainders is properly assigned.

def match(pattern, text):
	"Match pattern against start of text; return longest match found or None."
	remainders = pattern(text) # your code here.
	if remainders:
		shortest = min(remainders, key=len)
		return text[:len(text)-len(shortest)]

def lit(s):
	return lambda t: set([t[len(s):]]) if t.startswith(s) else null

def seq(x, y):
	return lambda t: set().union(*map(y, x(t)))

def alt(x, y):
	return lambda t: x(t) | y(t)

def oneof(chars):
	return lambda t: set([t[1:]]) if (t and t[0] in chars) else null

dot = lambda t: set([t[1:]]) if t else null

eol = lambda t: set(['']) if t == '' else null

def star(x):
	return lambda t: (set([t]) |
		set(t2 for t1 in x(t) if t1 != t for t2 in star(x)(t1)))

null = frozenset([])

def test():
	assert match(star(lit('a')), 'aaaaabbbaa') == 'aaaaa'
	assert match(lit('hello'), 'hello how are you?') == 'hello'
	assert match(lit('x'), 'hello how are you?') == None
	assert match(oneof('xyz'), 'x**2 + y**2 = r**2') == 'x'
	assert match(oneof('xyz'), '   x is here!') == None
	return 'tests pass'

print test()