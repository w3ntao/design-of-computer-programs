"""
UNIT 3: Functions and APIs: Polynomials

A polynomial is a mathematical formula like:

	30 * x**2 + 20 * x + 10

More formally, it involves a single variable (here 'x'), and the sum of one
or more terms, where each term is a real number multiplied by the variable
raised to a non-negative integer power. (Remember that x**0 is 1 and x**1 is x,
so 'x' is short for '1 * x**1' and '10' is short for '10 * x**0'.)

We will represent a polynomial as a Python function which computes the formula
when applied to a numeric value x.  The function will be created with the call:

	p1 = poly((10, 20, 30))

where the nth element of the input tuple is the coefficient of the nth power of x.
(Note the order of coefficients has the x**n coefficient neatly in position n of
the list, but this is the reversed order from how we usually write polynomials.)
poly returns a function, so we can now apply p1 to some value of x:

	p1(0) == 10

Our representation of a polynomial is as a callable function, but in addition,
we will store the coefficients in the .coefs attribute of the function, so we have:

	p1.coefs == (10, 20, 30)

And finally, the name of the function will be the formula given above, so you should
have something like this:

	>>> p1
	<function 30 * x**2 + 20 * x + 10 at 0x100d71c08>

	>>> p1.__name__
	'30 * x**2 + 20 * x + 10'

Make sure the formula used for function names is simplified properly.
No '0 * x**n' terms; just drop these. Simplify '1 * x**n' to 'x**n'.
Simplify '5 * x**0' to '5'.  Similarly, simplify 'x**1' to 'x'.
For negative coefficients, like -5, you can use '... + -5 * ...' or
'... - 5 * ...'; your choice. I'd recommend no spaces around '**'
and spaces around '+' and '*', but you are free to use your preferences.

Your task is to write the function poly and the following additional functions:

	is_poly, add, sub, mul, power, deriv, integral

They are described below; see the test_poly function for examples.
"""
from collections import defaultdict

def decorator(d):
	"Make function d a decorator: d wraps a function fn."
	import functools
	def _d(fn):
		return functools.update_wrapper(d(fn), fn)
	functools.update_wrapper(_d, d)
	return _d

@decorator
def memo(f):
	"""Decorator that caches the return value for each call to f(*args).
	Then when called again with same args, we can just look it up."""
	cache = {}
	def _f(*args):
		try:
			return cache[args]
		except KeyError:
			result = f(*args)
			try:
				cache[args] = result
			except TypeError: # args refuses to be a dict key
				pass
			return result
	_f.cache = cache
	return _f

def poly(coefs):
	"""Return a function that is the polynomial with these coefficients.
	For example if coefs=(10, 20, 30) return the function of x that computes
	'30 * x**2 + 20 * x + 10'.  Also store coefs on the .coefs attribute of
	the function, and the str of the formula on the .__name__ attribute.'"""
	return polynomial(canonical(coefs))

@memo
def polynomial(coefs):
	"""Return a polynomial function with these attributes.  Memoized, so any
	two polys with the same coefficients will be identical polys."""
	# Build a function by evaluating a lambda in the empty environment.
	# Horner's rule involves fewer multiplications than the normal formula...
	p = eval('lambda x: ' + horner_formula(coefs), {})
	p.__name__ = polynomial_formula(coefs)
	p.coefs = coefs
	return p

def horner_formula(coefs):
	"""A relatively efficient form to evaluate a polynomial.
	E.g.:  horner_formula((10, 20, 30, 0, -50))
		   == '(10 + x * (20 + x * (30 + x * x * -50)))',
	which is 4 multiplies and 3 adds."""
	c = coefs[0]
	if len(coefs) == 1:
		return str(c)
	else:
		factor = 'x * ' + horner_formula(coefs[1:])
		return factor if c == 0 else '(%s + %s)' % (c, factor)

def polynomial_formula(coefs):
	"""A simple human-readable form for a polynomial.
	E.g.:  polynomial_formula((10, 20, 30, 0, -50))
		   == '-50 * x**4 + 30 * x**2 + 20 * x + 10',
	which is 7 multiplies and 3 adds."""
	terms = [term(c, n) for (n, c) in reversed(list(enumerate(coefs))) if c != 0]
	return ' + '.join(terms)

def term(c, n):
	"Return a string representing 'c * x**n' in simplified form."
	if n == 0:
		return str(c)
	xn = 'x' if (n == 1) else ('x**' + str(n))
	return xn if (c == 1) else '-' + xn if (c == -1) else str(c) + ' * ' + xn

def canonical(coefs):
	"Canonicalize coefs by dropping trailing zeros and converting to a tuple."
	if not coefs: coefs = [0]
	elif isinstance(coefs, (int, float)): coefs = [coefs]
	else: coefs = list(coefs)
	while coefs[-1] == 0 and len(coefs) > 1:
		del coefs[-1]
	return tuple(coefs)

def is_poly(x):
	"Return true if x is a poly (polynomial)."
	## For examples, see the test_poly function
	return callable(x) and hasattr(x, 'coefs')

def add(p1, p2):
	"Return a new polynomial which is the sum of polynomials p1 and p2."
	coefs = [0] * max(len(p1.coefs), len(p2.coefs))
	for (n, c) in enumerate(p1.coefs): coefs[n] = c
	for (n, c) in enumerate(p2.coefs): coefs[n] += c
	return poly(coefs)

def sub(p1, p2):
	"Return a new polynomial which is p1 - p2."
	coefs = [0] * max(len(p1.coefs), len(p2.coefs))
	for (n, c) in enumerate(p1.coefs): coefs[n] = c
	for (n, c) in enumerate(p2.coefs): coefs[n] -= c
	return poly(coefs)

def mul(p1, p2):
	"Return a new polynomial which is the product of polynomials p1 and p2."
	# Given terms a*x**n and b*x**m, accumulate a*b in results[n+m]
	results = defaultdict(int)
	for (n, a) in enumerate(p1.coefs):
		for (m, b) in enumerate(p2.coefs):
			results[n + m] += a * b
	return poly([results[i] for i in range(max(results)+1)])

def power(p, n):
	"Return a poly which is p to the nth power (n a non-negative integer)."
	if n == 0:
		return poly((1,))
	if n % 2 == 0:
		return power(mul(p, p), n//2)
	else:
		return mul(p, power(p, n-1))

def deriv(p):
	"Return the derivative of a function p (with respect to its argument)."
	return poly([n*c for (n, c) in enumerate(p.coefs) if n > 0])

def integral(p, C=0):
	"Return the integral of a function p (with respect to its argument)."
	return poly([C] + [float(c)/(n+1) for (n, c) in enumerate(p.coefs)])

def test_poly():
	global p1, p2, p3, p4, p5, p9
	# global to ease debugging in an interactive session

	p1 = poly((10, 20, 30))
	assert p1(0) == 10
	for x in (1, 2, 3, 4, 5, 1234.5):
		assert p1(x) == 30 * x**2 + 20 * x + 10
	assert same_name(p1.__name__, '30 * x**2 + 20 * x + 10')

	assert is_poly(p1)
	assert not is_poly(abs) and not is_poly(42) and not is_poly('cracker')

	p3 = poly((0, 0, 0, 1))
	assert p3.__name__ == 'x**3'
	p9 = mul(p3, mul(p3, p3))
	#assert p9 == poly([0,0,0,0,0,0,0,0,0,1])
	assert p9(2) == 512
	p4 =  add(p1, p3)
	assert same_name(p4.__name__, 'x**3 + 30 * x**2 + 20 * x + 10')

	assert same_name(poly((1, 1)).__name__, 'x + 1')
	assert (power(poly((1, 1)), 10).__name__ ==
			'x**10 + 10 * x**9 + 45 * x**8 + 120 * x**7 + 210 * x**6 + 252 ' +
			'* x**5 + 210 * x**4 + 120 * x**3 + 45 * x**2 + 10 * x + 1')

	assert add(poly((10, 20, 30)), poly((1, 2, 3))) == poly((11, 22, 33))
	assert sub(poly((10, 20, 30)), poly((1, 2, 3))) == poly((9, 18, 27))
	assert (mul(poly((10, 20, 30)), poly((1, 2, 3)))
			== poly((10, 40, 100, 120, 90)))
	assert power(poly((1, 1)), 2) == poly((1, 2, 1))
	assert (power(poly((1, 1)), 10)
			== poly((1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1)))

	assert deriv(p1) == poly((20, 60))
	assert integral(poly((20, 60))) == poly((0, 20, 30))
	p5 = poly((0, 1, 2, 3, 4, 5))
	assert same_name(p5.__name__,
					 '5 * x**5 + 4 * x**4 + 3 * x**3 + 2 * x**2 + x')
	assert p5(1) == 15
	assert p5(2) == 258
	assert same_name(deriv(p5).__name__,
					 '25 * x**4 + 16 * x**3 + 9 * x**2 + 4 * x + 1')
	assert deriv(p5)(1) == 55
	assert deriv(p5)(2) == 573
	#Additional Test Case:
	p6 = poly((1,))
	assert integral(p6)(10) == 10

def same_name(name1, name2):
	"""Use same_name rather than name1 == name2 to allow for some
	variation in naming conventions."""
	def canonical_name(name): return name.replace(' ', '').replace('+-', '-')
	return canonical_name(name1) == canonical_name(name2)

class poly(object):
	"""poly objects are like the poly functions we defined earlier, but are
	objects of a class. We coerce arguments to poly, so you can do (x + 1)
	and the 1 will be converted to a poly first."""

	def __init__(self, coefs):
		coefs = canonical(coefs)
		self.fn = eval('lambda x: ' + horner_formula(coefs), {})
		self.__name__ = polynomial_formula(coefs)
		self.coefs = coefs

	def __call__(self, x): return self.fn(x)

	def __eq__(self, other):
		return isinstance(other, poly) and self.coefs == other.coefs

	def __add__(self, p2): return add(self, coerce_poly(p2)) # p + p2
	def __sub__(self, p2): return sub(self, coerce_poly(p2)) # p - p2
	def __mul__(self, p2): return mul(self, coerce_poly(p2)) # p * p2
	def __pow__(self, n): return power(self, n)              # p ^ n
	def __neg__(self): return poly((-c for c in self.coefs)) # - p
	def __pos__(self): return self                           # + p

	# A need the _r methods so that 1 + x works as well as x + 1.

	def __rmul__(self, p2): return mul(self, coerce_poly(p2)) # 5 * x
	def __radd__(self, p2): return add(self, coerce_poly(p2)) # 1 + x

	# I added a __hash__ method after a suggestion by Jeffrey Tratner

	def __hash__(self): return hash(self.coefs)

	def __repr__(self):
		return ''

def coerce_poly(p):
	"Make this into a poly if it isn't already."
	return p if isinstance(p, poly) else poly(p)

def is_poly(p): return isinstance(p, poly)

def Poly(formula):
	"Parse the formula using eval in an environment where x is a poly."
	return eval(formula, {'x': poly((0, 1))})

"""
Now for an extra credit challenge: arrange to describe polynomials with an
expression like '3 * x**2 + 5 * x + 9' rather than (9, 5, 3).  You can do this
in one (or both) of two ways:

(1) By defining poly as a class rather than a function, and overloading the
__add__, __sub__, __mul__, and __pow__ operators, etc.  If you choose this,
call the function test_poly1().  Make sure that poly objects can still be called.

(2) Using the grammar parsing techniques we learned in Unit 5. For this
approach, define a new function, Poly, which takes one argument, a string,
as in Poly('30 * x**2 + 20 * x + 10').  Call test_poly2().
"""

def test_poly1():
	# I define x as the polynomial 1*x + 0.
	x = poly((0, 1))
	# From here on I can create polynomials by + and * operations on x.
	newp1 =  30 * x**2 + 20 * x + 10 # This is a poly object, not a number!
	assert p1(100) == newp1(100) # The new poly objects are still callable.
	assert same_name(p1.__name__,newp1.__name__)
	assert (x + 1) * (x - 1) == x**2 - 1 == poly((-1, 0, 1))

def test_poly2():
	newp1 = Poly('30 * x**2 + 20 * x + 10')
	assert p1(100) == newp1(100)
	assert same_name(p1.__name__,newp1.__name__)

if __name__ == '__main__':
	test_poly()
	test_poly1()
	test_poly2()
	print "tests pass"