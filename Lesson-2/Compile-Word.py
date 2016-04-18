# User Instructions
#
# Write a function, compile_word(word), that compiles a word
# of UPPERCASE letters as numeric digits. For example:
# compile_word('YOU') => '(1*U + 10*O +100*Y)'
# Non-uppercase words should remain unchaged.
import itertools
import re
import string

def faster_solve(formula):
	f, letters = compile_formula(formula)
	for digits in itertools.permutations((1,2,3,4,5,6,7,8,9,0), len(letters)):
		try:
			if f(*digits) is True:
				table = string.maketrans(letters, "".join(map(str, digits)))
				return formula.translate(table)
		except ArithmeticError:
			return None

def compile_formula(formula, verbose=False):
	letters = "".join(set(re.findall("[A-Z]", formula)))
	parms = ", ".join(letters)
	tokens = map(compile_word, re.split("([A-Z]+)", formula))
	body = "".join(tokens)
	f = "lambda %s: %s" % (parms, body)
	if verbose: print f
	return eval(f), letters

def compile_word(word):
	if word.isupper():
		terms = [("%s*%s" % (10**i, d))
					for (i, d) in enumerate(reversed(word))]
		return "(" + "+".join(terms) + ")"
	else:
		return word

examples ="""TWO + TWO == FOUR
A**2 + B**2 == C**2
A**2 + BE**2 == BY**2
X / X == X
A**N + B**N == C**N and N >	 1
ATOM**0.5 == A + TO + M
GLITTERS is not GOLD
ONE < TWO and FOUR < FIVE
ONE < TWO < THREE
RAMN == R**3 + RM**3 == N**3 + RX**X
sum(range(AA)) == BB
sum(range(POP)) == BOBO
ODD + ODD == EVEN
PLUTO not in set([PLANETS])
""".splitlines()

for formula in examples:
	print faster_solve(formula)
